################################################################################
# ols_mcp/api.py
# This module contains wrapper functions that interact with the OLS API endpoints
################################################################################
from typing import Any

import requests


def search_ontologies(
    query: str,
    ontologies: list[str] | None = None,
    max_results: int = 20,
    exact: bool = False,
    verbose: bool = False,
) -> list[dict[str, Any]]:
    """
    Search across all ontologies in the OLS.

    Args:
        query: The search term
        ontologies: List of specific ontology IDs to search within (optional)
        max_results: Maximum number of results to return
        exact: Whether to perform exact matching
        verbose: If True, print progress information during retrieval

    Returns:
        A list of dictionaries, where each dictionary represents a search result.
    """
    base_url = "https://www.ebi.ac.uk/ols/api/search"

    params: dict[str, Any] = {"q": query, "rows": max_results, "exact": exact}

    if ontologies:
        params["ontology"] = ",".join(ontologies)

    if verbose:
        print(f"Searching OLS for: {query}")

    response = requests.get(base_url, params=params)
    response.raise_for_status()
    data = response.json()

    # Extract the docs from the response
    results = data.get("response", {}).get("docs", [])

    if verbose:
        print(f"Found {len(results)} results")

    return results


def get_ontology_details(ontology_id: str, verbose: bool = False) -> dict[str, Any]:
    """
    Get details about a specific ontology.

    Args:
        ontology_id: The ID of the ontology (e.g., 'go', 'uberon')
        verbose: If True, print progress information

    Returns:
        A dictionary containing ontology details.
    """
    base_url = f"https://www.ebi.ac.uk/ols/api/ontologies/{ontology_id}"

    if verbose:
        print(f"Fetching details for ontology: {ontology_id}")

    response = requests.get(base_url)
    response.raise_for_status()
    data = response.json()

    if verbose:
        print(f"Retrieved details for {ontology_id}")

    return data


def get_ontology_terms(
    ontology_id: str,
    max_results: int = 20,
    page_size: int = 20,
    iri: str | None = None,
    short_form: str | None = None,
    obo_id: str | None = None,
    verbose: bool = False,
) -> list[dict[str, Any]]:
    """
    Get classes/terms from a specific ontology.

    Args:
        ontology_id: The ID of the ontology (e.g., 'go', 'uberon')
        max_results: Maximum number of results to return
        page_size: Number of results per page
        iri: Filter by specific IRI
        short_form: Filter by short form
        obo_id: Filter by OBO ID
        verbose: If True, print progress information

    Returns:
        A list of dictionaries, where each dictionary represents a term.
    """
    base_url = f"https://www.ebi.ac.uk/ols/api/ontologies/{ontology_id}/terms"

    params: dict[str, Any] = {"size": min(page_size, max_results)}

    if iri:
        params["iri"] = iri
    if short_form:
        params["short_form"] = short_form
    if obo_id:
        params["obo_id"] = obo_id

    all_terms: list[dict[str, Any]] = []
    page = 0

    if verbose:
        print(f"Fetching terms from ontology: {ontology_id}")

    while len(all_terms) < max_results:
        params["page"] = page

        response = requests.get(base_url, params=params)
        response.raise_for_status()
        data = response.json()

        terms = data.get("_embedded", {}).get("terms", [])
        if not terms:
            break

        all_terms.extend(terms)

        if verbose:
            print(f"Fetched page {page + 1}, total terms so far: {len(all_terms)}")

        # Check if we have more pages
        if (
            not data.get("page", {}).get("number", 0)
            < data.get("page", {}).get("totalPages", 0) - 1
        ):
            break

        page += 1

    # Truncate to max_results
    result = all_terms[:max_results]

    if verbose:
        print(f"Retrieved {len(result)} terms from {ontology_id}")

    return result
