# Content Component fixtures
import pytest
from manifester import Manifester

from robottelo.config import settings
from robottelo.constants import DEFAULT_LOC
from robottelo.constants import DEFAULT_ORG
from robottelo.utils.manifest import clone


@pytest.fixture(scope='session')
def default_org(session_target_sat):
    return session_target_sat.api.Organization().search(query={'search': f'name="{DEFAULT_ORG}"'})[
        0
    ]


@pytest.fixture(scope='session')
def default_location(session_target_sat):
    return session_target_sat.api.Location().search(query={'search': f'name="{DEFAULT_LOC}"'})[0]


@pytest.fixture
def function_org(target_sat):
    return target_sat.api.Organization().create()


@pytest.fixture(scope='module')
def module_org(module_target_sat):
    return module_target_sat.api.Organization().create()


@pytest.fixture(scope='class')
def class_org(class_target_sat):
    org = class_target_sat.api.Organization().create()
    yield org
    org.delete()


@pytest.fixture(scope='module')
def module_location(module_target_sat, module_org):
    return module_target_sat.api.Location(organization=[module_org]).create()


@pytest.fixture(scope='class')
def class_location(class_target_sat, class_org):
    loc = class_target_sat.api.Location(organization=[class_org]).create()
    yield loc
    loc.delete()


@pytest.fixture
def function_location(target_sat):
    return target_sat.api.Location().create()


@pytest.fixture
def function_location_with_org(target_sat, function_org):
    return target_sat.api.Location(organization=[function_org]).create()


@pytest.fixture(scope='module')
def module_manifest_org(module_target_sat):
    org = module_target_sat.api.Organization().create()
    with clone() as manifest:
        module_target_sat.upload_manifest(org.id, manifest.content)
    return org


@pytest.fixture(scope='module')
def module_org_with_manifest(module_org, module_target_sat):
    """Upload manifest to organization."""
    with clone() as manifest:
        module_target_sat.upload_manifest(module_org.id, manifest.content)
    return module_org


@pytest.fixture(scope='module')
def module_entitlement_manifest_org(module_org, module_entitlement_manifest, module_target_sat):
    """Creates an organization and uploads an entitlement mode manifest generated with manifester"""
    module_target_sat.upload_manifest(module_org.id, module_entitlement_manifest.content)
    module_org.sca_disable()
    return module_org


@pytest.fixture(scope='module')
def module_sca_manifest_org(module_org, module_sca_manifest, module_target_sat):
    """Creates an organization and uploads an SCA mode manifest generated with manifester"""
    module_target_sat.upload_manifest(module_org.id, module_sca_manifest.content)
    return module_org


@pytest.fixture
def function_entitlement_manifest_org(function_org, function_entitlement_manifest, target_sat):
    """Creates an organization and uploads an entitlement mode manifest generated with manifester"""
    target_sat.upload_manifest(function_org.id, function_entitlement_manifest.content)
    function_org.sca_disable()
    return function_org


@pytest.fixture
def function_sca_manifest_org(function_org, function_sca_manifest, target_sat):
    """Creates an organization and uploads an SCA mode manifest generated with manifester"""
    target_sat.upload_manifest(function_org.id, function_sca_manifest.content)
    return function_org


@pytest.fixture(scope='module')
def module_gt_manifest_org(module_target_sat):
    """Creates a new org and loads GT manifest in the new org"""
    org = module_target_sat.api.Organization().create()
    manifest = clone(org_environment_access=True, name='golden_ticket')
    module_target_sat.upload_manifest(org.id, manifest.content, interface='CLI')
    org.manifest_filename = manifest.filename
    return org


# Note: Manifester should not be used with the Satellite QE RHSM account until
# subscription needs are scoped and sufficient subscriptions added to the
# Satellite QE RHSM account. Manifester can be safely used locally with personal
# or stage RHSM accounts.


@pytest.fixture(scope='session')
def session_entitlement_manifest():
    """Yields a manifest in entitlement mode with subscriptions determined by the
    `manifest_category.robottelo_automation` setting in manifester_settings.yaml."""
    with Manifester(manifest_category=settings.manifest.entitlement) as manifest:
        yield manifest


@pytest.fixture(scope='session')
def session_sca_manifest():
    """Yields a manifest in entitlement mode with subscriptions determined by the
    `manifest_category.robottelo_automation` setting in manifester_settings.yaml."""
    with Manifester(manifest_category=settings.manifest.golden_ticket) as manifest:
        yield manifest


@pytest.fixture(scope='module')
def module_entitlement_manifest():
    """Yields a manifest in entitlement mode with subscriptions determined by the
    `manifest_category.robottelo_automation` setting in manifester_settings.yaml."""
    with Manifester(manifest_category=settings.manifest.entitlement) as manifest:
        yield manifest


@pytest.fixture(scope='module')
def module_sca_manifest():
    """Yields a manifest in Simple Content Access mode with subscriptions determined by the
    `manifest_category.golden_ticket` setting in manifester_settings.yaml."""
    with Manifester(manifest_category=settings.manifest.golden_ticket) as manifest:
        yield manifest


@pytest.fixture(scope='function')
def function_entitlement_manifest():
    """Yields a manifest in entitlement mode with subscriptions determined by the
    `manifest_category.robottelo_automation` setting in manifester_settings.yaml."""
    with Manifester(manifest_category=settings.manifest.entitlement) as manifest:
        yield manifest


@pytest.fixture(scope='function')
def function_sca_manifest():
    """Yields a manifest in Simple Content Access mode with subscriptions determined by the
    `manifest_category.golden_ticket` setting in manifester_settings.yaml."""
    with Manifester(manifest_category=settings.manifest.golden_ticket) as manifest:
        yield manifest


@pytest.fixture(scope='module')
def smart_proxy_location(module_org, module_target_sat, default_smart_proxy):
    location = module_target_sat.api.Location(organization=[module_org]).create()
    default_smart_proxy.location.append(module_target_sat.api.Location(id=location.id))
    default_smart_proxy.update(['location'])
    return location
