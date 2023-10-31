from rdflib import ConjunctiveGraph, URIRef
import requests
from requests.exceptions import InvalidURL, ConnectionError, ConnectTimeout
import random
import os
from tqdm import tqdm
import pandas as pd
import click

CONTEXT_SETTINGS = dict(help_option_names=["-h", "--help"])


@click.group(context_settings=CONTEXT_SETTINGS)
@click.version_option(version="1.0.0")
def cli():
    pass


def get_live_deploys_urls():
    results = []
    live_deploys_remote_file = "https://raw.githubusercontent.com/BioSchemas/bioschemas.github.io/master/_data/live_deployments.json"
    res = requests.get(live_deploys_remote_file)
    live_deploys = res.json()

    for r in live_deploys["resources"]:
        for p in r["profiles"]:
            if "exampleURL" in p.keys():
                results.append(p["exampleURL"])
            else:
                print(
                    f"no example URL for profile {p['profileName']} and url {r['url']}"
                )
    print(f"found {len(set(results))} live deploys")
    return list(set(results))


def retrieve_bioschemas(url):
    FC_get_md = (
        "https://fair-checker.france-bioinformatique.fr/api/inspect/get_rdf_metadata"
    )
    kg = ConjunctiveGraph()
    res = requests.get(url=FC_get_md, params={"url": url})
    try:
        kg.parse(data=res.text, format="json-ld")
    except Exception as e:
        print(e)
    # print(f"Loaded {len(kg)} RDF triples from {url}")
    return kg


def valid_bioschemas(url):
    # FC_bs_valid = "https://fair-checker.france-bioinformatique.fr/api/inspect/bioschemas_validation"
    FC_bs_valid = "https://fair-checker.france-bioinformatique.fr/api/inspect/bioschemas_validation_by_conformsto"
    res = requests.get(url=FC_bs_valid, params={"url": url})
    return res.json()


def has_conforms_to(kg):
    conformsTo = URIRef("http://purl.org/dc/terms/conformsTo")
    return (None, conformsTo, None) in kg


def check_live_deploy(url, dump_flag):
    ld = url
    row = {"URL": ld}
    try:
        status_code = requests.head(ld).status_code
        row["HTTP_status"] = status_code
        kg = retrieve_bioschemas(ld)
        # print(kg.serialize(format="ntriples"))
        row["nb_triples"] = len(kg)
        row["has_conforms_to"] = has_conforms_to(kg)
        if dump_flag:
            with open("out.nq", "a") as out_file:
                # kg.serialize(destination="out.nq", format="nquads")
                try :
                    nquads = kg.serialize(format="nquads")    
                    out_file.write(nquads)
                except Exception as e:
                    print(f"N-quads serialization errror with url: {ld}")
                    print(e)
    except InvalidURL as e:
        print(f"Invalid url: {ld}")
        row["info"] = f"Invalid url: {ld}"
    except ConnectionError as e:
        print(f"Time out when accessing url: {ld}")
        row["info"] = f"Time out when accessing url: {ld}"
    return row


def valid_live_deploy(url):
    rows = []
    ld = url
    try:
        row = {"Bioschemas Live Deploy URL": ld}
        bs_valid = valid_bioschemas(ld)
        for entity in bs_valid.keys():
            row = {"Bioschemas Live Deploy URL": ld}
            row["Evaluated entity"] = entity
            row["Reference profile"] = bs_valid[entity]["ref_profile"]
            row["Is valid"] = bs_valid[entity]["conforms"]
            row["Nb errors"] = len(bs_valid[entity]["errors"])
            row["Nb warnings"] = len(bs_valid[entity]["warnings"])
            row["Is the latest profile"] = bs_valid[entity]["latest_profile"]
            row["Is deprecated profile"] = bs_valid[entity]["deprecated"]
            rows.append(row)
    except Exception as e:
        print(f"Error while validating {ld}")
    return rows


@cli.command(
    help="Checks that Bioschemas metadata can be harvested on Bioschemas Live Deploy web pages. By default, 3 live deploys are randomly picked."
)
@click.option("--all", is_flag=True, help="Check all live deploys")
@click.option("--dump", is_flag=True, help="Dumps metadata in nquads")
def check(all, dump):
    lds = get_live_deploys_urls()

    if not all:
        lds = random.sample(lds, 3)
    
    if dump:
        if os.path.exists("out.nq"):
            os.remove("out.nq")

    rows = []
    print(f"checking {len(lds)} live deploys")
    for ld in tqdm(lds):
        row = check_live_deploy(ld, dump)
        rows.append(row)
    df1 = pd.DataFrame.from_records(rows)
    df1.to_csv("bioschemas_harvesting.csv")
    df1.to_markdown("bioschemas_harvesting.md")


@cli.command(
    name="validate",
    help="Validate Bioschemas profiles on Live Deploy web pages. By default, 3 live deploys are randomly picked. ",
)
@click.option("--all", is_flag=True, help="Check all live deploys")
def valid(all):
    lds = get_live_deploys_urls()

    if not all:
        lds = random.sample(lds, 3)

    rows = []
    print(f"checking {len(lds)} live deploys")
    for ld in tqdm(lds):
        results = valid_live_deploy(ld)
        for r in results:
            rows.append(r)
    df2 = pd.DataFrame.from_records(rows)
    df2.to_csv("bioschemas_validation.csv")
    df2.to_markdown("bioschemas_validation.md")


if __name__ == "__main__":
    cli()
