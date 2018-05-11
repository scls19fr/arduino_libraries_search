from utils import repository_url_from_archive_url


def test_repository_url():
    url = "http://downloads.arduino.cc/libraries/github.com/bblanchon/ArduinoJson-5.9.0.zip"
    repository_url = repository_url_from_archive_url(url)
    assert repository_url == "https://github.com/bblanchon/ArduinoJson"
