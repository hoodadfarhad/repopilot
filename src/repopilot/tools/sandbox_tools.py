from crewai.tools import tool
from pathlib import Path
import shutil
import subprocess


SANDBOX_DIR = Path(__file__).parents[3] / "sandbox"
SANDBOX_DIR.mkdir(parents=True, exist_ok=True)


def reset_sandbox() -> None:
    """Wipe the sandbox and re-initialize it as a fresh uv project with gradio."""
    if SANDBOX_DIR.exists():
        shutil.rmtree(SANDBOX_DIR)
    SANDBOX_DIR.mkdir(parents=True)

    subprocess.run(["uv", "init", "--bare", "--python", "3.13"], cwd=SANDBOX_DIR, check=True)
    subprocess.run(["uv", "add", "gradio"], cwd=SANDBOX_DIR, check=True)
    subprocess.run(["uv", "add", "httpcore"], cwd=SANDBOX_DIR, check=True)

def get_repo_path() -> Path:
    """Return the cloned repository directory inside the sandbox."""
    repos = [p for p in SANDBOX_DIR.iterdir() if p.is_dir()]

    if len(repos) != 1:
        raise ValueError("Expected exactly one cloned repository in the sandbox.")

    return repos[0]





@tool
def repo_cloner(url: str) -> str:
    """Clone the Github repo into the sandbox directory"""
    result = subprocess.run(
    ["git", "clone", url],  
    cwd=SANDBOX_DIR,        
    capture_output=True,    
    text=True,                        
)
    print("RETURN CODE:", result.returncode)
    print("STDOUT:", result.stdout)
    print("STDERR:", result.stderr)

    if result.returncode != 0:
        return f"Clone failed:\n{result.stderr}"
    
    repo_path = get_repo_path()

    return f"Repository cloned successfully to: {repo_path}"

@tool
def list_sandbox_files() -> str:
    """List all files in the cloned repository."""
    EXCLUDED_DIRS = {
    # Version control
    ".git",
    ".svn",
    ".hg",

    # Python
    "__pycache__",
    ".venv",
    "venv",
    "env",
    ".tox",
    ".mypy_cache",
    ".pytest_cache",

    # JavaScript / TypeScript
    "node_modules",
    ".next",
    ".nuxt",
    "dist",
    "build",
    "coverage",

    # Java / Gradle
    "target",
    ".gradle",

    # Rust
    "target",

    # Go
    "vendor",

    # General tooling / IDEs
    ".idea",
    ".vscode",

    # Caches
    ".cache",
            }   
    address = get_repo_path();
    files = sorted(
    str(p.relative_to(address))
    for p in address.rglob("*")
    if p.is_file()
    and not any(part in EXCLUDED_DIRS for part in p.parts)
    )

    return "\n".join(files) if files else "The repository is empty."


@tool("Read Sandbox File")
def read_sandbox_file(filename: str) -> str:
    """
    Read and return the text contents of a file in the sandbox directory.

    Args:
        filename: The name of the file to read (e.g. "solution.py").
    Returns:
        The file's contents, or a message if the file does not exist.
    """
    address = get_repo_path();
    path = address/filename
    if not path.is_file():
        return f"No such file in the sandbox: {filename}"
    return path.read_text()


sandbox_tools = [list_sandbox_files,read_sandbox_file,repo_cloner]
