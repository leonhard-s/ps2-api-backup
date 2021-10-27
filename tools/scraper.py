"""Scraper for all static collections in the PlanetSide 2 API."""

import argparse
import asyncio
import json
import os
import pathlib
from typing import Any, Dict, List, cast

import auraxium
from auraxium import census
from auraxium.types import CensusData

# Namespace to scrape
_NAMESPACE = 'ps2:v2'
# Directory to store generated files in
_OUTPUTDIR = pathlib.Path('data/')
# Step size used for pagination, limited to 5k due to "items" collection
_PAGE_SIZE = 5000

# Collections to exclude from the backup
_BLACKLIST: List[str] = [
    # Character-specific tables
    'single_character_by_id',
    'character',
    'character_name',
    'characters_achievement',
    'characters_currency',
    'characters_directive',
    'characters_directive_objective',
    'characters_directive_tier',
    'characters_directive_tree',
    'characters_skill',
    'characters_stat',
    'characters_stat_by_faction',
    'characters_stat_history',
    'characters_weapon_stat',
    'characters_weapon_stat_by_faction',
    'characters_item',
    'characters_world',
    'characters_online_status',
    'characters_friend',
    # Leaderboards
    'leaderboard',
    'characters_leaderboard',
    # Image assets
    'image',
    'image_set',
    'image_set_default',
    # Outfits
    'outfit',
    'outfit_member',
    'outfit_member_extended',
    'outfit_rank',
    # Real-time map status
    'map',
    # Event endpoints
    'world_stat_history',
    'empire_scores',
    'characters_event_grouped',
    'characters_event',
    'event',
    'world_event',
]


async def process_blacklist(client: auraxium.Client) -> List[str]:
    """Check the blacklist for validity and return valid collections.

    Validity means that every name in the blacklist represents an entry
    in the global datatype list.
    """
    # Download the global list of collections
    query = census.Query(None, namespace=_NAMESPACE,
                         service_id=client.service_id)
    data = cast(Dict[str, List[Dict[str, Any]]], await client.request(query))
    # Create a list of all known collections
    collections: List[str] = [d['name'] for d in data['datatype_list']]
    # Check the blacklist entries against the items in this list
    for name in _BLACKLIST:
        if name not in collections:
            raise ValueError(f'Unknown blacklist entry "{name}"')
    # Filter the output list by the blacklist
    return list(set(collections).difference(_BLACKLIST))


async def scrape_collection(collection: str, client: auraxium.Client) -> None:
    entries: List[CensusData] = []
    # Scrape data into memory
    query = census.Query(collection, namespace=_NAMESPACE,
                         service_id=client.service_id)
    # The items collection is hard-limited to 5k entries per query, so
    # we'll use that for everything
    query.limit(_PAGE_SIZE)
    index: int = -1
    while True:
        index += 1
        # Adjust starting size
        query.start(index * _PAGE_SIZE)
        # Fetch data
        payload = cast(Dict[str, List[Dict[str, Any]]],
                       await client.request(query))
        data = payload[f'{collection}_list']
        entries.extend(data)
        # Quit loop when limit is exhausted
        if len(data) != _PAGE_SIZE:
            break
    # Flush data to disk
    with open(_OUTPUTDIR / f'{collection}.json', 'w') as file_:
        json.dump(entries, file_, indent=4)


async def main(service_id: str) -> None:
    """Async component of the "if __name__ == '__main__'" clause."""
    loop = asyncio.get_running_loop()
    async with auraxium.Client(loop, service_id=service_id) as client:
        # Validate blacklist configuration
        collections = sorted(await process_blacklist(client))
        # Start scraping
        print(f'Scraping {len(collections)} collections')
        total = len(collections)
        for index, collection in enumerate(collections):
            print(f'Scraping collection {index+1} of {total}: {collection}')
            await scrape_collection(collection, client)
        print('done')


if __name__ == '__main__':
    try:
        service_id = os.environ['SERVICE_ID']
    except KeyError:
        parser = argparse.ArgumentParser()
        parser.add_argument('service_id', type=str,
                            help='Service ID to use for scraping')
        args = parser.parse_args()
        service_id = args.service_id
    loop = asyncio.new_event_loop()
    loop.run_until_complete(main(service_id))
