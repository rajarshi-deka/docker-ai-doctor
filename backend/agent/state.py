from typing import TypedDict

class AgentState(TypedDict):
    container_name: str
    status: str
    logs: str

    root_cause: str
    severity: str
    fix: str
    action: str

    auto_fix: bool   
    execute: bool