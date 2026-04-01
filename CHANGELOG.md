# Changelog

All notable changes to this project will be documented in this file.
Bump `version` in `pyproject.toml`, add an entry here, then `git tag vX.Y.Z` to trigger a release.

## [Unreleased]

## [0.1.1] — 2026-04-02

### Fixed
- README install command and package references updated to atlassian-buddy

## [0.1.0] — 2026-04-02

### Added
- Initial release as `atlassian-buddy` (forked from `spike-mcp`)
- MCP tools: `search_confluence`, `get_confluence_page`, `search_jira`, `write_spike_doc`, `update_spike_doc`, `create_epic`, `create_story`, `create_task`, `get_project_config`
- `.spike.toml` project config with search order: explicit path → cwd → git root walk-up → `~/.spike.toml`
- Confluence markdown → storage format conversion (headings, lists, bold/italic, fenced code, Mermaid diagrams)
- Jira markdown → Atlassian Document Format (ADF) JSON conversion
- Next-gen and classic Jira project support (auto-detects via `parent` field fallback)
- `confluence.base_url` config override for orgs where Confluence and Jira are on different Atlassian Cloud domains
- `jira.required_fields` config table — org-specific mandatory fields merged into every create call
- CDATA injection protection for Mermaid/code blocks in Confluence pages
