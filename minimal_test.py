# Minimal test to verify basic imports work
try:
    import os
    print("✓ os imported successfully")
except Exception as e:
    print(f"✗ Error importing os: {e}")

try:
    import json
    print("✓ json imported successfully")
except Exception as e:
    print(f"✗ Error importing json: {e}")

try:
    from flask import Flask
    print("✓ flask imported successfully")
except Exception as e:
    print(f"✗ Error importing flask: {e}")

try:
    from flask_cors import CORS
    print("✓ flask_cors imported successfully")
except Exception as e:
    print(f"✗ Error importing flask_cors: {e}")

try:
    from dotenv import load_dotenv
    print("✓ python-dotenv imported successfully")
except Exception as e:
    print(f"✗ Error importing python-dotenv: {e}")

try:
    import requests
    print("✓ requests imported successfully")
except Exception as e:
    print(f"✗ Error importing requests: {e}")

print("Minimal test completed!")