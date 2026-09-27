"""Integration tests for RSI Engine - Structural Validation"""

import pytest
import os


class TestRSIIntegrationStructure:
    """Integration tests for RSI Engine structure and API definition"""

    def test_rsi_main_module_exists(self):
        """Test RSI main module exists"""
        main_path = os.path.join(os.path.dirname(__file__), '../../services/rsi-engine/synthos_rsi_engine/main.py')
        assert os.path.exists(main_path), "RSI main module should exist"

    def test_rsi_api_endpoints_defined(self):
        """Test RSI API endpoints are defined in main module"""
        main_path = os.path.join(os.path.dirname(__file__), '../../services/rsi-engine/synthos_rsi_engine/main.py')
        with open(main_path, 'r') as f:
            content = f.read()
            
            # Check for key API endpoints
            expected_endpoints = [
                '/rsi/cycle/start',
                '/rsi/cycle/{cycle_id}',
                '/rsi/cycles',
                '/rsi/status',
                '/rsi/emergency-stop',
                '/safety/gdi',
                '/safety/constraints',
                '/system/state',
                '/system/rollback/{version}'
            ]
            
            for endpoint in expected_endpoints:
                assert endpoint in content, f"Endpoint {endpoint} should be defined"

    def test_rsi_fastapi_app_structure(self):
        """Test RSI uses FastAPI application structure"""
        main_path = os.path.join(os.path.dirname(__file__), '../../services/rsi-engine/synthos_rsi_engine/main.py')
        with open(main_path, 'r') as f:
            content = f.read()
            assert 'FastAPI' in content, "Should use FastAPI"
            assert 'app = FastAPI' in content, "Should create FastAPI app instance"
            assert '@app.get' in content or '@app.post' in content, "Should define API routes"

    def test_rsi_cors_configuration(self):
        """Test RSI has CORS configuration"""
        main_path = os.path.join(os.path.dirname(__file__), '../../services/rsi-engine/synthos_rsi_engine/main.py')
        with open(main_path, 'r') as f:
            content = f.read()
            assert 'CORSMiddleware' in content, "Should configure CORS"

    def test_rsi_health_check_endpoint(self):
        """Test RSI has health check endpoint"""
        main_path = os.path.join(os.path.dirname(__file__), '../../services/rsi-engine/synthos_rsi_engine/main.py')
        with open(main_path, 'r') as f:
            content = f.read()
            assert '/health' in content, "Should have health check endpoint"

    def test_rsi_coordinator_integration(self):
        """Test RSI main module integrates coordinator"""
        main_path = os.path.join(os.path.dirname(__file__), '../../services/rsi-engine/synthos_rsi_engine/main.py')
        with open(main_path, 'r') as f:
            content = f.read()
            assert 'RSICoordinator' in content, "Should import and use RSICoordinator"
            assert 'coordinator' in content, "Should create coordinator instance"

    def test_rsi_safety_integration(self):
        """Test RSI main module integrates safety components"""
        main_path = os.path.join(os.path.dirname(__file__), '../../services/rsi-engine/synthos_rsi_engine/main.py')
        with open(main_path, 'r') as f:
            content = f.read()
            assert 'GoalDriftIndex' in content, "Should import GoalDriftIndex"
            assert 'Gatekeeper' in content or 'gatekeeper' in content, "Should integrate gatekeeper"

    def test_rsi_state_manager_integration(self):
        """Test RSI main module integrates state manager"""
        main_path = os.path.join(os.path.dirname(__file__), '../../services/rsi-engine/synthos_rsi_engine/main.py')
        with open(main_path, 'r') as f:
            content = f.read()
            assert 'StateManager' in content, "Should import StateManager"
            assert 'state_manager' in content, "Should create state manager instance"

    def test_rsi_governance_integration(self):
        """Test RSI main module integrates governance components"""
        main_path = os.path.join(os.path.dirname(__file__), '../../services/rsi-engine/synthos_rsi_engine/main.py')
        with open(main_path, 'r') as f:
            content = f.read()
            assert 'ProposalManager' in content or 'AuditLogger' in content, "Should integrate governance components"

    def test_rsi_error_handling(self):
        """Test RSI has error handling"""
        main_path = os.path.join(os.path.dirname(__file__), '../../services/rsi-engine/synthos_rsi_engine/main.py')
        with open(main_path, 'r') as f:
            content = f.read()
            assert 'HTTPException' in content, "Should handle HTTP exceptions"
            assert 'try:' in content and 'except' in content, "Should have try-except blocks"

    def test_rsi_response_models(self):
        """Test RSI defines response models"""
        main_path = os.path.join(os.path.dirname(__file__), '../../services/rsi-engine/synthos_rsi_engine/main.py')
        with open(main_path, 'r') as f:
            content = f.read()
            assert 'BaseModel' in content, "Should use Pydantic BaseModel for responses"
            assert 'ImprovementCycleRequest' in content or 'ImprovementCycleResponse' in content, "Should define request/response models"