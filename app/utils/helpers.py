import uuid
from typing import Optional

def generate_id() -> str:
    """Generate a unique identifier."""
    return str(uuid.uuid4())

def validate_prompt(prompt: Optional[str]) -> bool:
    """Validate that a prompt is not empty or None."""
    return bool(prompt and prompt.strip())