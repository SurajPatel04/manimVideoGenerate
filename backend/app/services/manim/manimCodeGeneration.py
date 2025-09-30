from langchain.agents import (
    create_tool_calling_agent,
    AgentExecutor
)
from langchain_core.prompts import (
    ChatPromptTemplate,
    MessagesPlaceholder
)
from langchain_core.messages import (
    SystemMessage,
    HumanMessage
)
from app.schema.ServiceSchema import (
    mainmState,
    CheckMaimCode
)
from app.core.llm import (
    llmPro,
    llmFlash
)
from langchain_core.tools import tool
from dotenv import load_dotenv
from langgraph.graph import END
import os
import subprocess
import uuid
from app.core.internalServerErrorHandle import retry
from app.core.logger import logger
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

MANIM_RENDER_TIMEOUT = 1000
critical = """
<CRITICAL>:You MUST write code that is compatible with Manim v0.19+ ONLY. Do NOT use any deprecated or removed methods..

Note it is Important: 
    If in a Graph there is decimal number need then it should be 2 decimal only
    All written texy in the 2d in the screen way 
    If try to write what is happing if needed
    All text and the scene should remain in the frame. The text and scene transitions should be smooth.

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
            from manim import WHITE, ORIGN

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

These errors occur frequently, so apply the following fixes to prevent them. The most common errors you should avoid are listed below:

## General import & API changes

### NameError / ImportError: missing names (e.g. `Color`, `ParametricSurface`, `ParametricFunction`, `DirectionalLight`, `PBRMaterial`, `Text3D`)
**Cause:** API reorganized; some classes renamed or removed.
**Fix:** Import from top-level `manim`. Replace removed classes with recommended alternatives.

```py
# Good imports
from manim import (
    Scene, ThreeDScene, Circle, Square, Text, MathTex,
    Axes, NumberPlane, Surface, ParametricFunction,
    Color, DirectionalLight, AmbientLight, PointLight
)
# ParametricSurface was renamed to Surface in v0.19+
```

- `ParametricSurface` → use `Surface`.
- `PBRMaterial` does not exist — use `.set_fill` / `.set_stroke` styling.
- `Text3D` doesn't exist: extrude 2D text if you need 3D: `text = Text("Hi"); text.extrude(depth)`.

## Camera & 3D API

### AttributeError: `'ThreeDCamera' object has no attribute 'animate'`
**Cause:** 3D camera does not support `.animate`.
**Fix:** Use `self.move_camera(...)` or `self.set_camera_orientation(...)` inside a `ThreeDScene`.

```py
# Correct for ThreeDScene
self.move_camera(phi=45 * DEGREES, theta=-30 * DEGREES, run_time=2)
# or instant
self.set_camera_orientation(phi=45 * DEGREES, theta=-30 * DEGREES)
```

### AttributeError: `'ThreeDCamera' object has no attribute 'get_position'` / `'frame'` / 'get_distance'
**Fix:** Use `self.camera.frame_center`, `self.camera.frame.get_center()`, or `self.camera.distance`.

## Animation / Scene.play errors

### ValueError: `Unexpected argument None passed to Scene.play()`
**Cause:** Passing the result of `self.move_camera(...)` (which returns None) to `self.play()`.
**Fix:** Either animate camera frames (`self.camera.frame.animate...`) in `play()` (2D) or call `self.move_camera()` separately (3D).

```py
# Wrong
self.play(self.move_camera(phi=...))
# Right (ThreeDScene)
self.move_camera(phi=..., run_time=2)
# Or animate frame in 2D
self.play(self.camera.frame.animate.set_width(10))
```

### Exception: `Called Scene.play with no animations` (`self.play()` with no args)
**Fix:** Ensure at least one animation object is passed: `self.play(Create(obj))`.

## Mobject constructor argument changes (most common)

Many `__init__` keyword arguments were removed. Instead set properties after construction.

### Unexpected keyword args removed in v0.19+: `opacity`, `x_range` on Mobject, `z_range` on 2D Axes, `numbers`, `line_config`, `vector`, `start_vector`, `other_angle`, `disappearing_time`, etc.
**Fix pattern:** Remove these arguments from constructors and call setter methods after creating the object.

```py
# Wrong
c = Circle(opacity=0.8)
# Right
c = Circle()
c.set_opacity(0.8)

# Wrong: Surface(..., z_range=...)
# Right: use Surface(u_range=..., v_range=...) or axes with x_range/y_range
```

Specific notes:
- `Axes` (2D) takes `x_range` and `y_range` only. For 3D use `ThreeDAxes` or `Surface`.
- `Circle`, `Line`, `Square` do **not** accept `u_range`/`v_range`; use parametric objects for ranges.

## TracedPath API changes

### TypeError: `TracedPath.__init__() missing 1 required positional argument: 'traced_point_func'`
**Cause:** API changed: TracedPath expects a function returning the point to trace.
**Fix:** Use `traced_point_func=` and `dissipating_time` (replaces disappearing_time).

```py
from manim import TracedPath
trace = TracedPath(traced_point_func=lambda: bob.get_center(), stroke_width=2, dissipating_time=3)
self.add(trace)
```

## 2D vs 3D object API & helpers

### `Mobject.__init__()` got unexpected keyword argument `z_range` / `x_range` / `x_label` / `numbers`
**Cause:** Passing axis-like kwargs to generic Mobjects.
**Fix:** Use `Axes` / `NumberLine` / `ThreeDAxes` constructors where appropriate and avoid passing these kwargs to generic Mobjects.

- Add labels after creating axes:
```py
axes = Axes(x_range=[-5,5,1], y_range=[-3,3,1])
x_label = axes.get_x_axis_label("x")
self.add(axes, x_label)
```

### AttributeError: `ThreeDAxes` object has no attribute `add_numbers`
**Fix:** Use `.add_coordinates()` or add tick labels manually.

## Deprecated animations & utilities

- `ShowCreation` → use `Create`.
- `get_graph()` on axes → use `axes.plot()`.

## LaTeX / DVI errors

### `ValueError: latex error converting to dvi` or `latex error converting to dvi`
**Fixes:**
- Ensure LaTeX is installed and accessible to Manim in your environment.
- Escape or fix problematic LaTeX code. Test with a minimal `MathTex` example.

## Updater & callback signature changes

### `TypeError: .scene_updater() missing 1 required positional argument: 'dt_scene'`
**Cause:** Updater functions must accept `dt` (time delta).
**Fix:** Define updaters with `(mobject, dt)` or `(dt,)` depending on context. Example:

```py
def my_updater(mob, dt):
    mob.rotate(dt)

dot.add_updater(my_updater)
```

## Path, Arrow, Bezier changes

- `CubicBezier.add_tip()` removed — use `Arrow` or `CurvedArrow`.
- `QuadraticBezier` name removed — use `Bezier([p0, p1, p2])`.
- To get path points from a mobject, ensure the mobject actually has points.

## Color & constants

- `LIGHT_BLUE` may be undefined — use `BLUE_E`, `Color("#ADD8E6")` or import from `manim`.
- Rate functions now import from top-level: `from manim.rate_functions import ease_in_out`.

## Common gotchas (short checklist)
- Do not pass `move_camera()` into `self.play()`; call it separately or animate a camera frame for 2D.
- Replace constructor kwargs with setter methods (e.g., `.set_fill()`, `.set_opacity()`, `.set_stroke()`).
- Use `Surface` where older docs refer to `ParametricSurface`.
- Use `Create` instead of `ShowCreation`.
- Use `axes.plot()` instead of `get_graph()`.
- For 3D camera adjustments: use `move_camera` / `set_camera_orientation`.

## The user's required tasks (kept and clarified)
1. Layout Plan: Before writing the code, add a commented-out layout plan describing placement & spacing to avoid overlap.
2. Produce full Manim code for the requested animation (2D or 3D as appropriate) that follows v0.19+ APIs.
3. Class name must match the filename (without `.py`).
4. Save the final code to a file using the provided tool (your environment/setup).

Notes:
- Keep all content in frame. Use `camera.frame` for 2D control and `move_camera` / `set_camera_orientation` for 3D.
- When creating traces, use the `traced_point_func` signature.
- Always include `dt` in updater functions.

## Minimal example fixes (small snippets)

1. Replace `ShowCreation` with `Create`:
```py
self.play(Create(circle))
```

2. Set opacity after creation:
```py
c = Circle()
c.set_opacity(0.6)
self.add(c)
```

3. TracedPath new usage:
```py
trace = TracedPath(traced_point_func=lambda: bob.get_center(), dissipating_time=2)
self.add(trace)
```

4. 3D camera movement (ThreeDScene):
```py
self.move_camera(phi=60*DEGREES, theta=-30*DEGREES, run_time=3)
```


## nTypeError: Mobject.next_to() got an unexpected keyword argument align_l

# Basic placement with padding
mobject.next_to(target_mobject, direction=RIGHT, buff=1.0)

# If you need alignment
mobject.next_to(target_mobject, direction=RIGHT, buff=1.0, aligned_edge=UP)

    direction → RIGHT, LEFT, UP, or DOWN

    buff → gap between objects

    aligned_edge → align edges (e.g., UP, DOWN, LEFT, RIGHT)

## TypeError: Mobject.__init__() got an unexpected keyword argument get_x_axis_label'
    Create your axes normally, then call the method afterwards:

    axes = Axes(
        x_range=[-6.28, 6.28, 1.57],
        y_range=[-1.5, 1.5, 0.5],
        axis_config={"include_tip": False},
    )

    # correct usage:
    x_label = axes.get_x_axis_label("x")
    y_label = axes.get_y_axis_label("y")
    self.add(axes, x_label, y_label)

## Too few rows and columns to fit all submobjetcs
    Use this equations.arrange_in_grid(rows=3, cols=2, col_widths=[10])
---
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
    output_format=state.format
    width, height = (state.resolution or "1920x1080").split("x")
    if not os.path.exists(filepath):
        return f"Error: File '{filepath}' not found."

    command = ["manim", "render", filepath, scene_name, "--format", output_format, "--custom_folders", "-r", f"{width},{height}"]
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

        full_output = []
        for line in process.stdout:
            print(line, end='')
            full_output.append(line)

        process.wait()

        if process.returncode != 0:
            logger.error("MANIM EXECUTION FAILED for file '%s'. Full output:\n%s", full_output, exc_info=True)
            error_text = None
            print("------------Collecting All the Error Only--------------")
            for i, line in enumerate(full_output):
                if "ERROR" in line or "Traceback" in line:
                    # Join from the first error-related line till the end
                    error_text = "".join(full_output[i:])
                    break
            if error_text is not None:
                return f"MANIM EXECUTION FAILED. The file '{filename}' has an error. Review output below:\n\n{error_text}"
            return f"MANIM EXECUTION FAILED. The file '{filename}' has an error. Review output below:\n\n{full_output[-1]}"

        print("--- Finished rendering successfully ---")
        return f"Manim render completed for {filename}."

    except FileNotFoundError:
        return "Error: 'manim' command not found. Is Manim installed and in your PATH?"

def agentCreateFile(state: mainmState):
    tools = [createFileAndWriteMainmCode]
    animationTypeRule = ANIMATION_MAP.get(state.animationType)
    # Generate unique name first
    unique_name = f"Animation_{uuid.uuid4().hex[:8]}"
    state.filename = f"{unique_name}.py"
    systemPrompt = """
    You are a Manim code generation expert. Your task is to:
    1. Create complete, working Manim v0.19+ Optimise code, Do not include any explanation, markdown, or extra text. Output only valid Manim Python code
    2. You MUST call the tool `createFileAndWriteMainmCode` with:
     - The filename MUST be exactly: {filename}
     - The class name MUST be exactly: {class_name}

Note:
    - All code must use real newlines and proper indentation (no literal \\n outside strings).
    - Use only valid and non-deprecated Manim methods.
    - The code must be ready to run as a `.py` file without syntax errors.
    - If there is to many text then the text size should be smaller and fade out some text if not needed
`
    
    Must DO thing because it is critical: You MUST call the createFileAndWriteMainmCode tool with:
    - filename: "{filename}"
    - content: [complete Python code as string]

    ANIMATION RULES - Follow these specific guidelines:
    {animationTypeRule}

    """

    human_message = f"""
    Create Manim animation for: {state.description}

    Requirements:
    - Filename: {state.filename}
    - Class name: {unique_name}
    - Use createFileAndWriteMainmCode tool to save the code
    - Complete working Manim v0.19+ code
    """

    prompt = ChatPromptTemplate.from_messages([
        ("system", systemPrompt),
        ("human", "{input}"),
        MessagesPlaceholder(variable_name="agent_scratchpad")
    ])

    agent = create_tool_calling_agent(llmFlash, tools, prompt=prompt)
    agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True, max_iterations=3)

    print(f"--- Creating file: {state.filename} ---")

    try:
        result = agent_executor.invoke({
            "input": human_message,
            "filename": state.filename,
            "class_name": unique_name,
            "animationTypeRule":animationTypeRule,
        })
        print(f"Agent result: {result}")

        filepath = f"./temp/{state.filename}"
        if not os.path.exists(filepath):
            print(f"❌ File was not created: {filepath}")
        else:
            print(f"✅ File created successfully: {filepath}")

    except Exception as e:
        print(f"Agent execution failed: {e}")

    return state

def agentCheckFileCode(state: mainmState):
    code= read_file(state.filename)
    message = state.description
    systemPrompt = """
    You are a Manim v0.19+ code validator. Your job is to analyze Python code for potential execution errors.

    **VALIDATION FOCUS:**
    1. Syntax correctness for Manim v0.19+
    2. Import statement validity
    3. Deprecated method usage detection
    4. LaTeX syntax in MathTex (must use raw strings)

    **CRITICAL CHECKS:**
    - No `.to_center()` methods (use `.move_to(ORIGIN)`)
    - No deprecated imports (import from `manim` directly)
    - MathTex uses raw strings: `MathTex(r"x^2")` not `MathTex("x^2")`
    - Proper tool calling syntax
    - Do not set `opacity` in the constructor; use `.set_opacity()` after creation.

    **CODE TO VALIDATE:**
    ```python
    {code}
    ```

    **TASK:**
    Return a JSON object with:
    - "is_code_good": true/false
    - "error_message": "" if good, otherwise specific issue found

    Focus on execution-breaking errors, not style preferences.
    """
    structured_llm = llmFlash.with_structured_output(CheckMaimCode)
    print("\n--- Checking Code file ---")



    messages = [
        SystemMessage(content=systemPrompt.format(
        code=code,
        )),
        HumanMessage(content=f"{message}")
    ]
    evaluationResult = structured_llm.invoke(messages)

    state.isCodeGood = evaluationResult.isCodeGood
    if not evaluationResult.isCodeGood:
        state.validationError = evaluationResult.errorMessage
        state.validationErrorHistory.append(evaluationResult.errorMessage)
    else:
        state.validationError = None
    print("\n--- Agent Final Answer (Structured Object) ---")
    print(f"Type of result: {type(evaluationResult)}")
    print(f"Is Code Good: {state.isCodeGood}")
    print(f"Error Message: {state.validationError}")
    return state


def agentReWriteManimCode(state: mainmState):
    tools = [createFileAndWriteMainmCode]
    animationTypeRule = ANIMATION_MAP.get(state.animationType)
    filename = state.filename
    validationError = state.validationError
    validationErrorHistory = state.validationErrorHistory
    executionErrorHistory = state.executionErrorHistory
    executionError = state.executionError
    description = state.description
    state.rewriteAttempts += 1
    code = read_file(filename)


    systemPrompt = """
You are a Manim v0.19+ code debugger. Your job is to fix the broken code based on error analysis and provide error free Optimise code

Note:
    1. Ensure that all text objects do not overlap with the graph, other text, or any other objects in the scene.

    2. Your task is to fix the broken code and output **only valid Python code**. 
    **DO NOT** include explanations, markdown, comments, or any extra text. 

**CURRENT CODE TO FIX:**
```python
{code}
```

**ERROR ANALYSIS:**
Current Execution Error: {executionError}
Current Validation Error: {validationError}
Previous Execution Failures: {executionErrorHistory}
Previous Validation Failures: {validationErrorHistory}

**TARGET WHAT THE USER WANT:** {description}

### ANIMATION RULES - Follow these specific guidelines:
{animationTypeRule}


**FIX STRATEGY:**
1. Identify the root cause from error messages above
2. Apply Manim v0.19+ correct syntax from CRITICAL section
3. Ensure no deprecated methods (.to_center(), .get_graph(), etc.)
4. Use proper imports: `from manim import Scene, Text, Create, etc.`
5. Fix layout issues with .next_to(), .arrange(), .move_to(ORIGIN)
6. Use raw strings for MathTex: `MathTex(r"x^2")`


**TASK:**
1. Generate the corrected code that fixes ALL errors listed above
2. Call createFileAndWriteMainmCode with:
   - filename: "{filename}"
   - content: [fixed code as string]

Focus on making the code execute without errors while following v0.19+ syntax.
"""

    prompt = ChatPromptTemplate.from_messages([
        ("system", systemPrompt),
        ("human", "Fix the code to eliminate all errors and make it execute successfully."),
        MessagesPlaceholder(variable_name="agent_scratchpad")
    ])

    agent = create_tool_calling_agent(llmFlash, tools, prompt)
    agentExecutor = AgentExecutor(agent=agent, tools=tools, verbose=True, max_iterations=3)

    try:
        result = agentExecutor.invoke({
            "code": code,
            "executionError": executionError or "None",
            "validationError": validationError or "None",
            "executionErrorHistory": executionErrorHistory,
            "validationErrorHistory": validationErrorHistory,
            "description": description,
            "filename": filename,
            "animationTypeRule":animationTypeRule,
        })
        print(f"\n--- Rewrite attempt #{state.rewriteAttempts} completed ---")
        print(result.get('output', 'No output'))
    except Exception as e:
        print(f"Rewrite failed: {e}")

    return state

def agentRunManimCode(state: mainmState):
    code = read_file(state.filename)
    state.code = code
    resultMessage = run_manim_scene(filename=state.filename, state=state)
    print(f"Execution Result: {resultMessage}")


    if "MANIM EXECUTION FAILED" in resultMessage:
        state.executionSuccess = False
        state.executionError = resultMessage
        state.executionErrorHistory.append(resultMessage)
    else:
        state.executionSuccess = True
        state.executionError = ""

        state.executionErrorHistory.clear()
        state.validationErrorHistory.clear()
        state.validationError = None

    return state


def manimRouter(state: mainmState):
    if state.isCodeGood is True:
        return "agentRunManimCode"
    elif state.rewriteAttempts >= 3:
        print("Rewrite limit reached. Ending graph.")
        # return END
        return "limit_reached"
    else:
        return "agentReWriteManimCode"

def executionRouter(state: mainmState):
    """Routes the graph after a Manim execution attempt."""
    if state.executionSuccess:
        print("✅ Manim execution successful. Ending graph.")
        return "done"
    else:
        # Prevent infinite loops
        if state.rewriteAttempts >= 3:
            print("Rewrite limit reached after execution failure. Ending graph.")
            return "limit"
        print("Manim execution failed. Routing to rewrite node.")
        return "fix"


def handleFailureAndReset(state: mainmState) -> mainmState:
    """Resets the attempt counter to start the entire process over."""
    if state.createAgain >= 1:
        return END
    else:
        print(f"Maximum rewrite attempts reached. Resetting and starting over.")
        state.rewriteAttempts  = 0
        state.createAgain += 1
        return state

def shouldStartOverRouter(state: mainmState):
    """Checks the 'createAgain' flag to decide the next step."""
    if state.createAgain == 1:
        print("Starting the process over one time.")
        return "agentCreateFile" # Loop back to the beginning
    else:
        print("Full retry and start-over process failed. Ending.")