import pytest, requests

def pytest_addoption(parser):
    parser.addoption("--base-url", action="store", default="http://localhost:8000",
                     help="Base URL for API under test")
    parser.addoption("--offline", action="store_true", default=False,
                     help="Stub out HTTP calls (no real server needed)")

@pytest.fixture(scope="session")
def base_url(request):
    return request.config.getoption("--base-url")

@pytest.fixture(autouse=True)
def _offline_stub(request, monkeypatch):
    if not request.config.getoption("--offline"):
        return

    class _Resp:
        def __init__(self, code=200, json_obj=None, text=""):
            self.status_code = code
            self._json = json_obj
            self.text = text
        def json(self):
            if self._json is not None:
                return self._json
            return {}

    def _fake_request(method, url, **kwargs):
        # Simple happy-path stub: always 200
        return _Resp(200, {"ok": True}, "OK")

    monkeypatch.setattr(requests, "request", _fake_request, raising=True)
