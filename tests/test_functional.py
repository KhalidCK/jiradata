from click.testing import CliRunner
from jiradata.jiradata import cli
from dataclasses import fields
import pandas as pd

# cat response.json | jiradata myreport.csv


def test_cli(shared_datadir, tmp_path):
    runner = CliRunner()
    result = runner.invoke(cli, ['--help'])
    assert result.exit_code == 0
    data = str(shared_datadir/'response.json')
    report = tmp_path/'report.csv'
    result = runner.invoke(cli, [str(report), data])
    print(result.stdout)
    assert result.exit_code == 0
    processed = pd.read_csv(report)
    assert len(processed) == 1


def test_cli_custom_field(shared_datadir, tmp_path):
    runner = CliRunner()
    data = str(shared_datadir/'response-epic.json')
    report = tmp_path/'report.csv'
    customfield = 'customfield_10000'
    result = runner.invoke(cli, ['--custom-field',customfield , str(report), data])
    print(result.stdout)
    assert result.exit_code == 0
    processed = pd.read_csv(report)
    assert len(processed) > 0
    csvcols = list(processed.columns)
    assert customfield in csvcols
    #assert any([col for col in processed.columns if 'epic_' in col])

def test_cli_epic_field(shared_datadir, tmp_path):
    runner = CliRunner()
    data = str(shared_datadir/'response-epic.json')
    report = tmp_path/'report.csv'
    epicfield = 'customfield_10000'
    result = runner.invoke(cli, ['--epic-field',epicfield , str(report), data])
    print(result)
    print(result.stdout)
    assert result.exit_code == 0
    processed = pd.read_csv(report)
    assert len(processed) > 0
    csvcols = list(processed.columns)
    assert any([col for col in csvcols if 'epic_' in col])

def test_cli_infer_excel_format_output(shared_datadir,tmp_path):
    runner = CliRunner()
    data = str(shared_datadir/'response.json')
    report = tmp_path/'report.xlsx'
    result = runner.invoke(cli, [str(report), data])
    print(result.stdout)
    assert result.exit_code == 0
    processed = pd.read_excel(report,engine='openpyxl')
    assert len(processed) == 1