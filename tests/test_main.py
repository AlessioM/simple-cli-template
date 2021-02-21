import pytest
from click.testing import CliRunner

import adder.adder
import adder.config
import adder.main


def test_correct_parameters(mocker):
    """tests that the cli app accepts valid parameters and processes them"""
    process_mock = mocker.patch.object(adder.main, "process", return_value=10)
    runner = CliRunner()
    result = runner.invoke(adder.main.command_line, ["--number-a", "20"])
    process_mock.assert_called_once_with(20, adder.config.cfg.default_number_b)
    assert result.exit_code == 0
    assert result.output == "10\n"


@pytest.mark.parametrize("number_a,number_b", [("a", 1), (1, "b")])
def test_invalid_parameters(number_a, number_b):
    """tests that the cli fails with wrong parameters"""
    runner = CliRunner()
    result = runner.invoke(
        adder.main.command_line, ["--number-a", number_a, "--number-b", number_b]
    )
    assert result.exit_code != 0
