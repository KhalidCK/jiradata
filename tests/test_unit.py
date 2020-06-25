import json
import pandas as pd

from jiradata.jiradata import (Comment, comment2str, get_gist_issue,
                               get_last_comment, make_report, add_epic)

# def test_retrieve_value_from_issue():
#     simple = {'myitem': 'stuff'}
#     assert get_value(simple['myitem']) == 'stuff'
#     nested = {'myitem': {'a': 1, 'name': 'myname'}}
#     assert get_value(nested['myitem']) == 'myname'
#     withlist = {'myitem': ['a', 'b']}
#     assert get_value(withlist['myitem']) == 'a,b'
#     outofscope = {'myitem': {'a': 1}}
#     assert get_value(outofscope['myitem']) == ''


def test_retrieve_last_comment():
    commentA = {'self': 'https://jira.io/rest/api/2/issue/782674/comment/747211',
                'id': '747211',
                'author': {'self': 'https://jira.io/rest/api/2/user?username=takzeo.musashi%40legends.com',
                           'name': 'takzeo.musashi@legends.com',
                           'key': 'takzeo.musashi@legends.com',
                           'displayName': 'Name A',
                           'active': True,
                           'timeZone': 'Europe/Paris'},
                'body': 'Message A',
                'created': '2020-03-18T14:41:00.289+0100',
                'updated': '2020-03-18T14:41:00.289+0100'}
    commentB = {'self': 'https://jira.io/rest/api/2/issue/782674/comment/747211',
                'id': '747211',
                'author': {'self': 'https://jira.io/rest/api/2/user?username=takzeo.musashi%40legends.com',
                           'name': 'takzeo.musashi@legends.com',
                           'key': 'takzeo.musashi@legends.com',
                           'displayName': 'Name B',
                           'active': True,
                           'timeZone': 'Europe/Paris'},
                'body': 'Message B',
                'created': '2020-03-18T14:41:00.289+0100',
                'updated': '2020-03-18T14:41:00.289+0100'}
    comments = [commentA, commentB]
    assert get_last_comment(comments) == Comment('Name B',
                                                 '2020-03-18T14:41:00.289+0100',
                                                 'Message B')


def test_comment_to_text():
    comment = Comment(author='Nobody Land',
                      updated='2019-06-19T12:03:31.693+0200',
                      msg='See you later, space cowboy')

    assert comment2str(
        comment) == '2019-06-19,Nobody Land:See you later, space cowboy'
    assert comment2str(Comment('', '', '')) == ''


def test_get_all_default_field_from_issue(shared_datadir):
    issue = json.load(open(shared_datadir/'response.json')
                      )['issues'][0]['fields']
    expected = {
        'key': 'myid',
        'assignee': 'uzumaki.kickass@freeworld.com',
        'comment': Comment('Takzeo Musashi',
                           '2020-03-18T14:41:00.289+0100',
                           'No pain, no gain'),
        'created': '2020-03-23T17:38:38.000+0100',
        'creator': 'creator.kickass@freeworld.com',
        'description': 'Let me write something\r\nReally long\r\n\r\nCause why not ?',
        'issuetype': 'Task',
        'labels': "plusultra,backfire",
        'priority': 'Highest',
        'reporter': 'reporter.kickass@freeworld.com',
        'status': 'In Progress',
        'summary': 'How to escape ?'}
    assert get_gist_issue(key='myid', issue=issue) == expected


def test_get_all_field_and_customfield(shared_datadir):
    issue = json.load(open(shared_datadir/'response.json'))
    fields = issue['issues'][0]['fields']
    expected = {
        'key': 'myid',
        'assignee': 'uzumaki.kickass@freeworld.com',
        'comment': Comment('Takzeo Musashi',
                           '2020-03-18T14:41:00.289+0100',
                           'No pain, no gain'),
        'created': '2020-03-23T17:38:38.000+0100',
        'creator': 'creator.kickass@freeworld.com',
        'description': 'Let me write something\r\nReally long\r\n\r\nCause why not ?',
        'issuetype': 'Task',
        'labels': "plusultra,backfire",
        'priority': 'Highest',
        'reporter': 'reporter.kickass@freeworld.com',
        'status': 'In Progress',
        'summary': 'How to escape ?',
        'customfield_10005': '00|i40000'}
    custom = {'customfield_10005': lambda x: str(x)}
    proc = get_gist_issue(key='myid', issue=fields, custom_field=custom)
    assert proc == expected


def test_make_report(shared_datadir):
    issue = json.load(open(shared_datadir/'response.json'))
    fields = issue['issues']
    df = make_report(fields)
    assert len(df) == 1


def test_make_report_epic(shared_datadir):
    report = pd.read_json(shared_datadir/'processed.json')
    expected = pd.read_json(shared_datadir/'expected_epic.json')
    processed = add_epic(report, 'customfield_10000')
    assert len(processed) == 3
    cols = set(processed.columns)
    assert 'epic_key' in cols
    assert 'epic_summary' in cols
    # raise exception if not equal
    pd.testing.assert_frame_equal(
        expected, processed, check_like=True, check_dtype=False)
