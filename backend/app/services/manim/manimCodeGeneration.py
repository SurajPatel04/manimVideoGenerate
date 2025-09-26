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

load_dotenv()

MANIM_RENDER_TIMEOUT = 1000
critical = """
<CRITICAL>:You MUST write code that is compatible with Manim v0.19+ ONLY. Do NOT use any deprecated or removed methods..

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

Here is the Correct Code example
from manim import *

class Animation_148b09e8(ThreeDScene):
    def construct(self):
        # Layout Plan:
        # 1. ThreeDAxes will be centered at the origin.
        # 2. The title (parametric equations) will be placed at the top of the screen (UP * 3.5) to avoid overlap with the 3D objects.
        # 3. The torus surface will be created at the origin, within the axes.

        # Step 1: Create ThreeDAxes and set up the camera
        self.camera.background_color = BLACK
        self.set_camera_orientation(phi=75 * DEGREES, theta=-45 * DEGREES, distance=10)

        axes = ThreeDAxes(
            x_range=[-5, 5, 1],
            y_range=[-5, 5, 1],
            z_range=[-3, 3, 1],
            x_length=10,
            y_length=10,
            z_length=6,
        )
        self.add(axes)

        # Step 2: Display the parametric equations as a title
        title = VGroup(
            MathTex(r"x = (R + r \cos v) \cos u", font_size=36),
            MathTex(r"y = (R + r \cos v) \sin u", font_size=36),
            MathTex(r"z = r \sin v", font_size=36)
        ).arrange(DOWN, buff=0.2)
        
        # Use add_fixed_in_frame_mobjects to keep the title static
        self.add_fixed_in_frame_mobjects(title)
        title.to_corner(UL)

        self.play(Write(title), run_time=2)
        self.wait(1)

        # Step 3: Define constants and create the torus surface
        R = 3
        r = 1

        torus = Surface(
            lambda u, v: np.array([
                (R + r * np.cos(v)) * np.cos(u),
                (R + r * np.cos(v)) * np.sin(u),
                r * np.sin(v)
            ]),
            u_range=[0, 2 * PI],
            v_range=[0, 2 * PI],
            resolution=(32, 32)
        )

        torus.set_style(fill_color=BLUE_D, fill_opacity=0.8, stroke_color=BLUE_E)
        torus.move_to(ORIGIN)

        self.play(Create(torus), run_time=3)
        self.wait(1)

        # Step 4: Rotate the torus around the Z-axis
        self.play(
            Rotate(
                torus, 
                angle=TAU, 
                axis=Z_AXIS, 
                run_time=5, 
                rate_func=linear
            )
        )
        self.wait(2)


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
    Text object has no attribute 'fix_in_frame'
        Fix -- self.add_fixed_in_frame_mobjects(my_text)

    ValueError: Invalid ambient rotation angle.
        Fix: Make sure the angle is a number in radians, not degrees or None.
            Example:
            # self.begin_ambient_camera_rotation(rate=0.2)   
            # OR
            # self.begin_ambient_camera_rotation(rate=0.2, about="theta")  # if specifying axis


    TypeError: Mobject.__init__() got an unexpected keyword argument 'z_range'
    Axes → 2D (takes only x_range, y_range).
    ThreeDAxes → 3D (takes x_range, y_range, z_range).

    TypeError: Mobject.__init__() got an unexpected keyword argument 'x_range'
        Fix: replace Surface with ParametricSurface and use u_range, v_range.

    Invalid ambient rotation angle.
      fix: self.begin_ambient_camera_rotation(rate=0.1, about="theta")

    AttributeError: ThreeDAxes object has no attribute 'add_numbers'
        Fix: ThreeDAxes in Manim v0.19+ does not have .add_numbers(). Use .add_coordinates() instead.

    NameError: name 'Color' is not defined
        Fix: from manim import Color

    NameError: name 'LEFT' is not defined
        In Manim, these direction vectors are predefined, but you must import them explicitly.
in Manim v0.19+, you should import directly below mention from the top-level manim package. like this from manim import , DirectionalLight,
    This includes:
    Scene types: Scene, ThreeDScene
    3D objects: Cube, Sphere, ParametricSurface
    Lights: DirectionalLight,
    2D objects: Circle, Square, Text, MathTex, etc.
    Animations: Create, Write, FadeIn, Transform, etc.
    Axes & plots: Axes, NumberPlane

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

        anim.add_ambient_camera_rotation(rate=0.1)  #WRONG

        Correct usage:
            class MyScene(ThreeDScene):
            def construct(self):
                cube = Cube()
                self.add(cube)
                self.add_ambient_camera_rotation(rate=0.1)  # add rotation to the scene
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
        self.move_camera() returns None, so play() sees None → error.
        Fix: Either animate the camera with .animate inside play():
        self.play(
            phase_tracker.animate.set_value(4 * PI),
            self.camera.frame.animate.set_phi(self.camera.get_phi() + 10 * DEGREES)
        )
        or call move_camera() separately:
        self.play(phase_tracker.animate.set_value(4 * PI))
        self.move_camera(phi=self.camera.get_phi() + 10 * DEGREES, run_time=2)
        Never pass move_camera() directly into play().

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
        Use self.move_camera(phi=…, theta=…, run_time=…) in ThreeDScene.
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
    -- NameError: name 'LIGHT_BLUE' is not defined fix: LIGHT_BLUE is undefined in Manim v0.19+; use BLUE_E or define it with Color("#ADD8E6").

    -- TypeError: Mobject.apply_points_function_about_point() got an unexpected keyword argument 'scale_tips'
        Fix: Remove scale_tips and, if you need arrow tip scaling, set it separately with arrow.set_tip_length() or use Arrow/Vector with custom tip size.

    -- TypeError: Unexpected argument None passed to Scene.play().
        Fix: don’t put it inside self.play().
            Example:
            self.play(LaggedStart(*[GrowArrow(a) for a in arrows]))
            self.move_camera(phi=new_phi, theta=-45*DEGREES, run_time=2)

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

    -- TypeError: Mobject.__init__() got an unexpected keyword argument 'x_range'
        Fix
        # from manim import NumberLine
        # line = NumberLine(x_range=[-5, 5, 1])

    -- TypeError: Mobject.__init__() got an unexpected keyword argument 'color_map'
        Correct way
        surface = Surface(func, x_range=[-3, 3], y_range=[-3, 3])
        surface.set_fill_by_value(axes=axes, colors=colors)  # or use set_color method

    -- TypeError: Surface.set_fill_by_value() missing 1 required positional argument: 'axes'
        Correc Way: axes must be provided to set_fill_by_value.
        surface = Surface(func, x_range=[-3, 3], y_range=[-3, 3])
        surface.set_fill_by_value(axes=axes, colors=colors)

    -- ValueError: Unsupported keyword argument(s): min_value, max_value
        Error: min_value / max_value are not valid for set_fill_by_value() in surface.
        Correct Way:
        surface.set_fill_by_value(
            axes=axes,
            colorscale=[(BLUE, -1), (GREEN, 0), (RED, 1)],  # map color to specific z-values
            axis=2
        )


    -- ValueError: Unsupported keyword argument(s): h_range
        Correct Way: Replace h_range, replaces h_range, v_min, v_max with axis set_fill_by_value.
            Example:
                surface.set_fill_by_value(
                    axes=axes,
                    colorscale=[(BLUE, -1), (GREEN, 0), (RED, 1)],  # (color, value) pairs
                    axis=2  # use z-axis for coloring
                )
                surface.set_opacity(0.8)

    -- TypeError: Mobject.__init__() got an unexpected keyword argument 'z_range'
        Use only x_range and y_range

    -- ValueError: operands could not be broadcast together with shapes (16,) (3,) (16,)
        Your func must return 3D coords, not just z.
        def func(x, y):
            return np.array([x, y, np.sin(x) * np.cos(y)])

    --TypeError: Mobject.__getattr__.<locals>.setter() got an unexpected keyword argument 'x_label'
        Fix: Don’t pass x_label in the constructor; instead, add it after creating the axes:
        axes = Axes(x_range=[-5,5,1], y_range=[-3,3,1])
        x_label = axes.get_x_axis_label("x")
        self.add(axes, x_label)

    -- AttributeError: 'ThreeDCamera' object has no attribute 'frame'
        HOW TO FIX
        In 3D scenes, don’t use .frame.
        Use self.set_camera_orientation(...) or self.move_camera(...) instead.

    -- ValueError: Called Scene.play with no animations
        Scene.play() must have at least one animation.
        self.play() → error
        self.play(Create(obj)) or self.play(FadeIn(obj)) → correct

    -- 'ThreeDCamera' object has no attribute 'get_distance'
        Use self.camera.distance to access or set the camera distance instead.

    -- name 'QuadraticBezier' is not defined
        How to fix
        Manim 0.19+ → use Bezier([p0, p1, p2]) instead

    -- Exception: Cannot call Mobject.point_from_proportion for a Mobject with no points
        Only call point_from_proportion() on mobjects with a path (like Line, Circle, Bezier).
        circle = Circle()
        dot = Dot(circle.point_from_proportion(0.25))

    -- Unexpected argument None passed to Scene.play().
        Correct way:
        self.play(obj.animate.shift(RIGHT))  # no None
    -- name 'DirectionalLight' is not defined
        Use AmbientLight or PointLight instead.

    -- NameError: name 'PBRMaterial' is not defined
        PBRMaterial doesn’t exist in Manim.
        Use instead:
            sphere = Sphere()
            sphere.set_fill(color=BLUE, opacity=0.8)
            sphere.set_stroke(color=WHITE, width=1)
        Replace material=PBRMaterial() with .set_fill(...) / .set_stroke(...).

    -- does not exist in Manim CE:
        FadeInFromPixels
        FadeOutToPixels
        PixelateIn
        PixelateOut

        Use FadeIn / FadeOut instead.

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

    if not os.path.exists(filepath):
        return f"Error: File '{filepath}' not found."

    command = ["manim", "render", filepath, scene_name, "--format", output_format, "--custom_folders"]
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

        full_output = ""
        for line in process.stdout:
            print(line, end='')
            full_output += line

        process.wait()

        if process.returncode != 0:
            logger.error("MANIM EXECUTION FAILED for file '%s'. Full output:\n%s", full_output, exc_info=True)
            return f"MANIM EXECUTION FAILED. The file '{filename}' has an error. Review output below:\n\n{full_output}"

        print("--- Finished rendering successfully ---")
        return f"Manim render completed for {filename}."

    except FileNotFoundError:
        return "Error: 'manim' command not found. Is Manim installed and in your PATH?"

def agentCreateFile(state: mainmState):
    tools = [createFileAndWriteMainmCode]

    # Generate unique name first
    unique_name = f"Animation_{uuid.uuid4().hex[:8]}"
    state.filename = f"{unique_name}.py"

    systemPrompt = """
    You are a Manim code generation expert. Your task is to:
    1. Create complete, working Manim v0.19+ code, Do not include any explanation, markdown, or extra text. Output only valid Manim Python code
    2. You MUST call the tool `createFileAndWriteMainmCode` with:
     - The filename MUST be exactly: {filename}
     - The class name MUST be exactly: {class_name}

Note:
    - All code must use real newlines and proper indentation (no literal \\n outside strings).
    - Use only valid and non-deprecated Manim methods.
    - The code must be ready to run as a `.py` file without syntax errors.
`

    Must DO thing because it is critical: You MUST call the createFileAndWriteMainmCode tool with:
    - filename: "{filename}"
    - content: [complete Python code as string]

    Important below is the error you got the most so i am providing error with the fix so avoid these error 
    {critical}
    {important}
    {mandatoryChecklist}
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
        ("system", systemPrompt.format(
            filename=state.filename,
            class_name=unique_name,
            critical=critical,
            important=important,
            mandatoryChecklist=mandatoryChecklist
        )),
        ("human", "{input}"),
        MessagesPlaceholder(variable_name="agent_scratchpad")
    ])

    agent = create_tool_calling_agent(llmPro, tools, prompt=prompt)
    agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True, max_iterations=3)

    print(f"--- Creating file with Gemini 2.5 Pro: {state.filename} ---")

    try:
        result = agent_executor.invoke({"input": human_message})
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
    4. Layout/positioning issues that cause overlaps
    5. LaTeX syntax in MathTex (must use raw strings)

    **CRITICAL CHECKS:**
    - No `.to_center()` methods (use `.move_to(ORIGIN)`)
    - No deprecated imports (import from `manim` directly)
    - MathTex uses raw strings: `MathTex(r"x^2")` not `MathTex("x^2")`
    - Proper tool calling syntax
    - No overlapping object placement but check correctly 
    - Ensure that no mobjects visually overlap unless intended.
    - Do not set `opacity` in the constructor; use `.set_opacity()` after creation.
    - All objects stay within frame boundaries

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
        code=code
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
    filename = state.filename
    validationError = state.validationError
    validationErrorHistory = state.validationErrorHistory
    executionErrorHistory = state.executionErrorHistory
    executionError = state.executionError
    description = state.description
    state.rewriteAttempts += 1
    code = read_file(filename)

    print(f"Rewrite attempt #{state.rewriteAttempts}")
    print(f"Execution errors: {executionErrorHistory}")
    print(f"Validation errors: {validationErrorHistory}")

    systemPrompt = """
You are a Manim v0.19+ code debugger. Your job is to fix the broken code based on error analysis 

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

Important below is the error you got the most so i am providing error with the fix so avoid these error 
{critical}]


**IMPORTANT GUIDELINES:**
{important}

**FIX STRATEGY:**
1. Identify the root cause from error messages above
2. Apply Manim v0.19+ correct syntax from CRITICAL section
3. Ensure no deprecated methods (.to_center(), .get_graph(), etc.)
4. Use proper imports: `from manim import Scene, Text, Create, etc.`
5. Fix layout issues with .next_to(), .arrange(), .move_to(ORIGIN)
6. Use raw strings for MathTex: `MathTex(r"x^2")`

**MANDATORY CHECKLIST:**
{mandatoryChecklist}

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

    agent = create_tool_calling_agent(llmPro, tools, prompt)
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
            "critical": critical,
            "important": important,
            "mandatoryChecklist": mandatoryChecklist
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