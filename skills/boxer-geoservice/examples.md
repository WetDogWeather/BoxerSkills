# Worked GetMap commands

The host application executes these; the agent only assembles parameters.

## GFS 2 m temperature — Canada

```
GET /geoservice?
  SERVICE=WMS&REQUEST=GetMap&VERSION=1.3.1
  &LAYERS=gfs-global-atmos-temperature-16-epsg_4326
  &BBOX=-141,42,-52,83
  &CRS=EPSG:4326
  &WIDTH=1024&HEIGHT=1024
  &FORMAT=image/png
  &ELEVATION=2m
  &STYLES=truwx_temperature
  &FORECAST=PT0H
```

Look up levels first via mcp_metadata `list_source_variable_levels`.

## HRRR CONUS — Web Mercator

```
LAYERS=hrrr-conus-natf-temperature-16-epsg_3857
BBOX=-13914936.35,2753408.11,-7347086.39,6446275.84
CRS=EPSG:3857
ELEVATION=2m
```

## RTMA (observed) — no FORECAST

```
LAYERS=rtma-conus-rtma-temperature-16-epsg_4326
BBOX=-125,24,-66,50
ELEVATION=2m
```

Do **not** include `FORECAST` — `rtma` is `observed` in `list_source_temporal_types`.

## JSON shape for host apps

Many clients want a params object:

```json
{
  "path": "/geoservice",
  "method": "GET",
  "params": {
    "SERVICE": "WMS",
    "REQUEST": "GetMap",
    "VERSION": "1.3.1",
    "LAYERS": "gfs-global-atmos-temperature-16-epsg_4326",
    "BBOX": "-141,42,-52,83",
    "CRS": "EPSG:4326",
    "WIDTH": 1024,
    "HEIGHT": 1024,
    "FORMAT": "image/png",
    "ELEVATION": "2m",
    "STYLES": "truwx_temperature",
    "FORECAST": "PT0H"
  }
}
```
