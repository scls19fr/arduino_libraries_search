from click.testing import CliRunner

from arduino_libraries_search import main as arduino_libraries_search_main
from arduino_libraries_show_license import main as arduino_libraries_show_license_main


def test_cli_search_noparameters():
    runner = CliRunner()
    result = runner.invoke(arduino_libraries_search_main, [])
    assert result.exit_code == 0

# ToDo: test cli with parameters


def test_cli_show_license():
    runner = CliRunner()
    result = runner.invoke(arduino_libraries_show_license_main, ['ArduinoJson'])
    assert result.exit_code == 0

    runner = CliRunner()
    result = runner.invoke(arduino_libraries_show_license_main, ['XYZArduinoJsonXYZ'])
    assert result.exit_code == 1
