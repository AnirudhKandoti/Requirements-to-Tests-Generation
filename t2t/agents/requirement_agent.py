from pathlib import Path
from ..utils.openapi_loader import load_openapi
from ..utils.jira_loader import load_jira
from ..guardrails.validator import ensure_paths, limit_scope, schema_validate_stub
from ..generators.gherkin import write_feature
from ..generators.pytest_gen import write_tests

class RequirementAgent:
    def run(self, openapi_path, jira_path, out_dir):
        ensure_paths(out_dir)
        _, index = load_openapi(openapi_path)
        issues = load_jira(jira_path)
        trace_rows = []
        for req in issues:
            scoped_ops = limit_scope(req['links'], index)
            for meta in scoped_ops.values():
                schema_validate_stub(meta)
            scenarios = [{
                "name": f"{req['id']} hits {m['method']} {m['route']}",
                "method": m['method'],
                "route": m['route'],
                "expect_status": 200,
                "operation_id": op_id
            } for op_id, m in scoped_ops.items()]
            feature_file = write_feature(out_dir, req, scenarios)
            test_file = write_tests(out_dir, req, scoped_ops)
            trace_rows.append((req['id'], feature_file, test_file))
        Path(out_dir, 'artifacts', 'traceability.tsv').write_text(
            "RequirementID\tFeatureFile\tTestFile\n" + "\n".join(f"{a}\t{b}\t{c}" for a,b,c in trace_rows),
            encoding="utf-8"
        )
        return trace_rows
