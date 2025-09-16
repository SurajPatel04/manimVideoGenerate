from app.core.llm import llmFlash
from langchain_core.messages import (
    AIMessage, 
    SystemMessage, 
    HumanMessage
)
from pydantic import ValidationError
from app.schema.ServiceSchema import isQueryPossible,CodeGenPossibility
import logging
def isQuery(state: isQueryPossible):
    userQuery = state.userQuery
    print("\n\n\n Checking User Query \n\n\n")
    structuredLlm = llmFlash.with_structured_output(CodeGenPossibility)
    systemPrompt = """
You are a meticulous and highly analytical 'Manim Feasibility Expert'. Your primary goal is to provide a structured, accurate assessment of a user's request for a video animation based on the capabilities of the Python Manim library.

Step 1: Understand Your Role and Constraints**
You must strictly adhere to the known capabilities and limitations of Manim.
Capabilities:Mathematical animations (graphs, equations, geometry), algorithm visualization, text/LaTeX manipulation, and object transformations.

Limitations:No photorealism, no complex character animation, no external assets (logos, specific images)

Step 2: Provide Final Output**
After your internal analysis, your final output MUST be a single, raw JSON object and nothing else. Do not include your chain of thought or any other conversational text in the final response.

The JSON object must conform to this exact structure:
{
  "isFesible": <boolean>,
  "reason": "<string>",
  "chatName": "<string>"
}

- `isFeasible`: `true` if the core request is achievable, otherwise `false`.
- `reason`: A single, clear sentence explaining the verdict.
- `chatName`: Provide a short chat name 
"""

    msg = [
        SystemMessage(content=systemPrompt),
        HumanMessage(content=userQuery)
    ]

    try:
        result = structuredLlm.invoke(msg)
        print(f"isFesible {result.isFesible} \n reason: {result.reason} \n chatName: {result.chatName}")
        
        updated_state = state.model_copy(update={
            "isFesible":result.isFesible,
            "reason": result.reason,
            "chatName": result.chatName,
        })
        return updated_state
    except (ValidationError, RuntimeError) as err:
        print(f"DEBUG: Exception in feasibility check: {err}")
        logging.exception("isUserQueryPossible failed", err)
        raise
