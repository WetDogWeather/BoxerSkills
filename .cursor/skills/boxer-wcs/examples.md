# Worked GetCoverage URLs

The host application (or caller) executes these; the agent only assembles the
URL or parameters.

## GFS 2 m temperature — point, **current** (wall-clock now)

Do **not** use `t(...)`. Probe `f(PT0H)` at the region center, read `modelRun`,
then fetch the two `f(PTnH)` hours that bracket `now` and interpolate.

Example: GFS `global` center is `lat(0)`, `long(0)`. Probe:

```
GET {base}/wcs/GetCoverage?
  CoverageId=gfs-global-atmos_latest
  &RANGESUBSET=temperature
  &FORMAT=json
  &SUBSET=lat(0)
  &SUBSET=long(0)
  &SUBSET=z(2)
  &SUBSET=f(PT0H)
```

JSON includes `"modelRun": "2026-08-24T12:00:00Z"`. If `now` is
`2026-08-24T15:37:00Z`, then `n = 3` so bracket `f(PT3H)` and `f(PT4H)`.
User point (Montreal):

```
GET {base}/wcs/GetCoverage?
  CoverageId=gfs-global-atmos_latest
  &RANGESUBSET=temperature
  &FORMAT=json
  &SUBSET=lat(45.5)
  &SUBSET=long(-73.57)
  &SUBSET=z(2)
  &SUBSET=f(PT3H)
```

Repeat with `f(PT4H)`. Interpolate the two `values` to 15:37Z.

For a **box**, fetch only the closest hour (`PT4H` is 23 min away, `PT3H` is
37 min away → use `f(PT4H)`). Do not interpolate.

Look up levels first via mcp_metadata `list_source_variable_levels`
(e.g. gfs/global/atmos/temperature; AGL 2 → catalog `2m` → `z(2)`).
Do not convert units: isobaric 200 → catalog `200i` → `is(200)`.

## GFS 2 m temperature — point, analysis of the latest run only

Only when the user wants the **run analysis** (valid at run time), not “now”:

```
CoverageId=gfs-global-atmos_latest
RANGESUBSET=temperature
FORMAT=json
SUBSET=lat(40)
SUBSET=long(-98)
SUBSET=z(2)
SUBSET=f(PT0H)
```

## HRRR CONUS surface temperature — bbox, 1 h forecast, NetCDF

```
CoverageId=hrrr-conus-sfcf_latest
RANGESUBSET=temperature
FORMAT=netcdf
SUBSET=long(-97.3102856,-96.3)
SUBSET=lat(32.9644625,33.9)
SUBSET=z(2)
SUBSET=f(PT1H)
```

## HRRR CONUS native — hybrid level 10, all forecasts (JSON)

Hybrid levels live under product `natf`, not `sfcf`.

```
CoverageId=hrrr-conus-natf_latest
RANGESUBSET=temperature
FORMAT=json
SUBSET=lat(40)
SUBSET=long(-98)
SUBSET=hy(10)
```

Omit `f(...)` → full forecast run (large response).

## RTMA (observed) — no forecast SUBSET

```
CoverageId=rtma-conus-rtma_latest
RANGESUBSET=temperature
FORMAT=json
SUBSET=lat(40)
SUBSET=long(-98)
SUBSET=z(2)
```

Do **not** include `SUBSET=f(...)` — `rtma` is `observed` in
`list_source_temporal_types`.

## JSON shape for host apps

Many clients want a params object (note repeated `SUBSET`):

```json
{
  "path": "/wcs/GetCoverage",
  "method": "GET",
  "params": [
    ["CoverageId", "gfs-global-atmos_latest"],
    ["RANGESUBSET", "temperature"],
    ["FORMAT", "json"],
    ["SUBSET", "lat(45.5)"],
    ["SUBSET", "long(-73.57)"],
    ["SUBSET", "z(2)"],
    ["SUBSET", "f(PT3H)"]
  ]
}
```

Or a ready-to-fetch URL string (one bracket hour after the `f(PT0H)` probe):

```
{base}/wcs/GetCoverage?CoverageId=gfs-global-atmos_latest&RANGESUBSET=temperature&FORMAT=json&SUBSET=lat(45.5)&SUBSET=long(-73.57)&SUBSET=z(2)&SUBSET=f(PT3H)
```
