# umbc-mcp

## Development

### Pre-commit Hooks

This project uses pre-commit hooks for code quality and consistency. The hooks include:

- **Ruff**: Modern Python linter and formatter
- **Pre-commit hooks**: Basic checks for trailing whitespace, end-of-file fixes, merge conflicts, etc.

#### Setup

Install the development dependencies:
```bash
uv sync --dev
```

Install the pre-commit hooks:
```bash
uv run pre-commit install
```

#### Usage

Run on all files:
```bash
uv run pre-commit run --all-files
```

Run on staged files (automatically runs on commit):
```bash
git commit -m "your message"
```

Run specific hooks:
```bash
uv run pre-commit run ruff --all-files
uv run pre-commit run ruff-format --all-files
```

### Testing

Run tests with:
```bash
PYTHONPATH=. uv run pytest
```
