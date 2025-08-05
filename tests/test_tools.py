import unittest
from unittest.mock import Mock, patch

from ols_mcp.tools import (
    get_ontology_info,
    get_similar_ontology_terms,
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


    @patch("ols_mcp.api.requests.get")
    def test_get_similar_terms_for_ontology_id(self, mock_get_terms):
        """Test get_similar_terms_for_ontology_id"""
        # Mock response with missing fields
        mock_response = Mock()
        mock_response.json.return_value = {
            "elements": [{
            "appearsIn" : [ "clo", "upa", "stato", "xpo", "gallont", "peco", "envo", "fbbt", "po", "rbo", "hp", "gaz", "omrse", "cteno", "eupath", "hcao", "vsao", "poro", "geno", "plana", "msio", "oae", "phipo", "hba", "dpo", "oostt", "caro", "cl", "mro", "efo", "obib", "omit", "idomal", "fovt", "ado", "ro", "pcl", "psdo", "cco", "opl", "uberon", "rexo", "planp", "ohd", "one", "ppo", "eco", "vbo", "genepio", "sepio", "foodon", "ceph", "chiro", "omp", "mp", "go", "cido", "iceo", "wbbt", "htn", "dhba", "mpio", "zp", "bao", "aism", "ino", "pso", "mfmo", "to", "pco", "dideo", "wbls", "upheno", "bmont", "ecto", "dron", "ohmi", "ecao", "gecko", "bcio", "cmpo", "fbbi", "maxo", "bspo", "ecocore", "swo", "pato", "covoc", "pride", "ido", "agro", "omiabis", "mondo", "ohpi", "mco", "obcs", "fypo", "apollo_sv", "ons", "fbdv", "wbphenotype", "obi", "vo", "pr", "reto", "ogsf", "nbo", "oba", "ontoneo", "tao", "idocovid19", "flopo", "ncro", "epio", "bcgo", "micro", "gexo", "cob", "slso", "gsso" ],
            "curie" : "GO:0008150",
            "definedBy" : [ "ido", "go" ],
            "definition" : [ {
            "type" : [ "reification" ],
            "value" : "A biological process is the execution of a genetically-encoded biological module or program. It consists of all the steps required to achieve the specific biological objective of the module. A biological process is accomplished by a particular set of molecular functions carried out by specific gene products (or macromolecular complexes), often in a highly regulated manner and in a particular temporal sequence.",
            "axioms" : [ {
                "http://www.geneontology.org/formats/oboInOwl#hasDbXref" : "GOC:pdt"
            } ]
            }, "Note that, in addition to forming the root of the biological process ontology, this term is recommended for the annotation of gene products whose biological process is unknown. When this term is used for annotation, it indicates that no information was available about the biological process of the gene product annotated as of the date the annotation was made; the evidence code 'no data' (ND), is used to indicate this." ],
            "definitionProperty" : [ "http://purl.obolibrary.org/obo/IAO_0000115", "http://www.w3.org/2000/01/rdf-schema#comment" ],
            "directAncestor" : [ "http://purl.obolibrary.org/obo/BFO_0000015", "http://purl.obolibrary.org/obo/BFO_0000003" ],
            "directParent" : [ "http://purl.obolibrary.org/obo/BFO_0000015" ],
            "hasDirectChildren" : True,
            "hasDirectParents" : True,
            "hasHierarchicalChildren" : True,
            "hasHierarchicalParents" : True,
            "hierarchicalAncestor" : [ "http://purl.obolibrary.org/obo/BFO_0000015", "http://purl.obolibrary.org/obo/BFO_0000003" ],
            "hierarchicalParent" : [ "http://purl.obolibrary.org/obo/BFO_0000015" ],
            "hierarchicalProperty" : "http://www.w3.org/2000/01/rdf-schema#subClassOf",
            "imported" : False,
            "iri" : "http://purl.obolibrary.org/obo/GO_0008150",
            "isDefiningOntology" : True,
            "isObsolete" : False,
            "isPreferredRoot" : True,
            "label" : [ "biological_process" ],
            "linkedEntities" : {
            "http://www.w3.org/2001/XMLSchema#anyURI" : {
                "numAppearsIn" : 1.0,
                "hasLocalDefinition" : False,
                "type" : [ "class", "entity" ],
                "label" : [ "anyURI" ],
                "curie" : "anyURI"
            }
            },
            "linksTo" : [ "http://www.geneontology.org/formats/oboInOwl#creation_date", "http://www.w3.org/2001/XMLSchema#anyURI", "http://purl.obolibrary.org/obo/BFO_0000015", "http://purl.obolibrary.org/obo/GO_0050789", "http://www.geneontology.org/formats/oboInOwl#hasExactSynonym", "http://purl.obolibrary.org/obo/GO_0000004", "http://www.geneontology.org/formats/oboInOwl#hasDbXref", "http://purl.obolibrary.org/obo/go#goslim_pombe", "http://purl.obolibrary.org/obo/RO_0002211", "http://purl.obolibrary.org/obo/GO_0044003", "http://purl.obolibrary.org/obo/RO_0002212", "http://purl.obolibrary.org/obo/RO_0002010", "http://purl.obolibrary.org/obo/go#goslim_chembl", "http://www.geneontology.org/formats/oboInOwl#id", "http://purl.obolibrary.org/obo/UBERON_0000062", "http://purl.obolibrary.org/obo/GO_0008150", "http://www.w3.org/2000/01/rdf-schema#subClassOf", "http://www.geneontology.org/formats/oboInOwl#inSubset", "http://purl.obolibrary.org/obo/go#goslim_metagenomics", "http://www.geneontology.org/formats/oboInOwl#hasOBONamespace", "http://purl.obolibrary.org/obo/go#goslim_candida", "http://purl.obolibrary.org/obo/go#goslim_plant", "http://www.w3.org/2000/01/rdf-schema#comment", "http://purl.obolibrary.org/obo/go#goslim_pir", "http://purl.obolibrary.org/obo/IAO_0000115", "http://purl.obolibrary.org/obo/IAO_0000233", "http://purl.obolibrary.org/obo/go#goslim_yeast", "http://www.geneontology.org/formats/oboInOwl#created_by", "http://purl.obolibrary.org/obo/GO_0044699", "http://purl.obolibrary.org/obo/GO_0007582", "http://purl.obolibrary.org/obo/RO_0002213", "http://purl.obolibrary.org/obo/GO_0048519", "http://purl.obolibrary.org/obo/GO_0048518", "http://purl.obolibrary.org/obo/RO_0002215", "http://www.geneontology.org/formats/oboInOwl#hasRelatedSynonym", "http://www.w3.org/2000/01/rdf-schema#label", "http://purl.obolibrary.org/obo/BFO_0000003", "http://www.geneontology.org/formats/oboInOwl#hasAlternativeId" ],
            "numDescendants" : 25698.0,
            "numHierarchicalDescendants" : 27870.0,
            "ontologyId" : "go",
            "ontologyIri" : "http://purl.obolibrary.org/obo/go/extensions/go-plus.owl",
            "ontologyPreferredPrefix" : "GO",
            "relatedFrom" : [ {
                "property" : "http://purl.obolibrary.org/obo/RO_0002215",
                "value" : "http://purl.obolibrary.org/obo/UBERON_0000062",
                "type" : [ "related" ],
                "http://www.w3.org/1999/02/22-rdf-syntax-ns#type" : "http://www.w3.org/2002/07/owl#Restriction",
                "http://www.w3.org/2002/07/owl#onProperty" : "http://purl.obolibrary.org/obo/RO_0002215",
                "http://www.w3.org/2002/07/owl#someValuesFrom" : "http://purl.obolibrary.org/obo/GO_0008150",
                "isObsolete" : False
            }],
            "score" : 0.9998359680175781,
            "searchableAnnotationValues" : [ False ],
            "shortForm" : "GO_0008150",
            "synonym" : [ "biological process", "physiological process", "single organism process", "single-organism process" ],
            "synonymProperty" : [ "http://www.geneontology.org/formats/oboInOwl#hasExactSynonym", "http://www.geneontology.org/formats/oboInOwl#hasRelatedSynonym" ],
            "type" : [ "class", "entity" ],
            }, {
                "appearsIn" : [ "bao" ],
                "curie" : "BAO:0000264",
                "definedBy" : [ "bao" ],
                "definition" : [ "Any process specifically pertinent to the functioning of integrated living units: cells, tissues, organs, and organisms. A process is a collection of molecular events with a defined beginning and end (from GO)." ],
                "definitionProperty" : "http://purl.obolibrary.org/obo/IAO_0000115",
                "directAncestor" : [ "http://www.bioassayontology.org/bao#BAO_0003114" ],
                "directParent" : [ "http://www.bioassayontology.org/bao#BAO_0003114" ],
                "hasDirectChildren" : False,
                "hasDirectParents" : True,
                "hasHierarchicalChildren" : False,
                "hasHierarchicalParents" : True,
                "hierarchicalAncestor" : [ "http://www.bioassayontology.org/bao#BAO_0003114" ],
                "hierarchicalParent" : [ "http://www.bioassayontology.org/bao#BAO_0003114" ],
                "hierarchicalProperty" : "http://www.w3.org/2000/01/rdf-schema#subClassOf",
                "imported" : True,
                "iri" : "http://www.bioassayontology.org/bao#BAO_0000264",
                "isDefiningOntology" : True,
                "isObsolete" : False,
                "isPreferredRoot" : False,
                "label" : [ "biological process" ],
                "linkedEntities" : {},
                "linksTo" : [ "http://www.w3.org/2000/01/rdf-schema#subClassOf", "http://purl.obolibrary.org/obo/deprecated", "http://www.bioassayontology.org/bao#BAO_0003114", "http://www.w3.org/2000/01/rdf-schema#label", "http://purl.obolibrary.org/obo/IAO_0000115" ],
                "numDescendants" : 0.0,
                "numHierarchicalDescendants" : 0.0,
                "ontologyId" : "bao",
                "ontologyIri" : "http://www.bioassayontology.org/bao/bao_complete.owl",
                "ontologyPreferredPrefix" : "BAO",
                "score" : 0.9899990558624268,
                "searchableAnnotationValues" : [ True ],
                "shortForm" : "BAO_0000264",
                "type" : [ "class", "entity" ],
                "http://purl.obolibrary.org/obo/IAO_0000115" : "Any process specifically pertinent to the functioning of integrated living units: cells, tissues, organs, and organisms. A process is a collection of molecular events with a defined beginning and end (from GO).",
                "http://purl.obolibrary.org/obo/deprecated" : "true",
                "http://www.w3.org/1999/02/22-rdf-syntax-ns#type" : "http://www.w3.org/2002/07/owl#Class",
                "http://www.w3.org/2000/01/rdf-schema#label" : "biological process",
                "http://www.w3.org/2000/01/rdf-schema#subClassOf" : "http://www.bioassayontology.org/bao#BAO_0003114"
            }],
            "page": {"number": 0, "totalPages": 1}
        }
        mock_get_terms.raise_for_status.return_value = None
        mock_get_terms.return_value = mock_response
        result = get_similar_ontology_terms("http://purl.obolibrary.org/obo/GO_0008150", "GO")

        # Verify missing fields are handled with defaults
        expected_result = [{
            "id": "BAO:0000264",
            "iri": "http://www.bioassayontology.org/bao#BAO_0000264",
            "label": "biological process",
            "definition": "Any process specifically pertinent to the functioning of integrated living units: cells, tissues, organs, and organisms. A process is a collection of molecular events with a defined beginning and end (from GO).",
            "score":  0.9899990558624268
        }]
        self.assertEqual(len(result), 1)
        self.assertEqual(result, expected_result)

if __name__ == "__main__":
    unittest.main()
