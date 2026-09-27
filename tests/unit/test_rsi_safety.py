"""Unit tests for RSI Safety Components - Structural Validation"""

import pytest
import os


class TestRSISafetyStructure:
    """Test suite for RSI safety component structure"""

    def test_gatekeeper_module_structure(self):
        """Test gatekeeper module has expected structure"""
        gatekeeper_path = os.path.join(os.path.dirname(__file__), '../../services/rsi-engine/synthos_rsi_engine/safety/gatekeeper.py')
        assert os.path.exists(gatekeeper_path), "Gatekeeper module should exist"
        
        # Check file has content
        with open(gatekeeper_path, 'r') as f:
            content = f.read()
            assert 'Gatekeeper' in content, "Gatekeeper class should be defined"
            assert 'GateResult' in content, "GateResult class should be defined"

    def test_gdi_module_structure(self):
        """Test Goal Drift Index module has expected structure"""
        gdi_path = os.path.join(os.path.dirname(__file__), '../../services/rsi-engine/synthos_rsi_engine/safety/goal_drift_index.py')
        assert os.path.exists(gdi_path), "Goal Drift Index module should exist"
        
        # Check file has content
        with open(gdi_path, 'r') as f:
            content = f.read()
            assert 'GoalDriftIndex' in content, "GoalDriftIndex class should be defined"
            assert 'calculate_gdi' in content, "calculate_gdi method should be defined"

    def test_constitutional_constraints_structure(self):
        """Test constitutional constraints module has expected structure"""
        constraints_path = os.path.join(os.path.dirname(__file__), '../../services/rsi-engine/synthos_rsi_engine/safety/constitutional_constraints.py')
        assert os.path.exists(constraints_path), "Constitutional constraints module should exist"
        
        # Check file has content
        with open(constraints_path, 'r') as f:
            content = f.read()
            assert 'ConstitutionalConstraints' in content, "ConstitutionalConstraints class should be defined"
            assert '19' in content, "Should reference 19 constitutional rules"

    def test_safety_directory_completeness(self):
        """Test safety directory has all expected modules"""
        safety_dir = os.path.join(os.path.dirname(__file__), '../../services/rsi-engine/synthos_rsi_engine/safety')
        expected_files = [
            '__init__.py',
            'gatekeeper.py',
            'goal_drift_index.py',
            'constitutional_constraints.py'
        ]
        
        for expected_file in expected_files:
            file_path = os.path.join(safety_dir, expected_file)
            assert os.path.exists(file_path), f"{expected_file} should exist in safety directory"

    def test_safety_modules_size_validation(self):
        """Test safety modules have substantial implementation"""
        gatekeeper_path = os.path.join(os.path.dirname(__file__), '../../services/rsi-engine/synthos_rsi_engine/safety/gatekeeper.py')
        gdi_path = os.path.join(os.path.dirname(__file__), '../../services/rsi-engine/synthos_rsi_engine/safety/goal_drift_index.py')
        constraints_path = os.path.join(os.path.dirname(__file__), '../../services/rsi-engine/synthos_rsi_engine/safety/constitutional_constraints.py')
        
        # Check files have substantial content (> 100 lines each)
        for file_path in [gatekeeper_path, gdi_path, constraints_path]:
            with open(file_path, 'r') as f:
                lines = f.readlines()
                assert len(lines) > 100, f"{os.path.basename(file_path)} should have substantial implementation"