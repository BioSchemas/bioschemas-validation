import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__),'../'))

import unittest

from os import walk
import json

from bioschemas_profile_shape.bioschemas_shape_gen import gen_SHACL_from_profile
from bioschemas_profile_shape.bioschemas_shape_gen import gen_SHACL_from_target_class
from bioschemas_profile_shape.bioschemas_shape_gen import validate_shape_from_RDF
from bioschemas_profile_shape.bioschemas_shape_gen import validate_any_from_RDF
from bioschemas_profile_shape.bioschemas_shape_gen import validate_any_from_microdata
from bioschemas_profile_shape.bioschemas_shape_gen import validate_shape_from_microdata
from bioschemas_profile_shape.bioschemas_shape_gen import generate_profiles_from_files



class GenSHACLTestCase(unittest.TestCase):
    def test_validate_shape_tool(self):
        classes = ["sc:SoftwareApplication"]
        minimal_software_properties = ["sc:name", "sc:description", "sc:url"]
        recommended_software_properties = [
            "sc:additionalType",
            "sc:applicationCategory",
            "sc:applicationSubCategory",
            "sc:author" "sc:license",
            "sc:citation",
            "sc:featureList",
            "sc:softwareVersion",
        ]

        shape = gen_SHACL_from_profile(
            "toolShape",
            target_classes=classes,
            min_props=minimal_software_properties,
            rec_props=recommended_software_properties,
        )

        validate_shape_from_RDF(
            input_uri="https://bio.tools/api/jaspar?format=jsonld",
            rdf_syntax="json-ld",
            shacl_shape=shape,
        )

    def test_validate_shape_dataset(self):
        classes = ["sc:Dataset"]
        minimal_dataset_properties = [
            "sc:name",
            "sc:description",
            "sc:identifier",
            "sc:keywords",
            "sc:url",
        ]
        recommended_dataset_properties = ["sc:license", "sc:creator", "sc:citation"]

        shape = gen_SHACL_from_profile(
            "datasetShape",
            target_classes=classes,
            min_props=minimal_dataset_properties,
            rec_props=recommended_dataset_properties,
        )
        validate_shape_from_microdata(
            input_uri="https://data.inrae.fr/dataset.xhtml?persistentId=doi:10.15454/PL3HWQ",
            shacl_shape=shape,
        )

    def test_generate_shape_gene(self):
        classes = ["bsc:Gene"]
        minimal_dataset_properties = ["sc:identifier", "sc:name", "dct:conformsTo"]
        recommended_dataset_properties = [
            "sc:description",
            "sc:encodesBioChemEntity",
            "sc:isPartOfBioChemEntity",
            "sc:url",
        ]
        shape = gen_SHACL_from_profile(
            "geneShape",
            target_classes=classes,
            min_props=minimal_dataset_properties,
            rec_props=recommended_dataset_properties,
        )
        validate_shape_from_microdata(
            input_uri="https://bgee.org/?page=gene&gene_id=ENSMUSG00000038170",
            shacl_shape=shape,
        )

    def test_generate_right_shape(self):
        target_class = "sc:SoftwareApplication"
        shape = gen_SHACL_from_target_class(target_class=target_class)
        validate_shape_from_RDF(
            input_uri="https://bio.tools/api/jaspar?format=jsonld",
            rdf_syntax="json-ld",
            shacl_shape=shape,
        )

    def test_any_resource(self):
        # todo assertions on error count for each test
        # validate_any_from_RDF(
        #     input_url="https://bio.tools/api/jaspar?format=jsonld", rdf_syntax="json-ld"
        # )
        # validate_any_from_microdata(
        #     input_url="https://bio.tools/jaspar"
        # )

        # TODO issue with schema.org url in @context
        # validate_any_from_RDF(
        #     input_url="https://data.inrae.fr/api/datasets/export?exporter=schema.org&persistentId=doi%3A10.15454/PL3HWQ", rdf_syntax="json-ld"
        # )

        # TODO cannot find any embedded JSONLD
        # validate_any_from_microdata(
        #     input_url="https://data.inrae.fr/dataset.xhtml?persistentId=doi:10.15454/PL3HWQ"
        # )

        # res = validate_any_from_microdata(
        #     input_url="https://doi.pangaea.de/10.1594/PANGAEA.914331"
        # )
        # print(res)

        # res = validate_any_from_microdata(
        #     input_url="https://search.datacite.org/works/10.7892/boris.108387"
        # )
        # print(res)

        # res = validate_any_from_microdata(
        #     # input_url="https://bgee.org/?page=gene&gene_id=ENSMUSG00000038170"
        #     input_url="https://bgee.org/?page=gene&gene_id=ENSG00000274928"
        # )

        #

        # res = validate_any_from_microdata(
        #     # input_url="https://bgee.org/?page=gene&gene_id=ENSMUSG00000038170"
        #     input_url="https://pippa.psb.ugent.be/pippa_experiments/consult_experiment_basic_info/55"
        # )

        res = validate_any_from_microdata(
            input_url="https://bedroesb.github.io/rdmkit/human_data.html"
        )

    def test_read_profiles_from_files(self):
        bs_profiles = generate_profiles_from_files()
        print(json.dumps(bs_profiles, indent=4, sort_keys=True))

    def test_workflow(self):
        validate_any_from_microdata(
            #input_url="https://workflowhub.eu/workflows/18"
            input_url = "https://workflowhub.eu/workflows/3"
        )

    def test_disprot(self):
        validate_any_from_microdata(
            input_url = "https://disprot.org/DP00004"
        )

    def test_persons(self):
        validate_any_from_microdata(
            input_url="https://bedroesb.github.io/rdmkit/human_data.html"
        )

    def test_molecular_entity(self):
        url = "https://www.metanetx.org/chem_info/MNXM680"
        res = validate_any_from_microdata(
            input_url=url
        )

        self.assertEqual(len(res[url]["warnings"]),1)
        self.assertEqual(len(res[url]["errors"]), 0)

    def test_training_material(self):
        # Microdata
        url = "https://tess.elixir-europe.org/materials/a-gentle-introduction-to-dsw-for-convergers"

        # JSON-LD
        url = "https://bioschemas.org/tutorials/what_why_bioschemas"

        res = validate_any_from_microdata(
            input_url=url
        )



if __name__ == "__main__":
    unittest.main()
