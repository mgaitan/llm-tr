import click
import pytest

from llm_tr import get_paste, get_system_language_name


def test_get_system_language_name_en_locale(mocker):
    mocker.patch("locale.getdefaultlocale", return_value=("en_US", "UTF-8"))

    result = get_system_language_name()
    assert result == "english"


def test_get_system_language_name_es_locale(mocker):
    mocker.patch("locale.getdefaultlocale", return_value=("es_ES", "UTF-8"))
    result = get_system_language_name()
    assert result == "spanish"


def test_get_paste_success(mocker):
    mock_pyclip = mocker.patch("llm_tr.pyclip")
    mock_pyclip.paste.return_value = "test text"

    result = get_paste()
    assert result == "test text"


def test_get_paste_no_pyclip(mocker):
    mocker.patch("llm_tr.pyclip", None)

    with pytest.raises(click.BadParameter):
        get_paste()
