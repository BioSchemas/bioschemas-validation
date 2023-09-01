import json
import unittest

from rdflib import ConjunctiveGraph

class MyTestCase(unittest.TestCase):
    def test_something(self):
        jsonld = """
        { "@context": "http://schema.org", "@type": "DataCatalog", "@id": "https://www.metanetx.org/", "http://purl.org/dc/terms/conformsTo": { "@id": "https://bioschemas.org/profiles/DataCatalog/0.3-RELEASE-2019_07_01", "@type": "CreativeWork" }, "description": "Reconciliation of metabolites and biochemical reactions for automated model construction and genome annotation for large-scale metabolic networks", "keywords": "metabolism, network, model, metabolite, compound, chemical, biochemical, reaction, namespace, reconciliation", "name": "MetaNetX/MNXref", "provider": [ { "@id": "https://www.sib.swiss/", "@type": "Organization", "name": "SIB Swiss Intitute of Bioinformatics" }, { "@id": "https://www.vital-it.ch/", "@type": "Organization", "name": "Vital-IT", "logo": "https://vital-it.ch/images/vital-it_logo.png" } ], "url": "https://www.metanetx.org/", "citation": [ { "@id": "http://dx.doi.org/10.1093/nar/gkaa992", "@type": "CreativeWork", "name": "MetaNetX/MNXref: unified namespace for metabolites and biochemical reactions in the context of metabolic models" }, { "@id": "https://dx.doi.org/10.1093/nar/gkv1117", "@type": "CreativeWork", "name": "MetaNetX/MNXref - reconciliation of metabolites and biochemical reactions to bring together genome-scale metabolic networks" }, { "@id": "https://dx.doi.org/10.1093/bioinformatics/btt036", "@type": "CreativeWork", "name": "MetaNetX.org: a website and repository for accessing, analysing and manipulating metabolic networks" }, { "@id": "https://dx.doi.org/10.1093/bib/bbs058", "@type": "CreativeWork", "name": "Reconciliation of metabolites and biochemical reactions for metabolic networks" } ], "dataset": [ { "@context": "https://schema.org", "@type": "Dataset", "@id": "https://www.metanetx.org/ftp/", "description": "The MNXref reconciliation of metabolites and biochemical reactions namespace", "identifier": [], "keywords": "metabolite, compound, chemical, biochemical, reaction, namespace, reconciliation", "name": "MNXref namespace", "creator": [ { "@type": "Person", "name": "The MetaNetX/MNXref team" } ], "url": "/ftp/latest/", "license": "https://creativecommons.org/licenses/by/4.0/" } ], "dateCreated": "2011", "license": { "@id": "https://creativecommons.org/licenses/by/4.0/", "@type": "CreativeWork", "name": "Creative Commons Attribution 4.0 International License" }, "fileFormat": [ "text/plain", "text/html", "application/sbml+xml", "chemical/x-inchi", "chemical/x-daylight-smiles", "image/png" ] }
        """

        data = json.loads(jsonld)

        kg = ConjunctiveGraph()
        kg.parse(data=jsonld, format="json-ld")
        print(kg.serialize(format="turtle"))


if __name__ == '__main__':
    unittest.main()
