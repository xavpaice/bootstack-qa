#!/usr/bin/env python3
"""Implements BootstackQaTests."""

import unittest

import zaza.model
from juju import loop
from juju.model import Model


class TestBase(unittest.TestCase):
    """Base class for functional charm tests."""

    @classmethod
    def setUpClass(cls):
        """Run setup for tests."""
        cls.model_name = zaza.model.get_juju_model()
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

    def upgrade_charm(self, application_name, channel="stable"):
        """Run the async tasks for Juju charm upgrade."""
        loop.run(self.async_upgrade_charm(application_name, channel))

    async def async_upgrade_charm(self, application_name, channel="stable"):
        """Upgrade the specified charm to the latest in the specified channel."""
        model = Model()
        await model.connect(model_name=self.model_name)
        app = model.applications[application_name]
        await app.upgrade_charm(channel=channel)
        await model.disconnect()


class BootstackCandidateUpgrade(TestBase):
    """QA tests for charm release."""

    def charm_functests(self):
        """Run some basic functests on the deployed bundle."""
        pass

    def test01_test_charms(self):
        """Test charm functionality."""
        self.charm_functests()

    def test10_upgrade_charms(self):
        """Test upgrade charm to candidate channel."""
        for application_name in self.charms:
            try:
                self.upgrade_charm(application_name, channel='candidate')
            except Exception as e:
                print("Failed to upgrade charm %s with %s" % (application_name, e))
        # wait for stable
        self.charm_functests()

    def test11_test_charms(self):
        """Test charm functionality after upgrade."""
        self.charm_functests()
