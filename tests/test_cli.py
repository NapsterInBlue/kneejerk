import os
from unittest import TestCase, mock
from click.testing import CliRunner

from kneejerk.cli import main


class TestCLI(TestCase):
    def setUp(self) -> None:
        os.mkdir('tempDir')

    def tearDown(self) -> None:
        os.rmdir('tempDir')

    def test_no_args(self):
        """
        Invoking kneejerk without any arguments should
        provide a helpful prompt that tells available options
        """
        runner = CliRunner()
        result = runner.invoke(main)

        assert result.exit_code == 0
        assert 'Usage' in result.output
        assert '--help' in result.output
        assert 'Commands' in result.output

    def test_empty_dir(self):
        """
        Pointing kneejerk at an empty directory won't fail, but
        will instead provide a message letting the user know
        there weren't any images found
        """
        runner = CliRunner()
        result = runner.invoke(main, ['score', '-i', 'tempDir'])

        assert result.exit_code == 0
        assert "Didn't find image at directory" in result.output

    @mock.patch('kneejerk.image_server.plt.show')
    def test_basic_score(self, mocked_show):
        """
        Calls `kneejerk score`, pointing at a directory that
        has images to verify "No images" warning doesn't show up

        The mock.patch skips over the entire user-interface of
        this function.

        TODO: Figure out how to simulate user input to interface
              with the MPL GUI
        """
        runner = CliRunner()
        result = runner.invoke(main, ['score', '-i', 'tests/images'])

        assert not result.exception
        assert result.exit_code == 0
        assert "Didn't find image at directory" not in result.output
