import json, yaml
from openapi_spec_validator import validate_spec
from pathlib import Path

def load_openapi(path):
    p = Path(path)
    text = p.read_text(encoding='utf-8')
    data = yaml.safe_load(text) if p.suffix.lower() in {'.yaml', '.yml'} else json.loads(text)
    try:
        validate_spec(data)
    except Exception as e:
        print(f"[warn] OpenAPI validation warning: {e}")
    index = {}
    for route, methods in (data.get('paths') or {}).items():
        if isinstance(methods, dict):
            for method, op in methods.items():
                if isinstance(op, dict):
                    op_id = op.get('operationId') or f"{method.upper()} {route}"
                    index[op_id] = {'route': route, 'method': method.upper(), 'op': op}
    return data, index
