# WMS GetMap parameters

HTTP: **`GET {base_url}/geoservice`**

## Required

| Param | Value |
|-------|-------|
| `SERVICE` | `WMS` |
| `REQUEST` | `GetMap` |
| `VERSION` | `1.3.1` |
| `LAYERS` | Full layer id (see SKILL.md) |
| `BBOX` | `minx,miny,maxx,maxy` |
| `WIDTH` | pixels (e.g. `1024`) |
| `HEIGHT` | pixels (e.g. `1024`) |
| `FORMAT` | `image/png` |
| `CRS` | `EPSG:4326` or `EPSG:3857` (must match layer `epsg_` suffix) |

## Common optional

| Param | When |
|-------|------|
| `ELEVATION` | Variable has levels (e.g. `2m`, `sfc`, `85000i`) |
| `STYLES` | Colormap id from `list_styles` |
| `FORECAST` | Forecast sources only (`PT0H`, `PT6H`, …) |
| `RUN` | Model run (`latest` or ISO time) |
| `TIME` | Products indexed by wall-clock time |
| `TRANSPARENT` | `true` / `false` |

## Layer id template

```
{source}-{region}-{product}-{variable}-{depth}-epsg_{code}
```

Product `all` in catalogs → `none` in the layer string.

## BBOX

Pass the **user's** map extent as `minx,miny,maxx,maxy`. Units must match the layer `epsg_` suffix.

| Layer suffix | Units |
|--------------|-------|
| `epsg_4326` | lon/lat degrees |
| `epsg_3857` | Web Mercator meters |

`list_source_region_bound` and `list_region_bound` (mcp_metadata) do **not** supply GetMap BBOX. Use `list_region_bound` when the user named a region token; use `list_source_region_bound` to pick `{region}` when the user gives source + extent but not region. Keep the user's BBOX for GetMap.
