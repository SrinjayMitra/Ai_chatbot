import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "scripts"))

from unittest.mock import patch, MagicMock
import scraper.scrape_products as scrape_products


FAKE_HTML = """
<html><body>
  <h1>Inline Backwater Valve</h1>
  <div class="entry-content">
    <p>Prevents sewer backflow into residential lines.</p>
    <p>Rated for municipal surcharge events.</p>
  </div>
</body></html>
"""


def test_scrape_page_extracts_name_and_description():
    mock_resp = MagicMock()
    mock_resp.text = FAKE_HTML
    mock_resp.raise_for_status = MagicMock()

    with patch("scraper.scrape_products.requests.get", return_value=mock_resp):
        result = scrape_products.scrape_page(
            "https://www.galaxyplastics.com/product-category/municipal/inline-backwater-valve/"
        )

    assert result["name"] == "Inline Backwater Valve"
    assert "backflow" in result["description"]
    assert result["category"] == "Product Category"


def test_scrape_page_returns_none_on_request_failure():
    import requests
    with patch("scraper.scrape_products.requests.get", side_effect=requests.RequestException("boom")):
        result = scrape_products.scrape_page("https://www.galaxyplastics.com/broken/")
    assert result is None