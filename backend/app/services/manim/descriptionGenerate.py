from langchain_core.messages import (
    AIMessage, 
    SystemMessage, 
    HumanMessage
)
from app.schema.ServiceSchema import (
    DescriptionGenerationState, 
    GenDescriptions, 
    DetailDescription, 
    CheckDetailedDescription, 
    CodeGenPossibility
)
from langchain.agents import (
    create_tool_calling_agent,
    AgentExecutor
)
from langchain_core.prompts import (
    ChatPromptTemplate,
    MessagesPlaceholder
)
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
)
ANIMATION_MAP = {
    AnimationType.GRAPH2D: GRAPH2D,
    AnimationType.COMPUTER_DATASTRUCTURE: COMPUTER_DATASTRUCTURE,
    AnimationType.GRAPH3D: GRAPH3D,
    AnimationType.STATISTICS: STATISTICS,
    AnimationType.PHYSICS: PHYSICS,
}

load_dotenv()


validation = """
**VALIDATION CRITERIA:**

**1. TECHNICAL COMPLETENESS:**
- Specific object positions (coordinates given)
- Exact colors, sizes, and fonts specified
- Animation timing and durations provided
- Clear step-by-step sequence

**2. IMPLEMENTATION FEASIBILITY:**
- Each step can be directly translated to Manim code
- Animation sequence is logical and flows well
- All required parameters are specified

"""



async def generateDetailedDescription(state: DescriptionGenerationState):
    print("\n******Generating detailed description ********\n")
    animationTypeRule = ANIMATION_MAP.get(state.animationType)
    userQuery = state.userQuery
    structuredLlm = llmFlash.with_structured_output(DetailDescription)
    
    systemPrompt = """
You are a **Manim v0.19+ Animation Planner**.
Your task: Convert the user’s request into a **complete, step-by-step scene description**.

**Important:** Only provide detailed scene descriptions. **Do not write Manim code, syntax, or functions.**

---

## Rules (all must be followed)

1. Use **Manim v0.19+ assumptions**.
2. Always use **integers** for axes, positions, and labels unless decimals are required. If decimals are needed, use **two decimal places**.
3. Ensure **no overlaps**: All objects and text must have at least **1 unit spacing**.
4. Background is **black**, unless otherwise specified.
5. Every step must specify:

   * Exact **position** (x,y) or (x,y,z)
   * **Color**
   * **Size or scale**
   * **Font and font_size** (if text)
   * **Animation type** and duration
   * **Camera moves** (if 3D)

---

## Animation Type Rules

{animationTypeRule}

---

## Output Format

* Always use **Step N:** format.
* Avoid vague descriptions like “place somewhere” or “make visible.”
* Only provide **detailed scene descriptions**.
* Include every necessary detail for rendering the scene accurately.

### Example

Step 1: Place a NumberPlane at coordinates (0,0) with x_range from -5 to 5 and y_range from -3 to 3. Background color: black. 
Step 2: Show the text 'ax² + bx + c = 0' at position (0,2), font='Arial', font_size=64, color=white, opacity=1. Animate the writing of the text over 2 seconds. 
Step 3: Move the character 'c' to position (3,2) using a transformation animation over 2 seconds. 
Step 4: Place a red cube at coordinates (-2,0,1), size 1, opacity 0.8. Rotate the cube around the y-axis for 3 seconds.
"""

    # msg = [
    #     SystemMessage(content=systemPrompt.format(
    #         animationTypeRule=animationTypeRule,
    #         validation=validation,
    #     )),
    #     HumanMessage(content=userQuery),
    # ]
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", systemPrompt),
        ("human", "{input}"),
        MessagesPlaceholder(variable_name="agent_scratchpad")
    ])

    agent = create_tool_calling_agent(llmFlash, tools=[],prompt=prompt)
    agent_executor = AgentExecutor(agent=agent,tools=[],verbose=True, max_iterations=3)

    try:
        result = await retry(
            agent_executor,
            {
                "input": userQuery,
                "animationTypeRule":animationTypeRule,
                "validation":validation
            },
            retries=3,
            delay=1
        )
        # print(result.description)
        return state.model_copy(update={
            "detailedDescription": result.get("output", "")
        })
    except (ValidationError, RuntimeError) as err:
        logging.exception("generateDetailedDescription failed", err)
        raise




def validateDescription(state: DescriptionGenerationState):
    """ This function checks the description, 
    if the description is correct then True otherwise False """
    print("\n******Checking is this Correct or not ********\n")
    detailedDescription = state.detailedDescription
    userQuery = state.userQuery
    animationTypeRule = ANIMATION_MAP.get(state.animationType)
    structured_llm = llmFlash.with_structured_output(CheckDetailedDescription)
    
    system_prompt = """
You are a **Manim v0.19+ description validator**.
Your task: Check if the description matches the **user’s original request** and is **technically implementable** under Manim v0.19+.

---

## Validation Rules

{validation}

## Animation Type Rules

{animationTypeRule}

---

## Description to Validate

{detailedDescription}

## User’s Original Request

{userQuery}

---

## Task

* Return `true` if the description matches the **user’s query** and includes all necessary elements for implementation.
* Return `false` if any required element is missing or does not match the user request.
* **Do not check Manim syntax or code correctness.**
* If `false`, list **all discrepancies or missing elements** inside `detailedDescriptionError`, not just one.

  * Example:
        Step 3: Text object missing font specification.
        Step 4: Animation duration for movement not provided.

Focus only on **matching the user request and completeness**, ignoring any code or syntax concerns.

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
    
    nextStage = ""
    try:
        result = structured_llm.invoke(messages)
        # print("Description is good or not: ", result.isThisGoodDescrription)
        if result.isThisGoodDescrription:
            nextStage = "createFileAndWriteMainmCode"
        else:
            nextStage = "refineDescription"
        print("Description Error: ", result.detailedDescriptionError)
        
        return state.model_copy(update={
            "isGood": result.isThisGoodDescrription,
            "detailedDescriptionError": result.detailedDescriptionError,
        })

    except (ValidationError, ValueError) as e:
        logging.exception("CheckPickedDescription parsing failed")
        raise



async def refineDescription(state: DescriptionGenerationState):
    print("\n**** refineDescription *****\n")
    animationTypeRule = ANIMATION_MAP.get(state.animationType)

    userQuery = state.userQuery
    description = state.detailedDescription
    detailedDescriptionError = state.detailedDescriptionError or "No specific error provided."
    structured = llmFlash.with_structured_output(DetailDescription)
    descriptionRefine = state.descriptionRefine + 1
    
    systemPrompt = """
You are a **Manim v0.19+ description refiner**.
Your task: Revise the given description so it satisfies **all validation rules** in one pass.

Do not just fix the listed errors. Instead:

* Apply the reported errors **AND** double-check every step against the full validation rules.
* Ensure the final output is **implementation-ready** in Manim with no missing details.

---

## Validation Rules

{validation}

## Animation Type Rules

{animationTypeRule}

---

## Inputs

* Current Description: {description}
* Reported Errors: {detailedDescriptionError}
* User’s Request: {userQuery}

---

## Output Format

* Step-by-step description (Step 1, Step 2, …).
* Each step must specify: position, color, size, font, font_size, opacity, animation type + duration.
* Titles must be aligned (to_edge(UP)) and scaled properly.
* Maintain ≥1 unit spacing.
* Only output **textual description** (never code or syntax).

### Example (Textual Description Only)


Step 1: Place a NumberPlane at coordinates (0,0) with x_range from -5 to 5 and y_range from -3 to 3. Background color: black. 
Step 2: Show the text 'ax² + bx + c = 0' at position (0,2), font='Arial', font_size=64, color=white, opacity=1. Animate the writing of the text over 2 seconds. 
Step 3: Move the character 'c' to position (3,2) using a transformation animation over 2 seconds. 
Step 4: Place a red cube at coordinates (-2,0,1), size 1, opacity 0.8. Rotate the cube around the y-axis for 3 seconds.

"""

    # messages = [
    #     SystemMessage(content=systemPrompt.format(
    #         description=description,
    #         detailedDescriptionError=detailedDescriptionError,
    #         userQuery=userQuery,
    #         animationTypeRule=animationTypeRule,
    #         validation=validation,
    #     )),
    #     HumanMessage(content="Refine the description to fix the validation errors. You will be provided with the CURRENT DESCRIPTION and the VALIDATION ERRORS TO FIX")
    # ]
    humanMessage = "Refine the description to fix the validation errors. You will be provided with the CURRENT DESCRIPTION and the VALIDATION ERRORS TO FIX"
    prompt = ChatPromptTemplate.from_messages([
        ("system", systemPrompt),
        ("human", "{input}"),
        MessagesPlaceholder(variable_name="agent_scratchpad")
    ])

    agent = create_tool_calling_agent(llmFlash,tools=[] ,prompt=prompt)
    agent_executor = AgentExecutor(agent=agent,tools=[],verbose=True, max_iterations=3)
    try:
        # result = structured.invoke(messages)
        # print(f"Refinement attempt #{descriptionRefine}")
        # print(f"Refined description: {result.description}")
        # result = agent_executor.invoke({
        #     "detailedDescriptionError":detailedDescriptionError,
        #     "description":description,
        #     "input": humanMessage,
        #     "animationTypeRule":animationTypeRule,
        #     "validation":validation,
        #     "userQuery":userQuery
        # })
        result = await retry(
            agent_executor,
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
        return state.model_copy(update={
            "detailedDescription": result.get("output", ""),
            "descriptionRefine": descriptionRefine,
        })
    except (ValidationError, ValueError) as e:
        logging.exception("refineDescription failed", e)
        raise

def router(state: DescriptionGenerationState) -> str:
    if state.isGood is True:
        return "END"
    elif state.descriptionRefine >= 10:
        return "END"
    else: 
        return "refineDescription"

