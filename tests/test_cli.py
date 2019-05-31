from unittest import TestCase

from kneejerk.cli import main
from click.testing import CliRunner


class TestCLI(TestCase):
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
