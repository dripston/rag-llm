import os
import json

def test_file_paths():
    """Test file paths and working directory"""
    print(f"Current working directory: {os.getcwd()}")
    print(f"Files in current directory: {os.listdir('.')}")
    
    # Check if the file exists
    file_path = "embedded_prisma_data.json"
    print(f"Does {file_path} exist? {os.path.exists(file_path)}")
    
    # Try to create a test file
    test_data = [{"test": "data"}]
    try:
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(test_data, f, indent=2)
        print(f"Successfully created {file_path}")
    except Exception as e:
        print(f"Error creating {file_path}: {e}")
    
    # Try to read it back
    try:
        if os.path.exists(file_path):
            with open(file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            print(f"Successfully read {file_path}: {data}")
        else:
            print(f"{file_path} does not exist after creation attempt")
    except Exception as e:
        print(f"Error reading {file_path}: {e}")

if __name__ == "__main__":
    test_file_paths()