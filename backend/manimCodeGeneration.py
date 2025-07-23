from langchain_core.tools import tool
from langchain.agents import create_tool_calling_agent, AgentExecutor
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from llm import llmPro
import os
import subprocess

filename =""
@tool
def create_File_and_Write_mainm_Code(filename, content):
    """This tool is used to write a python code directly in the file"""
    filename = filename
    try:
        with open(filename, "w") as f:
            f.write(content)

    except IOError as e:
        print(f"Error writing to file: {e}")

@tool
def run_manim_scene(filename, flags="-p -ql"):
    """
    Renders a Manim scene by building and running the correct command.
    
    Args:
        filename (str): The name of the Python file (e.g., "animation.py").
        scene_name (str): name of the scene_name == filename
        flags (str): A string of command-line flags (e.g., "-p -qh").
                     Defaults to low-quality preview.
    """
    scene_name = filename
    if not os.path.exists(filename):
        print(f"Error: File '{filename}' not found.")
        return

    # Build the command as a list of strings
    command = ["manim", "render", filename, scene_name]
    command.extend(flags.split()) # Add flags like -p and -ql

    print(f"--- Running Manim Command: {' '.join(command)} ---")
    try:
        # We use Popen for long-running processes like Manim to see live output
        process = subprocess.Popen(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )

        # Print output and errors in real-time
        while True:
            output = process.stdout.readline()
            if output == '' and process.poll() is not None:
                break
            if output:
                print(output.strip())
        
        # Capture any remaining errors
        stderr = process.communicate()[1]
        if stderr:
            print("--- Errors ---")
            print(stderr)

    except FileNotFoundError:
        print("Error: 'manim' command not found. Is Manim installed and in your PATH?")
    
    print(f"--- Finished rendering {filename} ---")
    

tools = [create_File_and_Write_mainm_Code, run_manim_scene]

def Agent_For_Creating_File():
    system_prompt = ("""You are helpful ai assitent you work is this to write manim python code for animation in the file throguh the tool
    Note: filename and animation class name should be same
    """)

    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", system_prompt),
            ("human", "{input}"),
            MessagesPlaceholder(variable_name="agent_scratchpad")
        ]
    )
    human_message = """
    first wirte hello then throguh the cool animation move to lets start
    """
    agent = create_tool_calling_agent(llmPro, tools, prompt = prompt)
    exc  = AgentExecutor(agent=agent, tools=tools, verbose=True)
    result = exc.invoke({"input":human_message})
    Agent_For_Executing_File()

def Agent_For_Executing_File():
    system_prompt = ("""
You are helpful ai assitent you work is use tool to run the file 
""")
    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", system_prompt),
            ("human", "{input}"),
            MessagesPlaceholder(variable_name="agent_scratchpad")
        ]
    )
    human_message = """
    run the file
    """
    agent = create_tool_calling_agent(llmPro, tools, prompt = prompt)
    exc  = AgentExecutor(agent=agent, tools=tools, verbose=True)
    result = exc.invoke({"input":human_message})

Agent_For_Creating_File()