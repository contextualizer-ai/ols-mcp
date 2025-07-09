.PHONY: test-coverage clean install dev format lint all server build upload-test upload release deptry mypy test-mcp test-mcp-extended test-integration

# Default target
all: clean install dev test-coverage format lint mypy deptry build test-mcp test-mcp-extended test-integration

# Install everything for development
dev:
	uv sync --group dev

# Install production only
install:
	uv sync

# Run tests with coverage
test-coverage:
	uv run pytest --cov=ols_mcp --cov-report=html --cov-report=term tests/

# Clean up build artifacts
clean:
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	rm -rf src/*.egg-info

# Run server mode
server:
	uv run python src/ols_mcp/main.py

# Format code with black
format:
	uv run black src/ tests/

lint:
	uv run ruff check --fix src/ tests/

# Check for unused dependencies
deptry:
	uvx deptry .

# Type checking
mypy:
	uv run mypy src/

# Build package with hatch
build:
	uv run hatch build

# Upload to TestPyPI (using token-based auth)
upload-test:
	uv run twine upload --repository testpypi dist/*

# Upload to PyPI (using token-based auth - set TWINE_PASSWORD environment variable first)
upload:
	uv run twine upload dist/*

# Complete release workflow
release: clean test-coverage build upload

# Integration Testing
test-integration:
	@echo "🔬 Testing OLS integration..."
	uv run pytest tests/test_integration.py -v -m integration

# Run all unit tests (mocked)
test-unit:
	@echo "🧪 Running unit tests..."
	uv run pytest tests/test_api.py tests/test_tools.py -v

# Run integration tests that hit real API
test-real-api:
	@echo "🌐 Testing against real OLS API..."
	uv run pytest tests/test_integration.py -v -m integration

# MCP Server testing
test-mcp:
	@echo "Testing MCP protocol handshake..."
	echo '{"jsonrpc": "2.0", "method": "initialize", "params": {"protocolVersion": "1.0", "capabilities": {"tools": {}}, "clientInfo": {"name": "test-client", "version": "1.0.0"}}, "id": 1}' | timeout 3 uv run python src/ols_mcp/main.py 2>/dev/null | head -1

test-mcp-extended:
	@echo "Testing MCP protocol initialization..."
	@(echo '{"jsonrpc": "2.0", "method": "initialize", "params": {"protocolVersion": "2025-03-26", "capabilities": {"tools": {}}, "clientInfo": {"name": "test-client", "version": "1.0.0"}}, "id": 1}'; \
	 sleep 0.1; \
	 echo '{"jsonrpc": "2.0", "method": "tools/list", "id": 2}'; \
	 sleep 0.1; \
	 echo '{"jsonrpc": "2.0", "method": "tools/call", "params": {"name": "search_ontologies", "arguments": {"term": "cancer", "ontology": "mondo", "n": 2}}, "id": 3}') | \
	timeout 5 uv run python src/ols_mcp/main.py 2>/dev/null | head -10

# OLS MCP - Claude Desktop config:
#   Add to ~/Library/Application Support/Claude/claude_desktop_config.json:
#   {
#     "mcpServers": {
#       "ols-mcp": {
#         "command": "uv",
#         "args": ["run", "python", "src/ols_mcp/main.py"],
#         "cwd": "/path/to/ols-mcp"
#       }
#     }
#   }
#
# Claude Code MCP setup:
#   claude mcp add -s project ols-mcp uv run python src/ols_mcp/main.py
#
# Goose setup:
#   goose session --with-extension "uv run python src/ols_mcp/main.py"