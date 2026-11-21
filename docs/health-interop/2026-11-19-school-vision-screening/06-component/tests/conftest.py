"""
Pytest configuration and fixtures for School Vision Screening component tests.
"""

import pytest
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from unittest.mock import AsyncMock, MagicMock
import httpx


@pytest.fixture
def mock_httpx_client():
    """Mock httpx.AsyncClient for testing"""
    client = AsyncMock(spec=httpx.AsyncClient)
    return client


@pytest.fixture
def sample_patient():
    """Sample patient data"""
    return {
        "id": "pat-1",
        "family": "Gonzalez",
        "given": ["Maria", "Isabel"],
        "birth_date": "2018-03-15",
        "gender": "female",
        "school_roll": "SCL-2026-0042",
        "national_id": "NHS-1234567890",
    }


@pytest.fixture
def sample_practitioner():
    """Sample practitioner data"""
    return {
        "id": "prac-1",
        "family": "Ruiz",
        "given": ["Carmen"],
        "employee_id": "EMP-2026-015",
        "license_number": "LIC-ENF-2026-004521",
    }


@pytest.fixture
def sample_organization():
    """Sample organization data"""
    return {
        "id": "org-1",
        "name": "Colegio Publico San Isidro",
        "org_type": "school",
        "identifier": "SCH-28079-01",
    }


@pytest.fixture
def sample_encounter():
    """Sample encounter data"""
    return {
        "id": "enc-1",
        "patient_id": "pat-1",
        "practitioner_id": "prac-1",
        "org_id": "org-1",
        "start": "2026-11-15T09:30:00Z",
        "end": "2026-11-15T09:45:00Z",
    }


@pytest.fixture
def goldens_dir():
    """Path to goldens directory"""
    from pathlib import Path
    return Path(__file__).parent / "goldens"


# Goldens loading helpers
def load_golden(goldens_dir: str, category: str, name: str) -> dict:
    """Load a golden file"""
    import json
    from pathlib import Path
    path = Path(goldens_dir) / category / f"{name}.json"
    if path.exists():
        with open(path) as f:
            return json.load(f)
    return None


@pytest.fixture
def load_golden_fn(goldens_dir):
    """Fixture to load golden files"""
    return lambda category, name: load_golden(goldens_dir, category, name)