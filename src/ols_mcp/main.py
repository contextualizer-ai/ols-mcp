################################################################################
# ols_mcp/main.py
# This module sets up the FastMCP CLI interface
################################################################################

from fastmcp import FastMCP

from ols_mcp.tools import (
    get_ontology_info,
    get_similar_ontology_terms,
    get_terms_from_ontology,
    search_all_ontologies,
)

# Create the FastMCP instance at module level
mcp: FastMCP = FastMCP("Ontology Lookup Service (OLS) MCP" ,
                       instructions="""
                        This server provides tools to interact with the OLS API.
                        You can search for ontologies, retrieve information about them,
                        get terms from specific ontologies, and find similar terms across ontologies.
                        Use the available commands to explore and retrieve data from OLS.
                    """)

# Register all tools
mcp.tool(search_all_ontologies)
mcp.tool(get_ontology_info)
mcp.tool(get_terms_from_ontology)
mcp.tool(get_similar_ontology_terms)

def main():
    """Main entry point for the application."""
    mcp.run()


if __name__ == "__main__":
    main()
