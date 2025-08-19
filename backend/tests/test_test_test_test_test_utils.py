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

@patch.dict(os.environ, {"GOOGLE_API_KEY": "test-api-key"})
@patch('google.generativeai.configure')
def test_configure_genai_google_api_key(mock_configure):
    configure_genai()
    mock_configure.assert_called_once_with(api_key="test-api-key")

@patch.dict(os.environ, {"GEMINI_API_KEY": "test-api-key"})
@patch('google.generativeai.configure')
def test_configure_genai_gemini_api_key(mock_configure):
    configure_genai()
    mock_configure.assert_called_once_with(api_key="test-api-key")

@patch.dict(os.environ, {"GOOGLE_API_KEY": "test-api-key", "GEMINI_API_KEY": "another-test-api-key"})
@patch('google.generativeai.configure')
def test_configure_genai_both_api_keys(mock_configure):
    configure_genai()
    mock_configure.assert_called_once_with(api_key="test-api-key")

@patch('os.getenv', side_effect=lambda key: None)
@patch('google.generativeai.configure')
def test_configure_genai_no_env_vars(mock_getenv, mock_configure):
    with pytest.raises(ValueError) as excinfo:
        configure_genai()
    assert "No se encontró la API Key" in str(excinfo.value)
    mock_configure.assert_not_called()

@patch('os.getenv', side_effect=lambda key: "test-api-key" if key == "GOOGLE_API_KEY" else None)
@patch('google.generativeai.configure', side_effect=Exception("API error"))
def test_configure_genai_api_error(mock_configure, mock_getenv):
    with pytest.raises(Exception) as excinfo:
        configure_genai()
    assert "API error" in str(excinfo.value)

@patch('os.getenv', return_value="test-api-key")
@patch('google.generativeai.configure')
def test_configure_genai_happy_path(mock_configure, mock_getenv):
    configure_genai()
    mock_configure.assert_called_once_with(api_key="test-api-key")

@patch('os.getenv', side_effect=lambda key: "  test-api-key  " if key == "GOOGLE_API_KEY" else None)
@patch('google.generativeai.configure')
def test_configure_genai_whitespace_api_key(mock_configure, mock_getenv):
    configure_genai()
    mock_configure.assert_called_once_with(api_key="  test-api-key  ")

@patch('os.getenv', side_effect=lambda key: "" if key == "GOOGLE_API_KEY" else None)
@patch('google.generativeai.configure')
def test_configure_genai_empty_api_key(mock_configure, mock_getenv):
    with pytest.raises(ValueError) as excinfo:
        configure_genai()
    assert "No se encontró la API Key" in str(excinfo.value)
    mock_configure.assert_not_called()

@patch('os.getenv', side_effect=lambda key: None if key == "GOOGLE_API_KEY" else "test-api-key")
@patch('google.generativeai.configure')
def test_configure_genai_gemini_only(mock_configure, mock_getenv):
    configure_genai()
    mock_configure.assert_called_once_with(api_key="test-api-key")

@patch('google.generativeai.configure', side_effect=TypeError("Invalid API key type"))
@patch('os.getenv', return_value="test-api-key")
def test_configure_genai_type_error(mock_getenv, mock_configure):
    with pytest.raises(TypeError) as excinfo:
        configure_genai()
    assert "Invalid API key type" in str(excinfo.value)