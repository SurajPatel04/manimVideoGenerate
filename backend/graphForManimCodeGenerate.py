from langgraph.graph import StateGraph, START, END
from schema import mainmState
from manimCodeGeneration import agent_check_file_code, agent_create_file, agent_re_write_manim_code, agent_run_manim_code, manimRouter,executionRouter

graph_build = StateGraph(mainmState)

# creating node 
graph_build.add_node("agent_check_file_code", agent_check_file_code)
graph_build.add_node("agent_create_file", agent_create_file)
graph_build.add_node("agent_run_manim_code", agent_run_manim_code)
graph_build.add_node("agent_re_write_manim_code", agent_re_write_manim_code)


# In your graph definition script

# 1. Create the new router node
graph_build.add_node("execution_router", executionRouter)

# 2. Adjust the edges
# The initial part of your graph remains the same...
graph_build.add_edge(START, "agent_create_file")
graph_build.add_edge("agent_create_file", "agent_check_file_code")
graph_build.add_conditional_edges(
    "agent_check_file_code",
    manimRouter,
    {
        "agent_run_manim_code": "agent_run_manim_code",
        "agent_re_write_manim_code": "agent_re_write_manim_code",
        END: END
    }
)
graph_build.add_edge("agent_re_write_manim_code", "agent_check_file_code")

# 3. Connect agent_run_manim_code to the new router instead of END
graph_build.add_conditional_edges(
    "agent_run_manim_code",
    executionRouter,
    {
        "fix": "agent_re_write_manim_code",
        END: END
    }
)

# Compile the graph
graph_for_mainm_code_generate = graph_build.compile()

graph_for_mainm_code_generate = graph_build.compile()