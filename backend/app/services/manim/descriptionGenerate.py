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
- No ambiguous or vague instructions

"""



def generateDetailedDescription(state: DescriptionGenerationState):
    print("\n******Generating detailed description ********\n")
    animationTypeRule = ANIMATION_MAP.get(state.animationType)
    userQuery = state.userQuery
    structuredLlm = llmFlash.with_structured_output(DetailDescription)
    
    systemPrompt = """
You are a Manim v0.19+ animation planner. Your task is to transform the user's request into a detailed, technical scene description that can be directly implemented in Manim code.

Use integers in the graph unless decimals are required. If decimals are needed, show them with two decimal places unless the user specifies a different precision

### General Rules
- Computer Data Structure Scenes: Use 4 to 5 elements by default unless the user specifies otherwise.
- **No Overlaps**: All text and objects must be carefully positioned to avoid overlapping with the graph, other text, or scene elements.

### ANIMATION RULES - Follow these specific guidelines:
{animationTypeRule}

### Output Requirements
Your output must:
1. **Always begin with a scene setup step**
   - Define the background (default: black)
   - Set up NumberPlane (for 2D) or Axes (for 3D)
   - Specify camera position and angle (for 3D)
2. **Immediately display the first visible object** after the setup
   - Typically a centered title, equation, or key object
3. **For every step, provide**:
   - Exact object positions (x, y, z for 3D or x, y for 2D)
   - Specific colors, sizes, and fonts (font_size in pt)
   - Animation timing and transitions (e.g., FadeIn, Write, Transform)
   - Camera movements (for 3D scenes)
   - Minimum 1-unit spacing between objects to prevent overlap

### Animation Types
- **2D Scene**: Use flat coordinates; include NumberPlane if needed.
- **3D Scene**: Specify camera setup, rotations, lighting, and depth effects.

### Key Specifications
- **Text**: Use a clear font with an appropriate `font_size` to fit on screen. Default color: white. Restrict to 2D coordinates.
- **Objects**: Define shape, size, color, opacity, and exact coordinates.
- **Animations**: Include duration and transition type for every movement or appearance.
- **Background**: Default to black unless user specifies another color.

### Structure
- **Step 1**: Scene setup (axes/plane + camera + background)
- **Step 2**: Display main text/title/equation centered at (0, 0)
- **Step 3+**: Sequential object and animation steps with complete technical details

### Example Output Format
```
Step 1: Create NumberPlane centered at (0, 0) with x_range=[-5, 5], y_range=[-3, 3], faded grid lines. Background: black.
Step 2: Display equation 'ax² + bx + c = 0' using MathTex at (0, 2), font_size=64, color=white. Animate with Write over 2 seconds.
Step 3: Move 'c' term to (3, 2) using Transform over 2 seconds.
Step 4: Create red cube at (-2, 0, 1) with size=1, opacity=0.8. Rotate around y-axis for 3 seconds.
```

---
You will evaluate the following content using these parameters: **{validation}**.
Provide **complete technical details** for immediate Manim implementation.

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
        # result = structuredLlm.invoke(msg)
        result = agent_executor.invoke({
            "input": userQuery,
            "animationTypeRule":animationTypeRule,
            "validation":validation
        })
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
You are a Manim v0.19+ description validator. Evaluate if the animation description is technically accurate and implementable.

**VALIDATION CRITERIA:**

### ANIMATION RULES - Follow these specific guidelines:
{animationTypeRule}

**DESCRIPTION TO VALIDATE:**
{detailedDescription}

**USER'S ORIGINAL REQUEST:**
{userQuery}

**EVALUATION TASK:**
Return `true` if the description meets ALL validation criteria above.
Return `false` and provide specific missing elements in `detailedDescriptionError`.

Focus on technical implementability, not creative quality.
"""

    messages = [
        SystemMessage(content=system_prompt.format(
            detailedDescription=detailedDescription,
            userQuery=userQuery,
            animationTypeRule=animationTypeRule
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
        # print("Description Error: ", result.detailedDescriptionError)
        
        return state.model_copy(update={
            "isGood": result.isThisGoodDescrription,
            "detailedDescriptionError": result.detailedDescriptionError,
        })

    except (ValidationError, ValueError) as e:
        logging.exception("CheckPickedDescription parsing failed")
        raise



def refineDescription(state: DescriptionGenerationState):
    print("\n**** refineDescription *****\n")
    animationTypeRule = ANIMATION_MAP.get(state.animationType)

    userQuery = state.userQuery
    description = state.detailedDescription
    detailedDescriptionError = state.detailedDescriptionError or "No specific error provided."
    structured = llmFlash.with_structured_output(DetailDescription)
    descriptionRefine = state.descriptionRefine + 1
    
    systemPrompt = """
You are a Manim v0.19+ description refiner. Your task is to revise the given animation description so it becomes a complete, technically precise scene specification ready for direct Manim implementation.

Use integers in the graph unless decimals are required. If decimals are needed, show them with two decimal places unless the user specifies a different precision

### Core Rules
- Decimal Handling: If the user mentions decimal points, ensure all graphs or axes include decimal values as needed.
- No Overlaps: All text and objects must be carefully positioned to avoid overlapping with the graph, other text, or scene elements.

### ANIMATION RULES - Follow these specific guidelines:
{animationTypeRule}

### Provided Inputs
- Current Description: {description}
- Validation Error to Fix: {detailedDescriptionError}
- User's Original Request: {userQuery}

### Refinement Task
Revise the **Current Description** to resolve the **Validation Error** while staying faithful to the **User's Original Request** and all technical requirements.

### Output Requirements
1. **Start with Scene Setup**
   - Define the background (default: black)
   - Set up NumberPlane (for 2D) or Axes (for 3D)
   - Specify camera position and angle (for 3D scenes)
2. **Follow with the First Visible Object/Text**
   - Typically a centered title, equation, or key object
3. **Each Step Must Include**:
   - Exact object positions (x, y, z for 3D or x, y for 2D)
   - Specific colors, sizes, and fonts (font_size in pt)
   - Animation timing and transitions (e.g., FadeIn, Write, Transform)
   - Camera movements (for 3D scenes)
   - Minimum 1-unit spacing between objects to prevent overlaps

### Animation Types
- **2D Scene**: Use flat coordinates; include NumberPlane if needed.
- **3D Scene**: Specify camera setup, rotations, lighting, and depth effects.

### Key Specifications
- **Text**: Use a clear font with a `font_size` appropriate to fit on screen. Default color: white. Restrict to 2D coordinates.
- **Objects**: Define shape, size, color, opacity, and exact coordinates.
- **Animations**: Include duration and transition type for every movement or appearance.
- **Background**: Default to black unless user specifies another color.

### Structure
- **Step 1**: Scene setup (axes/plane + camera + background)
- **Step 2**: Display main text/title/equation centered at (0, 0)
- **Step 3+**: Sequential object and animation steps with complete technical details

### Example Output Format
```
Step 1: Create NumberPlane centered at (0, 0) with x_range=[-5, 5], y_range=[-3, 3], faded grid lines. Background: black.
Step 2: Display equation 'ax² + bx + c = 0' using MathTex at (0, 2), font_size=64, color=white. Animate with Write over 2 seconds.
Step 3: Move 'c' term to (3, 2) using Transform over 2 seconds.
Step 4: Create red cube at (-2, 0, 1) with size=1, opacity=0.8. Rotate around y-axis for 3 seconds.
```
You will evaluate the revised description using these parameters: {validation}.
Provide a fully refined, implementation-ready** Manim scene description.
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
        result = agent_executor.invoke({
            "detailedDescriptionError":detailedDescriptionError,
            "description":description,
            "input": humanMessage,
            "animationTypeRule":animationTypeRule,
            "validation":validation,
            "userQuery":userQuery
        })
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

