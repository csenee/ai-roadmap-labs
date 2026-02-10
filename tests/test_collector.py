import json
import pytest

from src.collector import main as collector

class DummyResponse:
    def __init__(self, status_code, payload=None):
        self.status_code = status_code
        self._payload = payload or {}
    
    def json(self):
        return self._payload

def test_get_pokemon_info_returns_json_on_200(monkeypatch):
    def fake_get(url, timeout=10):
        return DummyResponse(200, {"name": "pikachu", "height": 4, "weight": 60})
    
    monkeypatch.setattr(collector.requests, "get", fake_get)

    data = collector.get_pokemon_info("pikachu")
    assert data["name"] == "pikachu"
    assert "height" in data
    assert "weight" in data

def test_get_pokemon_info_returns_none_on_404(monkeypatch):
    def fake_get(url, timeout=10):
        return DummyResponse(404)
    
    monkeypatch.setattr(collector.requests, "get", fake_get)

    data = collector.get_pokemon_info("doesnotexist")
    assert data is None

def test_save_jsonwrites_file_to_data_dir(tmp_path, monkeypatch):
    monkeypatch.setattr(collector, "DATA_DIR", str(tmp_path))

    payload = {"name": "bulbasaur", "height": 7, "weight": 69}
    collector.save_json(payload)

    out_file = tmp_path / "bulbasaur.json"
    assert out_file.exists()

    saved = json.loads(out_file.read_text(encoding="utf-8"))
    assert saved["name"] == "bulbasaur"