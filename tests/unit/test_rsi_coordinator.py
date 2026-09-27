"""Unit tests for RSI Coordinator - Structural Validation"""

import pytest
import os
import sys

# Add services directory to path for testing
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../services/rsi-engine'))


class TestRSICoordinatorStructure:
    """Test suite for RSI Coordinator structure and implementation"""

    def test_rsi_service_exists(self):
        """Test RSI service directory exists"""
        rsi_path = os.path.join(os.path.dirname(__file__), '../../services/rsi-engine')
        assert os.path.exists(rsi_path), "RSI engine service directory should exist"

    def test_rsi_main_module_exists(self):
        """Test RSI main module exists"""
        main_path = os.path.join(os.path.dirname(__file__), '../../services/rsi-engine/synthos_rsi_engine/main.py')
        assert os.path.exists(main_path), "RSI main module should exist"

    def test_rsi_coordinator_module_exists(self):
        """Test RSI coordinator module exists"""
        coordinator_path = os.path.join(os.path.dirname(__file__), '../../services/rsi-engine/synthos_rsi_engine/core/coordinator.py')
        assert os.path.exists(coordinator_path), "RSI coordinator module should exist"

    def test_rsi_safety_modules_exist(self):
        """Test RSI safety modules exist"""
        safety_dir = os.path.join(os.path.dirname(__file__), '../../services/rsi-engine/synthos_rsi_engine/safety')
        assert os.path.exists(safety_dir), "RSI safety directory should exist"
        
        gatekeeper_path = os.path.join(safety_dir, 'gatekeeper.py')
        gdi_path = os.path.join(safety_dir, 'goal_drift_index.py')
        constraints_path = os.path.join(safety_dir, 'constitutional_constraints.py')
        
        assert os.path.exists(gatekeeper_path), "Gatekeeper module should exist"
        assert os.path.exists(gdi_path), "Goal Drift Index module should exist"
        assert os.path.exists(constraints_path), "Constitutional constraints module should exist"

    def test_rsi_mutation_module_exists(self):
        """Test RSI mutation module exists"""
        mutation_path = os.path.join(os.path.dirname(__file__), '../../services/rsi-engine/synthos_rsi_engine/mutation/generator.py')
        assert os.path.exists(mutation_path), "Mutation generator module should exist"

    def test_rsi_governance_modules_exist(self):
        """Test RSI governance modules exist"""
        governance_dir = os.path.join(os.path.dirname(__file__), '../../services/rsi-engine/synthos_rsi_engine/governance')
        assert os.path.exists(governance_dir), "RSI governance directory should exist"
        
        proposal_path = os.path.join(governance_dir, 'proposal_manager.py')
        audit_path = os.path.join(governance_dir, 'audit_logger.py')
        
        assert os.path.exists(proposal_path), "Proposal manager module should exist"
        assert os.path.exists(audit_path), "Audit logger module should exist"

    def test_rsi_evaluation_module_exists(self):
        """Test RSI evaluation module exists"""
        evaluation_path = os.path.join(os.path.dirname(__file__), '../../services/rsi-engine/synthos_rsi_engine/evaluation/benchmark_runner.py')
        assert os.path.exists(evaluation_path), "Benchmark runner module should exist"

    def test_rsi_config_exists(self):
        """Test RSI configuration exists"""
        config_path = os.path.join(os.path.dirname(__file__), '../../services/rsi-engine/synthos_rsi_engine/config.py')
        assert os.path.exists(config_path), "RSI config module should exist"

    def test_rsi_pyproject_exists(self):
        """Test RSI pyproject.toml exists"""
        pyproject_path = os.path.join(os.path.dirname(__file__), '../../services/rsi-engine/pyproject.toml')
        assert os.path.exists(pyproject_path), "RSI pyproject.toml should exist"

    def test_rsi_readme_exists(self):
        """Test RSI README exists"""
        readme_path = os.path.join(os.path.dirname(__file__), '../../services/rsi-engine/README.md')
        assert os.path.exists(readme_path), "RSI README should exist"