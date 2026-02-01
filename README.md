# Agent Skills

Skills follow the Agent Skills format: https://agentskills.io/

## Available Skills

### aria2-json-rpc

通过 JSON-RPC 控制 `aria2` daemon。

Use when:
- "download this URL / magnet / torrent"
- "pause/resume/remove this download"
- "list active/waiting/stopped downloads"
- "show global stats / speed / progress"

Skill definition: `skills/aria2-json-rpc/SKILL.md`

## Installation

If you use a Skills installer (e.g. `skills` CLI):

```bash
npx skills add <github-org-or-user>/<repo>
```

Or install by copying the skill folder into your agent's skills directory (agent-specific).

## Prerequisites

- `aria2c` running with RPC enabled (HTTP JSON-RPC endpoint)
- Network access to the RPC endpoint

Example (local):

```bash
aria2c --enable-rpc --rpc-listen-all=false --rpc-listen-port=6800
```

If you use a secret:

```bash
aria2c --enable-rpc --rpc-secret="YOUR_TOKEN" --rpc-listen-all=false --rpc-listen-port=6800
```

## Configuration

Example config file:
- `skills/aria2-json-rpc/config.example.json`

Recommended approach:
- Copy `skills/aria2-json-rpc/config.example.json` to `skills/aria2-json-rpc/config.json`
- Do not commit `config.json` (it may contain secrets)

Example:

```json
{
  "host": "localhost",
  "port": 6800,
  "secret": null,
  "secure": false,
  "timeout": 30000
}
```

## Repo Layout

```text
skills/
  aria2-json-rpc/
    SKILL.md
    config.example.json
openspec/
  changes/
    aria2-json-rpc-skill/     # design + milestone plan (work-in-progress)
```

## License

MIT (see `LISENCE`).
