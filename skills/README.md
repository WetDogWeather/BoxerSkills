# Boxer skill sources

Source trees for `boxer-wcs` and `boxer-geoservice`. The same content is committed
under [`.cursor/skills/`](../.cursor/skills/) so opening this repository as a
workspace loads the skills without an install step.

## Install into another project

From the BoxerSkills repo root:

```bash
python skills/install-cursor-skills.py
```

Wrappers: `install-cursor-skills.sh`, `install-cursor-skills.ps1`.

| Flag | Destination |
|------|-------------|
| _(default)_ | this repo’s `.cursor/skills/` (or the project root when scripts are vendored elsewhere) |
| `--personal` | `~/.cursor/skills/` |

Reload the agent IDE after install.
