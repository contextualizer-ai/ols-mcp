import unittest
from unittest.mock import Mock, patch

from ols_mcp.api import (
    get_ontology_details,
    get_ontology_terms,
    get_similar_terms,
    search_ontologies,
)


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

    @patch("ols_mcp.api.requests.get")
    def test_get_similar_terms(self, mock_get):
        # Mock response
        mock_response = Mock()
        mock_response.json.return_value = {
            "elements": [{
            "appearsIn" : [ "clo", "upa", "stato", "xpo", "gallont", "peco", "envo", "fbbt", "po", "rbo", "hp", "gaz", "omrse", "cteno", "eupath", "hcao", "vsao", "poro", "geno", "plana", "msio", "oae", "phipo", "hba", "dpo", "oostt", "caro", "cl", "mro", "efo", "obib", "omit", "idomal", "fovt", "ado", "ro", "pcl", "psdo", "cco", "opl", "uberon", "rexo", "planp", "ohd", "one", "ppo", "eco", "vbo", "genepio", "sepio", "foodon", "ceph", "chiro", "omp", "mp", "go", "cido", "iceo", "wbbt", "htn", "dhba", "mpio", "zp", "bao", "aism", "ino", "pso", "mfmo", "to", "pco", "dideo", "wbls", "upheno", "bmont", "ecto", "dron", "ohmi", "ecao", "gecko", "bcio", "cmpo", "fbbi", "maxo", "bspo", "ecocore", "swo", "pato", "covoc", "pride", "ido", "agro", "omiabis", "mondo", "ohpi", "mco", "obcs", "fypo", "apollo_sv", "ons", "fbdv", "wbphenotype", "obi", "vo", "pr", "reto", "ogsf", "nbo", "oba", "ontoneo", "tao", "idocovid19", "flopo", "ncro", "epio", "bcgo", "micro", "gexo", "cob", "slso", "gsso" ],
            "curie" : "GO:0008150",
            "definedBy" : [ "ido", "go" ],
            "definition" : [ {
            "type" : [ "reification" ],
            "value" : (
                "A biological process is the execution of a genetically-encoded "
                "biological module or program. It consists of all the steps "
                "required to achieve the specific biological objective of the "
                "module. A biological process is accomplished by a particular set "
                "of molecular functions carried out by specific gene products (or "
                "macromolecular complexes), often in a highly regulated manner "
                "and in a particular temporal sequence."
            ),
            "axioms" : [ {
                "http://www.geneontology.org/formats/oboInOwl#hasDbXref": (
                    "GOC:pdt"
                )
            } ]
            }, (
                "Note that, in addition to forming the root of the biological "
                "process ontology, this term is recommended for the annotation "
                "of gene products whose biological process is unknown. When this "
                "term is used for annotation, it indicates that no information "
                "was available about the biological process of the gene product "
                "annotated as of the date the annotation was made; the evidence "
                "code 'no data' (ND), is used to indicate this."
            ) ],
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
                "definition" : [ (
                    "Any process specifically pertinent to the functioning of "
                    "integrated living units: cells, tissues, organs, and "
                    "organisms. A process is a collection of molecular events "
                    "with a defined beginning and end (from GO)."
                ) ],
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
                "http://purl.obolibrary.org/obo/IAO_0000115" : (
                    "Any process specifically pertinent to the functioning of "
                    "integrated living units: cells, tissues, organs, and "
                    "organisms. A process is a collection of molecular events "
                    "with a defined beginning and end (from GO)."
                ),
                "http://purl.obolibrary.org/obo/deprecated" : "true",
                "http://www.w3.org/1999/02/22-rdf-syntax-ns#type" : "http://www.w3.org/2002/07/owl#Class",
                "http://www.w3.org/2000/01/rdf-schema#label" : "biological process",
                "http://www.w3.org/2000/01/rdf-schema#subClassOf" : "http://www.bioassayontology.org/bao#BAO_0003114"
            }],
            "page": 0,
            "number": 0,
            "totalPages": 1,
        }
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        # Test the function
        results = get_similar_terms("http://purl.obolibrary.org/obo/GO_0008150", "GO", max_results=20)

        # Assertions
        print(results)
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["curie"], "BAO:0000264")
        self.assertEqual(results[0]["label"][0], "biological process")

        # Check that the API was called correctly
        mock_get.assert_called_once()
        args, kwargs = mock_get.call_args
        self.assertIn(args[0], "https://www.ebi.ac.uk/ols/api/v2/ontologies/go/classes/http%253A%252F%252Fpurl.obolibrary.org%252Fobo%252FGO_0008150/llm_similar")

def test_reality():
    assert 1 == 1


if __name__ == "__main__":
    unittest.main()
