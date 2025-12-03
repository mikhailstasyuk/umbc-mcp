from src.app.chat.prompts import get_system_prompt


def test_get_system_prompt_includes_project_name():
    """Verify system prompt includes the project name."""
    prompt = get_system_prompt(
        project_name="Test Project",
        project_description="A test description",
        base_prompt="You are a helpful assistant",
        max_attempts=5,
    )

    assert "Test Project" in prompt


def test_get_system_prompt_includes_project_description():
    """Verify system prompt includes the project description."""
    prompt = get_system_prompt(
        project_name="Test Project",
        project_description="A test description",
        base_prompt="You are a helpful assistant",
        max_attempts=5,
    )

    assert "A test description" in prompt


def test_get_system_prompt_includes_base_prompt():
    """Verify system prompt includes the base prompt."""
    prompt = get_system_prompt(
        project_name="Test Project",
        project_description="A test description",
        base_prompt="You are a helpful assistant",
        max_attempts=5,
    )

    assert "You are a helpful assistant" in prompt


def test_get_system_prompt_includes_max_attempts():
    """Verify system prompt includes the max attempts value."""
    prompt = get_system_prompt(
        project_name="Test Project",
        project_description="A test description",
        base_prompt="You are a helpful assistant",
        max_attempts=7,
    )

    assert "7" in prompt


def test_get_system_prompt_returns_string():
    """Verify system prompt returns a string."""
    prompt = get_system_prompt(
        project_name="Test Project",
        project_description="A test description",
        base_prompt="You are a helpful assistant",
        max_attempts=5,
    )

    assert isinstance(prompt, str)
    assert len(prompt) > 0
