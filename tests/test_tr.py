import pytest
import os
import locale
from llm_tr import get_system_language_name


def test_get_system_language_name_en_locale(mocker):
    mocker.patch('locale.getdefaultlocale', return_value=('en_US', 'UTF-8'))

    result = get_system_language_name()
    assert result == "english"

def test_get_system_language_name_es_locale(mocker):
    mocker.patch('locale.getdefaultlocale', return_value=('es_ES', 'UTF-8'))
    result = get_system_language_name()
    assert result == "spanish"
