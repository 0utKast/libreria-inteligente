import os
import pytest
from unittest.mock import patch
from backend.utils import configure_genai

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

@patch('os.getenv', side_effect=lambda x: None)
@patch('google.generativeai.configure')
def test_configure_genai_no_env(mock_getenv, mock_configure):
    with pytest.raises(ValueError) as excinfo:
        configure_genai()
    assert "No se encontró la API Key" in str(excinfo.value)
    mock_configure.assert_not_called()


@patch('os.getenv', side_effect=lambda x: "test_api_key" if x == "GOOGLE_API_KEY" else None)
@patch('google.generativeai.configure')
def test_configure_genai_google_api_key_only(mock_getenv,mock_configure):
    configure_genai()
    mock_configure.assert_called_once_with(api_key="test_api_key")

@patch('os.getenv', side_effect=lambda x: "test_api_key" if x == "GEMINI_API_KEY" else None)
@patch('google.generativeai.configure')
def test_configure_genai_gemini_api_key_only(mock_getenv,mock_configure):
    configure_genai()
    mock_configure.assert_called_once_with(api_key="test_api_key")

@patch.dict(os.environ, {"GOOGLE_API_KEY": ""})
@patch('google.generativeai.configure')
def test_configure_genai_empty_google_api_key(mock_configure):
    with pytest.raises(ValueError) as excinfo:
        configure_genai()
    assert "No se encontró la API Key" in str(excinfo.value)
    mock_configure.assert_not_called()

@patch.dict(os.environ, {"GEMINI_API_KEY": ""})
@patch('google.generativeai.configure')
def test_configure_genai_empty_gemini_api_key(mock_configure):
    with pytest.raises(ValueError) as excinfo:
        configure_genai()
    assert "No se encontró la API Key" in str(excinfo.value)
    mock_configure.assert_not_called()

@patch('os.getenv', side_effect=lambda x: "   " if x == "GOOGLE_API_KEY" else None)
@patch('google.generativeai.configure')
def test_configure_genai_whitespace_google_api_key(mock_getenv, mock_configure):
    with pytest.raises(ValueError) as excinfo:
        configure_genai()
    assert "No se encontró la API Key" in str(excinfo.value)
    mock_configure.assert_not_called()

@patch('os.getenv', side_effect=lambda x: "   " if x == "GEMINI_API_KEY" else None)
@patch('google.generativeai.configure')
def test_configure_genai_whitespace_gemini_api_key(mock_getenv, mock_configure):
    with pytest.raises(ValueError) as excinfo:
        configure_genai()
    assert "No se encontró la API Key" in str(excinfo.value)
    mock_configure.assert_not_called()