import pytest
import requests
from app.scraping.bcv_scraper import BcvScraper

class MockResponse:
    """Simple mock of requests.Response"""
    def __init__(self, text: str, status_code: int = 200):
        self.text = text
        self.status_code = status_code

    def raise_for_status(self):
        if self.status_code >= 400:
            raise requests.HTTPError(f"Status code was {self.status_code}")


def mock_get_factory(html: str, status_code: int = 200):
    """Return a function that can be used to monkeypatch requests.get"""
    def _mock_get(url, headers=None, verify=True):
        return MockResponse(html, status_code)
    return _mock_get


def test_get_exchange_rates(monkeypatch):
    html = (
        "<html>"
        "<body>"
        "<div>USD 36,95</div>"
        "<div>EUR 40,55</div>"
        "<div>Fecha Valor: 18 de septiembre de 2025</div>"
        "</body>"
        "</html>"
    )

    # Patch requests.get so no real HTTP request is made
    monkeypatch.setattr(requests, "get", mock_get_factory(html))

    scraper = BcvScraper()
    rates = scraper.get_exchange_rates()

    assert rates is not None, "Expected rates to be a dictionary, got None"
    assert pytest.approx(rates["USD"], 0.01) == 36.95
    assert pytest.approx(rates["EUR"], 0.01) == 40.55
    assert "fecha_valor" in rates