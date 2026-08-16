from crewai.tools import tool
from pathlib import Path
import shutil
import subprocess


SANDBOX_DIR = Path(__file__).parents[3] / "sandbox"
SANDBOX_DIR.mkdir(parents=True, exist_ok=True)
address = (SANDBOX_DIR / "AI-Digital-Hoodad")

def reset_sandbox() -> None:
    """Wipe the sandbox and re-initialize it as a fresh uv project with gradio."""
    if SANDBOX_DIR.exists():
        shutil.rmtree(SANDBOX_DIR)
    SANDBOX_DIR.mkdir(parents=True)

    subprocess.run(["uv", "init", "--bare", "--python", "3.13"], cwd=SANDBOX_DIR, check=True)
    subprocess.run(["uv", "add", "gradio"], cwd=SANDBOX_DIR, check=True)
    subprocess.run(["uv", "add", "httpcore"], cwd=SANDBOX_DIR, check=True)

@tool
def repo_cloner(url: str) -> str:
    """Clone the Github repo into the sandbox directory"""
    result = subprocess.run(
    ["git", "clone", url],  # Run git clone
    cwd=SANDBOX_DIR,        # Run it inside sandbox
    capture_output=True,    # Capture what git says
    text=True,              # Give me that output as strings
    check=True,             # Stop/raise an error if git fails
)
    return result.stdout

@tool("List Sandbox Files")
def list_sandbox_files() -> str:
    """
    List the filenames currently in the sandbox directory.

    Returns:
        A newline-separated list of filenames, or a message if the
        sandbox is empty.
    """
    names = sorted(p.name for p in address.iterdir())
    return "\n".join(names) if names else "The sandbox is empty."


@tool("Read Sandbox File")
def read_sandbox_file(filename: str) -> str:
    """
    Read and return the text contents of a file in the sandbox directory.

    Args:
        filename: The name of the file to read (e.g. "solution.py").
    Returns:
        The file's contents, or a message if the file does not exist.
    """
    path = address/filename
    if not path.is_file():
        return f"No such file in the sandbox: {filename}"
    return path.read_text()


sandbox_tools = [list_sandbox_files,read_sandbox_file,repo_cloner]
