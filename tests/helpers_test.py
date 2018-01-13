import os

from tests.fixtures import testdir_fixture

from webdriver_manager import helpers


class Test_normalize_outputdir:

    def test_normalize_output_dir(self, testdir_fixture):
        outputdir = helpers.normalize_outputdir()
        assert outputdir == testdir_fixture['path']

        outputdir = helpers.normalize_outputdir(None)
        assert outputdir == testdir_fixture['path']

        outputdir = helpers.normalize_outputdir('some_example')
        expected = os.path.join(testdir_fixture['path'], 'some_example')
        assert outputdir == expected

        drivers_path = os.path.join(testdir_fixture['path'], 'drivers')
        os.makedirs(drivers_path)
        outputdir = helpers.normalize_outputdir()
        assert outputdir == drivers_path