# PlanetSide 2 API Backup

This repository contains an automated backup of all static collections in the PlanetSide 2 API.

*Last updated: 2021-10-27*

## Limitations

To keep this backup easy to navigate, maintain, and compact, this backup does not contain all API data. Please note the following limitations:

- For localised text entries, only the English locale is retained
- NULL fields are not included
- Any form of dynamic data (characters, stats, outfits, events, etc.) has been excluded

For a full list of excluded collections, please refer to the `_BLACKLIST` constant at the top of the [`tools/scraper.py`](https://github.com/leonhard-s/ps2-api-backup/blob/main/tools/scraper.py) file.
