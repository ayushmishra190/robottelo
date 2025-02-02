# Architecture Fixtures
import pytest

from robottelo.constants import DEFAULT_ARCHITECTURE


@pytest.fixture(scope='session')
def default_architecture(session_target_sat):
    arch = (
        session_target_sat.api.Architecture()
        .search(query={'search': f'name="{DEFAULT_ARCHITECTURE}"'})[0]
        .read()
    )
    return arch


@pytest.fixture(scope='session')
def session_puppet_default_architecture(session_puppet_enabled_sat):
    arch = (
        session_puppet_enabled_sat.api.Architecture()
        .search(query={'search': f'name="{DEFAULT_ARCHITECTURE}"'})[0]
        .read()
    )
    return arch


@pytest.fixture(scope='module')
def module_architecture(module_target_sat):
    return module_target_sat.api.Architecture().create()
