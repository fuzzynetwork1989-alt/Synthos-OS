#!/usr/bin/env python3
"""
RSI Engine Activation Demonstration Script

This script demonstrates how to activate and use the Recursive Self-Improvement
engine for Synthos-OS, including the Cognitive DNA Evolution System.

Note: This is a demonstration script. For actual deployment, use the
Docker Compose setup as described in docs/rsi-activation-guide.md
"""

import requests
import json
import time
from typing import Dict, Any

class RSIEngineDemo:
    """Demonstration of RSI Engine activation and usage"""
    
    def __init__(self, base_url: str = "http://localhost:8004"):
        self.base_url = base_url
        self.session = requests.Session()
        
    def print_step(self, step_num: int, title: str):
        """Print a formatted step header"""
        print(f"\n{'='*60}")
        print(f"Step {step_num}: {title}")
        print(f"{'='*60}\n")
        
    def print_response(self, response: requests.Response, description: str):
        """Print formatted API response"""
        print(f"{description}:")
        print(f"Status Code: {response.status_code}")
        if response.status_code == 200:
            print(f"Response: {json.dumps(response.json(), indent=2)}")
        else:
            print(f"Error: {response.text}")
        print()
        
    def check_health(self) -> bool:
        """Check if RSI engine is healthy"""
        try:
            response = self.session.get(f"{self.base_url}/health")
            return response.status_code == 200
        except requests.exceptions.ConnectionError:
            return False
            
    def step1_verify_status(self):
        """Step 1: Verify RSI Engine Status"""
        self.print_step(1, "Verify RSI Engine Status")
        
        if not self.check_health():
            print("❌ RSI Engine is not running. Please start it first.")
            print("   Use: docker-compose up -d rsi-engine")
            return False
            
        response = self.session.get(f"{self.base_url}/health")
        self.print_response(response, "Health Check")
        return True
        
    def step2_start_manual_cycle(self):
        """Step 2: Start a Manual RSI Cycle"""
        self.print_step(2, "Start Manual RSI Cycle")
        
        payload = {
            "trigger_reason": "Initial system optimization",
            "auto_approve": False
        }
        
        response = self.session.post(
            f"{self.base_url}/rsi/cycle/start",
            json=payload
        )
        self.print_response(response, "Manual Cycle Start")
        
        if response.status_code == 200:
            cycle_data = response.json()
            return cycle_data.get("cycle_id")
        return None
        
    def step3_monitor_cycle(self, cycle_id: str):
        """Step 3: Monitor Cycle Progress"""
        self.print_step(3, "Monitor Cycle Progress")
        
        response = self.session.get(f"{self.base_url}/rsi/cycle/{cycle_id}")
        self.print_response(response, f"Cycle {cycle_id} Status")
        
    def step4_enable_autonomous_mode(self):
        """Step 4: Enable Autonomous Mode"""
        self.print_step(4, "Enable Autonomous Mode")
        
        response = self.session.post(f"{self.base_url}/rsi/autonomous/enable")
        self.print_response(response, "Enable Autonomous Mode")
        
    def step5_check_autonomous_status(self):
        """Step 5: Check Autonomous Status"""
        self.print_step(5, "Check Autonomous Status")
        
        response = self.session.get(f"{self.base_url}/rsi/autonomous/status")
        self.print_response(response, "Autonomous Mode Status")
        
    def step6_manual_trigger(self):
        """Step 6: Manual Trigger in Autonomous Mode"""
        self.print_step(6, "Manual Trigger in Autonomous Mode")
        
        payload = {
            "reason": "Performance optimization needed",
            "context": {
                "cpu_usage": 0.85,
                "memory_usage": 0.9
            }
        }
        
        response = self.session.post(
            f"{self.base_url}/rsi/autonomous/manual-trigger",
            json=payload
        )
        self.print_response(response, "Manual Trigger")
        
    def step7_meta_rsi_metrics(self):
        """Step 7: Monitor Meta-RSI Metrics"""
        self.print_step(7, "Monitor Meta-RSI Metrics")
        
        response = self.session.get(f"{self.base_url}/rsi/meta/metrics")
        self.print_response(response, "Meta-RSI Performance Metrics")
        
    def step8_safety_monitoring(self):
        """Step 8: Safety Monitoring"""
        self.print_step(8, "Safety Monitoring")
        
        # Check GDI status
        response = self.session.get(f"{self.base_url}/safety/gdi")
        self.print_response(response, "Goal Drift Index Status")
        
        # Check constraints
        response = self.session.get(f"{self.base_url}/safety/constraints")
        self.print_response(response, "Constitutional Constraints Summary")
        
    def step9_system_state(self):
        """Step 9: System State Management"""
        self.print_step(9, "System State Management")
        
        response = self.session.get(f"{self.base_url}/system/state")
        self.print_response(response, "Current System State")
        
    def step10_emergency_procedures(self):
        """Step 10: Emergency Procedures (Demonstration)"""
        self.print_step(10, "Emergency Procedures (Demonstration)")
        
        print("The following emergency procedures are available:")
        print()
        print("1. Emergency Stop:")
        print("   curl -X POST http://localhost:8004/rsi/emergency-stop")
        print()
        print("2. Disable Autonomous Mode:")
        print("   curl -X POST http://localhost:8004/rsi/autonomous/disable")
        print()
        print("3. Rollback to Version:")
        print("   curl -X POST http://localhost:8004/system/rollback/0.1.0")
        print()
        print("⚠️  These procedures should only be used in actual emergencies.")
        print()
        
    def run_full_demo(self):
        """Run the complete RSI activation demonstration"""
        print("🧬 Synthos-OS RSI Engine Activation Demonstration")
        print("   Recursive Self-Improvement with Cognitive DNA Evolution")
        print()
        
        # Step 1: Verify status
        if not self.step1_verify_status():
            return
            
        # Step 2: Start manual cycle
        cycle_id = self.step2_start_manual_cycle()
        if cycle_id:
            # Step 3: Monitor cycle
            self.step3_monitor_cycle(cycle_id)
            
        # Step 4: Enable autonomous mode
        self.step4_enable_autonomous_mode()
        
        # Step 5: Check autonomous status
        self.step5_check_autonomous_status()
        
        # Step 6: Manual trigger
        self.step6_manual_trigger()
        
        # Step 7: Meta-RSI metrics
        self.step7_meta_rsi_metrics()
        
        # Step 8: Safety monitoring
        self.step8_safety_monitoring()
        
        # Step 9: System state
        self.step9_system_state()
        
        # Step 10: Emergency procedures
        self.step10_emergency_procedures()
        
        print("🎉 RSI Engine Activation Demonstration Complete!")
        print()
        print("Next Steps:")
        print("1. Monitor improvement cycles")
        print("2. Review Meta-RSI metrics")
        print("3. Configure trigger conditions")
        print("4. Set up monitoring and alerting")
        print()

def main():
    """Main demonstration function"""
    demo = RSIEngineDemo()
    
    print("This demonstration requires the RSI Engine to be running.")
    print("Start it with: docker-compose up -d rsi-engine")
    print()
    
    proceed = input("Proceed with demonstration? (y/n): ")
    if proceed.lower() != 'y':
        print("Demonstration cancelled.")
        return
        
    try:
        demo.run_full_demo()
    except KeyboardInterrupt:
        print("\n\nDemonstration interrupted by user.")
    except Exception as e:
        print(f"\n\nError during demonstration: {e}")
        print("Make sure the RSI Engine is running on http://localhost:8004")

if __name__ == "__main__":
    main()