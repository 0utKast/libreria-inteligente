import os
import sys
import pathlib
import re
from unittest.mock import patch, MagicMock
import pytest
from google.generativeai import GenerativeModel, GenerateContentResponse

# Mock the google.generativeai module
class MockGenerativeModel:
    def __init__(self, model_name):
        self.model_name = model_name

    def generate_content(self, prompt):
        #Simulate different responses for testing purposes.
        if "Error" in prompt:
            raise Exception("Simulated Gemini API Error")
        elif "no supported" in prompt:
            return MockGenerateContentResponse(text="")
        elif "test_file.py" in prompt:
            return MockGenerateContentResponse(text="```python\nassert True\n```")
        elif "test_file.js" in prompt:
            return MockGenerateContentResponse(text="```javascript\ntest('test', () => {});\n```")
        else:
            return MockGenerateContentResponse(text="```python\nassert 1 == 1\n```")

class MockGenerateContentResponse:
    def __init__(self, text):
        self.text = text

@patch('google.generativeai.GenerativeModel', MockGenerativeModel)
def test_generate_test_file_success():
    # Test with a valid Python file
    test_file = pathlib.Path("./test_file.py")
    test_file.write_text("def test_func():\n    return True")
    with patch.dict(os.environ, {"GEMINI_API_KEY": "test_key"}):
        generate_test_file(str(test_file))
    test_file.unlink()

    #Test with a valid JavaScript file
    test_file = pathlib.Path("./test_file.js")
    test_file.write_text("const test = 1;")
    with patch.dict(os.environ, {"GEMINI_API_KEY": "test_key"}):
        generate_test_file(str(test_file))
    test_file.unlink()

@patch('google.generativeai.GenerativeModel', MockGenerativeModel)
def test_generate_test_file_error():
    # Test with API error
    test_file = pathlib.Path("./error_file.py")
    test_file.write_text("def error_func():\n    return False")
    with patch.dict(os.environ, {"GEMINI_API_KEY": "test_key"}):
        with pytest.raises(Exception) as e:
            generate_test_file(str(test_file))
            assert "Simulated Gemini API Error" in str(e.value)
    test_file.unlink()

@patch('google.generativeai.GenerativeModel', MockGenerativeModel)
def test_generate_test_file_not_supported():
    # Test with unsupported file type
    test_file = pathlib.Path("./test_file.txt")
    test_file.write_text("This is a text file.")
    with patch.dict(os.environ, {"GEMINI_API_KEY": "test_key"}):
        generate_test_file(str(test_file))
    test_file.unlink()


@patch('google.generativeai.GenerativeModel', MockGenerativeModel)
def test_generate_test_file_missing_api_key():
    test_file = pathlib.Path("./test_file.py")
    test_file.write_text("def test_func():\n    return True")
    with pytest.raises(SystemExit) as e:
        with patch.dict(os.environ, {}):
            generate_test_file(str(test_file))
    assert e.type == SystemExit
    test_file.unlink()


@patch('google.generativeai.GenerativeModel', MockGenerativeModel)
def test_generate_test_file_file_not_found():
    with patch.dict(os.environ, {"GEMINI_API_KEY": "test_key"}):
        generate_test_file("nonexistent_file.py")

#Import the function from the original file (replace with actual path if needed)
from backend.scripts.generate_tests import generate_test_file