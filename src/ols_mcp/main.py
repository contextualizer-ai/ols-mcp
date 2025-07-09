################################################################################
# ols_mcp/main.py
# This module sets up the FastMCP CLI interface
################################################################################

from fastmcp import FastMCP

from ols_mcp.tools import (
    get_ontology_info,
    get_terms_from_ontology,
    search_all_ontologies,
)

# Create the FastMCP instance at module level
mcp: FastMCP = FastMCP("ols_mcp")

# Register all tools
mcp.tool(search_all_ontologies)
mcp.tool(get_ontology_info)
mcp.tool(get_terms_from_ontology)


def main():
    """Main entry point for the application."""
    mcp.run()


if __name__ == "__main__":
    main()
