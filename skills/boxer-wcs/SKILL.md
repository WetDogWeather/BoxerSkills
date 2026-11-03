---
name: boxer-wcs
description: >-
  Build WCS GetCoverage HTTP commands (CoverageId, RANGESUBSET, SUBSET, FORMAT).
  Use when the host app already GETs /wcs/GetCoverage and the agent must assemble
  a valid URL or query parameters. Not for fetching data via MCP. Triggers on
  wcs, GetCoverage, CoverageId, RANGESUBSET, gfs, hrrr, netcdf, coverage data.
---

# WCS — build GetCoverage commands

Your **application sends** `GET {base}/wcs/GetCoverage` (or GetCapabilities).
This skill tells the agent how to build the query parameters / URL.

**Metadata MCP first, build URL/params in the skill second, execution MCP only if an actual fetch is needed.**

1. Discover tokens with **mcp_metadata** (do not guess).
2. Build a valid GetCoverage URL or params object using the rules below.
3. Return that for the host app to execute. This skill does **not** fetch coverage.
4. If the agent must **fetch the coverage itself**, call **mcp_wcs** only after the request is built.

## Workflow

1. Call **mcp_metadata** tools (filter with `source` / `region` / `product` / `variable` when known):
   - `list_source_region_products` — valid source/region/product combinations
   - `list_source_product_variables` — RANGESUBSET variable tokens
   - `list_source_variable_levels` — vertical level tokens
   - `list_source_temporal_types` — forecast vs observed
   - `list_source_region_bound` — region extents on a source (EPSG:4326)
   - `list_region_bound` — extent for a named region token (EPSG:4326)
   - Do **not** call `list_styles` (WMS-only).
   - If the user names a region, use `list_region_bound` for that token's box. Still confirm the region exists on the source with `list_source_region_products` or `list_source_region_bound`.
   - If the user gives **source + lon/lat BBOX** but not region, use `list_source_region_bound` to pick `{region}` (overlap with user BBOX). Keep the user's extent for spatial `SUBSET` — do not substitute the region extent.
2. Build **CoverageId**:

   `{source}-{region}-{product}_latest`

   - Map product `all` → `none` **only** in the CoverageId prefix.
   - For a specific model run: `{prefix}_{YYYY-MM-DDTHH:MM:SSZ}`.
   - Also valid: `_latest-complete`, `_latest-incomplete`.

3. Set WCS query parameters (see [getcoverage-params.md](getcoverage-params.md)).
4. Return a full URL (or params object) for the host app / caller to execute.
   Use **mcp_wcs** only if an actual coverage fetch is required.

## Rules (always apply)

- **RANGESUBSET** holds the variable token(s) (e.g. `temperature` or
  `wind_speed,wind_direction`). Never put the variable inside CoverageId.
- **Spatial SUBSET** is required: `lat`+`long` (geographic) or `x`+`y`
  (projected). Point: `lat(40)`, `long(-98)`. BBox: `lat(miny,maxy)`,
  `long(minx,maxx)`.
- **Vertical SUBSET** is a mechanical encode/decode of the catalog level
  token from `list_source_variable_levels`. Use the number the user said as
  `XX`. Do not convert units (hPa, mb, Pa, feet, meters). Confirm that
  catalog token exists; if it is absent, stop and report it. Do not pick a
  different token.

  WCS subset z(XX>0) means AGL (height above ground) XX which is encode in variable level as XXm
  WCS subset z(0) means ground level which is encoded in variable level as sfc
  WCS subset is(XX) means isobaric level XX which is encoded in variable level as XXi
  WCS subset fl(XX) means flight level XX which is encoded in variable level as flXX
  WCS subset hy(xx) means hybrid level XX which is encoded in variable level as  XXs
  WCS subset msl(xx) means mean sea level XX which is encoded in variable level as XXm_msl
  WCS subset tropo means tropopause which is encoded in variable level as tropo

  Examples: isobaric level 200 → catalog `200i` → `SUBSET=is(200)`.
  AGL 2 → catalog `2m` → `SUBSET=z(2)`. Ground → catalog `sfc` → `SUBSET=z(0)`.
- **Forecast / time SUBSET** (forecast sources only — see
  `list_source_temporal_types`; never for `observed`):
  - Use **`f(PTnH)`** relative to the CoverageId run. Do **not** use `t(...)`
    for current / now / present.
  - **`f(PT0H)` is the run’s analysis**, valid at the model run time — **not**
    “temperature right now.”
  - For **current / now / present** with `CoverageId=…_latest`:
    1. Get the region extent (`list_source_region_bound` or `list_region_bound`).
       Probe the **center of the region**
       (`lat((miny+maxy)/2)`, `long((minx+maxx)/2)`) with
       `FORMAT=json`, `SUBSET=f(PT0H)`, and the same `RANGESUBSET` / vertical
       SUBSET as the user request when known. Execute this probe via
       **mcp_wcs**. Read **`modelRun`** from the JSON.
    2. Let `now` be current UTC. Find the two forecast hours that bracket
       `now`: `n = floor((now − modelRun) / 1h)`, so `f(PTnH)` and
       `f(PT(n+1)H)` (validity `modelRun + n h` and `modelRun + (n+1) h`).
       If `now` lands exactly on a step, use that single `f(PTnH)`.
    3. **Point** request: GetCoverage the user's point at both bracket hours
       (`FORMAT=json`). Linearly interpolate `values` to `now`:
       `v = v0 + (v1 − v0) * (now − t0) / (t1 − t0)`.
    4. **Box** request: GetCoverage the user's box at the **closest** of the
       two hours. Do **not** interpolate.
  - Omit `f(...)` only when you want the **full** forecast run (large response).
- **FORMAT**: `json` or `netcdf`.
- **SOURCE**: if not specified, use `gfs`.

## Examples

See [examples.md](examples.md).

## Metadata (mcp_metadata)

**mcp_metadata** (backed by `boxer_src_properties`) is the only metadata source.
Call the tools above; prefer filtered lookups so only one branch enters context.
