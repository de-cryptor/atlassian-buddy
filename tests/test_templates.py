from atlassian_buddy.templates import CONFLUENCE_DOC_TEMPLATE, STORY_TEMPLATE, SYSTEM_PROMPT


def test_confluence_doc_has_required_sections():
    for section in [
        "Overview",
        "Problem Statement",
        "Goals",
        "Proposed Solution",
        "Flow Diagram",
        "Implementation Options",
        "Recommendation",
        "Epic",
        "References",
    ]:
        assert section in CONFLUENCE_DOC_TEMPLATE, f"Missing section: {section}"


def test_confluence_doc_has_text_diagram_placeholder():
    assert "```text" in CONFLUENCE_DOC_TEMPLATE


def test_story_template_is_formattable():
    result = STORY_TEMPLATE.format(
        context="Background info",
        what="Implement the thing",
        acceptance_criteria="# It works",
        out_of_scope="Nothing else",
        notes="TBD",
    )
    assert "Background info" in result
    assert "Implement the thing" in result
    assert "# It works" in result


def test_story_template_uses_jira_headings():
    assert "h2." in STORY_TEMPLATE


def test_system_prompt_research_first():
    assert "search_confluence" in SYSTEM_PROMPT
    assert "search_jira" in SYSTEM_PROMPT


def test_system_prompt_text_diagram():
    assert "```text" in SYSTEM_PROMPT


def test_system_prompt_jira_wiki_markup():
    assert "h2." in SYSTEM_PROMPT


def test_system_prompt_confirm_before_write():
    assert "get_project_config" in SYSTEM_PROMPT
    assert "confirm" in SYSTEM_PROMPT.lower() or "confirmation" in SYSTEM_PROMPT.lower()


def test_system_prompt_fibonacci_scale():
    assert "fibonacci" in SYSTEM_PROMPT.lower() or "Fibonacci" in SYSTEM_PROMPT


def test_system_prompt_imperative_verb():
    assert "imperative" in SYSTEM_PROMPT.lower()
