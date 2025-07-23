from langchain_core.tools import tool
from langchain.agents import create_tool_calling_agent, AgentExecutor
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import AIMessage, SystemMessage, HumanMessage
from llm import llmPro, llmFlash
from schema import mainmState, CheckMaimCode
import os
import subprocess
import uuid


test_message=""" A linked list has several methods to manage its nodes. Here are the most common ones:

**1. Append a Node (Add to End)**

This method adds a new node to the end of the list.

- **Structure:** The list consists of nodes, each with a `value` and a `next` pointer. The last node's `next` pointer is `None`.
- **Method:**
  1. A `new_node` is created with the given value.
  2. If the list is empty (the `head` is `None`), the `head` is set to this `new_node`.
  3. If the list is not empty, the animation will show a temporary pointer (e.g., `current`) starting at the `head`.
  4. This `current` pointer traverses the list, moving from one node to the next until `current.next` is `None`. This traversal is often visualized by highlighting each node as the pointer passes it.
  5. Once at the last node, its `next` pointer (currently `None`) is updated to point to the `new_node`.
- **Animation:**
  - A new node object appears on screen.
  - A traversal animation highlights nodes sequentially from the head.
  - The `next` pointer of the last node is animated to connect to the new node.
- **Color/Size:** The `new_node` can be a different color initially to distinguish it. The `current` traversal pointer can also have a unique color.

**2. Prepend a Node (Add to Beginning)**

This method adds a new node to the beginning of the list, making it the new head.

- **Structure:** Same as above.
- **Method:**
  1. A `new_node` is created.
  2. The `new_node`'s `next` pointer is set to the current `head` of the list.
  3. The list's `head` reference is updated to point to the `new_node`.
- **Animation:**
  - A new node object appears, typically to the left or above the current head.
  - A new pointer is drawn from the `new_node` to the old `head`.
  - The main `head` label/pointer moves from the old head to the `new_node`.
- **Color/Size:** The `new_node` and the new `head` pointer can be highlighted in a distinct color (e.g., green) to show the addition.

**3. Delete a Node by Value**

This method removes the first node that contains a specific value.

- **Structure:** Same as above.
- **Method:**
  1. **Case 1: Delete Head:** If the `head` node contains the value, the `head` reference is simply moved to the next node (`head.next`). The old head is unlinked.
  2. **Case 2: Delete Other Node:**
     - The animation shows two pointers, `previous` (starting at `None` or the `head`) and `current` (starting at the `head` or `head.next`).
     - They traverse the list together. `current` finds the node to delete, and `previous` points to the node just before it.
     - The `next` pointer of the `previous` node is re-routed to bypass the `current` node, pointing directly to `current.next`.
- **Animation:**
  - A traversal animation highlights nodes as they are checked.
  - The node to be deleted is often marked with a different color (e.g., red) or an 'X'.
  - The key animation is the pointer from the `previous` node "swinging" over the deleted node to connect to the next one.
  - The deleted node and its pointers fade out or move off-screen.
- **Color/Size:** Traversal pointers (`previous`, `current`) should be visible. The node targeted for deletion should be clearly marked. The updated pointer can flash or change color to draw attention.
******Checking is this Correct or not ********"""

@tool
def create_File_and_Write_mainm_Code(filename, content):
    """This tool is used to write a python code directly in a file for a Manim animation."""
    print("****************** Creatinf a file ****************")
    if not os.path.exists("./temp"):
        os.makedirs("./temp")
        
    filepath = f"./temp/{filename}"
    try:
        with open(filepath, "w") as f:
            f.write(content)
        return f"Successfully created file: {filepath}"
    except IOError as e:
        return f"Error writing to file: {e}"


def read_file(filename):
    """This tool is used to read a file"""
    print("****************** reading a file ****************")
    filepath = f"./temp/{filename}"
    try:
        with open(filepath, "r") as f:
            fileContent = f.read()
        
        return fileContent
    except IOError as e:
        return f"Error while reading a file: {e}"
    
@tool
def run_manim_scene(filename, flags="-ql"):

    """
    Renders a Manim scene from a file that has already been created.
    
    Args:
        filename (str): The name of the Python file (e.g., "HelloLetsStart.py").
        flags (str): A string of command-line flags (e.g., "-p -ql").
    """
    print("****************** runnign a manim file ****************")
    filepath = f"./temp/{filename}"
    scene_name = filename.replace(".py", "") # More robust way to get scene name

    if not os.path.exists(filepath):
        return f"Error: File '{filepath}' not found."

    command = ["manim", "render", filepath, scene_name]
    command.extend(flags.split())

    print(f"--- Running Manim Command: {' '.join(command)} ---")
    try:
        # Using run with capture_output is simpler for agent-based flows
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            check=True # This will raise an exception on non-zero exit codes
        )
        print(result.stdout)
        print("--- Finished rendering successfully ---")
        return f"Manim render completed for {filename}."
    except FileNotFoundError:
        return "Error: 'manim' command not found. Is Manim installed and in your PATH?"
    except subprocess.CalledProcessError as e:
        print("--- Errors ---")
        print(e.stderr)
        return f"MANIM EXECUTION FAILED. The file '{filename}' exists but has an error. Analyze the following error message and fix the code in the file: \n\nERROR:\n{e.stderr}"

# @tool
# def remove_file(filename):
#     os.remove(filename)



def agent_create_file(state: mainmState):
    tools = [create_File_and_Write_mainm_Code]

    system_prompt = """
    You are a helpful AI assistant for creating manim code in and try it be good in one go
    You can use only two tool 
    Your tasks are:
    1. Write Manim python code for an animation and save it to a file using the provided tool.
    2. The class name for the animation scene must be the same as the filename (without the .py extension).
    """ 

    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", system_prompt),
            ("human", "{input}"),
            MessagesPlaceholder(variable_name="agent_scratchpad")
        ]
    )

    # Generate a clean, usable ID
    # We'll use a prefix and the first 8 characters of the UUID's hex representation.
    unique_name = f"Animation_{uuid.uuid4().hex[:8]}"

    # 2. Write a clear, direct prompt using the clean ID
    human_message = f"""
    {test_message} 
    Use the filename "{unique_name}.py" and the class name "{unique_name}".
    """

    agent = create_tool_calling_agent(llmPro, tools, prompt=prompt)
    agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)
    
    print(f"--- Running agent with filename: {unique_name}.py ---")
    result = agent_executor.invoke({"input": human_message})
    print("\n--- Agent Final Answer ---")
    print(result['output'])
    state.filename = f"{unique_name}.py"
    print(f"{unique_name}.py")
    print(f"statte ************************* {state.filename} ")
    agent_check_file_code(state)


def agent_check_file_code(state: mainmState):
    code=read_file(state.filename)
    message = test_message
    system_prompt = f"""
    You are an expert Manim developer...

    Code is {code} 

    **Instructions**
    1. Analyze the Python script provided below in the "Code is..." section.
    2. Compare its code and visual style with the description below.
    3. Return **one** JSON object with two keys:
    • "is_code_good"   – true / false  
    • "error_message"  – empty string if good, otherwise concise reason
    """
    structured_llm = llmFlash.with_structured_output(CheckMaimCode)
    print("\n--- Checking Code file ---")



    messages = [
        SystemMessage(content=system_prompt),
        HumanMessage(content=f"{message}")
    ]
    evaluation_result = structured_llm.invoke(messages)

    state.is_code_good = evaluation_result.is_code_good
    state.error_message = evaluation_result.error_message
    print("\n--- Agent Final Answer (Structured Object) ---")
    print(f"Type of result: {type(evaluation_result)}")
    print(f"Is Code Good: {state.is_code_good}")
    print(f"Error Message: {state.error_message}")
    return state

def re_write_manim_code(state: mainmState):
    tools = [create_File_and_Write_mainm_Code]
    filename = state.filename
    error_message = state.error_message
    system_prompt = f"""
    You are helpful ai assitant, you are expert of manim code
    You will get the file name error message you work is to correct the error and re write the code

    error_message is {error_message}
    filename is {filename}
"""
    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", system_prompt),
            ("human", "{input}"),
            MessagesPlaceholder(variable_name="agent_scratchpad")
        ]
    )

    agent = create_tool_calling_agent(llmPro, tools, prompt)
    agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True, max_iterations=2)
    human_message=f"Fix the error"
    result = agent_executor.invoke({"input": human_message})
    print("\n--- re_write_manim_code ---")
    print(result['output'])

def agent_run_manim_code(state: mainmState):
    tools=[run_manim_scene, create_File_and_Write_mainm_Code]
    filename = state.filename
    system_prompt = f"""
    You are helpful ai aissitent who work is to first execute the mainm code through the tool (run_main_scene) if the execution got error then fix the with the help of tool [create_File_and_Write_mainm_Code]

    # ERROR HANDLING:
    # - If the `run_manim_scene` tool returns an error, **DO NOT** start from scratch.
    # - Your task is now to **debug the code**.
    # - Analyze the error message from the failed execution.
    # - Call `create_File_and_Write_mainm_Code` again, but this time with the **corrected code** to overwrite the faulty file. Repeat the debugging process until the execution is successful.
"""
    
    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", system_prompt),
            ("human", "{input}"),
            MessagesPlaceholder(variable_name="agent_scratchpad")
        ]
    )

    agent=create_tool_calling_agent(llmPro, tools=tools, prompt=prompt)
    agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True, max_iterations=5)
    human_message=f"Execute the code file name is {filename}"
    result = agent_executor.invoke({"input": human_message})
    print("\n--- agent run manim code ---")
    print(result['output'])


state = mainmState(
    is_code_good= None,
    error_message=None,
    filename= ""
)

agent_create_file(state)
print(state.filename)
print(state.is_code_good)
if (state.is_code_good == False):
    re_write_manim_code(state)
    agent_check_file_code(state)
agent_run_manim_code(state=state)