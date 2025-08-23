from schema import DescriptionGenerationState
from langgraph.graph import StateGraph, START, END
from descriptionGenerate import generate_Multiple_Description, pick_One_Description_And_Generate_Detailed_Description, validate_Description,refineDescription, router

graph_build = StateGraph(DescriptionGenerationState)
graph_build.add_node("generate_Multiple_Description", generate_Multiple_Description)
graph_build.add_node("pick_One_Description_And_Generate_Detailed_Description", pick_One_Description_And_Generate_Detailed_Description)
graph_build.add_node("validate_Description", validate_Description)
graph_build.add_node("refineDescription", refineDescription)


graph_build.add_edge(START, "generate_Multiple_Description")
graph_build.add_edge("generate_Multiple_Description", "pick_One_Description_And_Generate_Detailed_Description")
graph_build.add_edge("pick_One_Description_And_Generate_Detailed_Description", "validate_Description")
graph_build.add_conditional_edges("validate_Description",router)
graph_build.add_edge("refineDescription", "validate_Description")

graph_for_description_generate = graph_build.compile()