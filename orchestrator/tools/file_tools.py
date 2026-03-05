import os
import subprocess
from pathlib import Path

# Sets the workspace to the directory where you launched the ADK
WORKSPACE_DIR = Path.cwd() / "workspace"

# Ensure the folder exists so the agent doesn't crash on the first write
WORKSPACE_DIR.mkdir(parents=True, exist_ok=True)

def _get_safe_path(path_str: str) -> Path:
    """Helper to ensure the agent stays within the sandbox."""
    # This prevents the agent from using '../' to escape the folder
    requested_path = (WORKSPACE_DIR / path_str).resolve()
    if not str(requested_path).startswith(str(WORKSPACE_DIR.resolve())):
        raise PermissionError(f"Access denied: {path_str} is outside the workspace.")
    return requested_path

def create_project_dir(dir_name: str) -> str:
    """Creates a new directory within the workspace."""
    new_dir = _get_safe_path(dir_name)
    new_dir.mkdir(parents=True, exist_ok=True)
    return f"Created directory: {dir_name}"

def read_file(path: str) -> str:
    """Reads content from a file in the workspace."""
    safe_path = _get_safe_path(path)
    if not safe_path.exists():
        return f"Error: File {path} does not exist."
    return safe_path.read_text(encoding="utf-8")

def write_file(path: str, content: str) -> str:
    """Writes content to a file in the workspace."""
    safe_path = _get_safe_path(path)
    safe_path.parent.mkdir(parents=True, exist_ok=True)
    safe_path.write_text(content, encoding="utf-8")
    return f"Successfully wrote to {path}"

def execute_command(command: str) -> str:
    """Executes a shell command inside the workspace directory."""
    result = subprocess.run(
        command, 
        shell=True, 
        cwd=WORKSPACE_DIR, 
        capture_output=True, 
        text=True
    )
    if result.returncode == 0:
        return result.stdout if result.stdout else "Success."
    return f"Error: {result.stderr}"
