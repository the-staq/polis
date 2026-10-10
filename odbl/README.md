# odbl/: OpenStreetMap places used by Polis

**Data © OpenStreetMap contributors.** Available under the [Open Database License 1.0](https://opendatacommons.org/licenses/odbl/1-0/) (ODbL); contents under the [Database Contents License 1.0](https://opendatacommons.org/licenses/dbcl/1-0/). See [`LICENSE`](LICENSE) and <https://www.openstreetmap.org/copyright>.

This folder is the only place in Polis that holds OpenStreetMap data. It is not covered by the repository's Apache 2.0 or CC BY 4.0 licences (see [`../NOTICE`](../NOTICE)).

## What this is

Polis names and places real **public places** from OpenStreetMap: parks, football pitches, markets, station areas and place-word landmarks (the L and P tiers in the venue model). Everything else in the game, including clubs, institutions, pubs, cafés, gyms and rooms, is fictional and never comes from OSM. A real business name appears only when the business licenses it to us.

There is no cap on the number of OSM features. The layer is a derivative database of OpenStreetMap and is published here, in full, under the ODbL. This folder is our offer under ODbL §4.6: it contains the derivative database itself and the method used to make it (the picks file, the extractor described below, and the extract log).

## Files

| File | Contents |
|---|---|
| [`LICENSE`](LICENSE) | ODbL 1.0 and DbCL 1.0, full text |
| [`picks/london.yaml`](picks/london.yaml) | The hand-picked OSM elements for London: `venue_id`, `osm_type`, `osm_id`, `tier`, `kind`, `district`, `reason` |
| [`london/venues-osm.geojson`](london/venues-osm.geojson) | One GeoJSON Point per pick. Properties: `venue_id`, `osm_type`, `osm_id`, `osm_version`, `name`, `osm_tag`, `retrieved_at`. Top-level `license` and `attribution` |
| [`EXTRACT-LOG.yaml`](EXTRACT-LOG.yaml) | Append-only log of extracts: date, script version, Overpass URL, OSM base timestamp, element ids |

The schema for the GeoJSON is [`../schemas/venue-osm.schema.json`](../schemas/venue-osm.schema.json). Gameplay data (tier, kind, careers, needs met, sponsor slots) lives in [`../seeds/modern-earth-2026/venues/`](../seeds/modern-earth-2026/venues/) under CC BY 4.0 and joins to this layer by `venue_id` only. Those files never store an OSM name, point or id.

## Method

1. **Hand-picked by OSM id.** Each place is chosen on openstreetmap.org and listed by type and id in `picks/<city>.yaml`. There is no area or bounding-box query.
2. **Name and point only.** The extractor fetches exactly those ids from the Overpass API and keeps the `name` tag, one point (a node's position, or the Overpass center of a way or relation), the primary tag (for example `leisure=park`) and the element version. All other tags, outlines and editor metadata are discarded. Operator tags are never copied or shown; station areas are shown as "<name> station area".
3. **Never edited.** Names are published exactly as they are in OSM. A pick that fails a check is dropped, not renamed: elements with a `brand` or `brand:wikidata` tag; sensitive sites (schools, childcare, worship, police, hospitals, clinics, courts, prisons, military land, playgrounds); and names that fail the game's text-safety scrub. An unnamed element keeps `name: null` and the game shows a generic label.
4. **One source per data type.** London public-place names come from OSM only. They are never topped up from another dataset or by hand. NaPTAN is used for routing, not for station-area names.
5. **Deterministic output.** Features are sorted by `venue_id` and written as sorted-key JSON. `retrieved_at` is the OSM base timestamp of the Overpass response.

The extractor is `scripts/extract_osm_venues.py` with the `app/maps/overpass/` package in the Polis runtime repository. It reads the picks file, writes the GeoJSON and appends to the log; it touches no database.

## Refreshing

1. Edit `picks/<city>.yaml` (add, remove or change an element id).
2. Run the extractor against an Overpass endpoint. It records the endpoint URL and the OSM base timestamp in `EXTRACT-LOG.yaml`.
3. Check the report: every pick must be kept. If a pick is dropped, remove it from the picks file with a comment saying why.
4. Run `python -m pytest cli/tests/test_odbl_dataset.py` and commit the picks, GeoJSON and log together.

## Corrections and takedown

- **A name or position is wrong.** Fix it in OpenStreetMap, then re-extract. We never correct OSM data here by hand.
- **A place should not be in the game.** Open an issue on this repository. We remove the pick and its venue row, re-extract, and commit; the place then disappears from the game.
- **Attribution.** Every map screen in the game must show "Place names © OpenStreetMap contributors" with a link to <https://www.openstreetmap.org/copyright>, and the credits page must carry the ODbL notice.

## Using this data

You may use, share and adapt this database under the ODbL. If you publicly use it or a database made from it, keep the attribution, offer any adapted database under the ODbL, and do not apply technical restrictions that stop others doing the same. The full terms are in [`LICENSE`](LICENSE).
