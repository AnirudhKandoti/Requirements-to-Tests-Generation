from pathlib import Path
from jinja2 import Template

FEATURE_TMPL = Template("""
Feature: {{ title }}
  As a user of the API
  I want {{ title.lower() }}
  So that the service behaves as specified

  Background:
    Given the API base URL is "{{ base_url }}"

{% for s in scenarios -%}
  Scenario: {{ s.name }}
    When I call {{ s.method }} {{ s.route }}
    Then I receive a {{ s.expect_status }} response
    And the response matches the contract for operationId "{{ s.operation_id }}"
{% endfor -%}
""")

def write_feature(out_dir, req, scenarios, base_url="http://localhost:8000"):
    content = FEATURE_TMPL.render(title=req['title'], scenarios=scenarios, base_url=base_url)
    fname = f"{req['id']}_{req['title'].lower().replace(' ','_').replace('/','_')}.feature"
    Path(out_dir, 'features', fname).write_text(content.strip()+"\n", encoding='utf-8')
    return fname
