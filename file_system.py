# file_system.py
import os
from datetime import datetime

# Enhanced file system simulation with better structure tracking
file_system = {
    'Root': {
        'type': 'directory',
        'contents': {},
        'owner': 'system',
        'created': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
}

def create_file(filename, content, owner="user"):
    """Enhanced to prevent duplicate filenames and validate inputs"""
    if not filename or not isinstance(filename, str):
        raise ValueError("Filename must be a non-empty string")
    
    if filename in file_system['Root']['contents']:
        raise ValueError(f"File '{filename}' already exists")
    
    size_bytes = len(content.encode('utf-8'))
    file_system['Root']['contents'][filename] = {
        'type': 'file',
        'content': content,
        'size': size_bytes,
        'owner': owner,
        'created': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    return file_system['Root']['contents'][filename]

def read_file(filename):
    """Enhanced with better error handling"""
    if filename not in file_system['Root']['contents']:
        raise FileNotFoundError(f"File '{filename}' not found")
    return file_system['Root']['contents'][filename]['content']

def delete_file(filename):
    """Enhanced with validation"""
    if filename not in file_system['Root']['contents']:
        return False
    del file_system['Root']['contents'][filename]
    return True

def list_files():
    """Now returns consistent data structure with all required fields"""
    return [
        {
            'name': name,
            'owner': details['owner'],
            'size': details['size'],
            'created': details['created'],
            'type': details['type']
        }
        for name, details in file_system['Root']['contents'].items()
    ]

def get_directory_structure():
    def traverse(node):
        items = []
        for name, details in node.get("contents", {}).items():
            item = {
                "name": name,
                "type": details["type"]
            }
            if details["type"] == "directory":
                item["contents"] = traverse(details)
            items.append(item)
        return items

    return {"Root": traverse(file_system["Root"])}