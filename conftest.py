# This file must be at the root of the project
import pytest

from pseudocode_to_py import PseudoToPy


@pytest.fixture(scope="session")
def ptp():
    return PseudoToPy()
