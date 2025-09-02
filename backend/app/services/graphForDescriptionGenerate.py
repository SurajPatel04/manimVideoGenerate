from app.schema.ServiceSchema import DescriptionGenerationState
from langgraph.graph import StateGraph, START, END
from app.services.descriptionGenerate import (
    generateDetailedDescription,
    validateDescription,
    refineDescription,
    router,
    feasibilityRouter,
    isUserQueryPossible,
)

graph_build = StateGraph(DescriptionGenerationState)

graph_build.add_node("isUserQueryPossible", isUserQueryPossible)
graph_build.add_node("generateDetailedDescription", generateDetailedDescription)
graph_build.add_node("validateDescription", validateDescription)
graph_build.add_node("refineDescription", refineDescription)

graph_build.add_edge(START, "isUserQueryPossible")

graph_build.add_conditional_edges(
    "isUserQueryPossible",
    feasibilityRouter,
    {
        "generateDetailedDescription": "generateDetailedDescription",
        "END": END,
    },
)

graph_build.add_edge("generateDetailedDescription", "validateDescription")

graph_build.add_conditional_edges(
    "validateDescription",
    router,
    {
        "refineDescription": "refineDescription",
        "END": END,
    },
)

graph_build.add_edge("refineDescription", "validateDescription")

graph_for_description_generate = graph_build.compile()
