---
name: boxer-geoservice
description: >-
  Build Boxer geo_server WMS GetMap HTTP commands (LAYERS, BBOX, ELEVATION,
  STYLES, FORECAST). Use when the host app already GETs /geoservice and the
  agent must assemble valid query parameters. Not for fetching PNGs via MCP.
  Triggers on geoservice, WMS GetMap, layer id, elevation, gfs, hrrr, weather map,
  list sources.
---

# Boxer geoservice — build GetMap commands

Your **application sends** `GET {base}/geoservice`. This skill tells the agent
how to build the query parameters.

**Metadata MCP first, build URL/params in the skill second, execution MCP only if an actual fetch is needed.**

1. Discover tokens with **mcp_metadata** (do not guess).
2. Build a valid GetMap URL or params object using the rules below.
3. Return that for the host app to execute. This skill does **not** fetch maps.
4. If the agent must **fetch the PNG itself**, call **mcp_geoservice** only after the request is built.

## Workflow

1. Call **mcp_metadata** tools (filter with `source` / `region` / `product` / `variable` / `style` when known):
   - `list_source_region_products` — valid source/region/product combinations
   - `list_source_product_variables` — variable tokens
   - `list_source_variable_levels` — elevation tokens
   - `list_source_temporal_types` — whether `FORECAST` is allowed
   - `list_source_region_bound` — region extents on a source (EPSG:4326)
   - `list_region_bound` — extent for a named region token (EPSG:4326)
   - `list_styles` — style ids / colormaps
   - If the user names a region, use `list_region_bound` for that token's box. Still confirm the region exists on the source with `list_source_region_products` or `list_source_region_bound`.
   - If the user gives **source + lon/lat BBOX** but not region, use `list_source_region_bound` to pick `{region}` (overlap with user BBOX). Keep the user's BBOX for GetMap.
2. Build the layer id (do **not** put elevation in it):

   `{source}-{region}-{product}-{variable}-{depth}-epsg_{code}`

   - Map product `all` → `none` **only** in the layer string.
   - `variable` = the variable token from `list_source_product_variables` (e.g. `temperature`).
   - `depth` is usually `16`.

3. Set WMS query parameters (see [getmap-params.md](getmap-params.md)).
4. Return params (or a full URL) for the host app to execute.
   Use **mcp_geoservice** only if an actual map fetch is required.

## Rules (always apply)

- **ELEVATION** is a separate parameter (`2m`, `sfc`, `85000i`, …). Never inside `LAYERS`.
- **BBOX** units must match the layer suffix: `epsg_4326` = lon/lat degrees; `epsg_3857` = meters.
- **STYLES**: prefer `truwx_*` when it lists your variable; else `mp_*` or omit.
- **FORECAST**: only for sources with `temporal_type: forecast` from
  `list_source_temporal_types`. Never for `observed` (rtma, mrms, urma, casa).
- **SOURCE**: if not specified use gfs

## Examples

See [examples.md](examples.md).

## Metadata (mcp_metadata)

**mcp_metadata** (backed by `boxer_src_properties`) is the only metadata source.
Call the tools above; prefer filtered lookups so only one branch enters context.
