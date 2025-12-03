# UMBC MCP - AI Chat Service

A robust FastAPI-based chat service that integrates with OpenAI's API, designed for information retrieval and synthesis tasks.

## Features

- **OpenAI Integration**: Seamless integration with OpenAI's Chat Completions API
- **Dynamic System Prompts**: Context-aware prompts with project-specific instructions
- **Comprehensive Error Handling**: Robust error handling for all OpenAI API scenarios
- **Request Validation**: Input validation for message content and structure
- **Stateless Design**: RESTful API without conversation persistence
- **Production Ready**: Comprehensive testing, code quality tools, and monitoring integration

## Quick Start

### Prerequisites

- Python 3.12+
- OpenAI API key
- uv package manager (recommended)

### Installation

1. Clone the repository:
```bash
git clone https://github.com/mikhailstasyuk/umbc-mcp.git
cd umbc-mcp
```

2. Install dependencies:
```bash
uv sync
```

3. Set up environment variables:
```bash
cp .env.example .env
# Edit .env and add your OPENAI_API_KEY
```

4. Run the application:
```bash
uv run fastapi dev src/app/main.py
```

The API will be available at `http://localhost:8000`

## API Usage

### Health Check

```bash
curl http://localhost:8000/health
```

Response:
```json
{"status": "healthy"}
```

### Chat Endpoint

Send a POST request to `/chat` with your conversation:

```bash
curl -X POST "http://localhost:8000/chat" \
     -H "Content-Type: application/json" \
     -d '{
       "model": "gpt-4",
       "messages": [
         {"role": "user", "content": "What is machine learning?"}
       ]
     }'
```

#### Request Format

```json
{
  "model": "gpt-4",
  "messages": [
    {
      "role": "user",
      "content": "Your message here"
    }
  ]
}
```

#### Response Format

```json
{
  "message": "AI response here"
}
```

### Error Responses

The API returns appropriate HTTP status codes for different error scenarios:

- `401`: Authentication failed (invalid API key)
- `404`: Model not found
- `422`: Invalid request (empty messages, oversized content)
- `429`: Rate limit exceeded
- `500`: Internal server error
- `502`: Connection error
- `503`: Service unavailable (missing configuration)

## Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `OPENAI_API_KEY` | Your OpenAI API key | Required |
| `PROJECT_NAME` | Name of your project | "The current project" |
| `PROJECT_DESCRIPTION` | Project description | "The current project description" |
| `BASE_SYSTEM_PROMPT` | Base system prompt for AI | Specialized retrieval prompt |
| `CHAT_HISTORY_LIMIT` | Max messages to include in context | 20 |
| `MAX_CHAT_ITERATIONS` | Max retrieval attempts | 5 |
| `RETRIEVAL_TOP_K` | Top results to retrieve | 10 |
| `MAX_MESSAGE_LENGTH` | Max characters per message | 10000 |

## Development

### Running Tests

```bash
# Run all tests
uv run pytest

# Run with coverage
uv run coverage run -m pytest
uv run coverage xml

# Run specific test file
uv run pytest tests/unit/test_chat_service.py
```

### Code Quality

```bash
# Run pre-commit hooks
pre-commit run --all-files

# Run SonarQube analysis
sonar-scanner
```

### Project Structure

```
src/
├── app/
│   ├── chat/
│   │   ├── dependencies.py    # Dependency injection
│   │   ├── exceptions.py      # Custom exceptions
│   │   ├── prompts.py         # System prompt generation
│   │   ├── router.py          # API endpoints
│   │   ├── schemas.py         # Pydantic models
│   │   └── service.py         # Business logic
│   ├── config.py              # Application settings
│   ├── llm_providers/
│   │   └── client.py          # OpenAI client setup
│   └── main.py                # FastAPI application
tests/
├── unit/
│   ├── chat/
│   ├── llm_providers/
│   └── routers/
└── conftest.py                # Test fixtures
```

## API Documentation

When running the application, visit `http://localhost:8000/docs` for interactive Swagger documentation.

## Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/your-feature`
3. Write tests for your changes
4. Ensure all tests pass: `uv run pytest`
5. Run code quality checks: `pre-commit run --all-files`
6. Commit your changes: `git commit -m "feat: add your feature"`
7. Push to your branch: `git push origin feature/your-feature`
8. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For questions or issues, please open an issue on GitHub.
