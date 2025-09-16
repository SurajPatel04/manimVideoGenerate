from langgraph.graph import (
    StateGraph, 
    START, 
    END
)
from app.schema.ServiceSchema import isQueryPossible

from app.services.queryFeasibilityCheck import isQuery

graph_build = StateGraph(isQueryPossible)

graph_build.add_node("isQuery", isQuery)

graph_build.add_edge(START, "isQuery")
graph_build.add_edge("isQuery", END)

graph_for_query_fesibility_check = graph_build.compile()