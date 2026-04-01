import pytest
from pathlib import Path
from atlassian_buddy.config import (
    _find_toml,
    load_config,
    AtlassianBuddyConfig,
)

MINIMAL_TOML = """
[atlassian]
base_url = "https://myorg.atlassian.net"
email = "user@example.com"

[confluence]
space_key = "ENG"
parent_page_id = "111"

[jira]
project_key = "PLAT"
"""

FULL_TOML = MINIMAL_TOML + """
[tickets]
story_point_scale = [1, 2, 3, 5, 8]
"""


def test_find_toml_explicit_path(tmp_path: Path):
    cfg = tmp_path / ".atlassian_buddy.toml"
    cfg.write_text(MINIMAL_TOML)
    assert _find_toml(str(cfg)) == cfg


def test_find_toml_explicit_path_missing(tmp_path: Path):
    with pytest.raises(FileNotFoundError, match="not found"):
        _find_toml(str(tmp_path / "nonexistent.toml"))


def test_find_toml_in_cwd(tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
    cfg = tmp_path / ".atlassian_buddy.toml"
    cfg.write_text(MINIMAL_TOML)
    monkeypatch.chdir(tmp_path)
    assert _find_toml() == cfg


def test_find_toml_walks_up_to_git_root(tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
    (tmp_path / ".git").mkdir()
    cfg = tmp_path / ".atlassian_buddy.toml"
    cfg.write_text(MINIMAL_TOML)
    subdir = tmp_path / "src" / "app"
    subdir.mkdir(parents=True)
    monkeypatch.chdir(subdir)
    assert _find_toml() == cfg


def test_find_toml_home_fallback(tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
    monkeypatch.chdir(tmp_path)
    home_cfg = tmp_path / ".atlassian_buddy.toml"
    home_cfg.write_text(MINIMAL_TOML)
    monkeypatch.setattr(Path, "home", classmethod(lambda cls: tmp_path))
    assert _find_toml() == home_cfg


def test_find_toml_not_found_raises(tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
    monkeypatch.chdir(tmp_path)
    monkeypatch.setattr(Path, "home", classmethod(lambda cls: tmp_path))
    with pytest.raises(FileNotFoundError, match=".atlassian_buddy.toml"):
        _find_toml()


def test_load_config_missing_token(tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
    cfg = tmp_path / ".atlassian_buddy.toml"
    cfg.write_text(MINIMAL_TOML)
    monkeypatch.delenv("ATLASSIAN_API_TOKEN", raising=False)
    with pytest.raises(SystemExit, match="ATLASSIAN_API_TOKEN"):
        load_config(str(cfg))


def test_load_config_token_in_toml_raises(tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
    bad_toml = """
[atlassian]
base_url = "https://myorg.atlassian.net"
email = "user@example.com"
api_token = "secret"
"""
    cfg = tmp_path / ".atlassian_buddy.toml"
    cfg.write_text(bad_toml)
    monkeypatch.setenv("ATLASSIAN_API_TOKEN", "env-token")
    with pytest.raises(SystemExit, match="api_token"):
        load_config(str(cfg))


def test_load_config_success(tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
    cfg = tmp_path / ".atlassian_buddy.toml"
    cfg.write_text(MINIMAL_TOML)
    monkeypatch.setenv("ATLASSIAN_API_TOKEN", "my-secret-token")
    result = load_config(str(cfg))
    assert isinstance(result, AtlassianBuddyConfig)
    assert result.atlassian.base_url == "https://myorg.atlassian.net"
    assert result.atlassian.email == "user@example.com"
    assert result.confluence.space_key == "ENG"
    assert result.jira.project_key == "PLAT"
    assert result.api_token == "my-secret-token"


def test_load_config_defaults(tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
    minimal = """
[atlassian]
base_url = "https://myorg.atlassian.net"
email = "user@example.com"
"""
    cfg = tmp_path / ".atlassian_buddy.toml"
    cfg.write_text(minimal)
    monkeypatch.setenv("ATLASSIAN_API_TOKEN", "tok")
    result = load_config(str(cfg))
    assert result.tickets.story_point_scale == [1, 2, 3, 5, 8, 13]
    assert result.jira.epic_issue_type == "Epic"
    assert result.jira.default_label == "spike"


def test_load_config_custom_story_point_scale(tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
    cfg = tmp_path / ".atlassian_buddy.toml"
    cfg.write_text(FULL_TOML)
    monkeypatch.setenv("ATLASSIAN_API_TOKEN", "tok")
    result = load_config(str(cfg))
    assert result.tickets.story_point_scale == [1, 2, 3, 5, 8]


def test_load_config_mermaid_macro_default(tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
    cfg = tmp_path / ".atlassian_buddy.toml"
    cfg.write_text(MINIMAL_TOML)
    monkeypatch.setenv("ATLASSIAN_API_TOKEN", "tok")
    result = load_config(str(cfg))
    assert result.confluence.mermaid_macro == "mermaid"


def test_load_config_mermaid_macro_custom(tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
    toml = """
[atlassian]
base_url = "https://myorg.atlassian.net"
email = "user@example.com"

[confluence]
space_key = "ENG"
parent_page_id = "111"
mermaid_macro = "code"
"""
    cfg = tmp_path / ".atlassian_buddy.toml"
    cfg.write_text(toml)
    monkeypatch.setenv("ATLASSIAN_API_TOKEN", "tok")
    result = load_config(str(cfg))
    assert result.confluence.mermaid_macro == "code"
