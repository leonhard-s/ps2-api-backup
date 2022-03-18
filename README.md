# PlanetSide 2 API Backup

This repository contains an automated backup of all static collections in the PlanetSide 2 API.

*This repository is automatically updated at 06:00, 12:00, 18:00, and 24:00 UTC.*

## Format

The backup script paginates each collection and aggregates the contents of the `<collection>_list` payload key into a JSON list.
This list is then saved to the corresponding `data/<collection>_list.json` file.

If you wish to emulate API responses, you have to manually add the outer payload containing keys like `results`, `<collection>_list`, or `timing`.

## Limitations

This backup only contains static API data, i.e. data that is not expected to change within a given build of the game.

As such, any form of character data, statistics, outfits, events, and leaderboards have been manually excluded.

Additionally, the `state` field of all entries in the `world` collection is always set to `'online'` so as not to clutter the backups.

For a full list of excluded collections, please refer to the `_BLACKLIST` constant at the top of the [`tools/scraper.py`](https://github.com/leonhard-s/ps2-api-backup/blob/main/tools/scraper.py) file.

## File Endpoint Scraper

This project has a sister repository hosting all images available through the API's file endpoint:

[PS2 API Asset Repository](https://github.com/leonhard-s/ps2-api-files)

Note that the above is a quite performance-hungry repository containing upwards of 25'000 files, which is why file backups are not included in this repository.
