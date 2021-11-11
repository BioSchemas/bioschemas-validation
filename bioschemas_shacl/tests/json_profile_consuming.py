import json
import unittest
from pathlib import Path


class MyTestCase(unittest.TestCase):

    def test_something(self):
        base_path = Path(__file__).parent.parent  ## current directory
        #static_file_path = str((base_path / "data/specifications/Taxon/Taxon_v0.6-RELEASE.json").resolve())
        # static_file_path = str((base_path / "data/specifications/ComputationalTool/ComputationalTool_v1.0-RELEASE.json").resolve())
        static_file_path = str(
            (base_path / "data/specifications/ComputationalWorkflow/ComputationalWorkflow_v1.0-RELEASE.json").resolve())

        with open(static_file_path) as f:
            profile = json.load(f)
            print(json.dumps(profile, indent=True))
            for g in profile["@graph"]:
                if ("$validation") in g.keys():
                    for k in g["$validation"]["required"] :
                        print(f"required {k}")
                    for k in g["$validation"]["recommended"] :
                        print(f"recommended {k}")



if __name__ == '__main__':
    unittest.main()
