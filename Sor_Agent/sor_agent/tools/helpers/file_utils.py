# sor_agent/tools/helpers/file_utils.py
import os
from pathlib import Path

def read_file(file_path):
    with open(file_path, 'r') as file:
        return file.read()

def write_file(file_path, content):
    with open(file_path, 'w') as file:
        file.write(content)

def list_files(directory, exclude=[]):
    return [f for f in Path(directory).glob('*.py') if f.name not in exclude]
