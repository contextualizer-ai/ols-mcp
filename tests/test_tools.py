import unittest
from unittest.mock import patch

from ols_mcp.tools import (
    get_ontology_info,
    get_terms_from_ontology,
    search_all_ontologies,
)


class TestOLSTools(unittest.TestCase):
    """Test cases for the OLS tools module."""

    @patch("ols_mcp.tools.search_ontologies")
    def test_search_all_ontologies_basic(self, mock_search):
        """Test basic search_all_ontologies functionality."""
        # Mock the API response
        mock_search.return_value = [
            {
                "id": "GO:0008150",
                "iri": "http://purl.obolibrary.org/obo/GO_0008150",
                "short_form": "GO_0008150",
                "obo_id": "GO:0008150",
                "label": "biological_process",
                "description": ["A biological process"],
                "ontology_name": "go",
                "ontology_prefix": "GO",
                "type": "class",
                "extra_field": "should_be_filtered",
            }
        ]

        # Test the function
        result = search_all_ontologies("biological process")

        # Verify the API was called correctly
        mock_search.assert_called_once_with(
            query="biological process",
            ontologies=None,
            max_results=20,
            exact=False,
            verbose=True,
        )

        # Verify the result structure
        self.assertEqual(len(result), 1)
        expected_result = {
            "id": "GO:0008150",
            "iri": "http://purl.obolibrary.org/obo/GO_0008150",
            "short_form": "GO_0008150",
            "obo_id": "GO:0008150",
            "label": "biological_process",
            "description": ["A biological process"],
            "ontology_name": "go",
            "ontology_prefix": "GO",
            "type": "class",
        }
        self.assertEqual(result[0], expected_result)
        # Verify extra fields are filtered out
        self.assertNotIn("extra_field", result[0])

    @patch("ols_mcp.tools.search_ontologies")
    def test_search_all_ontologies_with_ontologies_parameter(self, mock_search):
        """Test search_all_ontologies with ontologies parameter."""
        mock_search.return_value = []

        # Test with comma-separated ontologies
        search_all_ontologies(
            "cancer", ontologies="go,mondo", max_results=10, exact=True
        )

        # Verify the ontologies parameter is parsed correctly
        mock_search.assert_called_once_with(
            query="cancer",
            ontologies=["go", "mondo"],
            max_results=10,
            exact=True,
            verbose=True,
        )

    @patch("ols_mcp.tools.search_ontologies")
    def test_search_all_ontologies_with_spaces_in_ontologies(self, mock_search):
        """Test search_all_ontologies with spaces around ontology names."""
        mock_search.return_value = []

        # Test with spaces around ontology names
        search_all_ontologies("test", ontologies=" go , mondo , chebi ")

        # Verify spaces are stripped
        mock_search.assert_called_once_with(
            query="test",
            ontologies=["go", "mondo", "chebi"],
            max_results=20,
            exact=False,
            verbose=True,
        )

    @patch("ols_mcp.tools.search_ontologies")
    def test_search_all_ontologies_empty_ontologies(self, mock_search):
        """Test search_all_ontologies with empty ontologies parameter."""
        mock_search.return_value = []

        # Test with empty ontologies string
        search_all_ontologies("test", ontologies="")

        # Verify None is passed when ontologies is empty
        mock_search.assert_called_once_with(
            query="test",
            ontologies=None,
            max_results=20,
            exact=False,
            verbose=True,
        )

    @patch("ols_mcp.tools.search_ontologies")
    def test_search_all_ontologies_handles_missing_fields(self, mock_search):
        """Test search_all_ontologies handles missing fields gracefully."""
        # Mock response with missing fields
        mock_search.return_value = [
            {
                "id": "GO:0008150",
                "label": "biological_process",
                # Missing other fields
            }
        ]

        result = search_all_ontologies("test")

        # Verify missing fields are handled with None/empty defaults
        expected_result = {
            "id": "GO:0008150",
            "iri": None,
            "short_form": None,
            "obo_id": None,
            "label": "biological_process",
            "description": [],
            "ontology_name": None,
            "ontology_prefix": None,
            "type": None,
        }
        self.assertEqual(result[0], expected_result)

    @patch("ols_mcp.tools.get_ontology_details")
    def test_get_ontology_info_basic(self, mock_get_details):
        """Test basic get_ontology_info functionality."""
        # Mock the API response
        mock_get_details.return_value = {
            "ontologyId": "go",
            "numberOfTerms": 50000,  # Use arbitrary number for testing
            "numberOfProperties": 15,
            "numberOfIndividuals": 5,
            "created": "2024-01-01T00:00:00Z",
            "updated": "2024-01-02T00:00:00Z",
            "loaded": "2024-01-03T00:00:00Z",
            "config": {
                "title": "Gene Ontology",
                "description": "The Gene Ontology project",
                "version": "2024-01-01",
                "homepage": "http://geneontology.org/",
                "preferredLanguage": "en",
                "fileLocation": "http://example.com/go.owl",
                "baseUris": ["http://purl.obolibrary.org/obo/go.owl"],
            },
            "extra_field": "should_be_filtered",
        }

        # Test the function
        result = get_ontology_info("go")

        # Verify the API was called correctly
        mock_get_details.assert_called_once_with(ontology_id="go", verbose=True)

        # Verify the result structure and key fields
        self.assertEqual(result["id"], "go")
        self.assertEqual(result["title"], "Gene Ontology")
        self.assertEqual(result["description"], "The Gene Ontology project")
        self.assertEqual(result["version"], "2024-01-01")
        self.assertEqual(result["homepage"], "http://geneontology.org/")
        self.assertIsNone(result["status"])
        self.assertEqual(result["number_of_terms"], 50000)  # Should match mock input
        self.assertEqual(result["number_of_properties"], 15)
        self.assertEqual(result["number_of_individuals"], 5)
        self.assertEqual(result["languages"], "en")
        self.assertEqual(result["created"], "2024-01-01T00:00:00Z")
        self.assertEqual(result["updated"], "2024-01-02T00:00:00Z")
        self.assertEqual(result["loaded"], "2024-01-03T00:00:00Z")
        self.assertEqual(result["file_location"], "http://example.com/go.owl")
        self.assertEqual(result["base_uris"], ["http://purl.obolibrary.org/obo/go.owl"])

        # Verify all expected fields are present
        expected_fields = {
            "id",
            "title",
            "description",
            "version",
            "homepage",
            "status",
            "number_of_terms",
            "number_of_properties",
            "number_of_individuals",
            "languages",
            "created",
            "updated",
            "loaded",
            "file_location",
            "base_uris",
        }
        self.assertEqual(set(result.keys()), expected_fields)
        # Verify extra fields are filtered out
        self.assertNotIn("extra_field", result)

    @patch("ols_mcp.tools.get_ontology_details")
    def test_get_ontology_info_missing_config(self, mock_get_details):
        """Test get_ontology_info with missing config section."""
        # Mock response with missing config
        mock_get_details.return_value = {
            "ontologyId": "go",
            "numberOfTerms": 25000,  # Use arbitrary number for testing
            # Missing config section
        }

        result = get_ontology_info("go")

        # Verify missing config fields are handled with None defaults
        expected_result = {
            "id": "go",
            "title": None,
            "description": None,
            "version": None,
            "homepage": None,
            "status": None,
            "number_of_terms": 25000,  # Should match mock input
            "number_of_properties": None,
            "number_of_individuals": None,
            "languages": None,
            "created": None,
            "updated": None,
            "loaded": None,
            "file_location": None,
            "base_uris": [],
        }
        self.assertEqual(result, expected_result)

    @patch("ols_mcp.tools.get_ontology_terms")
    def test_get_terms_from_ontology_basic(self, mock_get_terms):
        """Test basic get_terms_from_ontology functionality."""
        # Mock the API response
        mock_get_terms.return_value = [
            {
                "id": "GO:0008150",
                "iri": "http://purl.obolibrary.org/obo/GO_0008150",
                "short_form": "GO_0008150",
                "obo_id": "GO:0008150",
                "label": "biological_process",
                "description": ["A biological process"],
                "ontology_name": "go",
                "ontology_prefix": "GO",
                "type": "class",
                "is_obsolete": False,
                "has_children": True,
                "is_root": True,
                "extra_field": "should_be_filtered",
            }
        ]

        # Test the function
        result = get_terms_from_ontology("go")

        # Verify the API was called correctly
        mock_get_terms.assert_called_once_with(
            ontology_id="go",
            max_results=20,
            iri=None,
            short_form=None,
            obo_id=None,
            verbose=True,
        )

        # Verify the result structure
        expected_result = {
            "id": "GO:0008150",
            "iri": "http://purl.obolibrary.org/obo/GO_0008150",
            "short_form": "GO_0008150",
            "obo_id": "GO:0008150",
            "label": "biological_process",
            "description": ["A biological process"],
            "synonyms": [],
            "ontology_name": "go",
            "ontology_prefix": "GO",
            "type": "class",
            "is_obsolete": False,
            "has_children": True,
            "is_root": True,
        }
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0], expected_result)
        # Verify extra fields are filtered out
        self.assertNotIn("extra_field", result[0])

    @patch("ols_mcp.tools.get_ontology_terms")
    def test_get_terms_from_ontology_with_filters(self, mock_get_terms):
        """Test get_terms_from_ontology with filter parameters."""
        mock_get_terms.return_value = []

        # Test with all filter parameters
        get_terms_from_ontology(
            ontology_id="go",
            max_results=50,
            iri="http://purl.obolibrary.org/obo/GO_0008150",
            short_form="GO_0008150",
            obo_id="GO:0008150",
        )

        # Verify all parameters are passed correctly
        mock_get_terms.assert_called_once_with(
            ontology_id="go",
            max_results=50,
            iri="http://purl.obolibrary.org/obo/GO_0008150",
            short_form="GO_0008150",
            obo_id="GO:0008150",
            verbose=True,
        )

    @patch("ols_mcp.tools.get_ontology_terms")
    def test_get_terms_from_ontology_handles_missing_fields(self, mock_get_terms):
        """Test get_terms_from_ontology handles missing fields gracefully."""
        # Mock response with missing fields
        mock_get_terms.return_value = [
            {
                "id": "GO:0008150",
                "label": "biological_process",
                # Missing other fields
            }
        ]

        result = get_terms_from_ontology("go")

        # Verify missing fields are handled with defaults
        expected_result = {
            "id": "GO:0008150",
            "iri": None,
            "short_form": None,
            "obo_id": None,
            "label": "biological_process",
            "description": [],
            "synonyms": [],
            "ontology_name": None,
            "ontology_prefix": None,
            "type": None,
            "is_obsolete": False,
            "has_children": False,
            "is_root": False,
        }
        self.assertEqual(result[0], expected_result)


if __name__ == "__main__":
    unittest.main()
