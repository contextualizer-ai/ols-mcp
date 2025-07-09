################################################################################
# ols_mcp/tools.py
# This module contains tools that consume the generic API wrapper functions in
# ols_mcp/api.py and constrain/transform them based on use cases/applications
################################################################################
from typing import Any

from .api import get_ontology_details, get_ontology_terms, search_ontologies


def search_all_ontologies(
    query: str,
    ontologies: str | None = None,
    max_results: int = 20,
    exact: bool = False,
) -> list[dict[str, Any]]:
    """
    Search across all ontologies in the Ontology Lookup Service (OLS).

    Args:
        query (str): The search term to look for
        ontologies (str, optional): Comma-separated list of ontology IDs to search
            within (e.g., "go,uberon")
        max_results (int): Maximum number of results to return (default: 20)
        exact (bool): Whether to perform exact matching (default: False)

    Returns:
        List[Dict[str, Any]]: List of search results containing term information
    """
    ontology_list = None
    if ontologies:
        ontology_list = [ont.strip() for ont in ontologies.split(",")]

    results = search_ontologies(
        query=query,
        ontologies=ontology_list,
        max_results=max_results,
        exact=exact,
        verbose=True,
    )

    # Simplify the results for easier consumption
    simplified_results = []
    for result in results:
        simplified = {
            "id": result.get("id"),
            "iri": result.get("iri"),
            "short_form": result.get("short_form"),
            "obo_id": result.get("obo_id"),
            "label": result.get("label"),
            "description": result.get("description", []),
            "ontology_name": result.get("ontology_name"),
            "ontology_prefix": result.get("ontology_prefix"),
            "type": result.get("type"),
        }
        simplified_results.append(simplified)

    return simplified_results


def get_ontology_info(ontology_id: str) -> dict[str, Any]:
    """
    Get detailed information about a specific ontology.

    Args:
        ontology_id (str): The ID of the ontology (e.g., 'go', 'uberon', 'chebi')

    Returns:
        Dict[str, Any]: Dictionary containing detailed ontology information
    """
    details = get_ontology_details(ontology_id=ontology_id, verbose=True)

    # Extract key information for easier consumption
    config = details.get("config", {})
    simplified = {
        "id": details.get("ontologyId"),
        "title": config.get("title"),
        "description": config.get("description"),
        "version": config.get("version"),
        "homepage": config.get("homepage"),
        "status": details.get("status"),
        "number_of_terms": details.get("numberOfTerms"),
        "number_of_properties": details.get("numberOfProperties"),
        "number_of_individuals": details.get("numberOfIndividuals"),
        "languages": config.get("preferredLanguage"),
        "created": details.get("created"),
        "updated": details.get("updated"),
        "loaded": details.get("loaded"),
        "file_location": config.get("fileLocation"),
        "base_uris": config.get("baseUris", []),
    }

    return simplified


def get_terms_from_ontology(
    ontology_id: str,
    max_results: int = 20,
    iri: str | None = None,
    short_form: str | None = None,
    obo_id: str | None = None,
) -> list[dict[str, Any]]:
    """
    Get classes/terms from a specific ontology.

    Args:
        ontology_id (str): The ID of the ontology (e.g., 'go', 'uberon', 'chebi')
        max_results (int): Maximum number of results to return (default: 20)
        iri (str, optional): Filter by specific IRI
        short_form (str, optional): Filter by short form
        obo_id (str, optional): Filter by OBO ID

    Returns:
        List[Dict[str, Any]]: List of terms from the ontology
    """
    terms = get_ontology_terms(
        ontology_id=ontology_id,
        max_results=max_results,
        iri=iri,
        short_form=short_form,
        obo_id=obo_id,
        verbose=True,
    )

    # Simplify the results for easier consumption
    simplified_terms = []
    for term in terms:
        simplified = {
            "id": term.get("id"),
            "iri": term.get("iri"),
            "short_form": term.get("short_form"),
            "obo_id": term.get("obo_id"),
            "label": term.get("label"),
            "description": term.get("description", []),
            "synonyms": term.get("synonyms", []),
            "ontology_name": term.get("ontology_name"),
            "ontology_prefix": term.get("ontology_prefix"),
            "type": term.get("type"),
            "is_obsolete": term.get("is_obsolete", False),
            "has_children": term.get("has_children", False),
            "is_root": term.get("is_root", False),
        }
        simplified_terms.append(simplified)

    return simplified_terms
