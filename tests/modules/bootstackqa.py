#!/usr/bin/env python3
"""Implements BootstackQaTests."""

import unittest

from zaza import model


class TestBase(unittest.TestCase):
    """Base class for functional charm tests."""

    @classmethod
    def setUpClass(cls):
        """Run setup for tests."""
        cls.model_name = model.get_juju_model()
        cls.charms = [
            "elasticsearch",
            "filebeat",
            "grafana",
            "graylog",
            "hw-health",
            "mongodb",
            "nagios",
            "nrpe",
            "openstack-service-checks",
            "prometheus",
            "prometheus-alertmanager",
            "prometheus-ceph-exporter",
            "prometheus-openstack-exporter",
            "sysconfig",
            "telegraf",
        ]

    def charm_functests(self):
        """Run some basic functests on the deployed bundle.

        Tests to write:
        - nagios checks are green (with some known exceptions)
        - grafana hosts a known list of dashboards
        - metrics are available from the prometheus exporters and telegraf
        - graylog has entries in the stream
        """
        pass


class BootstackCandidateUpgrade(TestBase):
    """QA tests for charm release.

    Runs a deploy of the bundle using current stable charms, then tests upgrade.
    """

    def test10_upgrade_charms(self):
        """Test upgrade charm to candidate channel."""
        for application_name in self.charms:
            try:
                model.upgrade_charm(
                    application_name, channel="candidate", model_name=self.model_name
                )
            except Exception as e:
                print("Failed to upgrade charm %s with %s" % (application_name, e))
        model.block_until_all_units_idle(self.model_name)

    def test11_test_charms(self):
        """Test charm functionality after upgrade."""
        self.charm_functests()


class BootstackCandidateInstall(TestBase):
    """QA tests for charm release.

    Runs a deploy of the bundle using candidate charms.
    """

    def test11_test_charms(self):
        """Test charm functionality after upgrade."""
        self.charm_functests()
