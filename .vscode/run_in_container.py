#!/usr/bin/env python3
"""
Helper script to run post_consume_script in Docker container
This is used by VS Code launch configuration
"""
import subprocess
import os
import sys

document_id = os.environ.get("DOCUMENT_ID", "1")
container_name = "paperless-ngx-postprocessor-paperless-ngx-1"

# Try to get the actual container name if it's different
try:
    result = subprocess.run(
        ["docker", "ps", "--format", "{{.Names}}"],
        capture_output=True,
        text=True,
        check=True
    )
    import re
    containers = [name for name in result.stdout.strip().split("\n") 
                  if name and re.search(r'paperless.*paperless-ngx', name)]
    if containers:
        container_name = containers[0]
        print(f"Found container: {container_name}")
except Exception as e:
    print(f"Warning: Could not auto-detect container name: {e}")
    print(f"Using default: {container_name}")

cmd = [
    "docker", "exec",
    "-e", f"DOCUMENT_ID={document_id}",
    container_name,
    "bash", "-c",
    "cd /usr/src/paperless-ngx-postprocessor && source venv/bin/activate && python3 post_consume_script.py"
]

print(f"Running: {' '.join(cmd)}")
result = subprocess.run(cmd)
sys.exit(result.returncode)
