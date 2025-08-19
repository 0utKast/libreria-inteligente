import os
import pytest
import google.generativeai as genai
from unittest.mock import patch, MagicMock
from backend.utils import configure_genai
from dotenv import load_dotenv

@patch.dict(os.environ, {}, clear=True)  # Limpia las variables de entorno antes de cada prueba
def test_configure_genai_no_api_key():
    with pytest.raises(ValueError) as excinfo:
        configure_genai()
    assert "No se encontró la API Key" in str(excinfo.value)

@patch.dict(os.environ, {"GOOGLE_API_KEY": "test_api_key"})
@patch('google.generativeai.configure')
def test_configure_genai_google_api_key(mock_configure):
    configure_genai()
    mock_configure.assert_called_once_with(api_key="test_api_key")

@patch.dict(os.environ, {"GEMINI_API_KEY": "test_gemini_api_key"})
@patch('google.generativeai.configure')
def test_configure_genai_gemini_api_key(mock_configure):
    configure_genai()
    mock_configure.assert_called_once_with(api_key="test_gemini_api_key")

@patch.dict(os.environ, {"GOOGLE_API_KEY": "test_api_key", "GEMINI_API_KEY": "test_gemini_api_key"})
@patch('google.generativeai.configure')
def test_configure_genai_both_api_keys(mock_configure):
    configure_genai()
    mock_configure.assert_called_once_with(api_key="test_api_key")

@patch('os.getenv', side_effect=lambda key: None) #Simula que os.getenv siempre devuelve None
@patch('google.generativeai.configure')
def test_configure_genai_no_env_vars(mock_configure):
    with pytest.raises(ValueError) as excinfo:
        configure_genai()
    assert "No se encontró la API Key" in str(excinfo.value)
    mock_configure.assert_not_called()


@patch('os.getenv', side_effect=lambda key: "test_api_key" if key == "GOOGLE_API_KEY" else None)
@patch('google.generativeai.configure', side_effect=Exception("Generic Error"))
def test_configure_genai_exception_handling(mock_configure):
    with pytest.raises(Exception) as excinfo:
        configure_genai()
    assert "Generic Error" in str(excinfo.value)