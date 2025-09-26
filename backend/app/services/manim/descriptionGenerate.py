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



def generateDetailedDescription(state: DescriptionGenerationState):
    print("\n******Generating detailed description ********\n")
    userQuery = state.userQuery
    structuredLlm = llmFlash.with_structured_output(DetailDescription)
    
    systemPrompt = """
You are a Manim v0.19+ animation planner. Transform the user's request into a detailed, technical description ready for Manim code generation.
Note:
    Ensure that all text objects do not overlap with the graph, other text, or any other objects in the scene.

When generating Manim code for 3D scenes, ensure that all text and 3D objects fit comfortably on screen and remain readable during camera movement.

    Relative text size: Adjust font sizes proportionally. If there are many text elements, reduce their size so all remain balanced and readable.

    Fixed-frame text: Keep all descriptive text (titles, subtitles, equations, annotations) fixed to the frame using add_fixed_in_frame_mobjects(...) so it does not move with the 3D camera.
    
    
    Grouping and spacing: Group related text (such as multiple equations) in a VGroup and arrange them vertically with clear spacing.

    Title : Center the main title at the top of the frame, and center, and make sure the text is not too large
        
    Equations or other text in much smalle text size compare to title, write equation text below the title and shift them to the left or right (with enough spacing) so they don’t overlap the 3D object. 

    Margins: Always leave a comfortable margin between text and the frame edges.

    Graph scaling: Keep x, y, and z axis lengths proportional to maintain a balanced appearance of the 3D object.

    3D object centering: Place the 3D surface or graph so that its geometric center aligns with the origin (ORIGIN) and is fully visible inside the ThreeDAxes.

    Camera framing: Choose a camera orientation and distance that keeps the entire 3D object centered and clearly visible without cropping.

    Axes balance: If using ThreeDAxes, keep the axes centered around the origin to ensure the surface is balanced in the frame.

    LaTeX syntax: Use raw strings for LaTeX expressions, e.g. MathTex(r"x^2").


**OUTPUT REQUIREMENTS:**
- Always begin with a **scene setup step** (e.g., NumberPlane for 2D or Axes for 3D, background color, camera position).
- Always include the **first visible object/text** immediately after the setup (e.g., centered title or equation).
- Every step must specify:
  - Exact object positions (x, y, z for 3D or x, y for 2D)
  - Specific colors, sizes, and fonts
  - Animation timing and transitions
  - Camera movements (for 3D scenes)
  - Clear spacing to prevent overlaps

**ANIMATION TYPES:**
- **2D Scene**: Use flat coordinates, NumberPlane when needed
- **3D Scene**: Include camera position, rotations, lighting, depth

**KEY SPECIFICATIONS:**
-Text: Use a font_size appropriate to fit on the screen. In Manim, font_size is measured in point size (pt). Use white color and restrict to 2D positioning only.
- Objects: Define shape, size, color, opacity, and exact coordinates
- Animations: Include duration and transition type (FadeIn, Write, Transform, etc.)
- Spacing: Maintain at least 1 unit gap between objects to avoid overlaps
- Background: Default to black unless otherwise specified

**STRUCTURE:**
- Step 1: Scene setup (axes/plane + camera + background)
- Step 2: Display main text/title/equation centered at (0,0)
- Step 3+: Sequential object/animation steps with technical details

**EXAMPLE OUTPUT FORMAT:**
Step 1: Create NumberPlane centered at (0, 0) with x_range=[-5, 5], y_range=[-3, 3], faded grid lines. Background black.
Step 2: Display equation 'ax² + bx + c = 0' using MathTex at position (0, 2) with font_size=64, white color. Animate with Write over 2 seconds.
Step 3: Animate 'c' term moving right to position (3, 2) over 2 seconds using Transform.
Step 4: Create red cube at (-2, 0, 1) with size 1, opacity=0.8, rotating around y-axis for 3 seconds.

Provide complete technical details for immediate Manim implementation.
"""

    msg = [
        SystemMessage(content=systemPrompt),
        HumanMessage(content=userQuery),
    ]
    
    try:
        result = structuredLlm.invoke(msg)
        # print(result.description)
        return state.model_copy(update={
            "detailedDescription": result.description,
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

    structured_llm = llmFlash.with_structured_output(CheckDetailedDescription)
    
    system_prompt = """
You are a Manim v0.19+ description validator. Evaluate if the animation description is technically accurate and implementable.

**VALIDATION CRITERIA:**

**1. TECHNICAL COMPLETENESS:**
- Specific object positions (coordinates given)
- Exact colors, sizes, and fonts specified
- Animation timing and durations provided
- Clear step-by-step sequence

**2. MANIM v0.19+ COMPATIBILITY:**
- Uses correct object types (Text, MathTex, Circle, etc.)
- Specifies proper positioning methods (.move_to(), .next_to())
- Includes valid animation types (FadeIn, Transform, Create, etc.)
- Font sizes are reasonable (48+, not 1.5)

**3. LAYOUT VALIDATION:**
- No overlapping objects
- Objects stay within frame boundaries
- Proper spacing between elements
- 3D scenes include camera positioning

**4. IMPLEMENTATION FEASIBILITY:**
- Each step can be directly translated to Manim code
- Animation sequence is logical and flows well
- All required parameters are specified
- No ambiguous or vague instructions

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
            userQuery=userQuery
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
    # print("**** refineDescription *****")
    userQuery = state.userQuery
    description = state.detailedDescription
    detailedDescriptionError = state.detailedDescriptionError or "No specific error provided."
    structured = llmFlash.with_structured_output(DetailDescription)
    descriptionRefine = state.descriptionRefine + 1
    
    systemPrompt = """
You are a Manim v0.19+ description refiner. Fix the animation description based on validation errors.

Note:
    Ensure that all text objects do not overlap with the graph, other text, or any other objects in the scene.

When generating Manim code for 3D scenes, ensure that all text and 3D objects fit comfortably on screen and remain readable during camera movement.

    Relative text size: Adjust font sizes proportionally. If there are many text elements, reduce their size so all remain balanced and readable.

    Fixed-frame text: Keep all descriptive text (titles, subtitles, equations, annotations) fixed to the frame using add_fixed_in_frame_mobjects(...) so it does not move with the 3D camera.

    Grouping and spacing: Group related text (such as multiple equations) in a VGroup and arrange them vertically with clear spacing.

    Title : Center the main title at the top of the frame, and center, and make sure the text is not too large
        
    Equations or other text in much smalle text size compare to title, write equation text below the title and shift them to the left or right (with enough spacing) so they don’t overlap the 3D object. 

    Margins: Always leave a comfortable margin between text and the frame edges.

    Graph scaling: Keep x, y, and z axis lengths proportional to maintain a balanced appearance of the 3D object.

    3D object centering: Place the 3D surface or graph so that its geometric center aligns with the origin (ORIGIN) and is fully visible inside the ThreeDAxes.

    Camera framing: Choose a camera orientation and distance that keeps the entire 3D object centered and clearly visible without cropping.

    Axes balance: If using ThreeDAxes, keep the axes centered around the origin to ensure the surface is balanced in the frame.

    LaTeX syntax: Use raw strings for LaTeX expressions, e.g. MathTex(r"x^2").


**CURRENT DESCRIPTION:**
{description}

**VALIDATION ERROR TO FIX:**
{detailedDescriptionError}

**USER'S ORIGINAL REQUEST:**
{userQuery}

**REFINEMENT TASK:**
**OUTPUT REQUIREMENTS:**
- Always begin with a **scene setup step** (e.g., NumberPlane for 2D or Axes for 3D, background color, camera position).
- Always include the **first visible object/text** immediately after the setup (e.g., centered title or equation).
- Every step must specify:
  - Exact object positions (x, y, z for 3D or x, y for 2D)
  - Specific colors, sizes, and fonts
  - Animation timing and transitions
  - Camera movements (for 3D scenes)
  - Clear spacing to prevent overlaps

**ANIMATION TYPES:**
- **2D Scene**: Use flat coordinates, NumberPlane when needed
- **3D Scene**: Include camera position, rotations, lighting, depth

**KEY SPECIFICATIONS:**
-Text: Use a font_size appropriate to fit on the screen. In Manim, font_size is measured in point size (pt). Use white color and restrict to 2D positioning only.
- Objects: Define shape, size, color, opacity, and exact coordinates
- Animations: Include duration and transition type (FadeIn, Write, Transform, etc.)
- Spacing: Maintain at least 1 unit gap between objects to avoid overlaps
- Background: Default to black unless otherwise specified

**STRUCTURE:**
- Step 1: Scene setup (axes/plane + camera + background)
- Step 2: Display main text/title/equation centered at (0,0)
- Step 3+: Sequential object/animation steps with technical details

**EXAMPLE OUTPUT FORMAT:**
Step 1: Create NumberPlane centered at (0, 0) with x_range=[-5, 5], y_range=[-3, 3], faded grid lines. Background black.
Step 2: Display equation 'ax² + bx + c = 0' using MathTex at position (0, 2) with font_size=64, white color. Animate with Write over 2 seconds.
Step 3: Animate 'c' term moving right to position (3, 2) over 2 seconds using Transform.
Step 4: Create red cube at (-2, 0, 1) with size 1, opacity=0.8, rotating around y-axis for 3 seconds.
Make the description immediately implementable in Manim code.
"""

    messages = [
        SystemMessage(content=systemPrompt.format(
            description=description,
            detailedDescriptionError=detailedDescriptionError,
            userQuery=userQuery
        )),
        HumanMessage(content="Refine the description to fix the validation errors.")
    ]
    
    try:
        result = structured.invoke(messages)
        # print(f"Refinement attempt #{descriptionRefine}")
        # print(f"Refined description: {result.description}")
        return state.model_copy(update={
            "detailedDescription": result.description,
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

