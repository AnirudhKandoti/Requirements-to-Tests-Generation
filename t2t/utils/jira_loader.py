import json
from pathlib import Path

REQUIRED_FIELDS = {'id','title','description','links','priority'}

def load_jira(path):
    data = json.loads(Path(path).read_text(encoding='utf-8'))
    issues = data['issues'] if isinstance(data, dict) and 'issues' in data else data
    if not isinstance(issues, list):
        raise ValueError("Jira JSON must be a list or {'issues': [...]}")
    norm = []
    for it in issues:
        missing = REQUIRED_FIELDS - set(it.keys())
        if missing:
            raise ValueError(f"Jira issue missing fields: {missing}")
        norm.append({
            'id': str(it['id']),
            'title': it['title'],
            'description': it['description'],
            'links': it.get('links') or [],
            'priority': it.get('priority','Medium')
        })
    return norm
