"""Test for Satellite-maintain related Upgrade Scenario's

:Requirement: UpgradedSatellite

:CaseAutomation: Automated

:CaseLevel: Acceptance

:CaseComponent: ForemanMaintain

:Assignee: gtalreja

:TestType: Functional

:CaseImportance: High

:Upstream: No
"""
import pytest


class TestSatelliteMaintain:
    """The test class contains pre-upgrade and post-upgrade scenarios to test
    satellite-maintain utility

    Test Steps:
        1. Before Satellite upgrade, Perform test for "satellite-maintain upgrade list-versions"
        2. Upgrade satellite/capsule.
        3. Perform tests for satellite-maintain upgrade list-versions, after upgrade.
        4. Check if tests passed.
    """

    @staticmethod
    def satellite_upgradable_version_list(sat_obj):
        """
        This function is used to collect the details of satellite version  and upgradable
        version list.

        :return: satellite_version, upgradeable_version, major_version_change
        """

        cmd = "rpm -q satellite > /dev/null && rpm -q satellite --queryformat=%{VERSION}"
        # leaving this section as-is for now but this could be refactored to use sat_obj.version
        satellite_version = sat_obj.execute(cmd)
        if satellite_version.status == 0:
            satellite_version = satellite_version.stdout
        else:
            return [], [], None, None
        satellite_maintain_version = sat_obj.execute(
            "satellite-maintain upgrade list-versions --disable-self-upgrade"
        )
        upgradeable_version = [
            version for version in satellite_maintain_version.stdout if version != ''
        ]
        version_change = 0
        for version in upgradeable_version:
            version_change += int(version.split('.')[0])
        if version_change % 2 == 0:
            major_version_change = False
            y_version = ''
        else:
            major_version_change = True
            y_version = list(set(satellite_maintain_version) - set(satellite_version))[0].split(
                '.'
            )[-1]

        return satellite_version, upgradeable_version, major_version_change, y_version

    @staticmethod
    def version_details(
        satellite_version, major_version_change, y_version, upgrade_stage="pre-upgrade"
    ):
        """
        This function is used to update the details of zstream upgrade and
        next version upgrade
        :param str satellite_version: satellite version would be like 6.5.0, 6.6.0, 6.7.0
        :param bool major_version_change: For major version upgrade like 6.8 to 7.0, 7.0
        to 8.0 etc, then major_version_change would be True.
        :param str y_version: y_version change depends on major_version_change
        :param str upgrade_stage: upgrade stage would be pre or post.
        :return: zstream_version, next_version
        """

        major_version = satellite_version.split('.')[0:1]
        if major_version_change:
            major_version = [int(major_version[0]) + 1].append(y_version)
        else:
            y_version = int(satellite_version.split('.')[0:2][-1])
        zstream_version = ''
        if upgrade_stage == "pre-upgrade":
            major_version.append(str(y_version + 1))
            zstream_version = ".".join(satellite_version.split('.')[0:2]) + ".z"
        else:
            major_version.append(str(y_version))
            major_version.append("z")
        next_version = ".".join(major_version)
        return zstream_version, next_version

    @pytest.mark.pre_upgrade
    def test_pre_satellite_maintain_upgrade_list_versions(self, target_sat):
        """Pre-upgrade sceanrio that tests list of satellite version
        which satellite can be upgraded.

        :id: preupgrade-fc2c54b2-2663-11ea-b47c-48f17f1fc2e1

        :steps:
            1. Run satellite-maintain upgrade list-versions

        :expectedresults: Versions should be current z-stream.

        """
        (
            satellite_version,
            upgradable_version,
            major_version_change,
            y_version,
        ) = self.satellite_upgradable_version_list(target_sat)
        if satellite_version:
            # In future If satellite-maintain packages update add before
            # pre-upgrade test case execution then next version kind of
            # stuff check we can add it here.
            zstream_version, next_version = self.version_details(
                satellite_version[0], major_version_change, y_version
            )
        else:
            zstream_version = -1
        assert zstream_version in upgradable_version

    @pytest.mark.post_upgrade
    def test_post_satellite_maintain_upgrade_list_versions(self, target_sat):
        """Post-upgrade sceanrio that tests list of satellite version
        which satellite can be upgraded.

        :id: postupgrade-0bce689c-2664-11ea-b47c-48f17f1fc2e1

        :steps:
            1. Run satellite-maintain upgrade list-versions.

        :expectedresults: Versions should be next z-stream.

        """
        (
            satellite_version,
            upgradable_version,
            major_version_change,
            y_version,
        ) = self.satellite_upgradable_version_list(target_sat)
        if satellite_version:
            zstream_version, next_version = self.version_details(
                satellite_version[0], major_version_change, y_version, upgrade_stage="post-upgrade"
            )
        else:
            next_version = -1
        assert next_version in upgradable_version
