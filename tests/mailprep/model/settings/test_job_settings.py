import unittest
import io

from mailprep.model.settings.job_settings import JobSettings


class TestJobSettings(unittest.TestCase):

    def test_job_setting_from_file(self):
        source_file = io.StringIO('{"properties":{"name": "value"}}')
        job_settings = JobSettings.from_file(source_file)
        actual_value = job_settings.get('properties').get('name')
        assert actual_value == 'value'

    def test_job_settings_merge(self):
        job_settings = JobSettings().initialize({"properties":{"name": "value"}})
        job_settings.merge({"properties":{"name2": "value2"}})
        assert job_settings.get('properties').get('name') == 'value'
        assert job_settings.get('properties').get('name2') == 'value2'
