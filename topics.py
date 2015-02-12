#!/usr/bin/env python2.7
"""Pre-create some empty groups that Salford City Council requested."""
import argparse

import ckanapi


TOPICS = [
    {
        "name": "business-and-economy",
        "title": "Business & Economy",
        "image_url": "/base/images/groups/business.jpg",
    },
    {
        "name": "children-and-families",
        "title": "Children & Families",
        "image_url": "/base/images/groups/children.jpg",
    },
    {
        "name": "community-and-living",
        "title": "Community & Living",
        "image_url": "/base/images/groups/community.jpg",
    },
    {
        "name": "democracy-and-governance",
        "title": "Democracy & Governance",
        "image_url": "/base/images/groups/democracy.jpg",
    },
    {
        "name": "education-and-learning",
        "title": "Education & Learning",
        "image_url": "/base/images/groups/education.jpg",
    },
    {
        "name": "environment-and-waste",
        "title": "Environment & Waste",
        "image_url": "/base/images/groups/environment.jpg",
    },
    {
        "name": "health-and-social-care",
        "title": "Health & Social Care",
        "image_url": "/base/images/groups/health.jpg",
    },
    {
        "name": "housing",
        "title": "Housing",
        "image_url": "/base/images/groups/housing.jpg",
    },
    {
        "name": "jobs-and-careers",
        "title": "Jobs & Careers",
        "image_url": "/base/images/groups/jobs.jpg",
    },
    {
        "name": "leisure-and-culture",
        "title": "Leisure & Culture",
        "image_url": "/base/images/groups/leisure.jpg",
    },
    {
        "name": "planning-and-development",
        "title": "Planning & Development",
        "image_url": "/base/images/groups/planning.jpg",
    },
    {
        "name": "transport-and-streets",
        "title": "Transport & Streets",
        "image_url": "/base/images/groups/transport.jpg",
    },
]


def create_groups(api, url):
    if url.endswith('/'):
        url = url[:-1]
    for topic in TOPICS:
        topic["image_url"] = url + topic["image_url"]
        api.action.group_create(**topic)


def cli():
    """Parse and return the command-line arguments."""
    parser = argparse.ArgumentParser()
    parser.add_argument("-u", "--url",
                        default='https://www.salforddataquay.uk/')
    parser.add_argument("-a", "--apikey", required=True)
    return parser.parse_args()


def main():
    """Extract, transform and load the datasets into the Salford site."""
    args = cli()
    url = args.url
    apikey = args.apikey
    api = ckanapi.RemoteCKAN(url, apikey=apikey)
    create_groups(api, url)


if __name__ == '__main__':
    main()
