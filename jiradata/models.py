
from dataclasses import dataclass

@dataclass
class JiraTicket:
    ref: str
    status: str
    priority: str
    issue_type: str
    date_update: str
    date_created: str
    title: str
    description: str
    labels: list
    owner: str