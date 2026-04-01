# Changelog

All notable changes to this project will be documented in this file.
Bump `version` in `pyproject.toml`, add an entry here, then `git tag vX.Y.Z` to trigger a release.

## [Unreleased]

## [0.1.6] — 2026-04-02

### Fixed
- Workflow prompt now explicitly prohibits mermaid and plantuml; Claude was defaulting to mermaid from training data despite the macro being removed

## [0.1.5] — 2026-04-02

### Changed
- Removed Mermaid and PlantUML diagram support; all diagrams use plain `text` code blocks (always renders, no Confluence app required)
- Jira ticket descriptions now use Jira wiki markup (`h2.`, `#` numbered lists) for proper heading and list rendering
- `mermaid_macro` config field removed from `ConfluenceConfig`
- Updated workflow prompt to include `get_jira_issue` and `update_confluence_doc` tools

## [0.1.4] — 2026-04-02

### Fixed
- Mermaid macro no longer emits a spurious `language` parameter that prevented rendering in Confluence

### Added
- Markdown table → Confluence `<table>` conversion (previously rendered as raw text)
- PlantUML fenced block support (`\`\`\`plantuml`) renders via the Confluence PlantUML macro

## [0.1.3] — 2026-04-02

### Added
- `get_jira_issue` tool — fetch a Jira issue by key (`PLAT-123`) or full URL; returns summary, status, type, priority, assignee, description, labels, and story points

## [0.1.2] — 2026-04-02

### Changed
- Renamed config file from `.spike.toml` to `.atlassian_buddy.toml`
- Renamed MCP tools: `write_spike_doc` → `write_confluence_doc`, `update_spike_doc` → `update_confluence_doc`
- Renamed MCP prompt: `spike_workflow` → `buddy_workflow`
- Removed all spike-mcp branding from package internals

## [0.1.1] — 2026-04-02

### Fixed
- README install command and package references updated to atlassian-buddy

## [0.1.0] — 2026-04-02

### Added
- Initial release as `atlassian-buddy` (forked from `spike-mcp`)
- MCP tools: `search_confluence`, `get_confluence_page`, `search_jira`, `write_confluence_doc`, `update_confluence_doc`, `create_epic`, `create_story`, `create_task`, `get_project_config`
- `.atlassian_buddy.toml` project config with search order: explicit path → cwd → git root walk-up → `~/.atlassian_buddy.toml`
- Confluence markdown → storage format conversion (headings, lists, bold/italic, fenced code, Mermaid diagrams)
- Jira markdown → Atlassian Document Format (ADF) JSON conversion
- Next-gen and classic Jira project support (auto-detects via `parent` field fallback)
- `confluence.base_url` config override for orgs where Confluence and Jira are on different Atlassian Cloud domains
- `jira.required_fields` config table — org-specific mandatory fields merged into every create call
- CDATA injection protection for Mermaid/code blocks in Confluence pages
