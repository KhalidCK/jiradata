# Jira data

> Cause sometimes you need to sort out your issues 

Programmatic way to pull out your issues.


## Install

`pip install jiradata`

## How to use ?

Write a csv report

```shell
cat response.json | jiradata myreport.csv
```

## Hold up what is this `reponse.json` ?

Query issues from the JIRA REST API.

What I found convenient is to use the query API with POST ([JIRA rest api examples](https://developer.atlassian.com/server/jira/platform/jira-rest-api-example-query-issues-6291606/))

You can chain unix style arguments using [httpie](https://httpie.org/)

config.json

```json
{
  "jql": "project = QA",
  "startAt": 0,
  "maxResults": 2,
  "fields": ["id", "key"]
}
```

Command line (redirect stdout to the right location)

```sh
cat config.json|http -a myusername post 'https://myconfluence.com/api/2/search'
```

## Related

Built in jira : [Export results to microsoft Excel](https://confluence.atlassian.com/jira061/jira-user-s-guide/searching-for-issues/working-with-search-result-data/exporting-search-results-to-microsoft-excel)
