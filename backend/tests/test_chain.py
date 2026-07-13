from app.langchain_chain.chain import parse_bot_output, guess_category


# --- JSON parsing (no LLM call needed) ---

def test_parses_valid_match_json():
    raw = '{"product_name": "Inline Backwater Valve", "product_url": "https://x.com/valve", "category": "Municipal", "reason": "Prevents sewer backflow"}'
    result = parse_bot_output(raw)
    assert result["product_name"] == "Inline Backwater Valve"
    assert result["product_url"] == "https://x.com/valve"


def test_parses_no_match_json():
    raw = '{"product_name": null, "product_url": null, "category": null, "reason": "Nothing fits — contact sales"}'
    result = parse_bot_output(raw)
    assert result["product_name"] is None
    assert "contact sales" in result["reason"]


def test_handles_malformed_json_gracefully():
    raw = "Sorry, here's my answer: Inline Backwater Valve is a good fit!"
    result = parse_bot_output(raw)
    assert result["product_name"] is None
    assert "couldn't parse" in result["reason"]


# --- Category router ---

def test_guesses_municipal_from_sewer_keyword():
    assert guess_category("I need something to stop sewer backflow") == "Municipal"


def test_guesses_corrosion_control():
    assert guess_category("protecting metal pipes from rust underground") == "Corrosion Control"


def test_guesses_drainage():
    assert guess_category("surface water is pooling in my parking lot") == "Drainage"


def test_returns_none_for_unrelated_query():
    assert guess_category("do you sell umbrellas") is None