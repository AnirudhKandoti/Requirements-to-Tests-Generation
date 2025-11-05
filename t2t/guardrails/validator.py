from pathlib import Path

def ensure_paths(out_dir):
    Path(out_dir, 'features').mkdir(parents=True, exist_ok=True)
    Path(out_dir, 'tests').mkdir(parents=True, exist_ok=True)
    Path(out_dir, 'artifacts').mkdir(parents=True, exist_ok=True)

def limit_scope(jira_links, op_index):
    scoped = {}
    for link in jira_links:
        key = str(link).strip()
        if key in op_index:
            scoped[key] = op_index[key]
            continue
        parts = key.split(' ',1)
        if len(parts)==2:
            method, route = parts[0].upper(), parts[1]
            for op_id, meta in op_index.items():
                if meta['method']==method and meta['route']==route:
                    scoped[op_id] = meta
                    break
    return scoped

def schema_validate_stub(op_meta):
    return True
