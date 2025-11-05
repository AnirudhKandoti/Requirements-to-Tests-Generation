from pathlib import Path
from jinja2 import Template
import re

TEST_TMPL = Template("""
import requests

{% for t in tests %}
def test_{{ t.safe_name }}(base_url):
    url = base_url + "{{ t.route }}"
    resp = requests.request("{{ t.method }}", url)
    assert resp.status_code == {{ t.expect_status }}
{% endfor %}
""")

_SANITIZE_RE = re.compile(r"[^0-9a-zA-Z_]")
def _sanitize(name: str) -> str:
    return _SANITIZE_RE.sub("_", name)

def write_tests(out_dir, requirement, ops):
    tests = []
    for op_id, meta in ops.items():
        base = f"{requirement['id']}_{op_id}".lower().replace(" ", "_").replace("/", "_")
        safe_name = _sanitize(base)
        tests.append({
            "safe_name": safe_name,
            "route": meta["route"],
            "method": meta["method"],
            "expect_status": 200
        })
    content = TEST_TMPL.render(tests=tests)
    fname = f"test_req_{_sanitize(requirement['id'])}.py"
    Path(out_dir, "tests", fname).write_text(content.strip() + "\n", encoding="utf-8")
    return fname
