
from langgraph.prebuilt import create_react_agent
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
    CheckMaimCode,
    MatchCheck
)
from app.core.llm import (
    llmPro,
    llmFlash,
    llmFlashLite,
    llmOpenAI
)
from langchain_core.tools import tool
from dotenv import load_dotenv
from langgraph.graph import END
import os
import subprocess
import glob
import ast
import base64
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
    TEXT,
)
ANIMATION_MAP = {
    AnimationType.GRAPH2D: GRAPH2D,
    AnimationType.COMPUTER_DATASTRUCTURE: COMPUTER_DATASTRUCTURE,
    AnimationType.GRAPH3D: GRAPH3D,
    AnimationType.STATISTICS: STATISTICS,
    AnimationType.PHYSICS: PHYSICS,
    AnimationType.TEXT: TEXT,
}

load_dotenv()

MANIM_RENDER_TIMEOUT = 1000
critical = r"""
<CRITICAL>
Write code compatible with Manim v0.20+ ONLY. No deprecated/removed methods.

## GENERAL
- Always `from manim import *` and `import numpy as np`. Import everything from top-level manim (never manim.mobject / manim.mobjects).
- Keep all content in frame. Decimals: 2 places max. Transitions smooth.
- Background: `self.camera.background_color = BLACK` (NOT set_background). Camera.background_color CANNOT be animated — it has no `.animate`. Change it instantly with assignment.

## REMOVED / RENAMED (do not use the old names)
- `ParametricSurface` → `Surface`
- `ShowCreation` → `Create`
- `axes.get_graph(...)` → `axes.plot(...)`
- `AmbientLight`, `PointLight`, `DirectionalLight` and `manim.mobject.three_d.light` → REMOVED. Lighting is automatic; adjust with `self.renderer.camera.light_source.move_to([x,y,z])` if needed. Do NOT import these.
- `PBRMaterial`, `Text3D` → do not exist. Style with `.set_fill`/`.set_stroke`; for flat text in 3D use Text + `add_fixed_in_frame_mobjects`.
- `set_background` (Scene method) → removed.

## CONSTRUCTOR RULES (most common errors)
- Opacity/stroke NOT in constructor → set after: `c = Circle(); c.set_opacity(0.8)`. (fill_opacity in constructor is OK.)
- Removed kwargs (set via methods instead): `opacity`, `numbers`, `line_config`, `vector`, `start_vector`, `disappearing_time`, axis kwargs on generic Mobjects.
- 2D axes: `Axes(x_range=[...], y_range=[...])` only. 3D: `ThreeDAxes`. Circle/Line/Square do NOT take u_range/v_range.
- Surface: `resolution=(n,n)` (NOT res_u/res_v), `u_range`/`v_range`.
- Axis labels: create axes first, then `axes.get_x_axis_label(MathTex("x"))` / `get_y/get_z`. Don't pass label kwargs into Axes().
- next_to: `mobj.next_to(target, RIGHT, buff=1.0, aligned_edge=UP)` (no `align_l`).

## CAMERA & 3D (v0.20)
- The base Camera object (Scene) has NO `.animate` at all. You CANNOT do `self.camera.animate.anything(...)`. To change background color, just assign: `self.camera.background_color = BLACK` (instant, NOT inside self.play()).
- 3D camera (ThreeDScene) also has NO `.animate`. Use `self.set_camera_orientation(phi=.., theta=.., zoom=..)` or `self.move_camera(phi=.., theta=.., zoom=.., run_time=..)`.
- NEVER pass `move_camera(...)` into `self.play()` (it returns None → ValueError). Call it on its own line.
- `distance=` removed → use `zoom=` or `focal_distance=`. No `gamma` needed normally.
- 2D camera (MovingCameraScene): `self.play(self.camera.frame.animate.scale(s).move_to(p))`.
- `self.play()` must get ≥1 animation: `self.play(Create(obj))`.
- For 3D shapes (Cone, Cylinder, Surface), the `color` parameter only changes the wireframe/stroke. To change the solid fill color, you MUST use `checkerboard_colors=[YOUR_COLOR, YOUR_COLOR]` (e.g., `checkerboard_colors=[ORANGE, ORANGE]`).

## SPECIFIC FIXES
- Scene clearing: NEVER do `self.play(*[FadeOut(m) for m in self.mobjects])` as it causes a zip() ValueError. Instead, group specific objects to fade out, or just end the scene.
- TracedPath: `TracedPath(traced_point_func=lambda: bob.get_center(), dissipating_time=3)` then `self.add(trace)`.
- Updaters must take dt: `def upd(mob, dt): mob.rotate(dt)`.
- ThreeDAxes: no `add_numbers` → use `.add_coordinates()`.
- Colors: undefined names like `MY_CUSTOM_COLOR_NAME` → use built-ins (BLUE_E, TEAL...). If the description explicitly asks for a generic color like "LIGHT_BLUE", DO NOT use `LIGHT_BLUE` as a variable; you MUST map it to a built-in ManimColor constant (like `BLUE_C` or `TEAL`). If using `interpolate_color`, you MUST pass ManimColor constants (like BLUE, YELLOW), NEVER pass a hex string or text string.
- Bezier: `CubicBezier.add_tip()` removed (use Arrow/CurvedArrow); use `Bezier([p0,p1,p2])`.
- Grid overflow: `group.arrange_in_grid(rows=3, cols=2)`.
- Direction constants: UL/UR/DL/DR (not UP_LEFT). UP/DOWN/LEFT/RIGHT/ORIGIN valid.
- Arrow3D: Arrow3D is a 3D mesh (not a 2D VMobject). It does NOT accept `stroke_width`, `max_stroke_width_to_length_ratio`, or `max_tip_length_to_length_ratio`. The only valid arguments are: `start`, `end`, `thickness` (default 0.02), `height` (default 0.3), `base_radius` (default 0.08), `color`, and `resolution`.

## LaTeX (strict — these cause most failures)
- All MathTex/Tex use raw strings: `MathTex(r"x^2")`. Plain words → Text(); math → MathTex(). Never mix.
- MathTex wraps content in math mode ALREADY. NEVER put \begin{align*}...\end{align*}, \begin{equation}, or $...$ inside MathTex.
- For multi-line equations, do NOT use one big align block. Create SEPARATE MathTex objects, one per line, and stack them:
    lines = VGroup(MathTex(r"a=b"), MathTex(r"c=d")).arrange(DOWN, aligned_edge=LEFT)
- If you MUST align multiple lines in one object, use Tex with an explicit environment, NOT MathTex: `Tex(r"\begin{align*} a &= b \\ c &= d \end{align*}")`
- Keep each equation short. Prefer \tfrac over \frac.
- If "latex error converting to dvi": simplify the LaTeX. Literal ° should be ^\circ.

## REQUIRED OUTPUT
1. Begin with a commented layout plan (placement + spacing to avoid overlap).
2. Full runnable Manim v0.20+ code, 2D or 3D as appropriate.
3. Class name MUST match the filename (without .py).
4. Save via the provided file tool.
</CRITICAL>
"""
important = r"""
<IMPORTANT>
Import everything from the top-level manim package: `from manim import *`.
Never use deprecated paths like `manim.mobject` or `manim.mobjects`.
Do NOT import removed classes: ParametricSurface (use Surface), PointLight / AmbientLight / DirectionalLight (lighting is automatic in v0.20).
</IMPORTANT>
"""

mandatoryChecklist = r"""**VERIFY BEFORE SAVING:**
✓ No .to_center() — use .move_to(ORIGIN) or .to_edge()
✓ No overlaps — use .next_to() / .arrange()
✓ axes.plot() not get_graph(); Create not ShowCreation
✓ Opacity/stroke set AFTER construction, not in constructor
✓ All MathTex use raw strings r"..."; Text() for words, MathTex() for math (never mixed)
✓ Compatible with Manim v0.20+; `from manim import *` at top
✓ No removed classes (ParametricSurface→Surface; no AmbientLight/PointLight/DirectionalLight)
✓ 3D camera via set_camera_orientation/move_camera (no .animate); zoom not distance
✓ Class name matches filename
"""

MAX_REWRITE_ATTEMPTS = 3

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
def applyPatch(filename: str, edits: list):
    """Apply small edits to a Manim file. edits = list of {"old": str, "new": str}.
    Each 'old' must be copied EXACTLY from the current code and be UNIQUE."""
    print("****************** Applying patch ****************")
    filepath = f"./temp/{filename}"
    if not os.path.exists(filepath):
        return {"ok": False, "error": f"file not found: {filepath}"}

    with open(filepath, "r", encoding="utf-8") as f:
        code = f.read()

    for i, e in enumerate(edits, 1):
        old, new = e.get("old", ""), e.get("new", "")
        print(f"\n--- ATTEMPTING Patch Edit {i} ---")
        print(f"OLD:\n{old}\nNEW:\n{new}")

        if not old:
            print("=> FAILED: empty 'old' string")
            return {"ok": False, "error": f"empty 'old' string in edit {i}"}
        count = code.count(old)
        if count == 0:
            print("=> FAILED: patch target NOT FOUND (string didn't match perfectly)")
            return {"ok": False, "error": f"patch target NOT FOUND (copy it exactly): {old[:80]!r}"}
        if count > 1:
            print(f"=> FAILED: patch target NOT UNIQUE ({count}x in file)")
            return {"ok": False, "error": f"patch target NOT UNIQUE ({count}x), add more surrounding context: {old[:80]!r}"}
        
        print("=> SUCCESS: Patch applied in memory")
        code = code.replace(old, new, 1)

    try:
        ast.parse(code)
    except SyntaxError as e:
        print(f"=> FAILED: SyntaxError introduced by patch: {e.msg} (line {e.lineno})")
        return {"ok": False, "error": f"patch produced invalid syntax: {e.msg} (line {e.lineno}). Re-check your edit."}

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(code)
        
    print(f"\n--- FINAL CODE SAVED TO {filename} AFTER PATCH ---")
    print(code)
    print("--------------------------------------------------\n")
    return {"ok": True, "message": "patch applied"}

@tool
def read_current_file(filename: str):
    """Read the full current code if you need the whole file to rewrite it."""
    return read_file(filename)

@tool
def overwriteEntireFile(filename, content):
    """This tool is used to completely OVERWRITE a file with new Manim code. 
    Do NOT use this for small edits — use applyPatch instead. 
    Only use this when you need to write the file for the first time, or when you need to rewrite the entire file from scratch."""
    print("****************** Creating/Overwriting a file ****************")
    print(f"\n--- FULL CODE WRITTEN TO {filename} ---")
    print(content)
    print("--------------------------------------------------\n")
    if not os.path.exists("./temp"):
        os.makedirs("./temp")

    filepath = f"./temp/{filename}"
    try:
        with open(filepath, "w") as f:
            f.write(content)
        return f"Successfully created file: {filepath}"
    except IOError as e:
        return f"Error writing to file: {e}"


import subprocess
import os
import re
import ast
import json

MAX_REWRITE_ATTEMPTS = 3

# --- error classification ---
ERROR_PATTERNS = {
    "LATEX_FAILED":      [r"latex error", r"LaTeX Error", r"! Undefined control sequence", r"dvisvgm", r"No such file.*\.tex"],
    "DEPRECATED_API":    [r"has no attribute", r"is deprecated", r"unexpected keyword argument", r"takes no arguments"],
    "NAME_ERROR":        [r"NameError", r"is not defined"],
    "IMPORT_ERROR":      [r"ImportError", r"ModuleNotFoundError", r"cannot import name"],
    "TYPE_ERROR":        [r"TypeError"],
    "VALUE_ERROR":       [r"ValueError"],
    "ATTRIBUTE_ERROR":   [r"AttributeError"],
    "NO_SCENE":          [r"No scenes? inside", r"There are no scenes"],
}

def classify_error(text: str) -> str:
    for category, patterns in ERROR_PATTERNS.items():
        for p in patterns:
            if re.search(p, text, re.IGNORECASE):
                return category
    return "UNKNOWN"

def parse_traceback(output: str) -> dict:
    """Pull the meaningful part out of manim/python output."""
    lines = output.splitlines()

    tb_start = None
    for i, line in enumerate(lines):
        if line.strip().startswith("Traceback (most recent call last)"):
            tb_start = i
    traceback_block = "\n".join(lines[tb_start:]) if tb_start is not None else ""

    error_type, error_message = None, None
    for line in reversed(lines):
        m = re.match(r"^(\w+(?:Error|Exception|Warning)):\s*(.*)$", line.strip())
        if m:
            error_type, error_message = m.group(1), m.group(2)
            break

    line_number = None
    for line in reversed(lines):
        m = re.search(r'File ".*temp/.*\.py", line (\d+)', line)
        if m:
            line_number = int(m.group(1))
            break

    return {
        "error_type": error_type,
        "error_message": error_message,
        "line_number": line_number,
        "traceback": traceback_block or "\n".join(lines[-25:]),  # fallback: last 25 lines
    }

def run_manim_scene(filename, state: mainmState, mode: str = "production"):
    """
    mode="check"      -> fast validation render, writes NO video (for the debug loop)
    mode="production" -> your real render, produces the file you upload/send
    """
    print(f"****************** running manim ({mode}) ****************")
    filepath = f"./temp/{filename}"
    scene_name = filename.replace(".py", "")

    if not os.path.exists(filepath):
        return {"success": False, "category": "FILE_NOT_FOUND",
                "error_type": "FileNotFound", "error_message": f"{filepath} not found",
                "line_number": None, "traceback": "", "raw_tail": ""}

    if mode == "check":
        command = ["manim", "render", filepath, scene_name,
                   "-ql", "--custom_folders", "--format", "mp4", "--progress_bar", "none"]
    else:
        output_format = state.format
        width, height = (state.resolution or "1920x1080").split("x")
        command = ["manim", "render", filepath, scene_name,
                   "--format", output_format, "--custom_folders",
                   "-r", f"{width},{height}",
                   f"-{state.quality}", "--progress_bar", "none"]

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

        try:
            process.wait(timeout=300)
        except subprocess.TimeoutExpired:
            process.kill()
            logger.error("MANIM EXECUTION TIMEOUT (%s) for file '%s'.", mode, filename)
            return {"success": False, "category": "TIMEOUT",
                    "error_type": "Timeout",
                    "error_message": f"Render exceeded 300s",
                    "line_number": None, "traceback": "",
                    "raw_tail": "\n".join(full_output.splitlines()[-25:])}

        if process.returncode != 0:
            logger.error("MANIM EXECUTION FAILED (%s) for file '%s'.", mode, filename)
            parsed = parse_traceback(full_output)
            return {
                "success": False,
                "category": classify_error(full_output),
                **parsed,
                "raw_tail": "\n".join(full_output.splitlines()[-25:]),
            }

        print(f"--- Finished {mode} render successfully ---")
        return {"success": True, "filename": filename}

    except FileNotFoundError:
        return {"success": False, "category": "MANIM_NOT_INSTALLED",
                "error_type": "FileNotFoundError",
                "error_message": "'manim' not found in PATH",
                "line_number": None, "traceback": "", "raw_tail": ""}

def salvage_code_from_messages(messages, filepath):
    salvaged_code = None
    for msg in reversed(messages):
        if hasattr(msg, "response_metadata") and msg.response_metadata:
            finish_msg = msg.response_metadata.get("finish_message", "")
            if "Malformed function call: " in finish_msg:
                salvaged_code = finish_msg.split("Malformed function call: ", 1)[-1].strip()
                break
        if hasattr(msg, "content") and isinstance(msg.content, str) and "from manim import" in msg.content:
            salvaged_code = msg.content
            break
            
    if salvaged_code:
        if "```python" in salvaged_code:
            salvaged_code = salvaged_code.split("```python")[1].split("```")[0].strip()
        elif "```" in salvaged_code:
            salvaged_code = salvaged_code.split("```")[1].split("```")[0].strip()
            
        if salvaged_code.startswith("{") and "content" in salvaged_code:
            try:
                import json
                parsed = json.loads(salvaged_code)
                if "content" in parsed:
                    salvaged_code = parsed["content"]
            except:
                pass
                
        if "from manim import" in salvaged_code:
            print("Successfully salvaged code from raw LLM output! Writing to file.")
            if not os.path.exists("./temp"):
                os.makedirs("./temp")
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(salvaged_code)
            return True
    return False

async def generateInitialCode(state: mainmState):
    logger.info("--- NODE RUNNING: generateInitialCode ---")
    tools = [overwriteEntireFile]
    animationTypeRule = ANIMATION_MAP.get(state.animationType)

    unique_name = f"Animation_{uuid.uuid4().hex[:8]}"
    state.filename = f"{unique_name}.py"
    systemPrompt = """
You are a Manim v0.20+ code generation expert.

## OUTPUT
- Output ONLY valid Manim Python code via the tool — no explanation, markdown, or extra text.
- You MUST call `overwriteEntireFile` with:
  - filename: exactly "{filename}"
  - content: the complete Python code as a string
  - The class name MUST be exactly: {class_name}

## CODE REQUIREMENTS
- `from manim import *` and `import numpy as np` at the top.
- Real newlines and proper indentation (no literal \\n outside strings).
- Only valid, non-deprecated Manim v0.20+ methods.
- Ready to run as a .py file with no syntax errors.
- Class name must match the filename (without .py).
- Content should not overlap or be cut off. There should be no broken rendering artifacts such as white lines, gaps, or misplaced elements.

## UNIVERSAL DESIGN
1. Integers preferred; 2 decimals if needed. No literal "π" on axes.
2. No grid unless required. Central/relevant axes only.
3. Keep ALL content inside the frame with ~5% edge margins. Nothing clips.
4. Labels/data must not overlap — use .arrange(), .next_to(), corner placement.
5. Smooth transitions; fully fade out objects before transitioning to a new concept, BUT NEVER fade out the final objects at the very end of the animation. The final frame must show the completed scene.

## ANIMATION-TYPE RULES (authoritative — follow exactly; override the universal notes above on any layout conflict)
{animationTypeRule}
"""

    human_message = f"""
Create a Manim v0.20+ animation for:

{state.description}

- Save it using the overwriteEntireFile tool.
- filename: {state.filename}
- class name: {unique_name}
- Output complete, runnable Manim v0.20+ code that follows the ANIMATION RULES above.
"""

    agentExecutor = create_react_agent(llmFlash, tools=tools)

    messages = [
        SystemMessage(content=systemPrompt.format(
            filename=state.filename,
            class_name=unique_name,
            animationTypeRule=animationTypeRule,
        )),
        HumanMessage(content=human_message)
    ]

    print(f"--- Creating file: {state.filename} ---")

    try:
        result = await retry(
            agentExecutor,
            {"messages": messages},
            retries=3,
            delay=1
        )
        print(f"Agent result: {result}")

        filepath = f"./temp/{state.filename}"
        if not os.path.exists(filepath):
            print(f"File was not created: {filepath}. Attempting salvage...")
            salvaged = salvage_code_from_messages(result.get("messages", []), filepath)
            if not salvaged:
                print("Could not salvage code.")
        else:
            print(f"File created successfully via tool: {filepath}")

    except Exception as e:
        print(f"Agent execution failed: {e}")

    return state

DEPRECATED_PATTERNS = {
    "ShowCreation": "use Create",
    ".get_graph(": "use axes.plot()",
    ".to_center(": "use .move_to(ORIGIN)",
    "ParametricSurface": "use Surface (renamed in v0.20)",
    "set_background": "use self.camera.background_color = COLOR (direct assignment, instant)",
    "self.camera.animate": "Camera has NO .animate attribute. To change background: self.camera.background_color = COLOR (instant assignment, NOT inside self.play()). For 3D camera movement use self.move_camera() or self.set_camera_orientation().",
    "AmbientLight": "removed in v0.20 (auto lighting)",
    "PointLight": "removed in v0.20 (auto lighting)",
    "manim.mobject": "import from top-level manim",
}

KNOWN_FIXES = {
    "get_riemann_rectangles.*(fill_color|sample_type)": "get_riemann_rectangles takes no fill_color or sample_type kwarg. Call get_riemann_rectangles(graph, x_range=[a,b], dx=...) then use rects.set_fill(color, opacity). If you need a specific sample type, use input_sample_type='left'/'center'/'right'.",
    "unexpected keyword argument 'begin'": "Animations (like LaggedStart or FadeIn) do NOT take a 'begin' kwarg in Manim CE. To delay an animation, do not use 'begin='. Instead, split your animations into separate self.play() calls separated by self.wait(), or use Succession(Wait(0.5), YourAnimation()).",
    "has no attribute 'fix_in_frame'": "Mobjects do NOT have a .fix_in_frame() method in Manim CE. To fix text or objects to the camera in a ThreeDScene, use self.add_fixed_in_frame_mobjects(mobject).",
    "run_time of 0 <= 0 seconds": "You cannot use self.play(..., run_time=0). Manim requires run_time > 0. To apply an instant change, just modify the mobject directly (e.g., mobject.move_to(...)) without using self.play(), or use run_time=0.1.",
    "has no attribute '(cap_top|cap_bottom|top_cap|bottom_cap|top_circle|bottom_circle)'": "Cylinder objects do NOT have 'top_cap', 'bottom_cap', 'top_circle', or 'bottom_circle' attributes in Manim. To make a cylinder with different colored ends, either color the entire Cylinder a single color, or manually add Circle objects at the ends of the cylinder.",
    "set_camera_orientation.*distance": "distance= removed; use zoom= or focal_distance=.",
    "ParametricSurface": "renamed to Surface.",
    "get_graph": "use axes.plot().",
    "zip.*argument 2 is shorter": "This happens if you do `self.play(*[FadeOut(m) for m in self.mobjects])` (NEVER do this, just end the scene or group objects explicitly). It also happens when transforming two groups of mismatched lengths (use FadeTransform instead of Transform).",
    "latex error converting to dvi": "LaTeX compile failed. Common causes: (1) \\begin{align*} or $...$ placed INSIDE MathTex (MathTex is already math mode — remove the environment); (2) multi-line align block — split into separate MathTex objects stacked with VGroup.arrange(DOWN); (3) literal ° — use ^\\circ. Simplify the LaTeX.",
    "extra }": "Unbalanced braces, usually from a math environment nested inside MathTex. Remove \\begin/\\end{align*} from MathTex; use separate MathTex per line, or use Tex() for an align environment.",
    "unexpected keyword argument 'num_dashes'": "DashedLine does NOT take a 'num_dashes' kwarg. If you need 'num_dashes', wrap your shape with DashedVMobject(shape, num_dashes=50). If you are using DashedLine(a, b), use 'dash_length' and 'dashed_ratio' instead, or just DashedLine(a, b).",
    "'Camera' object has no attribute '(animate|background_mobject)'": "The base Camera object does not have an .animate or .background_mobject attribute. You cannot do self.camera.animate.set_color(...) or self.camera.background_mobject... To change the background color, use `self.camera.background_color = BLACK` directly (which happens instantly, do NOT put it inside self.play()).",
    "name '.*(BLUE|RED|GREEN|YELLOW|WHITE|BLACK|GREY|PURPLE|PINK|TEAL|GOLD).*' is not defined": "Manim uses specific color constants (e.g., BLUE, BLUE_A, BLUE_C, BLUE_E, YELLOW, RED). It does NOT use generic names like MY_CUSTOM_COLOR_NAME. Change the color name to a standard Manim color constant (like BLUE_C or TEAL). Do NOT pass a string to interpolate_color or to color kwargs; it requires ManimColor constants.",
    "'str' object has no attribute 'interpolate'": "You passed a string (like \"BLUE\" or \"#FFFFFF\") to interpolate_color, but it requires a ManimColor constant (like BLUE or WHITE). Remove the quotes around the color name.",
    "unexpected keyword argument '(max_stroke_width_to_length_ratio|max_tip_length_to_length_ratio|stroke_width)'": "Arrow3D is a 3D mesh (not a 2D VMobject). It does NOT accept `stroke_width`, `max_stroke_width_to_length_ratio`, or `max_tip_length_to_length_ratio`. Change `stroke_width` to `thickness`, and completely remove `max_stroke_width_to_length_ratio` and `max_tip_length_to_length_ratio` from the Arrow3D constructor.",
}

def lookup_fixes(error_message: str) -> str:
    hits = []
    for pattern, fix in KNOWN_FIXES.items():
        if re.search(pattern, error_message, re.IGNORECASE):
            hits.append(f"- {pattern}: {fix}")
    return "\n".join(hits) if hits else ""

def staticCheckCode(state: mainmState):
    logger.info("--- NODE RUNNING: staticCheckCode ---")
    code = read_file(state.filename)

    try:
        ast.parse(code)
    except SyntaxError as e:
        state.isCodeGood = False
        err = f"[SYNTAX_ERROR] {e.msg} (line {e.lineno})"
        state.validationError = err
        state.validationErrorHistory.append(err)
        print(f"--- Static check FAILED: {err} ---")
        return state

    for pattern, fix in DEPRECATED_PATTERNS.items():
        if pattern in code:
            line_no = next((i+1 for i, ln in enumerate(code.splitlines()) if pattern in ln), None)
            state.isCodeGood = False
            err = f"[DEPRECATED_API] '{pattern}': {fix}" + (f" (line {line_no})" if line_no else "")
            state.validationError = err
            state.validationErrorHistory.append(err)
            print(f"--- Static check FAILED: {err} ---")
            return state

    state.isCodeGood = True
    state.validationError = None
    print("--- Static check passed ---")
    return state


def format_history_compact(exec_hist, val_hist):
    """One-line signatures instead of full tracebacks. Big token saving."""
    lines = []
    for h in (exec_hist or [])[-3:]:                      # last 3 only
        lines.append(f"- attempt {h.get('attempt')}: [{h.get('category')}] "
                     f"{h.get('error_type')} at line {h.get('line')}")
    for v in (val_hist or [])[-3:]:
        lines.append(f"- {v[:120]}")                      # validation strings, trimmed
    return "\n".join(lines) if lines else "None"

def code_window(code, line_no, ctx=25):
    """Send only the region around the error if the file is large."""
    lines = code.splitlines()
    if not line_no or len(lines) <= 60:
        return code, False
    lo, hi = max(0, line_no - ctx), min(len(lines), line_no + ctx)
    numbered = "\n".join(f"{i+1}: {l}" for i, l in enumerate(lines[lo:hi], start=lo))
    return f"# (showing lines {lo+1}-{hi} around the error; full file on disk)\n{numbered}", True

async def fixCodeErrorsWithLLM(state: mainmState):
    logger.info("--- NODE RUNNING: fixCodeErrorsWithLLM ---")
    tools = [applyPatch, overwriteEntireFile, read_current_file]
    animationTypeRule = ANIMATION_MAP.get(state.animationType)
    filename = state.filename
    executionError = state.executionError
    validationError = state.validationError
    state.rewriteAttempts += 1
    code = read_file(filename)
    if executionError and isinstance(executionError, dict):
        line_no = executionError.get("line_number")
        exec_err_formatted = (f"[{executionError.get('category','UNKNOWN')}] "
                              f"{executionError.get('error_type')}: {executionError.get('error_message')}\n"
                              f"{executionError.get('traceback','')[:1500]}")
    elif not executionError and validationError:
        line_no = None
        exec_err_formatted = f"[VALIDATION_ERROR]\n{validationError}"
    else:
        line_no = None
        exec_err_formatted = str(executionError) if executionError else "None"

    history = format_history_compact(state.executionErrorHistory, state.validationErrorHistory)

    code_to_show, windowed = code_window(code, line_no)

    error_msg_only = executionError.get("error_message", "") if isinstance(executionError, dict) else str(executionError or "")
    known_fix = lookup_fixes(error_msg_only)
    known_fix_section = f"\n## KNOWN FIX FOR THIS ERROR\n{known_fix}\n" if known_fix else ""

    systemPrompt = """
You are a Manim v0.20+ code debugger. Fix the broken code with the SMALLEST change that works.

## HOW TO FIX (prefer patching)
1. Read the error category + line. Fix THAT specific failure.
2. PREFER the applyPatch tool: pass edits=[{{"old": <exact text from the code>, "new": <replacement>}}].
   - 'old' MUST be copied EXACTLY (whitespace included) and be UNIQUE in the file. Add surrounding lines if needed for uniqueness.
   - Make one edit per distinct fix; you may pass several edits at once.
3. ONLY if the fix requires large/structural rewrites, use overwriteEntireFile with the full corrected file instead.
4. Do NOT repeat a fix listed in PAST FAILURES — if the same error recurs, change your approach.
5. EXPLICIT FALLBACK: If applyPatch returns ok:false twice, STOP patching. Use overwriteEntireFile with read_current_file to do a full rewrite instead.
6. VISION SUGGESTIONS: If the error contains a [FIX_SUGGESTION] from the Vision QA step, treat it as a HINT, not an absolute command. You MUST verify that the suggested syntax is actually valid in Manim v0.20+ (e.g. don't blindly pass a list to TracedPath stroke_color). If the suggestion is hallucinated or invalid, ignore it and write a valid fix that achieves the same visual goal.
7. OVERLAPS: If the Vision QA reports an "overlap" (e.g., title overlapping a 3D object), the absolute best fix is usually to `FadeOut` the text before drawing the large object, or simply remove the text entirely if it's no longer needed.

## QUICK MANIM REMINDERS
- from manim import *; no deprecated methods.
- Camera has NO .animate — use self.camera.background_color = COLOR (instant, NOT inside self.play()).
- 3D camera: self.set_camera_orientation() / self.move_camera(). No .animate on camera.
- MathTex raw strings; Text() for words. Opacity/stroke set after construction.

## ERROR TO FIX
{exec_err_formatted}
{known_fix_section}
## PAST FAILURES (do not repeat)
{history}

## ORIGINAL GOAL & RULES
If you must do a full rewrite, ensure you fulfill this description:
{description}

{animationTypeRule}

## {window_note}CURRENT CODE
# NOTE: "N:" line-number prefixes are for reference only — do NOT include them in your patch 'old' text.
```python
{code_to_show}
```

Fix it. Prefer applyPatch with exact-match edits; use overwriteEntireFile only for large changes.
"""

    agentExecutor = create_react_agent(llmFlash, tools=tools)
    messages = [
        SystemMessage(content=systemPrompt.format(
            exec_err_formatted=exec_err_formatted,
            known_fix_section=known_fix_section,
            history=history,
            description=state.description,
            animationTypeRule=animationTypeRule,
            code_to_show=code_to_show,
            window_note="(windowed) " if windowed else "",
        )),
        HumanMessage(content="Fix the error using applyPatch (preferred). If patches fail repeatedly or a large rewrite is needed, use read_current_file and overwriteEntireFile."),
    ]

    try:
        result = await retry(agentExecutor, {"messages": messages}, retries=3, delay=1)
        print(f"\n--- Rewrite attempt #{state.rewriteAttempts} completed ---")
        filepath = f"./temp/{filename}"
        if not os.path.exists(filepath) or read_file(filename).strip() == "":
            print("File empty after rewrite. Attempting salvage...")
            salvage_code_from_messages(result.get("messages", []), filepath)
    except Exception as e:
        print(f"Rewrite failed: {e}")

    return state

def testRenderCode(state: mainmState):
    logger.info("--- NODE RUNNING: testRenderCode ---")
    code = read_file(state.filename)
    state.code = code
    result = run_manim_scene(filename=state.filename, state=state, mode="check")
    print(f"Check Result: {result}")

    state.executionSuccess = result["success"]
    if not result["success"]:
        state.executionError = result
        state.executionErrorHistory.append({
            "attempt": state.rewriteAttempts,
            "category": result["category"],
            "error_type": result.get("error_type"),
            "line": result.get("line_number"),
            "stage": "check",
        })
    else:
        state.executionError = None

    return state


def extract_sample_frames(filename, state: mainmState, num_frames=3):
    """Finds the generated low-quality video and extracts multiple frames using ffmpeg."""
    scene_name = filename.replace(".py", "")
    mp4s = glob.glob(f"./temp/{scene_name}*.mp4") + glob.glob(f"./media/**/{scene_name}*.mp4", recursive=True) + glob.glob(f"./videos/**/{scene_name}*.mp4", recursive=True)
    video_path = mp4s[-1] if mp4s else None

    if not video_path:
        return []

    try:
        dur_cmd = ["ffprobe", "-v", "error", "-show_entries",
                   "format=duration", "-of",
                   "default=noprint_wrappers=1:nokey=1", video_path]
        duration = float(subprocess.check_output(dur_cmd).decode().strip())
    except Exception:
        duration = 5.0

    out_dir = os.path.dirname(video_path)
    base_name = os.path.basename(video_path).replace(".mp4", "")
    frame_paths = []
    
    t1 = max(0.1, duration - 0.2)
    timestamps = [t1]
    
    for i, ts in enumerate(timestamps):
        out_path = os.path.join(out_dir, f"{base_name}_frame_{i}.jpg")
        cmd = ["ffmpeg", "-y", "-ss", str(ts), "-i", video_path, "-frames:v", "1", "-q:v", "2", out_path]
        subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        if os.path.exists(out_path):
            frame_paths.append((out_path, ts))
            
    return frame_paths

def verifyOutputMatchesDescription(state: mainmState):
    logger.info("--- NODE RUNNING: verifyOutputMatchesDescription ---")
    frame_data = extract_sample_frames(state.filename, state)

    if not frame_data:
        state.matchesRequest = None
        print("--- Match check skipped (no frames extracted) ---")
        return state

    model_name = getattr(llmFlash, 'model', getattr(llmFlash, 'model_name', 'Unknown Model'))
    num_frames = len(frame_data)
    timestamps = [f"{ts:.2f}s" for _, ts in frame_data]
    print(f"--- Vision Check Triggered ---")
    print(f"[VISION] LLM Model: {model_name}")
    print(f"[VISION] Passing {num_frames} frames to LLM at timestamps: {', '.join(timestamps)}")

    content_list = [
        {"type": "text", "text": f"User's original request:\n{state.userQuery}\n\nHere is the final frame of the animation. Does this image broadly show what the user asked for?"}
    ]

    for path, ts in frame_data:
        with open(path, "rb") as f:
            img_b64 = base64.b64encode(f.read()).decode()
            content_list.append({"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{img_b64}"}})

    vision_llm = llmFlash.with_structured_output(MatchCheck)
    messages = [
        SystemMessage(content=(
            "You are checking ONE thing: does this frame show the RIGHT KIND of content for the request? "
            "Return matches=TRUE by default. Return FALSE only if:\n"
            "- the frame is blank/black with nothing on it, OR\n"
            "- it shows a completely different subject than requested, OR\n"
            "- text massively covers the main object making it unreadable.\n"
            "NEVER fail for: axis label values, tick marks, ranges, buffer/margin sizes, exact positions, colors, or anything a reasonable viewer would consider correct. "
            "When in doubt, default to TRUE. "
            "If FALSE, provide a fix_suggestion to help correct it."
        )),
        HumanMessage(content=content_list),
    ]
    result = vision_llm.invoke(messages)
    state.matchesRequest = result.matches

    if not result.matches:
        err = f"[OUTPUT_MISMATCH] {result.reason}"
        if result.fix_suggestion:
            err += f"\n[FIX_SUGGESTION] {result.fix_suggestion}"
        state.validationError = err
        state.validationErrorHistory.append(err)
        print(f"--- Match check FAILED: {err} ---")
    else:
        print(f"--- Match check passed: {result.reason} ---")
    return state


def productionRender(state: mainmState):
    logger.info("--- NODE RUNNING: productionRender ---")
    print("****************** PRODUCTION render ****************")
    result = run_manim_scene(filename=state.filename, state=state, mode="production")
    print(f"Production Result: {result}")

    if not result["success"]:
        state.executionSuccess = False
        state.executionError = result
        state.executionErrorHistory.append({
            "attempt": state.rewriteAttempts,
            "category": result.get("category"),
            "error_type": result.get("error_type"),
            "line": result.get("line_number"),
            "stage": "production",
        })
    else:
        state.executionSuccess = True

    return state


def manimRouter(state: mainmState):
    if state.isCodeGood is True:
        return "testRenderCode"
    elif state.rewriteAttempts >= MAX_REWRITE_ATTEMPTS:
        print("Rewrite limit reached. Ending graph.")
        # return END
        return "limit_reached"
    else:
        return "fixCodeErrorsWithLLM"

def matchRouter(state: mainmState):
    if state.matchesRequest is False:
        if state.rewriteAttempts >= MAX_REWRITE_ATTEMPTS:
            print("Vision failed but out of rewrites. Shipping the video anyway!")
            return "render"
        return "fix"
    return "render" 

def executionRouter(state: mainmState):
    """Routes the graph after a Manim execution attempt."""
    if state.executionSuccess:
        print("Manim execution successful. Ending graph.")
        return "done"
    else:
        if state.rewriteAttempts >= MAX_REWRITE_ATTEMPTS:
            print("Rewrite limit reached after execution failure. Ending graph.")
            return "limit"
        print("Manim execution failed. Routing to rewrite node.")
        return "fix"


def handleFailureAndReset(state: mainmState) -> mainmState:
    """Resets the attempt counter to start the entire process over."""
    logger.info("--- NODE RUNNING: handleFailureAndReset ---")
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
        return "generateInitialCode"
    else:
        print("Full retry and start-over process failed. Ending.")
        return "stop"
