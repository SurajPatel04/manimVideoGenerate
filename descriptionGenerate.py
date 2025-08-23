from dotenv import load_dotenv
from langchain_core.tools import tool
from langgraph.graph import END
from langchain_core.messages import AIMessage, SystemMessage, HumanMessage
from pydantic import ValidationError
from schema import DescriptionGenerationState, GenDescriptions, PickOneDescription, CheckPickedDescription
from llm import llmPro, llmFlash
import logging



load_dotenv()


def generateMultipleDescription(state: DescriptionGenerationState):
    """
    Generates three animation descriptions using the model's structured output feature.
    """
    print("****** Generating Three Descriptions (Structured Output) ********\n")
    user_query = state.user_query

    structured_llm = llmFlash.with_structured_output(GenDescriptions)
    system_prompt = """
Your task is to generate **three candidate descriptions** that match the user's query.

Each description should be:
- Detailed
- Clear
- Technically descriptive
- Written to be used later as input for generating **Manim** (Mathematical Animation Engine) code.
"""
    msg = [
        SystemMessage(content=system_prompt),
        HumanMessage(content=user_query)
    ]

    try:
        # 4. Invoke the structured chain. The result is a Pydantic object, not a string.
        result = structured_llm.invoke(msg)
        
        print(result.descriptions, "\n\n")
        return state.model_copy(update={"descriptions": result.descriptions})

    except Exception as e:
        # This will now catch API errors or rare cases where the model fails
        # to generate structured output despite the constraints.
        logging.exception("Description generation with structured output failed")
        raise

def generateDetailedDescription(state: DescriptionGenerationState):
    print("******Generating detailed description ********\n\n")
    user_query = state.user_query
    # contnet = state.descriptions
    structured_llm = llmFlash.with_structured_output(PickOneDescription)
    system_prompt = f"""
You are an expert technical writer and Manim script planner. Your task is to analyze three AI-generated animation concepts and produce one single, final, highly detailed description that is ready for a Manim coder to use. Ensure that all text and shapes are arranged clearly, with no overlaps.

You will be given a user's query

**Your Process:**
1. Your fOutput MUST be the full, step-by-step, technically-rich description for the animation.

**Output Requirements:**
-   The output must be a complete, multi-step plan, not just a title or a summary.
-   It must be technically descriptive (mentioning colors, positions, Manim animations like `Transform`, `FadeIn`, etc.).
-   It must be precise and ready for a developer to turn into code.

**Example of BAD output (What NOT to do):**
"Description 1: Step-by-Step Derivation of the Quadratic Formula"

**Example of GOOD output (What TO do):**
"The animation will visually derive the quadratic formula...
1. Initial State: Display the equation `ax^2 + bx + c = 0`...
2. Isolate Constant Term: Animate `c` moving to the right...
(and so on, providing the full detailed plan)"
"""

    msg = [
        SystemMessage(content=system_prompt),
        HumanMessage(content=user_query),
        
    ]
    try:
        result = structured_llm.invoke(msg)
        print(result.description)
        return state.model_copy(update={"pickedOne": result.description})
    except (ValidationError, RuntimeError) as err:
        logging.exception("pick_One_Description_And_Generate_Detailed_Description failed")
        raise

def validateDescription(state: DescriptionGenerationState):
    """ This function checks the description, 
    if the description is correct then True otherwise False """
    print("******Checking is this Correct or not ********\n\n")
    picked_description = state.pickedOne
    user_query = state.user_query

    
    structured_llm = llmFlash.with_structured_output(CheckPickedDescription)
    system_prompt = f"""
Your task is to determine if the Candidate description is detailed, technically accurate, and directly addresses the user's query. The description will be used to generate Manim animations, so it must be precise.

Important Instruction:
1.  User Query: The original request from the user.
2.  Candidate Description: The description to be evaluated.

Instructions:
- If the description is high-quality, detailed, and relevant to the user's query, return `true` and leave error empty.
- If the description is vague, incomplete, irrelevant, or contains errors, return `false` and explain why in the error field.

Your entire response MUST be a single, valid JSON object and nothing else. Do not include explanations, markdown, or any text outside the JSON structure.

Example 1 (Good Description):
```json
{{
  "is_this_good_descrription": true,
  "pickedOneError": ""
}}

Example 2 (Bad Description)
{{
  "is_this_good_descrription": false,
  "pickedOneError": "The description lacks detail and does not explain how to perform the steps mentioned."
}}


Candidate Description:
{picked_description}

"""

    messages = [
        SystemMessage(content=system_prompt),
        HumanMessage(content=user_query)
    ]

    try:
        result = structured_llm.invoke(messages)
        print("Description is good or not: ",result.is_this_good_descrription)
        print("Description Error: ", result.pickedOneError)
        return state.model_copy(update={
            "is_good": result.is_this_good_descrription,
            "pickedOneError": result.pickedOneError
        })

    except (ValidationError, ValueError) as e:
        logging.exception("CheckPickedDescription parsing failed")
        raise

def refineDescription(state: DescriptionGenerationState):
    print("**** refineDescription *****")
    user_query = state.user_query
    description = state.pickedOne
    pickedDescriptionError = state.pickedOneError or "No specific error provided."
    structured = llmFlash.with_structured_output(PickOneDescription)
    DescriptionRefine = state.DescriptionRefine + 1
    system_prompt = f"""
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
        SystemMessage(content=system_prompt),
        HumanMessage(content=user_query),
    ]
    try:
        result = structured.invoke(messages)
        return state.model_copy(update={
            "pickedOne":result.description,
            "DescriptionRefine": DescriptionRefine
            })
    except (ValidationError, ValueError) as e:
        logging.exception("CheckPickedDescription parsing failed")
        raise

def router(state: DescriptionGenerationState) -> str:
    if state.is_good is True:
        return END
    elif state.DescriptionRefine >= 2:
        return END
    else: 
        return "refineDescription"

