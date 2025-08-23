from langgraph.graph import StateGraph, START, END
from schema import mainmState
from manimCodeGeneration import agent_check_file_code, agent_create_file, agent_re_write_manim_code, agent_run_manim_code, manimRouter,executionRouter, should_start_over_router, handle_failure_and_reset

graph_build = StateGraph(mainmState)

graph_build.add_node("agent_create_file", agent_create_file)
graph_build.add_node("agent_check_file_code", agent_check_file_code)
graph_build.add_node("agent_re_write_manim_code", agent_re_write_manim_code)
graph_build.add_node("agent_run_manim_code", agent_run_manim_code)
graph_build.add_node("handle_failure_node", handle_failure_and_reset)


graph_build.add_edge(START, "agent_create_file")
graph_build.add_edge("agent_create_file", "agent_check_file_code")
graph_build.add_edge("agent_re_write_manim_code", "agent_check_file_code")

graph_build.add_conditional_edges(
    "agent_check_file_code",
    manimRouter,
    {
        "agent_run_manim_code": "agent_run_manim_code",
        "agent_re_write_manim_code": "agent_re_write_manim_code",
        END: "handle_failure_node",
    },
)

graph_build.add_conditional_edges(
    "agent_run_manim_code",
    executionRouter,
    {
        "fix": "agent_re_write_manim_code",        
        "done": END, 
        "limit": "handle_failure_node",
    },
)

graph_build.add_conditional_edges(
    "handle_failure_node",
    should_start_over_router,
    {
        "agent_create_file": "agent_create_file", 
        END: END,
    },
)

graph_for_mainm_code_generate = graph_build.compile()