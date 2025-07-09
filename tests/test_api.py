import unittest
from unittest.mock import Mock, patch

from ols_mcp.api import get_ontology_details, get_ontology_terms, search_ontologies


class TestOLSAPI(unittest.TestCase):

    @patch("ols_mcp.api.requests.get")
    def test_search_ontologies(self, mock_get):
        # Mock response
        mock_response = Mock()
        mock_response.json.return_value = {
            "response": {
                "docs": [
                    {
                        "id": "GO:0008150",
                        "iri": "http://purl.obolibrary.org/obo/GO_0008150",
                        "short_form": "GO_0008150",
                        "obo_id": "GO:0008150",
                        "label": "biological_process",
                        "description": [
                            "Any process specifically pertinent to the functioning of "
                            "integrated living units"
                        ],
                        "ontology_name": "go",
                        "ontology_prefix": "GO",
                        "type": "class",
                    }
                ]
            }
        }
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        # Test the function
        results = search_ontologies("biological process", max_results=1)

        # Assertions
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["id"], "GO:0008150")
        self.assertEqual(results[0]["label"], "biological_process")

        # Check that the API was called correctly
        mock_get.assert_called_once()
        args, kwargs = mock_get.call_args
        self.assertEqual(args[0], "https://www.ebi.ac.uk/ols/api/search")
        self.assertIn("q", kwargs["params"])
        self.assertEqual(kwargs["params"]["q"], "biological process")

    @patch("ols_mcp.api.requests.get")
    def test_get_ontology_details(self, mock_get):
        # Mock response
        mock_response = Mock()
        mock_response.json.return_value = {
            "ontologyId": "go",
            "status": "LOADED",
            "numberOfTerms": 47000,
            "numberOfProperties": 10,
            "numberOfIndividuals": 0,
            "config": {
                "title": "Gene Ontology",
                "description": (
                    "The Gene Ontology project provides a controlled vocabulary to "
                    "describe gene and gene product attributes"
                ),
                "version": "2024-01-01",
                "homepage": "http://geneontology.org/",
                "preferredLanguage": "en",
            },
        }
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        # Test the function
        result = get_ontology_details("go")

        # Assertions
        self.assertEqual(result["ontologyId"], "go")
        self.assertEqual(result["status"], "LOADED")
        self.assertEqual(result["config"]["title"], "Gene Ontology")

        # Check that the API was called correctly
        mock_get.assert_called_once_with("https://www.ebi.ac.uk/ols/api/ontologies/go")

    @patch("ols_mcp.api.requests.get")
    def test_get_ontology_terms(self, mock_get):
        # Mock response
        mock_response = Mock()
        mock_response.json.return_value = {
            "_embedded": {
                "terms": [
                    {
                        "id": "GO:0008150",
                        "iri": "http://purl.obolibrary.org/obo/GO_0008150",
                        "short_form": "GO_0008150",
                        "obo_id": "GO:0008150",
                        "label": "biological_process",
                        "description": [
                            "Any process specifically pertinent to the functioning of "
                            "integrated living units"
                        ],
                        "ontology_name": "go",
                        "ontology_prefix": "GO",
                        "type": "class",
                        "is_obsolete": False,
                        "has_children": True,
                        "is_root": True,
                    }
                ]
            },
            "page": {"number": 0, "totalPages": 1},
        }
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        # Test the function
        results = get_ontology_terms("go", max_results=1)

        # Assertions
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["id"], "GO:0008150")
        self.assertEqual(results[0]["label"], "biological_process")
        self.assertTrue(results[0]["is_root"])

        # Check that the API was called correctly
        mock_get.assert_called_once()
        args, kwargs = mock_get.call_args
        self.assertEqual(args[0], "https://www.ebi.ac.uk/ols/api/ontologies/go/terms")


def test_reality():
    assert 1 == 1


if __name__ == "__main__":
    unittest.main()
