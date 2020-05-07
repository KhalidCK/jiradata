from click.testing import CliRunner
from jiradata.jiradata import cli,Issue
from dataclasses import fields
import pandas as pd

# cat response.json | jiradata myreport.csv


def test_cli(shared_datadir, tmp_path):
    runner = CliRunner()
    result = runner.invoke(cli, ['--help'])
    assert result.exit_code == 0
    data = str(shared_datadir/'response.json')
    report = tmp_path/'report.csv'
    # read stdin
    #result = runner.invoke(cli, [str(report)], input=param)
    result = runner.invoke(cli, [str(report), data])
    print(result.stdout)
    assert result.exit_code == 0
    processed = pd.read_csv(report)
    assert len(processed) == 1
    # next test
    assert set(processed.columns) == set(Issue._fields)
