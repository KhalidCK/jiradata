# Jira data

Massage data for JIRA issues.

> Cause sometimes you need to sort out issues

## How to use ?

Write csv file

```shell
cat response.json | jiradata myreport.csv
```

## Hold up what is this `reponse.json` ?

Query issues from the JIRA REST API.

What I found convenient is to query with POST ([JIRA rest api examples](https://developer.atlassian.com/server/jira/platform/jira-rest-api-example-query-issues-6291606/))

You can chain unix style arguments using the convenient [httpie](https://httpie.org/)

```sh
echo '{"jql":"project = QA","startAt":0,"maxResults":2,"fields":["id","key"]}'|http -a myusername post 'https://myconfluence.com/api/2/search'
```
