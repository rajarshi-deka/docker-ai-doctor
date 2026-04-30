from langgraph.graph import StateGraph, END
from .state import AgentState
from .nodes import investigator, diagnoser, planner, decision, executor_node

builder = StateGraph(AgentState)

builder.add_node("investigator", investigator)
builder.add_node("diagnoser", diagnoser)
builder.add_node("planner", planner)
builder.add_node("decision", decision)
builder.add_node("executor", executor_node)

builder.set_entry_point("investigator")

builder.add_edge("investigator", "diagnoser")
builder.add_edge("diagnoser", "planner")
builder.add_edge("planner", "decision")
builder.add_edge("decision", "executor")
builder.add_edge("executor", END)

graph = builder.compile()