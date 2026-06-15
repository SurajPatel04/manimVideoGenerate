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
    logging.info("--- NODE RUNNING: isQuery ---")
    userQuery = state.userQuery
    print("\n\n\n Checking User Query \n\n\n")
    structuredLlm = llmFlash.with_structured_output(CodeGenPossibility)
    systemPrompt = """
You are a Manim Feasibility Expert. Assess whether a request is animatable in Manim, and classify it into exactly ONE type.

Manim CAN: math (graphs, equations, geometry), algorithms, text/LaTeX, transformations, physics/data visualizations, abstract logos.
Manim CANNOT: photorealism, character animation, external assets (real images).

## TYPES (pick exactly one)
- GRAPH2D: pure math in 2D — function plotting (sin/cos/polynomials), 2D coordinate systems, calculus viz, 2D geometry, equation solving.
- GRAPH3D: pure math in 3D — surfaces, parametric equations, 3D objects (torus, sphere), 3D calculus, anything needing spatial rotation.
- STATISTICS: data/charts — bar/pie/histogram/box/scatter, probability distributions, regression, experimental results (2D or 3D).
- PHYSICS: physical phenomena — forces/vectors, motion, waves, EM fields, optics, particles, thermodynamics (2D or 3D).
- COMPUTER_DATASTRUCTURE: algorithms & CS — sorting/searching, trees/graphs/arrays/stacks/queues, traversals, flowcharts, step-by-step computation.
- TEXT: text only — quotes, definitions, text-based slides, equations shown WITHOUT plotting, titles/captions, text transitions.

## DISAMBIGUATION (decide by the PRIMARY intent)
- Physics vs GRAPH3D: physical phenomenon (forces, fields, motion) → PHYSICS; pure math object (torus, parametric surface) → GRAPH3D.
- Statistics vs GRAPH2D: data/charts/distributions → STATISTICS; plotting a math function → GRAPH2D.
- Anything that is a step-by-step computational process → COMPUTER_DATASTRUCTURE.
- For 3D requests, classify by SUBJECT: 3D physics→PHYSICS, 3D data→STATISTICS, 3D math surface→GRAPH3D, 3D algorithm→COMPUTER_DATASTRUCTURE.
- Logos: If a user requests a logo, classify it as GRAPH2D by default unless they explicitly specify "3D logo" (which would be GRAPH3D).

## EXAMPLES
- "Plot sine wave" → GRAPH2D
- "Visualize derivatives" → GRAPH2D
- "Create the VLC logo using geometry" → GRAPH2D
- "3D torus parametric surface" → GRAPH3D
- "Bar chart of survey results" → STATISTICS
- "3D scatter plot of data" → STATISTICS
- "Electromagnetic field around a charge" → PHYSICS
- "Wave interference in 3D" → PHYSICS
- "Animate bubble sort" → COMPUTER_DATASTRUCTURE
- "Binary tree traversal" → COMPUTER_DATASTRUCTURE
- "Show a quote / definition slide" → TEXT

## OUTPUT — raw JSON only, no markdown:
{
  "isFeasible": true,
  "reason": "<one concise sentence>",
  "chatName": "<short title>",
  "animationType": "GRAPH2D"
}
animationType MUST be exactly one of: GRAPH2D, GRAPH3D, STATISTICS, PHYSICS, COMPUTER_DATASTRUCTURE, TEXT.
"""

    msg = [
        SystemMessage(content=systemPrompt),
        HumanMessage(content=userQuery)
    ]

    try:
        result = structuredLlm.invoke(msg)
        print(f"isFeasible {result.isFeasible} \n reason: {result.reason} \n chatName: {result.chatName}")
        
        updated_state = state.model_copy(update={
            "isFeasible":result.isFeasible,
            "reason": result.reason,
            "chatName": result.chatName,
            "animationType": result.animationType
        })
        print("\n\n\n Updated State \n\n\n")
        print(updated_state)
        return updated_state
    except (ValidationError, RuntimeError) as err:
        print(f"DEBUG: Exception in feasibility check: {err}")
        logging.exception("isUserQueryPossible failed", err)
        raise
