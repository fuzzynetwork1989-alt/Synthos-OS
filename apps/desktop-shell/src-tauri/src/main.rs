// Prevents additional console window on Windows in release, DO NOT REMOVE!!
#![cfg_attr(not(debug_assertions), windows_subsystem = "windows")]

use serde::{Deserialize, Serialize};
use sysinfo::{System, SystemExt, ProcessExt, CpuExt};
use std::path::Path;
use std::fs;

#[derive(Debug, Serialize, Deserialize)]
struct SystemStatus {
    local_model: bool,
    memory_engine: bool,
    tool_gateway: bool,
    cpu_usage: f32,
    memory_usage: f32,
}

#[derive(Debug, Serialize, Deserialize)]
struct ProcessInfo {
    pid: u32,
    name: String,
    cpu_usage: f32,
    memory_usage: u64,
}

#[derive(Debug, Serialize, Deserialize)]
struct FileInfo {
    path: String,
    name: String,
    size: u64,
    is_file: bool,
}

#[tauri::command]
fn get_system_status() -> SystemStatus {
    let mut sys = System::new_all();
    sys.refresh_all();
    
    let cpu_usage = sys.global_cpu_info().cpu_usage();
    let total_memory = sys.total_memory();
    let used_memory = sys.used_memory();
    let memory_usage = (used_memory as f32 / total_memory as f32) * 100.0;

    // Check if local model service is running (simplified check)
    let local_model = check_service_running("ollama") || check_service_running("localhost:11434");
    
    // Check if memory engine is available
    let memory_engine = true; // Assuming memory engine is available
    
    // Check if tool gateway is running
    let tool_gateway = check_service_running("localhost:8001");

    SystemStatus {
        local_model,
        memory_engine,
        tool_gateway,
        cpu_usage,
        memory_usage,
    }
}

#[tauri::command]
fn get_processes() -> Vec<ProcessInfo> {
    let mut sys = System::new_all();
    sys.refresh_all();
    
    sys.processes()
        .iter()
        .map(|(pid, process)| ProcessInfo {
            pid: pid.as_u32(),
            name: process.name().to_string(),
            cpu_usage: process.cpu_usage(),
            memory_usage: process.memory(),
        })
        .collect()
}

#[tauri::command]
fn list_directory(path: String) -> Result<Vec<FileInfo>, String> {
    let path_obj = Path::new(&path);
    
    if !path_obj.exists() {
        return Err("Path does not exist".to_string());
    }

    let entries = fs::read_dir(path)
        .map_err(|e| e.to_string())?;

    let files: Vec<FileInfo> = entries
        .filter_map(|entry| entry.ok())
        .map(|entry| {
            let metadata = entry.metadata().ok();
            FileInfo {
                path: entry.path().to_string_lossy().to_string(),
                name: entry.file_name().to_string_lossy().to_string(),
                size: metadata.map(|m| m.len()).unwrap_or(0),
                is_file: metadata.map(|m| m.is_file()).unwrap_or(false),
            }
        })
        .collect();

    Ok(files)
}

#[tauri::command]
fn read_file(path: String) -> Result<String, String> {
    fs::read_to_string(&path).map_err(|e| e.to_string())
}

#[tauri::command]
fn write_file(path: String, content: String) -> Result<(), String> {
    fs::write(&path, content).map_err(|e| e.to_string())
}

#[tauri::command]
fn open_url(url: String) -> Result<(), String> {
    tauri::api::shell::open(&tauri::generate_context!().shell_scope(), url, None)
        .map_err(|e| e.to_string())
}

#[tauri::command]
fn open_file(path: String) -> Result<(), String> {
    tauri::api::shell::open(&tauri::generate_context!().shell_scope(), path, None)
        .map_err(|e| e.to_string())
}

#[tauri::command]
fn execute_command(command: String, args: Vec<String>) -> Result<String, String> {
    use std::process::Command;
    
    let output = Command::new(&command)
        .args(&args)
        .output()
        .map_err(|e| e.to_string())?;

    if output.status.success() {
        Ok(String::from_utf8_lossy(&output.stdout).to_string())
    } else {
        Err(String::from_utf8_lossy(&output.stderr).to_string())
    }
}

fn check_service_running(service_name: &str) -> bool {
    // Simplified service check - in production, this would be more sophisticated
    if service_name.contains("localhost") {
        let parts: Vec<&str> = service_name.split(':').collect();
        if parts.len() == 2 {
            if let Ok(port) = parts[1].parse::<u16>() {
                return check_port_open(port);
            }
        }
    }
    
    // Check if process is running
    let mut sys = System::new_all();
    sys.refresh_processes();
    
    for (_pid, process) in sys.processes() {
        if process.name().to_lowercase().contains(&service_name.to_lowercase()) {
            return true;
        }
    }
    
    false
}

fn check_port_open(port: u16) -> bool {
    use std::net::TcpListener;
    
    TcpListener::bind(format!("127.0.0.1:{}", port)).is_err()
}

fn main() {
    tauri::Builder::default()
        .invoke_handler(tauri::generate_handler![
            get_system_status,
            get_processes,
            list_directory,
            read_file,
            write_file,
            open_url,
            open_file,
            execute_command
        ])
        .run(tauri::generate_context!())
        .expect("error while running tauri application");
}
