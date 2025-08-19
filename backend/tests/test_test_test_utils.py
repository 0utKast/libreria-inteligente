import os
import pytest
import google.generativeai as genai
from unittest.mock import patch, Mock
from backend.utils import configure_genai
from dotenv import load_dotenv


@patch.dict(os.environ, {})
def test_configure_genai_no_api_key():
    with pytest.raises(ValueError) as excinfo:
        configure_genai()
    assert "No se encontró la API Key" in str(excinfo.value)


@patch.dict(os.environ, {"GOOGLE_API_KEY": "test_api_key"})
@patch("google.generativeai.configure")
def test_configure_genai_google_api_key(mock_configure):
    configure_genai()
    mock_configure.assert_called_once_with(api_key="test_api_key")


@patch.dict(os.environ, {"GEMINI_API_KEY": "test_api_key"})
@patch("google.generativeai.configure")
def test_configure_genai_gemini_api_key(mock_configure):
    configure_genai()
    mock_configure.assert_called_once_with(api_key="test_api_key")


@patch.dict(os.environ, {"GOOGLE_API_KEY": "test_api_key", "GEMINI_API_KEY": "another_test_api_key"})
@patch("google.generativeai.configure")
def test_configure_genai_both_api_keys(mock_configure):
    configure_genai()
    mock_configure.assert_called_once_with(api_key="test_api_key")


@patch("os.getenv", side_effect=lambda key: None)
@patch("google.generativeai.configure")
def test_configure_genai_no_env_variables(mock_getenv,mock_configure):
    with pytest.raises(ValueError) as excinfo:
        configure_genai()
    assert "No se encontró la API Key" in str(excinfo.value)
    mock_configure.assert_not_called()


@patch("os.getenv", return_value=None)
def test_configure_genai_empty_api_key(mock_getenv):
    with pytest.raises(ValueError) as excinfo:
        configure_genai()
    assert "No se encontró la API Key" in str(excinfo.value)



@patch("google.generativeai.configure", side_effect=Exception("Generic error"))
@patch.dict(os.environ, {"GOOGLE_API_KEY": "test_api_key"})
def test_configure_genai_raises_exception(mock_configure):
    with pytest.raises(Exception) as excinfo:
        configure_genai()
    assert "Generic error" in str(excinfo.value)

@patch("os.getenv", return_value="   ")
def test_configure_genai_whitespace_api_key(mock_getenv):
    with pytest.raises(ValueError) as excinfo:
        configure_genai()
    assert "No se encontró la API Key" in str(excinfo.value)

@patch("os.getenv", return_value="test_api_key")
@patch("google.generativeai.configure")
def test_configure_genai_happy_path(mock_configure, mock_getenv):
    configure_genai()
    mock_configure.assert_called_once_with(api_key="test_api_key")

@patch("os.getenv", side_effect=KeyError("API_KEY not found"))
@patch("google.generativeai.configure")
def test_configure_genai_keyerror(mock_getenv, mock_configure):
    with pytest.raises(KeyError) as excinfo:
        configure_genai()
    assert "API_KEY not found" in str(excinfo.value)
    mock_configure.assert_not_called()