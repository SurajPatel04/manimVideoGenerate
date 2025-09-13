from langchain_core.messages import (
    AIMessage, 
    SystemMessage, 
    HumanMessage
)
from app.schema.ServiceSchema import (
    DescriptionGenerationState, 
    GenDescriptions, 
    DetailDescription, 
    CheckPickedDescription, 
    CodeGenPossibility
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

load_dotenv()

def isUserQueryPossible(state: DescriptionGenerationState):
    userQuery = state.userQuery
    print("\n\n\n Checking User Query \n\n\n")
    structuredLlm = llmFlash.with_structured_output(CodeGenPossibility)
    systemPrompt = """
You are a meticulous and highly analytical 'Manim Feasibility Expert'. Your primary goal is to provide a structured, accurate assessment of a user's request for a video animation based on the capabilities of the Python Manim library.

Step 1: Understand Your Role and Constraints**
You must strictly adhere to the known capabilities and limitations of Manim.
Capabilities:Mathematical animations (graphs, equations, geometry), algorithm visualization, text/LaTeX manipulation, and object transformations.

Limitations:No photorealism, no complex character animation, no external assets (logos, specific images)

Step 2: Follow a Chain of Thought (Internal Monologue)
For the user's query provided, first perform an internal analysis:
1.  Deconstruct: Break down the user's request into its core components and entities (e.g., objects, actions, concepts).
2.  Analyze: For each component, evaluate if it falls within Manim's capabilities or its limitations.
3.  Synthesize: Based on your analysis, form a final conclusion on the overall feasibility.
4.  Formulate: Craft a clear, concise reason and, if necessary, an actionable suggestion for the user.

Step 3: Provide Final Output**
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
        return state.model_copy(update={
            "isFesible":result.isFesible,
            "reason": result.reason,
            "chatName": result.chatName,
            "currentStage": "isUserQueryPossible",
            "nextStage": "generateDetailedDescription"
            })
    except (ValidationError, RuntimeError) as err:
        logging.exception("isUserQueryPossible failed", err)
        raise

def feasibilityRouter(state: DescriptionGenerationState):
    """
    Routes based on whether the user's query is feasible in Manim.
    """
    if state.isFesible is True:
        return "generateDetailedDescription"
    else:
        return "END"

# def generateMultipleDescription(state: DescriptionGenerationState):
#     """
#     Generates three animation descriptions using the model's structured output feature.
#     """
#     print("****** Generating Three Descriptions (Structured Output) ********\n")
#     user_query = state.user_query

#     structured_llm = llmFlash.with_structured_output(GenDescriptions)
#     system_prompt = """
# Your task is to generate **three candidate descriptions** that match the user's query.

# Each description should be:
# - Detailed
# - Clear
# - Technically descriptive
# - Written to be used later as input for generating **Manim** (Mathematical Animation Engine) code.
# """
#     msg = [
#         SystemMessage(content=system_prompt),
#         HumanMessage(content=user_query)
#     ]

#     try:
#         # 4. Invoke the structured chain. The result is a Pydantic object, not a string.
#         result = structured_llm.invoke(msg)
        
#         print(result.descriptions, "\n\n")
#         return state.model_copy(update={"descriptions": result.descriptions})

#     except Exception as e:
#         # This will now catch API errors or rare cases where the model fails
#         # to generate structured output despite the constraints.
#         logging.exception("Description generation with structured output failed")
#         raise

def generateDetailedDescription(state: DescriptionGenerationState):
    print("\n******Generating detailed description ********\n")
    userQuery = state.userQuery
    # contnet = state.descriptions
    structuredLlm = llmFlash.with_structured_output(DetailDescription)
#     system_prompt = f"""
# You are an expert technical writer and Manim script planner. Your task is to analyze three AI-generated animation concepts and produce one single, final, highly detailed description that is ready for a Manim coder to use. Ensure that all text and shapes are arranged clearly, with no overlaps And generate description for the 3d when user mention 3d.

# You will be given a user's query

# 1. Generate a full, step-by-step, technically-rich description of an animation based on the user’s input text. Include all necessary details to implement the animation.

# Animation Type:
# - The animation can be either 2D or 3D. Determine which type based on the user's request. 
# - If 2D: Describe flat shapes, 2D transformations (position, scale, rotation), and 2D effects (color changes, opacity, transitions).
# - If 3D: Describe 3D objects, geometry, extrusion, motion paths in 3D space, rotations along axes, 3D transformations, and effects like lighting, shadows, and camera movement.

# Requirements:
# 2. Include object details: shape, color, size, and effects.
# 3. Describe motion: translation, rotation, scaling, or deformation, and their timing.
# 4. Specify camera position, angles, movement, and zooms for 3D animations.
# 5. Suggest smooth transitions, scene composition, and timing for all elements.
# 6. Make it visually appealing and “cool”, suitable for rendering in a tool like Manim, Blender, or similar.
# 7. For text-based animations, include text formatting (color, font, extrusion for 3D) and animation style (fade, scale, move, rotate).

# **Output Requirements:**
# -   The output must be a complete, multi-step plan, not just a title or a summary.
# -   It must be technically descriptive (mentioning colors, positions, Manim animations like `Transform`, `FadeIn`, etc.).
# -   It must be precise and ready for a developer to turn into code.

# **Example of BAD output (What NOT to do):**
# "Description 1: Step-by-Step Derivation of the Quadratic Formula"

# **Example of GOOD output (What TO do):**
# "The animation will visually derive the quadratic formula...
# 1. Initial State: Display the equation `ax^2 + bx + c = 0`...
# 2. Isolate Constant Term: Animate `c` moving to the right...
# (and so on, providing the full detailed plan)"
# """
    systemPrompt = f"""
You are an expert technical writer and Manim script planner and ypur purpose is to transform a general animation idea highly detailed description that is ready for a Manim code to use, step-by-step description suitable for a Manim v0.19+ code generator.. Your task is to analyze Human query and produce detailed description, highly detailed description that is ready for a Manim coder to implement.Ensure that text and objects do not overlap. Ensure all text, shapes, and objects are arranged clearly with no overlaps, and provide full 3D instructions when requested and Important: In v0.19, there’s no built-in 3D text class—you must use 2d for writing text.  

Note: for the Text you only write x and y position not z position.

1. **Determine Animation Type**
- If the user specifies "3D" or requests a 3D animation, all objects must be positioned in a three-dimensional coordinate system (x, y, z) with depth.
- If 2D, use flat positions (x, y) only.
- For 3D animations, include camera position, movement, rotation, zoom, perspective, lighting, and shadows.

2. **Object Details**
- Specify shape (cube, sphere, text, polygon, etc.), size, color, opacity, extrusion (for 3D text), and other effects (glow, stroke, texture).
- Ensure spatial separation in 3D so objects do not overlap unintentionally.
- Include any hierarchy or grouping of objects if needed.

3. **Motion and Animation**
- Specify translations, rotations (including axis for 3D), scaling, deformation, and timing in seconds.
- Describe smooth transitions using Manim animations like `Transform`, `FadeIn`, `MoveAlongPath`, `Rotate`, `ScaleInPlace`, etc.
- For 3D, describe motion paths in 3D space explicitly (with coordinates), and rotations along x, y, z axes.

4. **Camera Instructions (3D only)**
- Provide initial camera position and target (look-at point).
- Include camera rotation, zoom, panning, and tracking of moving objects.
- Suggest perspective adjustments to maintain visibility of all elements.
- Ensure objects in the foreground and background are distinguishable using depth, scaling, or fade effects.

5. **Text Animations**
- Include exact text content, font, size, color, and 3D extrusion if in 3D.
- Specify animation style: fade, scale, move, rotate, or any combination.
- Position text clearly in space so it does not overlap other objects.

6. **Scene Composition**
- Arrange all elements for visual clarity and appeal.
- Include timing for each step (duration for each animation or transition).
- Suggest effects that enhance readability and make the animation visually “cool” and engaging.

**Output Requirements**
- Provide a complete, multi-step animation plan ready for coding in Manim.
- Include technical details: positions, sizes, colors, coordinates, animations, and timings.
- Do not produce just a title or summary.
- Ensure 3D objects are fully visible and properly spaced in the scene.

**Example of Good Output**
"The animation will visually derive the quadratic formula in 3D:  
1. Initial State: Display the equation `ax^2 + bx + c = 0` as 3D text at position (0, 0, 2) with blue extrusion. Camera starts at (10, -10, 10) looking at the origin.  
2. Isolate Constant Term: Animate `c` moving to the right along the x-axis over 2 seconds using `MoveAlongPath`.  
3. Factorization Step: Introduce a red cube of size 1 at position (-2, 0, 1) to represent `a`, rotating around y-axis.  
(and so on, step by step, with all positions, timings, rotations, and camera movements clearly specified)"
"""

    # system_prompt = f"""
    # You are an expert Manim script planner. Your task is to create a single, detailed, step-by-step technical plan for a Manim animation based on the user's query.

    # The plan must be precise and ready for a developer to implement directly. Ensure all visual elements are positioned to avoid overlap.

    # Your output MUST be the full, numbered, step-by-step plan. Do not provide summaries or conversational text.

    # **Example of Required Output:**
    # "1. Initial State: Display the equation `ax^2 + bx + c = 0` using MathTex at the top of the screen.
    # 2. Isolate Constant: Animate the `+ c` term transforming and moving to the right side to become `-c`.
    # 3. Divide by 'a': Show the entire equation being divided by 'a', with the 'a' appearing in the denominator of each term."
    # """
    msg = [
        SystemMessage(content=systemPrompt),
        HumanMessage(content=userQuery),
    ]
    try:
        result = structuredLlm.invoke(msg)
        print(result.description)
        return state.model_copy(update={
            "detailedDescription": result.description,
            "currentStage":"generateDetailedDescription",
            "nextStage": "validateDescription"
            })
    except (ValidationError, RuntimeError) as err:
        logging.exception("generateDetailedDescription failed", err)
        raise

def validateDescription(state: DescriptionGenerationState):
    """ This function checks the description, 
    if the description is correct then True otherwise False """
    print("\n******Checking is this Correct or not ********\n")
    pickedDescription = state.detailedDescription
    userQuery = state.userQuery

    
    structured_llm = llmFlash.with_structured_output(CheckPickedDescription)
    system_prompt = f"""
Evaluate if the candidate description is detailed and accurate enough to create a Manim animation for the user's query. Ensure that text and objects do not overlap

Respond `true` if it is good. Respond `false` and provide a concise reason in `detailedDescriptionError` if it is not.

Candidate Description:
{pickedDescription}

"""

    messages = [
        SystemMessage(content=system_prompt),
        HumanMessage(content=userQuery)
    ]
    nextStage = ""
    try:
        result = structured_llm.invoke(messages)
        print("Description is good or not: ",result.isThisGoodDescrription)
        if result.isThisGoodDescrription:
            nextStage="createFileAndWriteMainmCode"
        else:
            nextStage="refineDescription"
        print("Description Error: ", result.detailedDescriptionError)
        return state.model_copy(update={
            "isGood": result.isThisGoodDescrription,
            "detailedDescriptionError": result.detailedDescriptionError,
            "currentStage":"validateDescription",
            "nextStage": nextStage
        })

    except (ValidationError, ValueError) as e:
        logging.exception("CheckPickedDescription parsing failed")
        raise

def refineDescription(state: DescriptionGenerationState):
    print("**** refineDescription *****")
    userQuery = state.userQuery
    description = state.detailedDescription
    pickedDescriptionError = state.detailedDescriptionError or "No specific error provided."
    structured = llmFlash.with_structured_output(DetailDescription)
    descriptionRefine = state.descriptionRefine + 1
    systemPrompt = f"""
You are a helpful AI assistant that generates high-quality, technically accurate descriptions. These descriptions will be used to generate **Manim** (Mathematical Animation Engine) code.

You will be given:
- A user query
- One or more candidate descriptions
- The previous description's evaluation or error (if applicable)

Your task is to:
1. Decide whether any of the provided descriptions are suitable.
2. If one is suitable, select it.
3. If neither is sufficient, either:
   - Merge the descriptions into a better one, or
   - Create a new, clearer and more detailed version.
4. Ensure the final description is focused and technically accurate.

Requirements:
- The description must directly address the user's query.
- It must be precise and structured.
- Use specific details about:
  - Structure
  - Methods
  - Colors
  - Sizes
  - Animations (if applicable)
- Avoid vague or general language.

Output:
- A single, clear, and technically descriptive paragraph that is ready for Manim code generation.

Previous Description:
{description}


Description Evaluation / Error:
{pickedDescriptionError}
"""
    messages = [
        SystemMessage(content=systemPrompt),
        HumanMessage(content=userQuery),
    ]
    try:
        result = structured.invoke(messages)
        return state.model_copy(update={
            "detailedDescription":result.description,
            "descriptionRefine": descriptionRefine
            })
    except (ValidationError, ValueError) as e:
        logging.exception("CheckPickedDescription parsing failed", e)
        raise

def router(state: DescriptionGenerationState) -> str:
    if state.isGood is True:
        return "END"
    elif state.descriptionRefine >= 10:
        return "END"
    else: 
        return "refineDescription"

