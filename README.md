# BoxerSkills

Agent skill playbooks for the Boxer weather platform. This is a Wet Dog / Boxer
git repository. It is not an AWS service and not a Cursor-hosted product.

Skills teach an agent how to build WCS GetCoverage and WMS GetMap requests from
catalog tokens. Discover tokens with **BoxerMcps** (`mcp_metadata`). Fetch data
or maps with **BoxerMcps** (`mcp_wcs`, `mcp_geoservice`) only when the agent must
execute HTTP itself.

## Layout

| Path | Role |
|------|------|
| [`.cursor/skills/boxer-wcs/`](.cursor/skills/boxer-wcs/) | WCS GetCoverage playbook (committed for agent discovery) |
| [`.cursor/skills/boxer-geoservice/`](.cursor/skills/boxer-geoservice/) | WMS GetMap playbook |
| [`skills/`](skills/) | Same trees plus optional install scripts for copying into another project |

## Use this repo as a workspace

1. Clone and open **BoxerSkills** in Cursor (or a similar agent IDE).
2. Skills under `.cursor/skills/` are picked up automatically after reload.
3. Point MCP at a running **BoxerMcps** deployment (or local stdio servers) in
   `.cursor/mcp.json` — for example remote URLs:

```json
{
  "mcpServers": {
    "boxer-metadata": {
      "url": "https://<stack>.api.wetdogweather.com/mcp-metadata/mcp"
    },
    "boxer-wcs": {
      "url": "https://<stack>.api.wetdogweather.com/mcp-wcs/mcp"
    },
    "boxer-geoservice": {
      "url": "https://<stack>.api.wetdogweather.com/mcp-geoservice/mcp"
    }
  }
}
```

Exact URL paths follow the BoxerMcps API Gateway mappings. See the BoxerMcps
README for deploy and path details.

## Copy skills into another project

From this repo root:

```bash
python skills/install-cursor-skills.py
```

That copies `skills/boxer-wcs` and `skills/boxer-geoservice` into the current
project’s `.cursor/skills/`. Use `--personal` to install under `~/.cursor/skills/`.

## Compatibility

Skill workflows assume BoxerMcps tool names and schemas (`list_sources`,
`list_source_region_products`, `wcs_get_coverage`, `wms_get_map`, and the rest).
Keep BoxerSkills and BoxerMcps releases aligned when those contracts change.

Default source when the user does not name one is `gfs`.
