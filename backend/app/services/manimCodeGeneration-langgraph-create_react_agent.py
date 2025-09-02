from langchain_core.tools import tool
from langchain.agents import create_tool_calling_agent, AgentExecutor
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import SystemMessage, HumanMessage
from langgraph.prebuilt import create_react_agent
from langgraph.errors import GraphRecursionError
from llm import llmPro, llmFlash
from schema import mainmState, CheckMaimCode
from dotenv import load_dotenv
from langgraph.graph import END
import os
import subprocess
import uuid
load_dotenv()

critical = """
<CRITICAL>:Ensure that text and objects do not overlap. You MUST write code that is compatible with Manim v0.19+ ONLY. Do NOT use any deprecated or removed methods..

If in a Graph there is decimal number need then it should be 2 decimal only
All written texy in the 2d in the screen way 
If try to write what is happing if needed
All text and the scene should remain in the frame. The text and scene transitions should be smooth.

in Manim v0.19+, you should import directly below mention from the top-level manim package. like this from manim import , DirectionalLight,
    This includes:
    Scene types: Scene, ThreeDScene
    3D objects: Cube, Sphere, ParametricSurface
    Lights: DirectionalLight, 
    2D objects: Circle, Square, Text, MathTex, etc.
    Animations: Create, Write, FadeIn, Transform, etc.
    Axes & plots: Axes, NumberPlane

    Removed in v0.19+
        Lighting Classes:
            AmbientLight
            PointLight
            DirectionalLight
            All classes from manim.mobject.three_d.light
            In Manim v0.19, ParametricSurface was renamed to Surface.

        Scene Method:
            set_background


    What's New
        Camera Lighting: Lighting is now handled automatically by the camera.
        Setting Background Color: Use self.camera.background_color = <color> to set the background color.
        Directional Lighting: For custom lighting effects, you can use DirectionalLight.

            Example usage:
            from manim import *

            class MyScene(ThreeDScene):
                def construct(self):
                    self.set_camera_orientation(phi=75 * DEGREES, theta=30 * DEGREES)
                    self.begin_ambient_camera_rotation(rate=0.05)
                    self.camera.background_color = BLACK
                    self.renderer.camera.light_source.move_to([0, 0, 5])

        Automatic Lighting:
            Lighting is now handled automatically by the camera.
            You can adjust the light direction using:
            self.renderer.camera.light_source.move_to([x, y, z])

        Background Color:
            Set the background color using:
            self.camera.background_color = BLACK

        Scene Setup:
            Use self.set_camera_orientation and self.begin_ambient_camera_rotation for camera positioning and rotation.

    -- TypeError: Mobject.__init__() got an unexpected keyword argument 'disappearing_time'
        How to fix: The TracedPath API changed. In earlier versions, TracedPath had a disappearing_time argument. In v0.19+, it no longer exists.
            Instead of disappearing_time, use the new dissipating_time argument:
            Example 
            
            from manim import TracedPath, BLUE, RED

            trace1 = TracedPath(bob1, stroke_width=2, color=BLUE, dissipating_time=3)
            trace2 = TracedPath(bob2, stroke_width=2, color=RED, dissipating_time=3)

            self.add(trace1, trace2)

    -- TypeError: TracedPath.__init__() missing 1 required positional argument: 'traced_point_func'

        Old version: TracedPath(bob1, ...) — passed the mobject directly.
        New version (v0.19+): TracedPath(traced_point_func=...) — you must give a function returning the point to trace.
        dissipating_time replaces disappearing_time.

        **CORRECT v0.19+ SYNTAX TO USE:**

    Your tasks are:
    1.  Before writing the main body of the code, write a commented-out "Layout Plan" that describes how you will position the main elements on the screen to avoid overlap.
    2.  Write the complete Manim python code for the animation.
    3.  The class name for the animation scene MUST be the same as the filename (without the .py extension).
    4.  Use the provided tool to save the final code to a file.
    
    Note:
    
    - And all the content should be in frame.
    - if you are creating 3d then do it correctly
        -- 2D Scenes use a camera.frame to control the view.
        -- 3D Scenes use the camera object directly for control.

    You got These error many time try to overcome these issue:
    - TypeError: Code.__init__() got an unexpected keyword argument 'code'
    - NameError: name 'Text3D' is not defined
    - ValueError: latex error converting to dvi.
    - TypeError: Mobject.__getattr__.<locals>.getter() takes 1 positional argument but 2 were given
    - Code.__init__() got an unexpected keyword argument 'code'
    -- Also, prefer using `axes.plot()` instead of the older `axes.get_graph()`.
    -- TypeError: Mobject.__getattr__.<locals>.getter() got an unexpected keyword argument 'x_range' 
    - AttributeError: 'object' has no attribute 'to_center'. Always use the `.move_to(ORIGIN)` method instead of `.to_center()`.
    -- latex error converting to dvi
    -- Text object has no attribute 'to_center'
    - In Manim v0.19 and newer versions, to_center() has been deprecated and removed. Instead, you should use:
    # Old way (doesn't work in v0.19+): axes.to_center()
    # New way (correct for v0.19+): axes.move_to(ORIGIN)

    -- TypeError: Mobject.__init__() got an unexpected keyword argument 'x_label'
    -- AttributeError: 'ThreeDCamera' object has no attribute 'animate'
    --TypeError: Unexpected argument None passed to Scene.play().
    --- The `NameError` for `ParametricSurface` was incorrectly "fixed" by explicitly importing it from `manim.mobject.three_d.three_dimensions`.  

        In Manim v0.19+, this import path is invalid and causes:
        ImportError: cannot import name 'ParametricSurface' from 'manim.mobject.three_d.three_dimensions'

         Correct usage: `from manim import ParametricSurface`

        Additionally, the animation for axes and labels should use `FadeIn` for smooth entrance rather than appearing instantly.

        The corrected file `Animation_b9cf9c45.py` failed due to the bad import and must be fixed as described.

    -- AttributeError: 'MoveAlongPath' object has no attribute 'submobjects'
        Mobjects (like Cube(), Sphere()) have submobjects.
        Animations (like MoveAlongPath(obj, path)) do not have submobjects.

    -- AttributeError: 'Animation_ed282dad' object has no attribute 'add_ambient_camera_rotation'
        cube = Cube()
        anim = Rotate(cube, angle=PI/4)

        anim.add_ambient_camera_rotation(rate=0.1)  # ❌ WRONG

        Correct usage:
            class MyScene(ThreeDScene):
            def construct(self):
                cube = Cube()
                self.add(cube)
                self.add_ambient_camera_rotation(rate=0.1)  # ✅ add rotation to the scene
                self.play(Rotate(cube, angle=PI/4))
                self.wait(2)
    -- AttributeError: 'Animation_b79f245b' object has no attribute 'set_background'
        How to fix:
            Use self.camera.background_color instead:
                Replace any line like: self.set_background(BLACK)
                With: self.camera.background_color = BLACK

    -- TypeError: .scene_updater() missing 1 required positional argument: 'dt_scene'
        Note:
            Always include dt for any updater function.
            dt is the time delta since the last frame — use it to make animations frame-rate independent.
            Works for both 2D and 3D scenes.

    -- AttributeError: 'ThreeDCamera' object has no attribute 'animate'
        In Manim v0.19+, you cannot use self.camera.animate.
        Replace: self.camera.animate.set_theta(-45 * DEGREES) 
        with either: self.set_camera_orientation(theta=-45 * DEGREES)  # instant
        or --> self.move_camera(theta=-45 * DEGREES, run_time=8)  # smooth

    -- TypeError: Mobject.__init__() got an unexpected keyword argument 'start_vector'
        In Manim v0.19+, Angle no longer accepts start_vector or other_angle.
        Use only:Angle(line1, line2, radius=..., color=...)

    -- TypeError: Unexpected argument None passed to Scene.play()
        The error happens because you passed self.move_camera(...) to self.play().
        # self.move_camera() returns None, so play() sees None → error.
        Fix: Either animate the camera with .animate inside play():
        self.play(
            phase_tracker.animate.set_value(4 * PI),
            self.camera.frame.animate.set_phi(self.camera.get_phi() + 10 * DEGREES)
        )
        or call move_camera() separately:
        # self.play(phase_tracker.animate.set_value(4 * PI))
        # self.move_camera(phi=self.camera.get_phi() + 10 * DEGREES, run_time=2)
        # Never pass move_camera() directly into play().

    -- TypeError: Mobject.__getattr__.<locals>.getter() got an unexpected keyword argument 'u_range'
        Fix: Remove u_range from Circle, Line, Square, or Scene.play() calls. Use it only with parametric objects.
        Example:
        # Correct
        curve = ParametricFunction(lambda t: np.array([t, t**2, 0]), t_range=[0,1])
        self.play(Create(curve))
        # Wrong
        circle = Circle(u_range=[0,1])  # causes your error

    -- ImportError: cannot import name 'ParametricSurface' from 'manim' 
        In Manim v0.19, ParametricSurface was renamed to Surface.

        Fix the import:

        from manim import Surface


        Example usage:

        surface = Surface(
            lambda u, v: np.array([np.cos(u)*np.cos(v), np.cos(u)*np.sin(v), u]),
            u_range=[-PI, PI],
            v_range=[0, TAU],
            resolution=(8, 8)
        )
    
    -- TypeError: Mobject.__init__() got an unexpected keyword argument 'opacity'
        opacity is not a constructor argument.
        Instead, set it after creating the object using .set_opacity().

    -- NameError: name 'ShowCreation' is not defined
        ShowCreation was removed. Replace it with Create:


    -- Important: In v0.19, there’s no built-in 3D text class—you must use to 2D Text
        You create 2D text and then use the .extrude() method on it.

    --  from manim.animation.rate_functions import linear ModuleNotFoundError: No module named 'manim.animation.rate_functions'
        In Manim v0.19+, LINEAR was moved.
        from manim.animation.rate_functions import linear
        All rate functions (like linear, smooth, there_and_back, etc.) live in the top-level manim module now:

    -- AttributeError: 'ThreeDCamera' object has no attribute 'animate'
        3D camera (ThreeDCamera) has no .animate.

        Fix use this
        # Use self.move_camera(phi=…, theta=…, run_time=…) in ThreeDScene.
        Do not pass move_camera to self.play() or Succession; it schedules animation internally.

    -- AttributeError: 'ThreeDCamera' object has no attribute 'get_position'
        Fix use this
        Use self.camera.frame_center or self.camera.frame.get_center() to get the camera’s position.

    -- NameError: name 'EASE_IN_OUT' is not defined
        Use this In Manim 0.19+, first import, from manim.rate_functions import ease_in_out then Use the function ease_in_out instead
    
    -- AttributeError: ParametricFunction object has no attribute 'scene'
        In Manim 0.19+, you can’t call scene on a Mobject. Instead, add it to the scene using self.add() or self.play().

    -- TypeError: Mobject.__getattr__.<locals>.setter() takes 2 positional arguments but 3 were given
        Use this In Manim 0.19+, mobj.set_fill(color=WHITE, opacity=1)

    -- AttributeError: NumberPlane object has no attribute 'center_on_screen'
        Use this In Manim 0.19+, plane.move_to(ORIGIN) 

    -- AttributeError: 'ThreeDCamera' object has no attribute 'set_field_of_view'
        Use this In Manim 0.19+ self.camera.frame.set(width=10) 
    
    -- TypeError: Mobject.__getattr__.<locals>.setter() got an unexpected keyword argument 'ambient_coefficient'
        Use this In Manim 0.19+, shading params like ambient_coefficient, diffuse_coefficient, specular_coefficient no longer exist — use only set_fill, set_stroke, and set_color.
    -- AttributeError: CubicBezier object has no attribute 'add_tip'
        Fix: In Manim v0.19+, CubicBezier has no add_tip(). Use a separate Arrow or CurvedArrow instead.
    -- NameError: name 'LIGHT_BLUE' is not defined fix: LIGHT_BLUE is undefined in Manim v0.19+; use BLUE_E or define it with Color("\\#ADD8E6").

    -- TypeError: Mobject.apply_points_function_about_point() got an unexpected keyword argument 'scale_tips'
        Fix: Remove scale_tips and, if you need arrow tip scaling, set it separately with arrow.set_tip_length() or use Arrow/Vector with custom tip size.

    -- TypeError: Unexpected argument None passed to Scene.play().
        Fix: don’t put it inside self.play().
            Example:
            # self.play(LaggedStart(*[GrowArrow(a) for a in arrows]))
            # self.move_camera(phi=new_phi, theta=-45*DEGREES, run_time=2)

    -- TypeError: Mobject.__init__() got an unexpected keyword argument 'vector'
        If you want to place it: dot = Dot(point=RIGHT)   # use 'point' instead of 'vector'
        or
        If you meant an arrow/vector: arrow = Vector(RIGHT)   # or Arrow(ORIGIN, RIGHT)


    -- TypeError: Mobject.apply_points_function_about_point() got an unexpected keyword argument 'scale_tips' 
        fix: Remove it and instead use: arrow.set_tip_length(0.3)

    -- Exception: Cannot call Mobject.get_start for a Mobject with no points
        Fix: Make sure the Mobject is not empty—use a proper shape or add points before calling get_start()
            Example:
                line = Line(LEFT, RIGHT)
                print(line.get_start()) 

    -- TypeError: NumberLine.add_numbers() got multiple values for argument 'x_values'
        x_values was removed in Manim v0.19+.
        line = NumberLine(x_range=[0, 10, 1])
        line.add_numbers(numbers=[0,1,2,3,4,5,6,7,8,9,10])
        Or auto-generate:
        line.add_numbers()

    -- Mobject.__getattr__.<locals>.getter() got an unexpected keyword argument 'y_values'
        # ax = Axes(x_range=[-5, 5, 1], y_range=[-5, 5, 1])
        # graph = ax.plot(lambda x: x**2)  # no y_values

    -- TypeError: Mobject.__init__() got an unexpected keyword argument 'numbers'
        Manim objects don’t accept custom arguments in __init__().

    -- TypeError: Mobject.__init__() got an unexpected keyword argument 'line_config'
        line_config is removed in Manim v0.19.
        Pass styling directly using stroke_color, stroke_width, etc.

    
    </CRITICAL>
"""

important = """
<IMPORTANT>: Always import all Manim classes directly from top-level `manim` package.
Do NOT use any deprecated paths such as `manim.mobjects` or `manim.mobject`.
Example correct imports:
from manim import Scene, ThreeDScene, Cube, Sphere, Text, MathTex, ParametricSurface, PointLight</IMPORTANT>

"""

mandatoryChecklist = """**MANDATORY CHECKLIST - VERIFY YOUR CODE:**
✓ No .to_center() methods used
✓ All positioning uses .move_to() or .to_edge()
✓ Layout: Uses .next_to() or .arrange() to prevent overlapping objects.
✓ Axes use .plot() not .get_graph()
✓ Code objects use correct parameter syntax
✓ Modern color constants used
✓ Proper animation syntax
✓ Compatible with Manim v0.19+
✓ LATEX: All MathTex uses raw strings r""
✓ LATEX: Plain text uses Text(), math uses MathTex()
✓ LATEX: No LaTeX syntax in Text() objects
✓ In Manim v0.19+, you should import directly from the top-level manim package. For example: from manim import DirectionalLight.
    This includes:
        Scene types: Scene, ThreeDScene
        3D objects: Cube, Sphere, Surface (formerly ParametricSurface)
        Lights: DirectionalLight
        2D objects: Circle, Square, Text, MathTex, etc.
        Animations: Create, Write, FadeIn, Transform, etc.
        Axes & plots: Axes, NumberPlane
"""

MAX_REWRITE_ATTEMPTS = 3
@tool
def createFileAndWriteMainmCode(filename, content):
    """This tool is used to write a python code directly in a file for a Manim animation."""
    print("****************** Creating a file ****************")
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
    

import subprocess
import os

def run_manim_scene(filename, state: mainmState):
    print("****************** running a manim file ****************")
    flags=f"--progress_bar display -{state.quality}"
    filepath = f"./temp/{filename}"
    scene_name = filename.replace(".py", "")

    if not os.path.exists(filepath):
        return f"Error: File '{filepath}' not found."

    command = ["manim", "render", filepath, scene_name]
    command.extend(flags.split())

    print(f"--- Running Manim Command: {' '.join(command)} ---")
    
    try:
        process = subprocess.Popen(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1
        )

        full_output = ""  # Collect all output
        for line in process.stdout:
            print(line, end='')       # Show real-time
            full_output += line       # Save for return

        process.wait()

        if process.returncode != 0:
            return f"MANIM EXECUTION FAILED. The file '{filename}' has an error. Review output below:\n\n{full_output}"

        print("--- Finished rendering successfully ---")
        return f"Manim render completed for {filename}."

    except FileNotFoundError:
        return "Error: 'manim' command not found. Is Manim installed and in your PATH?"

# @tool
# def remove_file(filename):
#     os.remove(filename)



def agentCreateFile(state: mainmState):
    tools = [createFileAndWriteMainmCode]

    system_prompt = """
    You are a helpful AI. You expert in creating manim code in and try it be good in one go and use manim v.19



{important}

{critical}

    **CORRECT v0.19+ SYNTAX TO USE:**

Create a Scene class named MainScene that follows these requirements:

1. Scene Setup:
    For 3D concepts: Use ThreeDScene.
        - Always import lights and 3D objects directly: Cube, Sphere, DirectionalLight, etc.
        - Position objects explicitly in 3D space with x, y, z coordinates: object.move_to([x, y, z]) or object.move_to(np.array([x, y, z])).
        - Use self.set_camera_orientation(...) for initial camera angles.
        - Use self.move_camera(..., run_time=...) for smooth transitions.
        - Use self.begin_3dillusion_camera_rotation(rate=...) / self.stop_3dillusion_camera_rotation() for automatic rotation.
        - Ensure objects are spaced along z-axis to prevent overlaps.
        - Add lights (DirectionalLight, PointLight) to illuminate all objects, creating shadows for depth.
        - Camera must provide a clear view where all objects are visible; avoid default top-down flattening.
    - For 2D concepts: Use Scene with NumberPlane when relevant.
    - Add titles and clear labels for all mathematical or visual elements.

2. Mathematical Elements:
   - Use MathTex for equations with proper LaTeX syntax
   - Include step-by-step derivations when showing formulas
   - Add mathematical annotations and explanations
   - Show key points and important relationships

3. Visual Elements:
   - Create clear geometric shapes and diagrams
   - Use color coding to highlight important parts
   - Add arrows or lines to show relationships
   - Include coordinate axes when relevant

4. Animation Flow:
   - Break down complex concepts into simple steps
   - Use smooth transitions between steps
   - Add pauses (self.wait()) at key moments
   - Use transform animations to show changes

5. Specific Requirements:
   - For equations: Show step-by-step solutions
   - For theorems: Visualize proof steps
   - For geometry: Show construction process
   - For 3D: Include multiple camera angles
   - For graphs: Show coordinate system and gridlines

6. Code Structure:
   - Import required Manim modules
   - Use proper class inheritance
   - Define clear animation sequences


7. **Positioning:**
   - Center objects: object.move_to(ORIGIN)
   - Move to coordinates: object.move_to([x, y, z]) or object.move_to(np.array([x, y, z]))
   - Edge positioning: object.to_edge(UP), object.to_edge(LEFT), etc.

8. **Axes and Graphs:**
   - Create axes: axes = Axes(x_range=[...], y_range=[...])
   - Plot functions: graph = axes.plot(lambda x: x**2, color=BLUE)
   - NOT: axes.get_graph() (deprecated)

9. Before writing the main body of the code, write a commented-out "Layout Plan" that describes how you will position the main elements on the screen to avoid overlap.
Example 
class MyScene(Scene):
    def construct(self):
        # Layout Plan:
        # 1. Main title will be at the top of the screen (to_edge(UP)).
        # 2. A circle will be placed on the left side.
        # 3. An explanation text block will be placed to the right of the circle using .next_to().
        # 4. The final formula will appear below everything, centered.

        title = Text("My Animation").to_edge(UP)
        my_circle = Circle().move_to(LEFT * 3)
        explanation = Text("This circle is an example.").next_to(my_circle, RIGHT, buff=0.5)
        # ... rest of the code ...

10. **Text and Math (CRITICAL - Prevents LaTeX DVI errors):**
   - Plain text: Text("Hello World")
   - Math expressions: MathTex(r"x^2 + y^2 = r^2")
   - ALWAYS use raw strings (r"") with MathTex
   - NEVER: MathTex("x^2") without raw string
   - Code blocks: Code("your_code_here", language="python")
   - NOT: Code(code="your_code_here") (wrong parameter name)

11. **Colors:**
   - Use: BLUE, RED, GREEN, YELLOW, etc. (modern constants)
   - Or: "#FF5733" (hex colors)

12. **Animations:**
   - Use: Create(), Write(), Transform(), etc.
   - Proper syntax: self.play(Create(object), run_time=2)

13. **Imports:**
   - Always use: from manim import *
   - Or specific imports: from manim import Scene, Text, Create, etc.

14. **Layout and Spacing Rules (CRITICAL - Prevents Overlapping)**
   - To prevent objects from overlapping, you MUST use Manim's relative positioning tools. Do NOT position everything manually at absolute coordinates unless you are certain they won't clash.

   - **Rule A: Use `.next_to()` for single objects.** This is the primary tool for placing a label or object next to another.
     - **Example:** `label = Text("My Circle").next_to(my_circle, UP, buff=0.5)`
     - This places `label` above `my_circle` with a gap (`buff`) of 0.5 units.

   - **Rule B: Use `.arrange()` for groups of objects.** This is the best way to line up multiple items in a row or column with even spacing.
     - **Example:** `my_group = VGroup(circle, square, text).arrange(RIGHT, buff=1)`
     - This arranges the objects horizontally with a gap of 1 unit between each.

   - **Rule C: Use `VGroup` and `.move_to()` for layout blocks.** For complex scenes, group related items together, and then position the entire group. This is safer than positioning many individual items.
     - **Example:**
       `diagram = VGroup(circle, arrow, square).move_to(LEFT * 3)`
       `explanation = Text("...").move_to(RIGHT * 3)`

{mandatoryChecklist}

    """ 
#     print("\n\n\n System Prompt Agent Create file \n\n\n")
#     print(system_prompt.format(
#     critical=critical,
#     important=important,
#     mandatoryChecklist=mandatoryChecklist
# ))
    
#     print("\n\n\n\n")
    # Format the system prompt with all variables
    formatted_system_prompt = system_prompt.format(
        critical=critical,
        important=important,
        mandatoryChecklist=mandatoryChecklist
    )

    # Generate a clean, usable ID
    # We'll use a prefix and the first 8 characters of the UUID's hex representation.
    unique_name = f"Animation_{uuid.uuid4().hex[:8]}"
    state.filename = f"{unique_name}.py"
    # 2. Write a clear, direct prompt using the clean ID
    human_message = f"""
    {state.description} 
    Use the filename "{unique_name}.py" and the class name "{unique_name}".
    """

    # Use create_react_agent with its own internal prompt system
    # Configure it to behave similarly to AgentExecutor with max_iterations
    agentExecutor = create_react_agent(
        model=llmFlash, 
        tools=tools
    )
    
    # Create messages with system instructions and user request
    messages = [
        SystemMessage(content=formatted_system_prompt),
        HumanMessage(content=human_message)
    ]
    
    print(f"--- Running agent with filename: {unique_name}.py ---")
    
    # Add iteration tracking similar to AgentExecutor
    max_iterations = 10
    try:
        result = agentExecutor.invoke(
            {"messages": messages},
            config={
                "recursion_limit": max_iterations,  # Maximum number of steps the agent can take (similar to max_iterations)
                "max_execution_time": 300,  # Maximum execution time in seconds (5 minutes)
                "debug": True,  # Enable debug output
                "verbose": True  # Show detailed execution steps
            }
        )
        print(f"✅ Agent completed successfully within {max_iterations} iterations")
    except GraphRecursionError as e:
        print(f"❌ RECURSION LIMIT REACHED: Agent hit the maximum of {max_iterations} iterations")
        print("🛑 Process stopped due to iteration limit. Cannot proceed further.")
        # Set state to indicate limit reached
        state.execution_success = False
        state.execution_error = f"RECURSION_LIMIT_REACHED: Maximum iterations ({max_iterations}) exceeded during file creation"
        return state
    except Exception as e:
        print(f"❌ Agent failed after {max_iterations} iterations: {str(e)}")
        state.execution_success = False
        state.execution_error = f"AGENT_ERROR: {str(e)}"
        return state


    print("\n--- Agent Final Answer ---")
    print(result['messages'][-1].content)
    print(f"{unique_name}.py")
    print(f"statte ************************* {state.filename} *************************")

    return state


def agentCheckFileCode(state: mainmState):
    code=read_file(state.filename)
    message = state.description
    system_prompt = """
    You are an expert Manim developer...

    {critical}
    
    Code is 
    {code} 

    **Instructions**
    1. Analyze the Python script provided below in the "Code is..." section.
        1.1. Code is important. code should not produce any error in execution check the all syntax 
        1.2. And all the content should be in frame. 
        1.3. text or anything should not overlap to each other
    2. Compare its code and visual style with the description below. code is more important code should not break on the execution
    3. Return **one** JSON object with two keys:
    • "is_code_good"   – true / false  
    • "error_message"  – empty string if good, otherwise concise reason

       You got These error many time try to overcome these issue:
    - TypeError: Code.__init__() got an unexpected keyword argument 'code'
    - NameError: name 'Text3D' is not defined
    - ValueError: latex error converting to dvi.
    - TypeError: Mobject.__getattr__.<locals>.getter() takes 1 positional argument but 2 were given
    - Code.__init__() got an unexpected keyword argument 'code'
    -- Also, prefer using `axes.plot()` instead of the older `axes.get_graph()`.
    -- TypeError: Mobject.__getattr__.<locals>.getter() got an unexpected keyword argument 'x_range' 
    - AttributeError: 'object' has no attribute 'to_center'. Always use the `.move_to(ORIGIN)` method instead of `.to_center()`.
    -- latex error converting to dvi
    -- Text object has no attribute 'to_center'
    - In Manim v0.19 and newer versions, to_center() has been deprecated and removed. Instead, you should use:
    # Old way (doesn't work in v0.19+): axes.to_center()
    # New way (correct for v0.19+): axes.move_to(ORIGIN)

    -- TypeError: Mobject.__init__() got an unexpected keyword argument 'x_label'
    -- AttributeError: 'ThreeDCamera' object has no attribute 'animate'
    --TypeError: Unexpected argument None passed to Scene.play().
    --- The `NameError` for `ParametricSurface` was incorrectly "fixed" by explicitly importing it from `manim.mobject.three_d.three_dimensions`.  

        In Manim v0.19+, this import path is invalid and causes:
        ImportError: cannot import name 'ParametricSurface' from 'manim.mobject.three_d.three_dimensions'

        Correct usage: `from manim import ParametricSurface`

        Additionally, the animation for axes and labels should use `FadeIn` for smooth entrance rather than appearing instantly.

        The corrected file `Animation_b9cf9c45.py` failed due to the bad import and must be fixed as described.

    -- AttributeError: 'MoveAlongPath' object has no attribute 'submobjects'
        Mobjects (like Cube(), Sphere()) have submobjects.
        Animations (like MoveAlongPath(obj, path)) do not have submobjects.

    -- AttributeError: 'Animation_ed282dad' object has no attribute 'add_ambient_camera_rotation'
        cube = Cube()
        anim = Rotate(cube, angle=PI/4)

        anim.add_ambient_camera_rotation(rate=0.1)  # ❌ WRONG
        Correct usage:
            class MyScene(ThreeDScene):
            def construct(self):
                cube = Cube()
                self.add(cube)
                self.add_ambient_camera_rotation(rate=0.1)  # ✅ add rotation to the scene
                self.play(Rotate(cube, angle=PI/4))
                self.wait(2)
    -- AttributeError: 'Animation_b79f245b' object has no attribute 'set_background'
        How to fix:
            Use self.camera.background_color instead:
                Replace any line like: self.set_background(BLACK)
                With: self.camera.background_color = BLACK
    -- TypeError: .scene_updater() missing 1 required positional argument: 'dt_scene'
        Note:
            Always include dt for any updater function.
            dt is the time delta since the last frame — use it to make animations frame-rate independent.
            Works for both 2D and 3D scenes.

{mandatoryChecklist}
    """
    structured_llm = llmFlash.with_structured_output(CheckMaimCode)
    print("\n--- Checking Code file ---")



    messages = [
        SystemMessage(content=system_prompt.format(
        critical=critical,
        mandatoryChecklist=mandatoryChecklist,
        code=code
        )),
        HumanMessage(content=f"{message}")
    ]
    evaluation_result = structured_llm.invoke(messages)

    state.is_code_good = evaluation_result.is_code_good
    if not evaluation_result.is_code_good:
        state.validation_error = evaluation_result.error_message
        state.validation_error_history.append(evaluation_result.error_message)
    else:
        state.validation_error = None
    print("\n--- Agent Final Answer (Structured Object) ---")
    print(f"Type of result: {type(evaluation_result)}")
    print(f"Is Code Good: {state.is_code_good}")
    print(f"Error Message: {state.validation_error}")
    return state

def agentReWriteManimCode(state: mainmState):
    tools = [createFileAndWriteMainmCode]
    filename = state.filename
    validation_error = state.validation_error
    validation_error_history = state.validation_error_history
    execution_error_history = state.execution_error_history
    execution_error = state.execution_error
    description = state.description
    state.rewrite_attempts += 1 
    code = read_file(filename)

    # 1. Define the prompt with placeholders for all variables.
    system_prompt = """
You are an expert Manim debugger and Python developer, using manim v0.19.
Your sole task is to fix the provided Manim code file by analyzing all available error information.

{critical}

{important}
---
CONTEXT FOR THE FIX:

File to fix: {filename}

Original User Description:
{description}

Code to fix:
```python
{code}
```

---
ERROR ANALYSIS:

You must fix all the errors listed below. Pay close attention to the histories to avoid repeating past mistakes.

1. CURRENT EXECUTION ERROR (Highest Priority - Must Fix):
{execution_error}

2. CURRENT VALIDATION ERROR (High Priority - Also Fix):
{validation_error}

3. PREVIOUS FAILED EXECUTION ATTEMPTS (Do not repeat these runtime errors):
{execution_error_history}

4. PREVIOUS FAILED VALIDATION ATTEMPTS (Do not repeat these logical errors):
{validation_error_history}

---

    **CORRECT v0.19+ SYNTAX TO USE:**

Create a Scene class named MainScene that follows these requirements:

1. Scene Setup:
   - For 3D concepts: Use ThreeDScene with appropriate camera angles
        -- Always import lights and 3D objects directly from manim (e.g., from manim import ThreeDScene, Cube, Sphere, DirectionalLight).
        -- ❌ camera.animate → not supported

            ✅ Use:

            self.set_camera_orientation(...) → instant camera position

            self.move_camera(..., run_time=...) → smooth transition

            self.begin_3dillusion_camera_rotation(rate=...) / self.stop_3dillusion_camera_rotation() → auto rotation

   - For 2D concepts: Use Scene with NumberPlane when relevant
   - Add title and clear mathematical labels

2. Mathematical Elements:
   - Use MathTex for equations with proper LaTeX syntax
   - Include step-by-step derivations when showing formulas
   - Add mathematical annotations and explanations
   - Show key points and important relationships

3. Visual Elements:
   - Create clear geometric shapes and diagrams
   - Use color coding to highlight important parts
   - Add arrows or lines to show relationships
   - Include coordinate axes when relevant

4. Animation Flow:
   - Break down complex concepts into simple steps
   - Use smooth transitions between steps
   - Add pauses (self.wait()) at key moments
   - Use transform animations to show changes

5. Specific Requirements:
   - For equations: Show step-by-step solutions
   - For theorems: Visualize proof steps
   - For geometry: Show construction process
   - For 3D: Include multiple camera angles
   - For graphs: Show coordinate system and gridlines

6. Code Structure:
   - Import required Manim modules
   - Use proper class inheritance
   - Define clear animation sequences


7. **Positioning:**
   - Center objects: object.move_to(ORIGIN)
   - Move to coordinates: object.move_to([x, y, z]) or object.move_to(np.array([x, y, z]))
   - Edge positioning: object.to_edge(UP), object.to_edge(LEFT), etc.

8. **Axes and Graphs:**
   - Create axes: axes = Axes(x_range=[...], y_range=[...])
   - Plot functions: graph = axes.plot(lambda x: x**2, color=BLUE)
   - NOT: axes.get_graph() (deprecated)

9. Before writing the main body of the code, write a commented-out "Layout Plan" that describes how you will position the main elements on the screen to avoid overlap.
Example 
class MyScene(Scene):
    def construct(self):
        # Layout Plan:
        # 1. Main title will be at the top of the screen (to_edge(UP)).
        # 2. A circle will be placed on the left side.
        # 3. An explanation text block will be placed to the right of the circle using .next_to().
        # 4. The final formula will appear below everything, centered.

        title = Text("My Animation").to_edge(UP)
        my_circle = Circle().move_to(LEFT * 3)
        explanation = Text("This circle is an example.").next_to(my_circle, RIGHT, buff=0.5)
        # ... rest of the code ...

10. **Text and Math (CRITICAL - Prevents LaTeX DVI errors):**
   - Plain text: Text("Hello World")
   - Math expressions: MathTex(r"x^2 + y^2 = r^2")
   - ALWAYS use raw strings (r"") with MathTex
   - NEVER: MathTex("x^2") without raw string
   - Code blocks: Code("your_code_here", language="python")
   - NOT: Code(code="your_code_here") (wrong parameter name)

11. **Colors:**
   - Use: BLUE, RED, GREEN, YELLOW, etc. (modern constants)
   - Or: "#FF5733" (hex colors)

12. **Animations:**
   - Use: Create(), Write(), Transform(), etc.
   - Proper syntax: self.play(Create(object), run_time=2)

13. **Imports:**
   - Always use: from manim import *
   - Or specific imports: from manim import Scene, Text, Create, etc.

14. **Layout and Spacing Rules (CRITICAL - Prevents Overlapping)**
   - To prevent objects from overlapping, you MUST use Manim's relative positioning tools. Do NOT position everything manually at absolute coordinates unless you are certain they won't clash.

   - **Rule A: Use `.next_to()` for single objects.** This is the primary tool for placing a label or object next to another.
     - **Example:** `label = Text("My Circle").next_to(my_circle, UP, buff=0.5)`
     - This places `label` above `my_circle` with a gap (`buff`) of 0.5 units.

   - **Rule B: Use `.arrange()` for groups of objects.** This is the best way to line up multiple items in a row or column with even spacing.
     - **Example:** `my_group = VGroup(circle, square, text).arrange(RIGHT, buff=1)`
     - This arranges the objects horizontally with a gap of 1 unit between each.

   - **Rule C: Use `VGroup` and `.move_to()` for layout blocks.** For complex scenes, group related items together, and then position the entire group. This is safer than positioning many individual items.
     - **Example:**
       `diagram = VGroup(circle, arrow, square).move_to(LEFT * 3)`
       `explanation = Text("...").move_to(RIGHT * 3)`

{mandatoryChecklist}
---
TOOL USAGE INSTRUCTIONS (VERY IMPORTANT):

After you have generated the corrected code, you will call the `createFileAndWriteMainmCode` tool.
When you call this tool, you **MUST** provide **BOTH** of the following arguments:
1.  `filename`: The name of the file to write to. Use the exact filename provided in the context above: {filename}.
2.  `content`: The complete and corrected Python code as a single string.
"""

    print("\n\n\n System prompt for re write \n\n\n")

    # Format the system prompt with all variables
    formatted_system_prompt = system_prompt.format(
        filename=filename,
        critical=critical,
        important=important,
        mandatoryChecklist=mandatoryChecklist,
        code=code,
        description=description,
        validation_error_history=validation_error_history,
        validation_error=validation_error,
        execution_error_history=execution_error_history,
        execution_error=execution_error,
    )
    
    print(formatted_system_prompt)
    print("\n\n\n\n")
    
    # Use create_react_agent with its own internal prompt system
    # Configure it to behave similarly to AgentExecutor with max_iterations
    agentExecutor = create_react_agent(
        model=llmFlash, 
        tools=tools
    )
    
    # Create messages with system instructions and user request
    messages = [
        SystemMessage(content=formatted_system_prompt),
        HumanMessage(content=f"Please fix the error in the code based on the error message provided. and i want this {description}")
    ]
    
    # Add iteration tracking similar to AgentExecutor for rewrite attempts
    max_iterations = 15
    try:
        result = agentExecutor.invoke(
            {"messages": messages},
            config={
                "recursion_limit": max_iterations,  # Higher limit for rewrite attempts (similar to max_iterations)
                "max_execution_time": 600,  # Maximum execution time in seconds (10 minutes)
                "debug": True,  # Enable debug output
                "verbose": True  # Show detailed execution steps
            }
        )
        print(f"✅ Rewrite agent completed successfully within {max_iterations} iterations")
    except GraphRecursionError as e:
        print(f"❌ RECURSION LIMIT REACHED: Rewrite agent hit the maximum of {max_iterations} iterations")
        print("🛑 Process stopped due to iteration limit. Cannot fix the code further.")
        # Set state to indicate limit reached
        state.execution_success = False
        state.execution_error = f"RECURSION_LIMIT_REACHED: Maximum iterations ({max_iterations}) exceeded during code rewrite"
        state.validation_error = "Code rewrite failed due to iteration limit"
        return state
    except Exception as e:
        print(f"❌ Rewrite agent failed after {max_iterations} iterations: {str(e)}")
        state.execution_success = False
        state.execution_error = f"REWRITE_AGENT_ERROR: {str(e)}"
        return state

    print("\n--- re_write_manim_code ---")
    print(result['messages'][-1].content)
    return state

def agentRunManimCode(state: mainmState):
    result_message = run_manim_scene(filename=state.filename, state=state)
    print(f"Execution Result: {result_message}")


    if "MANIM EXECUTION FAILED" in result_message:
        state.execution_success = False
        state.execution_error = result_message
        state.execution_error_history.append(result_message)
    else:
        state.execution_success = True
        state.execution_error = ""

        state.execution_error_history.clear()
        state.validation_error_history.clear()
        state.validation_error = None

    return state


def manimRouter(state: mainmState):
    # Check if recursion limit was reached during file creation or rewrite
    if hasattr(state, 'execution_error') and state.execution_error and "RECURSION_LIMIT_REACHED" in state.execution_error:
        print("🛑 RECURSION LIMIT REACHED - Stopping entire process")
        return END
    
    if state.is_code_good is True:
        return "agentRunManimCode"
    elif state.rewrite_attempts >= 3:
        print("❌ Rewrite limit reached. Ending graph.")
        return END
    else: 
        return "agentReWriteManimCode"
    
def executionRouter(state: mainmState):
    """Routes the graph after a Manim execution attempt."""
    # Check if recursion limit was reached during rewrite
    if hasattr(state, 'execution_error') and state.execution_error and "RECURSION_LIMIT_REACHED" in state.execution_error:
        print("🛑 RECURSION LIMIT REACHED - Stopping entire process")
        return END
    
    if state.execution_success:
        print("✅ Manim execution successful. Ending graph.")
        return "done"
    else:
        # Prevent infinite loops
        if state.rewrite_attempts >= 3:
            print("❌ Rewrite limit reached after execution failure. Ending graph.")
            return "limit"
        print("❌ Manim execution failed. Routing to rewrite node.")
        return "fix"


def handleFailureAndReset(state: mainmState) -> mainmState:
    """Resets the attempt counter to start the entire process over."""
    # Check if recursion limit was reached - if so, don't restart
    if hasattr(state, 'execution_error') and state.execution_error and "RECURSION_LIMIT_REACHED" in state.execution_error:
        print("🛑 RECURSION LIMIT REACHED - Not restarting process")
        return END
    
    if state.create_again >= 1:
        return END
    else:
        print(f"❌ Maximum rewrite attempts reached. Resetting and starting over.")
        state.rewrite_attempts  = 0
        state.create_again += 1
        return state

def shouldStartOverRouter(state: mainmState):
    """Checks the 'create_again' flag to decide the next step."""
    
    # Check if recursion limit was reached - if so, don't restart
    if hasattr(state, 'execution_error') and state.execution_error and "RECURSION_LIMIT_REACHED" in state.execution_error:
        print("🛑 RECURSION LIMIT REACHED - Process terminated")
        print("📋 SUMMARY: The agent exceeded the maximum allowed iterations")
        print("   This typically happens when the task is too complex for the current limits")
        print("   Consider simplifying the request or increasing iteration limits in the code")
        return END
    
    # CORRECT: Check if this is the first and only time we are starting over.
    if state.create_again == 1:
        print("✅ Starting the process over one time.")
        return "agentCreateFile" # Loop back to the beginning
    else:
        # If create_again is > 1, the single retry has already been used.
        print("❌ Full retry and start-over process failed. Ending.")
        return END