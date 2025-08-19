import os
import pytest
from unittest.mock import patch, MagicMock
from backend.utils import configure_genai
from dotenv import load_dotenv

@patch.dict(os.environ, {}, clear=True)
def test_configure_genai_no_api_key():
    with pytest.raises(ValueError) as excinfo:
        configure_genai()
    assert "No se encontró la API Key" in str(excinfo.value)

@patch.dict(os.environ, {"GOOGLE_API_KEY": "test_api_key"})
@patch('google.generativeai.configure')
def test_configure_genai_google_api_key(mock_configure):
    configure_genai()
    mock_configure.assert_called_once_with(api_key="test_api_key")

@patch.dict(os.environ, {"GEMINI_API_KEY": "test_api_key"})
@patch('google.generativeai.configure')
def test_configure_genai_gemini_api_key(mock_configure):
    configure_genai()
    mock_configure.assert_called_once_with(api_key="test_api_key")

@patch.dict(os.environ, {"GOOGLE_API_KEY": "test_api_key", "GEMINI_API_KEY": "another_test_api_key"})
@patch('google.generativeai.configure')
def test_configure_genai_both_api_keys(mock_configure):
    configure_genai()
    mock_configure.assert_called_once_with(api_key="test_api_key")

@patch('os.getenv', return_value=None)
@patch('google.generativeai.configure')
def test_configure_genai_no_env_file(mock_getenv, mock_configure):
    with pytest.raises(ValueError) as excinfo:
        configure_genai()
    assert "No se encontró la API Key" in str(excinfo.value)
    mock_configure.assert_not_called()

@patch('os.getenv', side_effect=Exception('Error reading env'))
def test_configure_genai_env_error(mock_getenv):
    with pytest.raises(Exception) as excinfo:
      configure_genai()
    assert "Error reading env" in str(excinfo.value)


@patch('google.generativeai.configure', side_effect=Exception("Error configuring API"))
@patch.dict(os.environ, {"GOOGLE_API_KEY": "test_api_key"})
def test_configure_genai_api_config_error(mock_configure):
    with pytest.raises(Exception) as excinfo:
        configure_genai()
    assert "Error configuring API" in str(excinfo.value)

@patch('os.getenv', return_value="test_api_key_from_env")
@patch('google.generativeai.configure')
def test_configure_genai_from_env_file(mock_getenv, mock_configure):
    configure_genai()
    mock_configure.assert_called_once_with(api_key="test_api_key_from_env")

@patch.dict(os.environ, {"GOOGLE_API_KEY": ""})
@patch('google.generativeai.configure')
def test_configure_genai_empty_api_key(mock_configure):
    with pytest.raises(ValueError) as excinfo:
        configure_genai()
    assert "No se encontró la API Key" in str(excinfo.value)
    mock_configure.assert_not_called()

@patch.dict(os.environ, {"GOOGLE_API_KEY": "   "})
@patch('google.generativeai.configure')
def test_configure_genai_whitespace_api_key(mock_configure):
    with pytest.raises(ValueError) as excinfo:
        configure_genai()
    assert "No se encontró la API Key" in str(excinfo.value)
    mock_configure.assert_not_called()

@patch('os.getenv', return_value="  ")
@patch('google.generativeai.configure')
def test_configure_genai_whitespace_api_key_env(mock_getenv, mock_configure):
    with pytest.raises(ValueError) as excinfo:
        configure_genai()
    assert "No se encontró la API Key" in str(excinfo.value)
    mock_configure.assert_not_called()