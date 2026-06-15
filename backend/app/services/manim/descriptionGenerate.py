from langchain_core.messages import (
    SystemMessage, 
    HumanMessage
)
from app.schema.ServiceSchema import (
    DescriptionGenerationState, 
    DetailDescription, 
    CheckDetailedDescription
)
from langchain_core.prompts import ChatPromptTemplate
from app.core.llm import (
    llmPro, 
    llmFlash
)
from dotenv import load_dotenv
from langchain_core.tools import tool
from langgraph.graph import END
from pydantic import ValidationError
from app.core.internalServerErrorHandle import retry
import logging
from app.schema.ServiceSchema import AnimationType 
from app.services.manim.animationTypes import (
    COMPUTER_DATASTRUCTURE,
    GRAPH2D,
    GRAPH3D,
    STATISTICS,
    PHYSICS,
    TEXT,
)
ANIMATION_MAP = {
    AnimationType.GRAPH2D: GRAPH2D,
    AnimationType.COMPUTER_DATASTRUCTURE: COMPUTER_DATASTRUCTURE,
    AnimationType.GRAPH3D: GRAPH3D,
    AnimationType.STATISTICS: STATISTICS,
    AnimationType.PHYSICS: PHYSICS,
    AnimationType.TEXT: TEXT,
}

load_dotenv()


validation = """
**VALIDATION CRITERIA:**

**1. COMPLETENESS:**
- Every object has an identity and color. Size/scale and font_size where they're meaningful (text, shapes) — not required for things like computed paths or curves.
- Positioning is specified either relationally ("top-left", "below title", "point (2,4) on axes") OR with coordinates — both are acceptable.
- Each step has an animation type and approximate duration.
- Derived values (angles, intersections) include the computed result.

**2. IMPLEMENTATION FEASIBILITY:**
- Each step maps to a clear Manim action.
- The sequence is logical and ordered.
- Nothing required by the user's request is missing.
"""



async def generateDetailedDescription(state: DescriptionGenerationState):
    logging.info("--- NODE RUNNING: generateDetailedDescription ---")
    print("\n******Generating detailed description ********\n")
    animationTypeRule = ANIMATION_MAP.get(state.animationType)
    userQuery = state.userQuery
    
    systemPrompt = """
You are a Manim v0.20+ Animation Planner. Convert the user's request into a complete, step-by-step scene description. Output a DESCRIPTION ONLY — no Manim code, syntax, or function names.

## RULES
1. Target Manim v0.20+.
2. Integers for axes/positions/labels unless decimals are required; if so, 2 decimal places.
3. No overlaps — keep ≥1 unit spacing between all objects and text.
4. Background black unless the user specifies otherwise.
5. Each step must specify: WHAT the object is, its color, size/scale, font + font_size (for text), and the animation type + approximate duration.
6. POSITIONING — prefer RELATIONSHIPS over absolute coordinates:
   - Describe placement relationally: "centered", "top-left corner", "below the title", "to the right of the axes", "along the x-axis from 0 to 5".
   - Give absolute (x,y)/(x,y,z) coordinates ONLY for points that are mathematically meaningful (a plotted data point, a graph origin, a vector endpoint). Let the coder handle pixel placement.
   - For anything mapped onto axes, describe it in DATA coordinates ("the point (2, 4) on the axes"), not screen coordinates.
7. MATH — when a value is derived (an angle, an intersection, a velocity), give BOTH the formula and the computed result (e.g. "refracted angle = arcsin(n1·sin(θi)/n2) ≈ 28.13°") so the coder can verify rather than guess.
8. Logos: If the user requests a logo without explicitly specifying "3D", assume it is a 2D logo and use standard 2D shapes (Circle, Rectangle, Polygon) instead of 3D objects.
9. Always explicitly state in Step 1: the background color, and whether axes are shown or hidden — even when using defaults (black background, no axes). This pre-empts validator objections.
10. COLORS: ONLY use standard Manim color names (e.g., BLUE, RED, YELLOW, TEAL, ORANGE, PURPLE, GREEN, BLUE_E). NEVER use generic or undefined names like LIGHT_BLUE, DARK_BLUE, or LIGHT_RED.

## ANIMATION TYPE RULES (these tell the downstream coder the correct v0.20 constructs to use; you describe the visual intent, these ensure correct syntax)
{animationTypeRule}

## OUTPUT FORMAT
- Use "Step N:" for each step.
- Be concrete — never "place somewhere" or "make visible."
- Describe only; no code.

### Example
Step 1: Place a NumberPlane at (0,0), x_range -5 to 5, y_range -3 to 3. Background black.
Step 2: Write 'ax^2 + bx + c = 0' at (0,2), font_size 64, white, over 2 seconds.
Step 3: Move 'c' to (3,2) via transform over 2 seconds.
"""


    
    prompt = ChatPromptTemplate.from_messages([
        ("system", systemPrompt),
        ("human", "{input}"),
    ])

    chain = prompt | llmFlash.with_structured_output(DetailDescription)

    try:
        result = await retry(
            chain,
            {
                "input": userQuery,
                "animationTypeRule":animationTypeRule,
                "validation":validation
            },
            retries=3,
            delay=1
        )
        # print(result.content)
        print(f"\n[DESCRIPTION_GENERATED]:\n{result.description}\n")
        return state.model_copy(update={
            "detailedDescription": result.description
        })
    except (ValidationError, RuntimeError) as err:
        logging.exception("generateDetailedDescription failed")
        raise




def validateDescription(state: DescriptionGenerationState):
    """ This function checks the description, 
    if the description is correct then True otherwise False """
    logging.info("--- NODE RUNNING: validateDescription ---")
    print("\n******Checking is this Correct or not ********\n")
    detailedDescription = state.detailedDescription
    userQuery = state.userQuery
    animationTypeRule = ANIMATION_MAP.get(state.animationType)
    structured_llm = llmFlash.with_structured_output(CheckDetailedDescription)
    
    system_prompt = """
You are a Manim v0.20+ description validator. Check whether the description (a) matches the user's original request and (b) is complete enough to implement. Do NOT check code or syntax.

## COMPLETENESS CRITERIA
{validation}

## ANIMATION TYPE RULES
{animationTypeRule}

## DESCRIPTION
{detailedDescription}

## USER REQUEST
{userQuery}

## TASK
Return TRUE if a Manim coder could build a scene that satisfies the user's core request from this description. Be LENIENT — minor unspecified details (exact point counts, a color shade, a duration ±1s) are NOT failures; the coder fills those with sensible defaults.

Return FALSE only if:
- A KEY element the user explicitly asked for is entirely absent (not just unstated-as-a-default), OR
- The description clearly contradicts the request, OR
- A step is genuinely impossible to interpret.

Do NOT fail a description for: missing exact coordinates, missing point counts, unstated defaults (e.g. "no axes" is the default — absence of axes instructions is fine), or a missing duration on one step.
If FALSE, list ALL real blocking issues at once. Default to TRUE when unsure.
"""

    messages = [
        SystemMessage(content=system_prompt.format(
            detailedDescription=detailedDescription,
            userQuery=userQuery,
            animationTypeRule=animationTypeRule,
            validation=validation
        )),
        HumanMessage(content="Validate this description for Manim implementation.")
    ]
    
    try:
        result = structured_llm.invoke(messages)
        logging.info("VALIDATE_DESCRIPTION result=%s refine_count=%s", result.isThisGoodDescrription, state.descriptionRefine)
        print("Description Error: ", result.detailedDescriptionError)
        
        return state.model_copy(update={
            "isGood": result.isThisGoodDescrription,
            "detailedDescriptionError": result.detailedDescriptionError,
        })

    except (ValidationError, ValueError) as e:
        logging.exception("CheckPickedDescription parsing failed")
        raise



async def refineDescription(state: DescriptionGenerationState):
    logging.info("--- NODE RUNNING: refineDescription ---")
    print("\n**** refineDescription *****\n")
    animationTypeRule = ANIMATION_MAP.get(state.animationType)

    userQuery = state.userQuery
    description = state.detailedDescription
    detailedDescriptionError = state.detailedDescriptionError or "No specific error provided."
    descriptionRefine = state.descriptionRefine + 1
    
    systemPrompt = """
You are a Manim v0.20+ description refiner. Revise the description so it satisfies ALL validation rules in one pass — fix the reported errors AND re-check every step against the full rules, so nothing else is left incomplete.

## COMPLETENESS CRITERIA
{validation}

## ANIMATION TYPE RULES
{animationTypeRule}

## INPUTS
- Current Description: {description}
- Reported Errors: {detailedDescriptionError}
- User Request: {userQuery}

## OUTPUT FORMAT
- "Step N:" format, description only (no code).
- Each step specifies: identity, color, size, font_size (text), animation type + duration, and placement (relational or, where mathematically meaningful, coordinates).
- Prefer relational placement; give coordinates only for meaningful points.
- Titles aligned to top, scaled to fit. Keep ≥1 unit spacing.
"""


    humanMessage = "Refine the description to fix the validation errors. You will be provided with the CURRENT DESCRIPTION and the VALIDATION ERRORS TO FIX"
    prompt = ChatPromptTemplate.from_messages([
        ("system", systemPrompt),
        ("human", "{input}"),
    ])

    chain = prompt | llmFlash.with_structured_output(DetailDescription)
    try:
        result = await retry(
            chain,
            {
                "detailedDescriptionError":detailedDescriptionError,
                "description":description,
                "input": humanMessage,
                "animationTypeRule":animationTypeRule,
                "validation":validation,
                "userQuery":userQuery
            },
            retries=3,
            delay=1
        )
        print(f"\n[DESCRIPTION_REFINED] (Attempt {descriptionRefine}):\n{result.description}\n")
        return state.model_copy(update={
            "detailedDescription": result.description,
            "descriptionRefine": descriptionRefine,
        })
    except (ValidationError, ValueError) as e:
        logging.exception("refineDescription failed")
        raise

def router(state: DescriptionGenerationState) -> str:
    if state.isGood is True:
        return "END"
    elif state.descriptionRefine >= 2:
        return "END"
    else: 
        return "refineDescription"

