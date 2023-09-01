# bioschemas-validation
A repository dedicated to the validation of Bioschemas markup against profiles.

# Validation tool
The [script](script) directory contains a basic command line tool interacting with the [FAIR-Checker](https://fair-checker.france-bioinformatique.fr) API. 
It can produces two tabular reports : 
* [bioschemas_harvesting.csv](bioschemas_harvesting.csv), informing on web page accessibility as well as on how many Schema.org annotations are served, and
* [bioschemas_validation.csv](bioschemas_validation.csv), informing on how many errors and warnings are detected when a Bioschemas profile is specified (only if a `dct:conformsTo` property is available)

# Automated reporting on Live Deploys
A GitHub action is run once a week on all available Bioschemas Live Deploys, and updates the CSV and MD files hosted on this repository. 

# Feedback
Please submit any found issue here https://github.com/BioSchemas/bioschemas-validation/issues. 
