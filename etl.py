#!/usr/bin/env python2.7
"""Import some datasets into the Salford site."""
import argparse
import time
import pickle

import ckanapi
import ckanapi.errors


def get_extra(dataset, name):
    """Return the value of the named extra from the given dataset."""
    value = None
    found = None
    for extra in dataset.get("extras"):
        if extra["key"] == name:
            assert not found, ("I assume datasets don't have two extras with "
                               "the same name")
            found = True
            value = extra["value"]
    return value


def get_licenses(url, apikey):
    """Return the list of license dicts from the given CKAN site."""
    return ckanapi.RemoteCKAN(url, apikey=apikey).action.license_list()


def get_license(title, url, apikey):
    """Return the license_id for the given license_title."""
    license_id = None
    for license_ in get_licenses(url, apikey):
        if license_["title"] == title:
            assert not license_id, ("The site shouldn't have two licenses "
                                    "with the same title")
            license_id = license_["id"]
    if not license_id:
        raise Exception("License not found: '{title}'".format(title=title))
    else:
        return license_id


def data_gov_uk_transform(dataset, url, apikey):
    """Transform a dataset from data.gov.uk.

    Into a format suitable for loading into the Salford site.

    """
    transformed_dataset = {}

    # Top-level keys that we'll keep. Sub-lists and sub-dicts are treated
    # separately below.
    whitelist = [
        "maintainer", "maintainer_email", "metadata_created",
        "metadata_modified", "author", "author_email", "version",
        "name", "isopen", "url", "notes", "title", "tags",
        # We need to make sure that ids are the same so harvesting works
        "id",
        # DGU fields
        "la_function",
        "la_service",
        "temporal_coverage-from",
        "temporal_coverage-to",
        "mandate",
        "update_frequency",
        "unpublished",
    ]

    for key in dataset:
        if key in whitelist:
            transformed_dataset[key] = dataset[key]

    if transformed_dataset.get('mandate'):
        if (isinstance(transformed_dataset['mandate'], list) and
                len(transformed_dataset['mandate'])):
            if transformed_dataset['mandate'][0]:
                transformed_dataset['mandate'] = transformed_dataset['mandate'][0]
            else:
                del transformed_dataset['mandate']

    transformed_dataset["resources"] = []
    resource_whitelist = ["created", "description", "format", "name",
                          "position", "url", "id"]
    for resource in dataset["resources"]:
        new_resource = {key: value for key, value in resource.items()
                        if key in resource_whitelist}
        transformed_dataset["resources"].append(new_resource)

    # Some datasets have a normal CKAN license_id and title.
    license_id = dataset.get("license_id")
    license_title = dataset.get("license_title")

    # Some datasets have a "license" extra.
    licence = get_extra(dataset, "licence")

    # Other datasets have "licence_url" and "licence_url_title" extras.
    licence_url = get_extra(dataset, "licence_url")
    licence_url_title = get_extra(dataset, "licence_url_title")

    if license_id and license_title:
        assert not (licence or licence_url or licence_url_title)
        transformed_dataset["license_id"] = license_id
        transformed_dataset["license_title"] = license_title
    elif licence:
        assert not (license_id or license_title or licence_url
                    or licence_url_title)
        import json
        list_ = json.loads(licence)
        assert len(list_) == 1
        item = list_[0]
        assert isinstance(item, basestring)
        title = item.split(",")[0].strip()
        id_ = get_license(title, url, apikey)
        transformed_dataset["license_id"] = id_
        transformed_dataset["license_title"] = title
    elif licence_url and licence_url_title:
        assert not (license_id or license_title or licence)
        transformed_dataset["license_title"] = licence_url_title
        transformed_dataset["license_id"] = get_license(licence_url_title,
                                                        url, apikey)
    else:
        assert False, "We should never get here"

    return transformed_dataset


def _create_dataset(dataset, client):
    """Create and return the given dataset if it doesn't already exist."""
    try:
        return client.action.package_create(**dataset)
    except ckanapi.errors.ValidationError as err:
        if ('name' in err.error_dict
                and err.error_dict['name'] == ['That URL is already in use.']):
            return client.action.package_show(id=dataset['name'])
        else:
            raise
    assert False, "We should never get here"


def load(datasets, url, apikey):
    """Create the given datasets on the Salford site."""
    salford = ckanapi.RemoteCKAN(url, apikey)
    for dataset in datasets:
        _create_dataset(dataset, salford)


def datagovuk_extract(import_uklp_datasets=False):
    """Extract the datasets from data.gov.uk.

    Return the cached datasets from the pickle file if it exists.
    Otherwise get the datasets from data.gov.uk, cache them in the pickle file,
    and return them.

    """
    pickle_filename = "datasets.pickle"
    try:
        with open(pickle_filename, "r") as pickle_file:
            datasets = pickle.load(pickle_file)
    except IOError:
        datagovuk = ckanapi.RemoteCKAN('http://data.gov.uk/')
        datasets = []  # List of all the extracted datasets.
        response = datagovuk.action.organization_show(
            id='salford-city-council')
        for package in response["packages"]:
            full_package_dict = datagovuk.action.package_show(id=package["id"])
            if import_uklp_datasets:
                datasets.append(full_package_dict)
            elif not get_extra(full_package_dict, 'UKLP'):
                datasets.append(full_package_dict)
            time.sleep(1)
        with open(pickle_filename, "w") as pickle_file:
            pickle.dump(datasets, pickle_file)
    return datasets


def cli():
    """Parse and return the command-line arguments."""
    parser = argparse.ArgumentParser()
    parser.add_argument("-u", "--url",
                        default='https://www.salforddataquay.uk/')
    parser.add_argument("-l", "--import-uklp",
                        default=False)

    parser.add_argument("-a", "--apikey", required=True)
    return parser.parse_args()


def main():
    """Extract, transform and load the datasets into the Salford site."""
    args = cli()
    url = args.url
    apikey = args.apikey
    import_uklp_datasets = args.import_uklp
    datasets = datagovuk_extract(import_uklp_datasets)
    datasets = [data_gov_uk_transform(dataset, url, apikey)
                for dataset in datasets]
    load(datasets, apikey=apikey, url=url)


if __name__ == '__main__':
    main()
