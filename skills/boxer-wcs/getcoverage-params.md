# WCS GetCoverage parameters

HTTP: **`GET {base_url}/wcs/GetCoverage`**

Repeat `SUBSET` once per axis / constraint (query string allows multiple
`SUBSET=` values).

## Required

| Param | Value |
|-------|-------|
| `CoverageId` | `{source}-{region}-{product}_latest` (see SKILL.md) |
| `RANGESUBSET` | Variable token(s), comma-separated (e.g. `temperature`) |
| `FORMAT` | `json` or `netcdf` |
| `SUBSET` | At least spatial: `lat(...)+long(...)` or `x(...)+y(...)` |

## Vertical SUBSET (no unit conversion)

Use the number the user said as `XX`. Do not convert hPa/mb/Pa or other units.
Confirm the catalog token with `list_source_variable_levels`. If it is absent,
stop and report it.

WCS subset z(XX>0) means AGL (height above ground) XX which is encode in variable level as XXm
WCS subset z(0) means groun level which is encoded in variable level as sfc
WCS subset is(XX) means isobaric level XX which is encoded in variable level as XXi
WCS subset fl(XX) means flight level XX which is encoded in variable level as flXX
WCS subset hy(xx) means hybrid level XX which is encoded in variable level as  XXs
WCS subset msl(xx) means mean sea level XX which is encoded in variable level as XXm_msl
WCS subset tropo means tropopause which is encoded in variable level as tropo

| SUBSET | Catalog token | Example |
|--------|---------------|---------|
| `z(XX)` with XX>0 | `XXm` | AGL 2 → `2m` → `z(2)` |
| `z(0)` | `sfc` | ground → `sfc` → `z(0)` |
| `is(XX)` | `XXi` | isobaric 200 → `200i` → `is(200)` |
| `fl(XX)` | `flXX` | flight level 30 → `fl30` → `fl(30)` |
| `hy(XX)` | `XXs` | hybrid 10 → `10s` → `hy(10)` |
| `msl(XX)` | `XXm_msl` | MSL 100 → `100m_msl` → `msl(100)` |
| `tropo` | `tropo` | tropopause → `tropo` |

## Common optional SUBSET values

| SUBSET | When |
|--------|------|
| `f(PTnH)` | Forecast hour **relative to the CoverageId run** (forecast sources only). `PT0H` = analysis at run time. For **current / now**, probe `f(PT0H)` at the region center, read `modelRun`, then use the bracketing `f(PTnH)` hours (see SKILL.md). Do **not** use `t(...)` for current / now |
| `f(PTaH,PTbH)` | Inclusive forecast range |
| `t(YYYY-MM-DDTHH:MM:SSZ)` | Absolute validity time (forecast sources). Do **not** use for current / now |

## Optional

| Param | When |
|-------|------|
| `INTERPOLATION` | e.g. `x(linear)`, `z(nearest)` — only if the user asks |

## CoverageId template

```
{source}-{region}-{product}_latest
```

Product `all` in catalogs → `none` in the CoverageId string.

## Spatial extent

Pass the **user's** point or box:

| Form | Example |
|------|---------|
| Point | `SUBSET=lat(40)` and `SUBSET=long(-98)` |
| BBox | `SUBSET=lat(32.96,33.9)` and `SUBSET=long(-97.31,-96.3)` |

`list_source_region_bound` and `list_region_bound` (mcp_metadata) do **not**
supply GetCoverage spatial SUBSET. Use `list_region_bound` when the user named
a region token; use `list_source_region_bound` to pick `{region}` when the user
gives source + extent but not region. Keep the user's extent for spatial
`SUBSET`.

## GetCapabilities

```
GET {base_url}/wcs/GetCapabilities
```

No query parameters required for the basic capabilities document.
