# bioschemas-validation [![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/BioSchemas/bioschemas-validation/HEAD)
This repository hosts the tool developped during the BioHackathon 2021 event. 

Special thanks to the contributors : 
- Thomas Rosnet 
- Ivan Mičetić 
- Sebastien Moretti 

Please submit GitHub issues to ask for new features or report bugs. 
Don't hesitate to contact Thomas Rosnet (thomas.rosnet@france-bioinformatique.fr) or Alban Gaignard (alban.gaignard@univ-nantes.fr) for any related question. 

## Motivations and aims 
Bioschemas profiles are community agreed standards leveraging Schema.org for Life Sciences. They specify the minimal, recommended, optional metadata as well as cardinality and expected reuse of controlled vocabulary. Conformance to these profiles are vital to support harvesting by initiatives such as OpenAIRE. 

The goal of this tool is to leverage Bioschemas profile to automatically generate validation code (SHACL shapes). These validation are run online and report possible metadata quality enhancements. 

## What does the tool
The Bioschmeas markup validation is performed as follows:
1. RDF data extraction from web pages (both static and dynamic)
2. For each typed entity (Schema.org or Bioschemas specific types) a SHACL(https://www.w3.org/TR/shacl/) shape is generated based on template.
3. The SHACL shape is evaluated against the extracted RDF data, producing warnings for missing recommended properties, and errors for missing minimal properties.

## Required software environment
To run the tool you need some Python packages.

Here is the recipe to install theses dependencies : 
```
conda create —name bioschemas-valid
conda activate bioschemas-valid
conda install rdflib pyshacl jinja2 selenium webdriver-manager lxml rich jupyter -c conda-forge
pip install extruct
```

## Usage
```
Bioschemas-shacl-validator, a command line tool to validate bisochemas annotated web resources.

Usage :
python main.py -u https://bgee.org/?page=gene&gene_id=ENSG00000274928
```

## Tutorial presented at SWAT4LS'2022
- [slides](https://drive.google.com/file/d/1q8pDUyT4DXv9kvOw64FoPD4OiOIjZyOk/view?usp=sharing)
- [notebook](https://github.com/BioSchemas/bioschemas-validation/tree/main/sandbox_notebooks) [![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/BioSchemas/bioschemas-validation/HEAD)

## Future works 
- Generate SHACL constraints from JSON serialization (Data Discovery Engine)
- Determine the validation profile from dct:conformsTo
- Suggest a relevent profile from a set of Bioschemas markup
