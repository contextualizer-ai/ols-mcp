# ols-mcp

MCP for retrieving things from the Ontology Lookup  Service

## Installation

You can install the package from source:

```bash
pip install -e .
```

Or using uv:

```bash
uv pip install -e .
```

## Usage

You can use the CLI:

```bash
ols_mcp 
```

Or import in your Python code:

```python
from ols_mcp.main import create_mcp

mcp = create_mcp()
mcp.run()
```

## Development

### Local Setup

```bash
# Clone the repository
git clone https://github.com/justaddcoffee/ols-mcp.git
cd ols-mcp

# Install development dependencies
uv pip install -e ".[dev]"
```


## License

BSD-3-Clause
