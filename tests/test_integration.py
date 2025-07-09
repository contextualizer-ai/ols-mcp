import unittest

import pytest

from ols_mcp.tools import (
    get_ontology_info,
    get_terms_from_ontology,
    search_all_ontologies,
)


class TestOLSIntegration(unittest.TestCase):
    """Integration tests that hit the real OLS API.

    These tests validate actual behavior against the live service.
    They focus on structure and behavior rather than specific counts
    since ontologies evolve over time.
    """

    @pytest.mark.integration
    def test_search_all_ontologies_real_api(self):
        """Test search_all_ontologies with real API call."""
        # Search for a well-known biological term
        results = search_all_ontologies("apoptosis", max_results=5)

        # Validate structure
        self.assertIsInstance(results, list)
        self.assertGreater(len(results), 0, "Should find some results for 'apoptosis'")
        self.assertLessEqual(len(results), 5, "Should respect max_results limit")

        # Validate each result has expected structure
        for result in results:
            self.assertIsInstance(result, dict)
            # Required fields
            self.assertIn("id", result)
            self.assertIn("label", result)
            self.assertIn("ontology_name", result)

            # Validate field types
            if result["id"] is not None:
                self.assertIsInstance(result["id"], str)
            if result["label"] is not None:
                self.assertIsInstance(result["label"], str)
            if result["description"] is not None:
                self.assertIsInstance(result["description"], list)
            if result["ontology_name"] is not None:
                self.assertIsInstance(result["ontology_name"], str)

    @pytest.mark.integration
    def test_search_all_ontologies_with_ontology_filter(self):
        """Test search with specific ontology filter."""
        # Search only in Gene Ontology
        results = search_all_ontologies(
            "biological_process", ontologies="go", max_results=3
        )

        self.assertIsInstance(results, list)
        self.assertGreater(len(results), 0, "Should find results in GO")

        # All results should be from GO
        for result in results:
            self.assertEqual(result["ontology_name"], "go")

    @pytest.mark.integration
    def test_get_ontology_info_real_api(self):
        """Test get_ontology_info with real API call."""
        # Test with Gene Ontology (well-established ontology)
        result = get_ontology_info("go")

        # Validate structure
        self.assertIsInstance(result, dict)

        # Validate key fields exist and have correct types
        self.assertEqual(result["id"], "go")
        self.assertIsInstance(result["title"], str)
        self.assertIn("Gene Ontology", result["title"])

        # Validate numeric fields are present and reasonable
        self.assertIsInstance(result["number_of_terms"], int)
        self.assertGreater(
            result["number_of_terms"], 10000, "GO should have many thousands of terms"
        )

        # Validate optional fields
        if result["description"] is not None:
            self.assertIsInstance(result["description"], str)
        if result["version"] is not None:
            self.assertIsInstance(result["version"], str)
        if result["homepage"] is not None:
            self.assertIsInstance(result["homepage"], str)

        # Validate expected structure
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

    @pytest.mark.integration
    def test_get_terms_from_ontology_real_api(self):
        """Test get_terms_from_ontology with real API call."""
        # Get a few terms from Gene Ontology
        results = get_terms_from_ontology("go", max_results=3)

        # Validate structure
        self.assertIsInstance(results, list)
        self.assertGreater(len(results), 0, "Should return some terms")
        self.assertLessEqual(len(results), 3, "Should respect max_results limit")

        # Validate each term structure
        for term in results:
            self.assertIsInstance(term, dict)

            # Required fields
            self.assertIn("id", term)
            self.assertIn("label", term)
            self.assertIn("ontology_name", term)
            self.assertEqual(term["ontology_name"], "go")

            # Validate field types
            if term["id"] is not None:
                self.assertIsInstance(term["id"], str)
            if term["label"] is not None:
                self.assertIsInstance(term["label"], str)
            if term["description"] is not None:
                self.assertIsInstance(term["description"], list)

            # Boolean fields should have proper defaults
            self.assertIsInstance(term["is_obsolete"], bool)
            self.assertIsInstance(term["has_children"], bool)
            self.assertIsInstance(term["is_root"], bool)

    @pytest.mark.integration
    def test_get_terms_from_ontology_with_specific_term(self):
        """Test retrieving a specific term by OBO ID."""
        # Search for the root biological process term
        results = get_terms_from_ontology("go", obo_id="GO:0008150", max_results=1)

        self.assertIsInstance(results, list)
        self.assertEqual(len(results), 1, "Should find exactly one term")

        term = results[0]
        self.assertEqual(term["obo_id"], "GO:0008150")
        self.assertEqual(term["label"], "biological_process")
        # Note: is_root status may vary based on OLS configuration
        self.assertIsInstance(term["is_root"], bool)

    @pytest.mark.integration
    def test_error_handling_invalid_ontology(self):
        """Test error handling for invalid ontology ID."""
        # Invalid ontology should raise a requests.HTTPError (404)
        import requests

        with self.assertRaises(requests.HTTPError):
            get_ontology_info("nonexistent_ontology_12345")

    @pytest.mark.integration
    def test_search_empty_query(self):
        """Test search behavior with empty query."""
        # This should either return empty results or raise an appropriate error
        try:
            results = search_all_ontologies("", max_results=1)
            # If it succeeds, should return empty list or very few results
            self.assertIsInstance(results, list)
            self.assertLessEqual(len(results), 1)
        except Exception:
            # Empty queries might raise exceptions, which is acceptable
            pass

    @pytest.mark.integration
    def test_robust_search_with_common_terms(self):
        """Test search with various common biological terms."""
        test_terms = ["protein", "cell", "membrane", "enzyme"]

        for term in test_terms:
            with self.subTest(term=term):
                results = search_all_ontologies(term, max_results=2)
                self.assertIsInstance(results, list)
                # Common biological terms should return results
                self.assertGreater(len(results), 0, f"Should find results for '{term}'")

                # Validate result structure
                for result in results:
                    # Some results might have None values, check accordingly
                    if result["id"] is not None:
                        self.assertIsInstance(result["id"], str)
                    if result["label"] is not None:
                        self.assertIsInstance(result["label"], str)
                    if result["ontology_name"] is not None:
                        self.assertIsInstance(result["ontology_name"], str)


if __name__ == "__main__":
    unittest.main()
