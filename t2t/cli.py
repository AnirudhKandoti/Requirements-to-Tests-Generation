import click
from .agents.requirement_agent import RequirementAgent
from .traceability.matrix import TraceabilityBuilder

@click.group()
def main():
    """T2T CLI"""
    pass

@main.command()
@click.option('--openapi', 'openapi_path', required=True, type=click.Path(exists=True))
@click.option('--jira', 'jira_path', required=True, type=click.Path(exists=True))
@click.option('--out', 'out_dir', required=True, type=click.Path())
def generate(openapi_path, jira_path, out_dir):
    """Generate Gherkin + pytest from Jira + OpenAPI with guardrails."""
    agent = RequirementAgent()
    agent.run(openapi_path, jira_path, out_dir)
    click.echo(f"✓ Generated tests and features in: {out_dir}")

@main.command()
@click.option('--run-dir', required=True, type=click.Path(exists=True))
@click.option('--csv', 'csv_out', required=True, type=click.Path())
@click.option('--html', 'html_out', required=False, type=click.Path())
def traceability(run_dir, csv_out, html_out):
    """Build a live traceability matrix from outputs."""
    tb = TraceabilityBuilder(run_dir)
    tb.build(csv_out, html_out)
    msg = f"✓ Traceability matrix written to {csv_out}"
    if html_out:
        msg += f", {html_out}"
    print(msg)

if __name__ == "__main__":
    main()
