#!/usr/bin/env python3
"""Implements BootstackQaTests"""

import unittest

import zaza.model


class TestBase(unittest.TestCase):
    """Base class for functional charm tests."""

    @classmethod
    def setUpClass(cls):
        """Run setup for tests."""
        cls.model_name = zaza.model.get_juju_model()


class BootstackQaTests(TestBase):
    """QA tests for charm release."""

    def test01_deploy(self):
        pass

    def test02_test_charms(self):
        pass

    def test20_upgrade_charms(self):
        pass
