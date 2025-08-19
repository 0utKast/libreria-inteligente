import os
import pytest
from unittest.mock import patch, Mock
from backend.utils import configure_genai
from dotenv import load_dotenv

@patch.dict(os.environ, {}, clear=True)
def test_configure_genai_no_api_key():
    with pytest.raises(ValueError) as excinfo:
        configure_genai()
    assert "No se encontró la API Key" in str(excinfo.value)

@patch.dict(os.environ, {"GOOGLE_API_KEY": "test_api_key"}, clear=True)
@patch('google.generativeai.configure')
def test_configure_genai_google_api_key(mock_configure):
    configure_genai()
    mock_configure.assert_called_once_with(api_key="test_api_key")

@patch.dict(os.environ, {"GEMINI_API_KEY": "test_api_key"}, clear=True)
@patch('google.generativeai.configure')
def test_configure_genai_gemini_api_key(mock_configure):
    configure_genai()
    mock_configure.assert_called_once_with(api_key="test_api_key")

@patch.dict(os.environ, {"GOOGLE_API_KEY": "test_api_key", "GEMINI_API_KEY": "another_test_api_key"}, clear=True)
@patch('google.generativeai.configure')
def test_configure_genai_both_api_keys(mock_configure):
    configure_genai()
    mock_configure.assert_called_once_with(api_key="test_api_key")

@patch('os.getenv', side_effect=lambda key: None)
@patch('google.generativeai.configure')
def test_configure_genai_no_env(mock_getenv, mock_configure):
    with pytest.raises(ValueError) as excinfo:
        configure_genai()
    assert "No se encontró la API Key" in str(excinfo.value)
    mock_configure.assert_not_called()


@patch.dict(os.environ, {"GOOGLE_API_KEY": "   "}, clear=True)
@patch('google.generativeai.configure')
def test_configure_genai_whitespace_api_key(mock_configure):
    with pytest.raises(ValueError) as excinfo:
        configure_genai()
    assert "No se encontró la API Key" in str(excinfo.value)
    mock_configure.assert_not_called()

@patch('os.getenv', side_effect=lambda key: "test_api_key" if key == "GOOGLE_API_KEY" else None)
@patch('google.generativeai.configure')
def test_configure_genai_google_api_key_only(mock_configure, mock_getenv):
    configure_genai()
    mock_configure.assert_called_once_with(api_key="test_api_key")


@patch('os.getenv', return_value=None)
def test_configure_genai_no_api_key_with_mock(mock_getenv):
    with pytest.raises(ValueError) as excinfo:
        configure_genai()
    assert "No se encontró la API Key" in str(excinfo.value)

@patch('os.getenv', side_effect=lambda key: "test_api_key" if key == "GEMINI_API_KEY" else None)
@patch('google.generativeai.configure')
def test_configure_genai_gemini_api_key_only(mock_configure, mock_getenv):
    configure_genai()
    mock_configure.assert_called_once_with(api_key="test_api_key")

@patch('os.getenv', side_effect=lambda key: "   " if key == "GOOGLE_API_KEY" else None)
@patch('google.generativeai.configure')
def test_configure_genai_whitespace_api_key_getenv(mock_configure, mock_getenv):
    with pytest.raises(ValueError) as excinfo:
        configure_genai()
    assert "No se encontró la API Key" in str(excinfo.value)
    mock_configure.assert_not_called()

@patch('os.getenv', side_effect=lambda key: "test_api_key" if key == "GOOGLE_API_KEY" else "another_test_api_key")
@patch('google.generativeai.configure')
def test_configure_genai_both_api_keys_getenv(mock_configure, mock_getenv):
    configure_genai()
    mock_configure.assert_called_once_with(api_key="test_api_key")

@patch('os.getenv', side_effect=lambda key: "test_api_key" if key == "GOOGLE_API_KEY" else "another_test_api_key")
@patch('google.generativeai.configure')
def test_configure_genai_both_api_keys_getenv_with_exception(mock_configure, mock_getenv):
    mock_configure.side_effect = Exception("Error al configurar la API")
    with pytest.raises(Exception) as excinfo:
        configure_genai()
    assert "Error al configurar la API" in str(excinfo.value)

@patch('os.getenv', side_effect=lambda key: "test_api_key" if key == "GOOGLE_API_KEY" else None)
@patch('google.generativeai.configure')
def test_configure_genai_google_api_key_only_with_exception(mock_configure, mock_getenv):
    mock_configure.side_effect = Exception("Error al configurar la API")
    with pytest.raises(Exception) as excinfo:
        configure_genai()
    assert "Error al configurar la API" in str(excinfo.value)


@patch('os.getenv', side_effect=lambda key: "test_api_key" if key == "GEMINI_API_KEY" else None)
@patch('google.generativeai.configure')
def test_configure_genai_gemini_api_key_only_with_exception(mock_configure, mock_getenv):
    mock_configure.side_effect = Exception("Error al configurar la API")
    with pytest.raises(Exception) as excinfo:
        configure_genai()
    assert "Error al configurar la API" in str(excinfo.value)