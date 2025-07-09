# ols-mcp

A Model Context Protocol (MCP) server for retrieving information from the Ontology Lookup Service (OLS). 

This package provides tools for searching ontologies, retrieving ontology details, and accessing ontology terms through a standardized MCP interface.

## Installation

### From PyPI

```bash
pip install ols-mcp
```

### From Source

```bash
# Clone the repository
git clone https://github.com/contextualizer-ai/ols-mcp.git
cd ols-mcp

# Install with uv (recommended)
uv sync --group dev

# Or with pip
pip install -e .
```

## Usage

### As MCP Server

The primary use case is as an MCP server that provides ontology search capabilities to AI agents and applications.

#### Claude Desktop Integration

Add to your Claude Desktop configuration (`~/Library/Application Support/Claude/claude_desktop_config.json`):

```json
{
  "mcpServers": {
    "ols-mcp": {
      "command": "ols-mcp",
      "args": []
    }
  }
}
```

#### Claude Code Integration

```bash
claude mcp add ols-mcp
```

#### Goose Integration

```bash
goose session start --with-mcp "ols-mcp"
```

### Available Tools

The MCP server provides three main tools:

1. **`search_all_ontologies`** - Search across all ontologies in OLS
2. **`get_ontology_info`** - Get detailed information about a specific ontology
3. **`get_terms_from_ontology`** - Retrieve terms from a specific ontology

### Direct Python Usage

```python
from ols_mcp.tools import search_all_ontologies, get_ontology_info, get_terms_from_ontology

# Search for biological terms
results = search_all_ontologies("apoptosis", max_results=5)

# Get information about Gene Ontology
go_info = get_ontology_info("go")

# Get terms from a specific ontology
terms = get_terms_from_ontology("go", max_results=10)
```

### CLI Usage

#### Running the MCP Server

Run the MCP server directly:

```bash
ols-mcp
```

#### Testing Individual Tools

You can test the tools directly using Python:

```bash
# Search for biological terms across all ontologies
uv run python -c "from ols_mcp.tools import search_all_ontologies; print(search_all_ontologies('apoptosis', max_results=3))"

# Get information about Gene Ontology
uv run python -c "from ols_mcp.tools import get_ontology_info; print(get_ontology_info('go'))"

# Get terms from a specific ontology
uv run python -c "from ols_mcp.tools import get_terms_from_ontology; print(get_terms_from_ontology('go', max_results=3))"
```

#### MCP Protocol Testing

Test the MCP protocol directly:

```bash
# Test basic protocol handshake
make test-mcp

# Test extended protocol with tool calls
make test-mcp-extended
```

## Development

### Prerequisites

- Python 3.11+
- [uv](https://docs.astral.sh/uv/) (recommended) or pip

### Setup

```bash
# Clone the repository
git clone https://github.com/contextualizer-ai/ols-mcp.git
cd ols-mcp

# Install development dependencies
uv sync --group dev
```

### Available Make Targets

#### Development
- `make dev` - Install development dependencies
- `make install` - Install production dependencies only
- `make clean` - Clean build artifacts

#### Testing
- `make test-unit` - Run unit tests (fast, mocked)
- `make test-real-api` - Run integration tests against live OLS API
- `make test-mcp` - Test MCP protocol functionality

#### Code Quality and Maintenance
- `make format` - Format code with Black
- `make lint` - Run Ruff linter with fixes
- `make mypy` - Run type checking
- `make deptry` - Check for unused dependencies
- `make test-coverage` - Run all tests with coverage report
- `make test-integration` - Run integration tests

#### Build & Release
- `make build` - Build package distributions
- `make upload-test` - Upload to TestPyPI
- `make upload` - Upload to PyPI
- `make release` - Complete release workflow (test → build → upload)

#### Server Operations
- `make server` - Run the MCP server locally
- `make all` - Run complete CI pipeline

### Running Tests

```bash
# Run all tests
make test-coverage

# Run only unit tests (fast)
make test-unit

# Run integration tests against real OLS API
make test-real-api

# Run with specific pytest options
uv run pytest tests/ -v -k "test_search"
```

#### Code Quality Tools

The project uses modern Python tooling:

- **uv** - Fast Python package manager
- **ruff** - Fast Python linter and formatter
- **black** - Code formatting (alternative to ruff format)
- **mypy** - Static type checking
- **pytest** - Testing framework with coverage reporting

### Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run the test suite: `make all`
5. Submit a pull request

### Release Process

Releases are automated via GitHub Actions:

1. Create and push a version tag:
   ```bash
   git tag v0.1.4
   git push origin v0.1.4
   ```

2. GitHub Actions will automatically:
   - Run the full test suite
   - Build the package
   - Publish to PyPI

## Architecture

### Project Structure

```
ols-mcp/
├── src/ols_mcp/
│   ├── __init__.py
│   ├── main.py          # FastMCP server setup
│   ├── api.py           # OLS API wrapper functions
│   └── tools.py         # MCP tools that wrap API functions
├── tests/
│   ├── test_api.py      # Unit tests for API functions
│   ├── test_tools.py    # Unit tests for MCP tools
│   └── test_integration.py # Integration tests with real OLS API
├── .github/workflows/   # CI/CD pipelines
├── Makefile            # Development automation
└── pyproject.toml      # Project configuration
```

### Key Components

- **`api.py`** - Low-level functions that interact with OLS REST API
- **`tools.py`** - Higher-level MCP tools that provide simplified interfaces
- **`main.py`** - FastMCP server that exposes tools via MCP protocol

## License

MIT
