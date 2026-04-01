# atlassian-buddy

[![PyPI](https://img.shields.io/pypi/v/atlassian-buddy)](https://pypi.org/project/atlassian-buddy/)
[![Python](https://img.shields.io/pypi/pyversions/atlassian-buddy)](https://pypi.org/project/atlassian-buddy/)

MCP server that connects Claude to Jira and Confluence. Engineers can research spikes, generate technical solutions with Mermaid architecture diagrams, write Confluence docs, and create Jira epic + story breakdowns through natural conversation — no Anthropic API key required.

---

## Features

- **Research** — search Confluence and Jira before generating anything
- **Design** — produce Mermaid architecture/flow diagrams as part of every confluence doc
- **Write** — create or update Confluence pages (markdown + Mermaid → Confluence storage format)
- **Ticket** — create Jira Epics, Stories with acceptance criteria, and Tasks; supports both next-gen and classic projects
- **Zero LLM cost** — Claude itself provides all intelligence; no separate AI API key needed

---

## Installation

Choose your preferred installer:

```bash
# pip
pip install atlassian-buddy

# pipx (recommended — isolated environment, auto-manages PATH)
pipx install atlassian-buddy

# uv
uv tool install atlassian-buddy
```

---

## Setup

### Step 1 — Create `~/.atlassian_buddy.toml`

Create `~/.atlassian_buddy.toml` in your home directory with your Atlassian details:

```bash
# macOS / Linux
touch ~/.atlassian_buddy.toml
```

```toml
[atlassian]
base_url = "https://yourorg.atlassian.net"
email    = "you@yourorg.com"

[confluence]
# If your Confluence is on a different domain than Jira, set this:
# base_url = "https://yourorg-docs.atlassian.net"
space_key      = "ENG"
parent_page_id = "123456"

[jira]
project_key        = "PLAT"
epic_issue_type    = "Epic"
story_issue_type   = "Story"
task_issue_type    = "Task"
default_label      = "spike"
story_points_field = "customfield_10016"
epic_link_field    = "customfield_10014"

[tickets]
story_point_scale = [1, 2, 3, 5, 8, 13]
```

> **Tip:** Config is also discovered automatically in your project root or any parent directory up to the git root — useful when running atlassian-buddy from a specific repo. The search order is: current directory → git root walk-up → `~/.atlassian_buddy.toml`.

#### Org-specific required fields

Some Jira projects enforce mandatory custom fields (e.g. Account, Tier, Work type). Add them under `[jira.required_fields]` and they will be merged into every ticket created:

```toml
[jira.required_fields]
customfield_11139 = 15                  # plain integer (check your field type)
customfield_11518 = { id = "12203" }    # single select
customfield_11664 = [{ id = "13089" }]  # multi-select (array)
```

To find the correct field IDs and allowed values for your project, call the Jira create-meta API:
```
GET /rest/api/3/issue/createmeta?projectKeys=PROJ&issuetypeNames=Epic&expand=projects.issuetypes.fields
```

### Step 2 — Set your API token

Generate an Atlassian API token at https://id.atlassian.com/manage-profile/security/api-tokens and export it:

```bash
export ATLASSIAN_API_TOKEN="your-token-here"
```

Never put the token in `.atlassian_buddy.toml` — it is read exclusively from the environment.

---

## Connect to Claude

atlassian-buddy works with both **Claude Desktop** (GUI app) and **Claude Code** (CLI). Follow the guide for whichever you use — or both.

---

### Option A — Claude Desktop

**Step 1 — Find the config file**

| Platform | Path |
|---|---|
| macOS | `~/Library/Application Support/Claude/claude_desktop_config.json` |
| Windows | `%APPDATA%\Claude\claude_desktop_config.json` |

**Step 2 — Find your binary path**

Run this in your terminal to get the exact path to use in the config:

```bash
which atlassian-buddy
```

**Step 3 — Add atlassian-buddy to `mcpServers`**

Use the block for whichever installer you used. All blocks have the same structure — the only difference is the `command` path.

**pip**
```json
{
  "mcpServers": {
    "atlassian-buddy": {
      "command": "/Users/YOU/.local/bin/atlassian-buddy",
      "env": {
        "ATLASSIAN_API_TOKEN": "your-token-here"
      }
    }
  }
}
```
> macOS path may be `~/Library/Python/3.x/bin/atlassian-buddy`. Run `which atlassian-buddy` to confirm.

**pipx**
```json
{
  "mcpServers": {
    "atlassian-buddy": {
      "command": "/Users/YOU/.local/bin/atlassian-buddy",
      "env": {
        "ATLASSIAN_API_TOKEN": "your-token-here"
      }
    }
  }
}
```
> Confirm the path with: `pipx environment atlassian-buddy | grep -i bin`

**uv**
```json
{
  "mcpServers": {
    "atlassian-buddy": {
      "command": "/Users/YOU/.local/bin/atlassian-buddy",
      "env": {
        "ATLASSIAN_API_TOKEN": "your-token-here"
      }
    }
  }
}
```
> Confirm the path with: `uv tool dir --bin` — the binary lives in that directory.

**Step 4 — Restart Claude Desktop**

Quit and reopen the app. A hammer icon (🔨) in the toolbar confirms the tools are active.

---

### Option B — Claude Code (CLI)

**Step 1 — Find your binary path**

```bash
which atlassian-buddy
```

**Step 2 — Add atlassian-buddy globally**

Run the command for whichever installer you used. Replace the path with the output of `which atlassian-buddy` above.

**pip**
```bash
claude mcp add atlassian-buddy ~/.local/bin/atlassian-buddy -s user -e ATLASSIAN_API_TOKEN="your-token-here"
```
> macOS path may be `~/Library/Python/3.x/bin/atlassian-buddy`. Use `which atlassian-buddy` to confirm.

**pipx**
```bash
claude mcp add atlassian-buddy ~/.local/bin/atlassian-buddy -s user -e ATLASSIAN_API_TOKEN="your-token-here"
```
> Confirm the exact path with: `pipx environment atlassian-buddy | grep -i bin`

**uv**
```bash
claude mcp add atlassian-buddy ~/.local/bin/atlassian-buddy -s user -e ATLASSIAN_API_TOKEN="your-token-here"
```
> Confirm the exact path with: `uv tool dir --bin`

**Step 3 — Verify the connection**

```bash
claude mcp list
```

You should see:

```
atlassian-buddy: /Users/YOU/.local/bin/atlassian-buddy  - ✓ Connected
```

**Step 4 — Start a new Claude Code session**

MCP servers are loaded at session start. Open a fresh session in any directory and atlassian-buddy tools will be available automatically.

---

## Example conversations

Start a session by invoking the workflow prompt at the top of your conversation:

```
/mcp__atlassian-buddy__buddy_workflow
```

Then talk naturally:

- "I need to spike on replacing our job queue with Temporal. Research what we have, design a solution with a diagram, write a spike doc in Confluence under the Platform space, then create an epic and stories in the PLAT project."
- "Search Confluence for our auth service architecture and summarise what you find."
- "Break down the confluence doc you just wrote into Jira tickets — 1 epic, stories with acceptance criteria, fibonacci points."
- "What Jira tickets are open in PLAT related to observability?"

---

## Tools

| Tool | Inputs | Description |
|---|---|---|
| `search_confluence` | `query`, `space_key?`, `limit?` | CQL full-text search across Confluence |
| `get_confluence_page` | `page_id` | Fetch full page content by ID |
| `search_jira` | `query`, `project_key?`, `limit?` | JQL full-text search across Jira |
| `get_jira_issue` | `issue_key_or_url` | Fetch a Jira issue by key (`PLAT-123`) or full URL |
| `write_confluence_doc` | `title`, `body_markdown`, `space_key?`, `parent_page_id?` | Create a Confluence page (markdown → storage format) |
| `create_epic` | `summary`, `description`, `project_key?`, `label?` | Create a Jira Epic |
| `create_story` | `epic_key`, `summary`, `description`, `acceptance_criteria`, `story_points?`, `project_key?`, `label?` | Create a Jira Story linked to an Epic |
| `create_task` | `epic_key`, `summary`, `description`, `project_key?`, `label?` | Create a Jira Task linked to an Epic |
| `create_subtask` | `task_key`, `summary`, `description`, `project_key?`, `label?` | Create a Jira Subtask under an existing Task or Story |
| `get_project_config` | — | Show current config targets (API token redacted) |

---

## Configuration reference

All fields in `.atlassian_buddy.toml`:

| Field | Required | Description |
|---|---|---|
| `atlassian.base_url` | Yes | Your Atlassian Cloud domain, e.g. `https://myorg.atlassian.net` |
| `atlassian.email` | Yes | Your Atlassian account email |
| `confluence.base_url` | No | Override if Confluence is on a different domain than Jira |
| `confluence.space_key` | No | Confluence space key for new confluence docs, e.g. `ENG` |
| `confluence.parent_page_id` | No | Page ID to nest new docs under |
| `jira.project_key` | No | Jira project key, e.g. `PLAT` |
| `jira.epic_issue_type` | No | Issue type name for epics (default: `Epic`) |
| `jira.story_issue_type` | No | Issue type name for stories (default: `Story`) |
| `jira.task_issue_type` | No | Issue type name for tasks (default: `Task`) |
| `jira.subtask_issue_type` | No | Issue type name for subtasks (default: `Subtask`) |
| `jira.default_label` | No | Label applied to all created tickets (default: `spike`) |
| `jira.story_points_field` | No | Custom field ID for story points; varies per instance |
| `jira.epic_link_field` | No | Custom field ID for epic link; classic projects only |
| `jira.required_fields` | No | Org-specific mandatory fields merged into every create call |
| `tickets.story_point_scale` | No | Fibonacci scale used when prompting for estimates |

---

## Contributing

```bash
git clone https://github.com/de-cryptor/atlassian-buddy
cd atlassian-buddy
python -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"
pytest
```

---

## License

MIT — see [LICENSE](LICENSE).
