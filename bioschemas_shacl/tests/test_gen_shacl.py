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

        res = validate_any_from_microdata(
            # input_url="https://bgee.org/?page=gene&gene_id=ENSMUSG00000038170"
            input_url="https://bgee.org/?page=gene&gene_id=ENSG00000274928"
        )

    def test_read_profiles_from_files(self):
        profile_files = []

        # get list of path of .json bioschemas profiles
        dir_path = os.path.join(os.path.dirname(__file__), '../data/specifications')
        for (sub_dir_path, dirnames, filenames) in walk(dir_path):
            # print(dirnames)

            for (dirpath, dirnames, filenames) in walk(sub_dir_path):
                for filename in filenames:
                    if filename.endswith("RELEASE.json"):
                        profile_files.append(dirpath + "/" + filename)
                        # print(dirpath + "/" + filename)
            break

        bs_profiles = {}
        #retrieve and parse content of .json profiles files
        for profile_file in profile_files:
            print("****** READING Profile *******")
            # print(profile_file)
            with open(profile_file) as f:
                profile = json.load(f)
                # print(json.dumps(profile, indent=True))

                bs_id = profile["@graph"][0]["@id"]
                bs_id = "sc:" + profile["@graph"][0]["rdfs:label"]
                print("*** Storing profile: " + bs_id)
                # print("rdfs:label = " + profile["@graph"][0]["rdfs:label"])
                print("rdfs:subClassOf = " + profile["@graph"][0]["rdfs:subClassOf"]["@id"])
                bs_profiles[bs_id] = {
                    "min_props": [],
                    "rec_props": []
                }
                for g in profile["@graph"]:
                    # print("*** Class: " + g["@id"])
                    # schema_class = g["@id"]


                    if ("$validation") in g.keys():
                        for k in g["$validation"]["required"]:
                            # print(f"required {k}")
                            bs_profiles[bs_id]["min_props"].append("sc:" + k)
                        if "recommended" in g["$validation"].keys():
                            for k in g["$validation"]["recommended"]:
                                # print(f"recommended {k}")
                                bs_profiles[bs_id]["rec_props"].append("sc:" + k)
        print(json.dumps(bs_profiles, indent=4, sort_keys=True))
        # print(bs_profiles)


if __name__ == "__main__":
    unittest.main()
