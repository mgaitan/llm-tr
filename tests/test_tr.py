import os
import tempfile

import click
import pytest

from llm_tr import get_paste, get_system_language_name, read_file_content


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


def test_read_file_content_existing_file():
    """Test reading content from an existing file."""
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as f:
        test_content = "Hola mundo\nEste es un archivo de prueba."
        f.write(test_content)
        f.flush()

        try:
            result = read_file_content(f.name)
            assert result == test_content
        finally:
            os.unlink(f.name)


def test_read_file_content_nonexistent_file():
    """Test reading content from a non-existent file."""
    result = read_file_content("/path/that/does/not/exist.txt")
    assert result is None


def test_read_file_content_directory():
    """Test reading content when path is a directory."""
    with tempfile.TemporaryDirectory() as temp_dir:
        result = read_file_content(temp_dir)
        assert result is None


def test_read_file_content_permission_error(mocker):
    """Test reading content when file has permission issues."""
    mock_path = mocker.patch('llm_tr.Path')
    mock_path_instance = mock_path.return_value
    mock_path_instance.is_file.return_value = True
    mock_path_instance.read_text.side_effect = OSError("Permission denied")

    result = read_file_content("some_file.txt")
    assert result is None


def test_read_file_content_unicode_error(mocker):
    """Test reading content when file has encoding issues."""
    mock_path = mocker.patch('llm_tr.Path')
    mock_path_instance = mock_path.return_value
    mock_path_instance.is_file.return_value = True
    mock_path_instance.read_text.side_effect = UnicodeDecodeError('utf-8', b'', 0, 1, 'invalid start byte')

    result = read_file_content("binary_file.bin")
    assert result is None
