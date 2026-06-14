TEXT = r"""
<TEXT_SCENE_RULES>
Generate a cinematic Manim v0.20+ equation scene using MovingCameraScene.

## HARD RULES
- Class extends `MovingCameraScene` (needed for camera moves).
- `MathTex` always raw string: `MathTex(r"...", font_size=50)`. Plain words use `Text()`. Never mix.
- Arrange any VGroup with `.arrange()` BEFORE `.next_to()`/`.move_to()`.
- Keep content in frame; reposition the camera frame to follow content down the canvas.
- Multi-line math: split into separate MathTex objects, not one giant `\\` block.

## STYLE (apply these for the "cinematic" look)
- Glow titles: layer a colored stroked copy behind the text:
  `glow = Text(t, weight=BOLD).set_color(BLUE).set_stroke(width=15, opacity=0.3)` behind a solid `Text(t)`.
- Camera as director: `self.camera.frame.animate.scale(s).move_to(pos)` with `rate_func=smooth` to pan/zoom between beats.
- Dynamic reveal: use `ValueTracker` + `always_redraw(lambda: DecimalNumber(tracker.get_value(), ...))` to animate a value counting up; emphasize with `Flash`.
- Neon finale: layer expanding fading `SurroundingRectangle`s (corner_radius=0.2, widths [10,20,30] / opacities [0.4,0.2,0.05]) around the answer; finish with `ApplyWave`.
- Colors: ≤4. BOLD titles, accent BLUE/TEAL, results highlighted. Holds ≥1.5s, major moves run_time 1.5–2.

## AVOID
- LaTeX inside Text() or prose in MathTex(); missing `r""`.
- `.next_to()` on un-arranged groups; content drifting off-frame.
- Linear motion on camera (use rate_func=smooth/ease_in_out_sine).

## REFERENCE (study the techniques, don't copy verbatim)
```python
from manim import *
class Demo(MovingCameraScene):
    def construct(self):
        t = Text("Title", font_size=60, weight=BOLD)
        glow = Text("Title", font_size=60, weight=BOLD).set_color(BLUE).set_stroke(width=15, opacity=0.3)
        self.play(FadeIn(glow, scale=1.5), Write(t), run_time=2)
        self.play(self.camera.frame.animate.scale(1.2).move_to(DOWN*3), run_time=2, rate_func=smooth)

        eq = MathTex(r"f(2x-1)+f(2)=4x-1", font_size=50).move_to(DOWN*3)
        self.play(Write(eq))

        tr = ValueTracker(0.0)
        num = always_redraw(lambda: DecimalNumber(tr.get_value(), num_decimal_places=2, color=RED).move_to(DOWN*4.5))
        self.play(FadeIn(num, shift=UP))
        self.play(tr.animate.set_value(1.5), run_time=3, rate_func=ease_in_out_sine)
        self.play(Flash(num, color=RED, num_lines=12))

        self.play(self.camera.frame.animate.scale(0.7).move_to(DOWN*6.5), eq.animate.set_opacity(0.2), run_time=2)
        ans = MathTex(r"f(4)=6.5", font_size=70).move_to(DOWN*6.5)
        box = SurroundingRectangle(ans, color=WHITE, buff=0.4, corner_radius=0.2)
        glow_box = VGroup(*[SurroundingRectangle(ans, color=TEAL, buff=0.4, corner_radius=0.2).set_stroke(width=w, opacity=o)
                            for w, o in zip([10,20,30],[0.4,0.2,0.05])])
        self.play(Write(ans))
        self.play(Create(box), FadeIn(glow_box), run_time=1.5)
        self.play(ApplyWave(ans, amplitude=0.15), run_time=1.5)
        self.wait(3)
```
</TEXT_SCENE_RULES>
"""

GRAPH2D = r"""
<2D_GRAPH_SCENE_RULES>
Generate a Manim v0.20+ 2D graph scene. Extend MovingCameraScene (enables camera moves).

## DESIGN SEQUENCE (mandatory order)
1. Title at ORIGIN center, Write it, wait, then SHRINK + move to top edge (keeps it as context). No equation in the title.
2. Axes after title moves. Central axes only, no grid. Integers on axes; 2 decimals only if needed. No "π" literal. Keep axes ≤78% frame width / ~55% height so labels never clip.
3. Equation(s) in a frame CORNER via `.to_corner(UL/UR/DL/DR, buff=LB)` — NEVER `next_to(axes, LEFT/RIGHT)` (wide axes push it off-frame). Color-code: function and its derivative in matching graph colors.
4. Plot the base graph, then add dynamic tracker-driven elements last.
5. ~5% margin on all edges. Background BLACK unless asked.

## FONT HIERARCHY (never invert)
TITLE 46 > EQUATION 36 > LABEL 28 > DESC 24.
`get_graph_label` takes a mobject: `axes.get_graph_label(graph, label=MathTex(r"x^2", font_size=24))`.

## CLIPPING RULES (most common visual bug — obey strictly)
- Labels/readouts must be anchored to a FIXED corner with `.to_corner(corner, buff=LB)`, NOT `.next_to(moving_dot, ...)` — a label following a dot to the frame edge WILL clip.
- Keep axes narrower than the frame (≤78% width) so corner labels have room.

## CORE API (v0.20 — use these, not old names)
- Plot: `axes.plot(f, x_range=[...], color=...)` (NOT get_graph)
- Parametric: `axes.plot_parametric_curve(lambda t: (x(t), y(t)), t_range=[a,b,step])`
- Point on graph from x: `axes.i2gp(x, graph)`; coords→point: `axes.c2p(x, y)`
- Tangent: `TangentLine(graph, alpha, length=...)`, alpha = (x - x0)/(x1 - x0)
- Trail behind a moving dot: `TracedPath(dot.get_center, stroke_color=..., stroke_width=4)` — `self.add(path)` AFTER creating the dot it tracks.
- Dashed: `DashedLine(a, b, color=...)` (no dash_length kwarg); for shapes `DashedVMobject(m, num_dashes=50)`
- Camera: `self.camera.frame.animate.scale(s).move_to(pos)` with `rate_func=smooth`

## CONSTRUCTOR RULES (cause most crashes)
- stroke opacity NOT in constructor → `.set_stroke(opacity=...)` after. (fill_opacity in constructor is fine.)
- `background_line_style={...}`, `axis_config={...}`, per-axis `x_axis_config={...}` only inside Axes/NumberPlane.
- `resolution=(20,20)` for Surface (NOT res_u/res_v).
- Always `from manim import *` and `import numpy as np`. Use UL/UR/DL/DR (not UP_LEFT). Custom colors as hex (LIGHT_BLUE="#87CEFA").

## STYLE
≤4 colors; match equation color to its graph. Drive motion with `ValueTracker` + `always_redraw`. Sweeps `rate_func=smooth`. Emphasize with `Flash`/`Indicate`. Holds ≥1.5s.

## REFERENCE TEMPLATE (study structure; adapt, don't copy verbatim)
```python
from manim import *
import numpy as np

class GraphScene(MovingCameraScene):
    def construct(self):
        self.camera.background_color = BLACK
        TITLE, EQ, LBL = 46, 36, 28
        LB = config.frame_width * 0.05

        # 1. Title -> shrink to top
        title = Text("Derivative & Tangent", font_size=TITLE, color=WHITE).move_to(ORIGIN)
        self.play(Write(title, run_time=1.5)); self.wait(1)
        self.play(title.animate.scale(0.7).to_edge(UP, buff=0.3))

        # 2. Axes (narrower than frame so labels fit)
        axes = Axes(
            x_range=[-7,7,1], y_range=[-2,2,1],
            x_length=config.frame_width*0.78, y_length=config.frame_height*0.55,
            axis_config={"include_numbers": True, "font_size": 24},
        ).center().shift(DOWN*0.3)
        self.play(Create(axes, run_time=1.5))

        # 3. Color-coded equations, corner-anchored
        eqs = VGroup(
            MathTex(r"f(x)=\sin(x)", color=BLUE, font_size=EQ),
            MathTex(r"f'(x)=\cos(x)", color=GREEN, font_size=EQ),
        ).arrange(DOWN, aligned_edge=LEFT).to_corner(UL, buff=LB).shift(DOWN*0.5)
        self.play(Write(eqs, run_time=1.5))

        # 4. Base graph
        graph = axes.plot(lambda x: np.sin(x), x_range=[-7,7], color=BLUE)
        self.play(Create(graph, run_time=1.5))

        # 5. Dynamic elements
        xt = ValueTracker(-7)
        dot = always_redraw(lambda: Dot(axes.i2gp(xt.get_value(), graph), color=BLUE, radius=0.08))
        tan = always_redraw(lambda: TangentLine(graph, alpha=(xt.get_value()-axes.x_range[0])/(axes.x_range[1]-axes.x_range[0]), length=4, color=YELLOW))
        d_dot = always_redraw(lambda: Dot(axes.c2p(xt.get_value(), np.cos(xt.get_value())), color=GREEN, radius=0.08))
        d_path = TracedPath(d_dot.get_center, stroke_color=GREEN, stroke_width=4)
        vline = always_redraw(lambda: DashedLine(dot.get_center(), d_dot.get_center(), color=GREY_A))
        # slope readout anchored to a FIXED corner (never follows the dot -> never clips)
        slope = always_redraw(lambda: VGroup(
            MathTex(r"m=", font_size=LBL, color=YELLOW),
            DecimalNumber(np.cos(xt.get_value()), num_decimal_places=2, font_size=LBL, color=YELLOW),
        ).arrange(RIGHT, buff=0.1).to_corner(UR, buff=LB))

        self.play(FadeIn(dot), FadeIn(tan), FadeIn(d_dot), FadeIn(vline), FadeIn(slope), run_time=0.5)
        self.add(d_path)  # add trail AFTER its dot exists

        # 6. Sweep
        self.play(xt.animate.set_value(7), run_time=6, rate_func=smooth)
        self.wait(2)

        # 7. Clean up
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1)
        self.wait(1)
```
</2D_GRAPH_SCENE_RULES>
"""

GRAPH3D = r"""
<3D_SCENE_RULES>
Generate a Manim v0.20+ 3D scene. Extend ThreeDScene.

## DESIGN SEQUENCE (mandatory order)
1. Title at ORIGIN center, Write it, wait, then fade out (LaggedStart letter-scatter encouraged). No equation in title.
2. Set camera orientation, then create ThreeDAxes (keep lengths ≤7 so it stays on screen).
3. Axis labels: place at arrow tips with get_x/y/z_axis_label, then pass them to
   `add_fixed_orientation_mobjects(...)` — this keeps them attached to the arrows
   (moving during rotation) while always facing the camera so text never tilts.
   The EQUATION, by contrast, uses `add_fixed_in_frame_mobjects(...)` to stay
   pinned flat in a screen corner. Use orientation-fixed for things that should
   follow the 3D scene, frame-fixed for things that should stay on screen.
4. Surface/graph centered at ORIGIN, then showcase with ambient camera rotation.
5. Background BLACK unless asked.

## CAMERA (v0.20 — old API removed)
- `self.set_camera_orientation(phi=70*DEGREES, theta=-45*DEGREES, zoom=0.9)`
- NEVER use `distance=` (removed in v0.20). Control apparent size with `zoom=` (smaller = see more) or `focal_distance=`.
- Animate camera: `self.move_camera(phi=..., theta=..., zoom=..., run_time=...)`. Do NOT pass move_camera into self.play.
- Spin to showcase: `self.begin_ambient_camera_rotation(rate=0.2)` ... `self.wait(n)` ... `self.stop_ambient_camera_rotation()`. Smoother than Rotate().

## FIXED TEXT (critical — all flat 2D text in a 3D scene)
- Any Text/MathTex meant to face the viewer MUST go through `self.add_fixed_in_frame_mobjects(m)` BEFORE positioning with `.to_corner(...)`. Otherwise it rotates with the 3D camera and looks broken/skewed.
- This applies to the equation AND the axis-label legend.
- Fixed-in-frame text stays put during ambient rotation (it does NOT track the spinning axes) — that's why a corner legend is correct, not labels glued to axis tips.

## SURFACE / OBJECTS
- `Surface(lambda u,v: np.array([u, v, f(u,v)]), u_range=[...], v_range=[...], resolution=(40,40))` (NOT res_u/res_v).
- Opacity NOT in constructor → `.set_fill_opacity(0.85)` / `.set_stroke_opacity(0.3)` after creation.
- Cool height gradient: `surface.set_fill_by_value(axes=axes, colorscale=[(BLUE_E,-1),(TEAL,0),(YELLOW,1)])`. If colorscale errors, try `colors=[...]` or fall back to a solid `fill_color`.
- Box = `Prism(dimensions=[x,y,z])`; cube = `Cube(side_length=...)` (no `Cuboid`).

## FONT HIERARCHY
TITLE 48-60 > EQUATION 36 > LABEL 28-30.

## COMMON FIXES
- `from manim import *` + `import numpy as np` always. UL/UR/DL/DR (not UP_LEFT).
- No 3D `.animate` on camera — use move_camera / set_camera_orientation.
- ≤4 colors. Holds ≥1s.

## REFERENCE TEMPLATE (study; adapt, don't copy verbatim)
```python
from manim import *
import numpy as np

class Surface3D(ThreeDScene):
    def construct(self):
        self.camera.background_color = BLACK
        TITLE, EQ, LBL = 56, 36, 30

        # 1. Title -> scatter fade
        title = Text("3D Surface", font_size=TITLE, color=WHITE).move_to(ORIGIN)
        self.play(Write(title, run_time=1.5)); self.wait(1)
        self.play(LaggedStart(*[l.animate.shift(np.array([np.random.uniform(-2,2), np.random.uniform(-2,2),0])).scale(0.5).set_opacity(0) for l in title], lag_ratio=0.1, run_time=2))

        # 2. Camera + axes (zoom, NOT distance)
        self.set_camera_orientation(phi=70*DEGREES, theta=-45*DEGREES, zoom=0.9)
        axes = ThreeDAxes(x_range=[-3,3,1], y_range=[-3,3,1], z_range=[-2,2,1], x_length=7, y_length=7, z_length=4)
        self.play(Create(axes, run_time=2))

        # 3a. Equation — fixed in frame (flat on screen)
        eq = MathTex(r"f(x,y)=\sin(x)\cos(y)", font_size=EQ, color=WHITE)
        self.add_fixed_in_frame_mobjects(eq)
        eq.to_corner(UL, buff=0.5)
        self.play(FadeIn(eq), run_time=1)

        # 3b. Axis-label legend — fixed in frame (stays flat & readable during spin)
        legend = VGroup(
            MathTex(r"x \rightarrow", font_size=LBL, color=WHITE),
            MathTex(r"y \rightarrow", font_size=LBL, color=WHITE),
            MathTex(r"z \uparrow",   font_size=LBL, color=WHITE),
        ).arrange(DOWN, aligned_edge=LEFT)
        self.add_fixed_in_frame_mobjects(legend)
        legend.to_corner(DR, buff=0.5)
        self.play(FadeIn(legend), run_time=1)

        # 4. Surface with height-based gradient (cool look)
        surface = Surface(
            lambda u, v: np.array([u, v, np.sin(u)*np.cos(v)]),
            u_range=[-3,3], v_range=[-3,3], resolution=(40,40),
        )
        surface.set_fill_by_value(axes=axes, colorscale=[(BLUE_E,-1),(TEAL,0),(YELLOW,1)])
        surface.set_fill_opacity(0.85); surface.set_stroke_opacity(0.3)
        self.play(Create(surface, run_time=3)); self.wait(1)

        # 5. Showcase spin via ambient rotation
        self.begin_ambient_camera_rotation(rate=0.2)
        self.wait(6)
        self.stop_ambient_camera_rotation()
        self.wait(1)
```
</3D_SCENE_RULES>
"""

COMPUTER_DATASTRUCTURE = r"""
<COMPUTER_DATASTRUCTURE_RULES>
Generate a Manim v0.20+ algorithm/data-structure visualization.

## DESIGN SEQUENCE (strict order)
1. Title at ORIGIN center → Write → fade out COMPLETELY before anything else (scatter-fade or standard fade). No equations in title.
2. Then concept explanation/mini-diagram (if applicable), then camera movement or transition to the main structure/objects. No animation that breaks this logical order.
3. Integers preferred; 2 decimals if needed. No π/symbolic constants in numeric labels.
4. 5% margin from all edges. ≥1% gap between objects and any text.

## OVERLAP PREVENTION (the #1 visual failure — obey)
- Same location, multiple texts → SEQUENTIAL: FadeIn(0.5) → wait(1.5) → FadeOut(0.5) → buffer(0.2) → next. One spot, one text at a time.
- Simultaneous texts → distribute to corners: `.to_corner(UL/UR/DL/DR, buff=0.5)`.
- Stacked texts → ≥0.8 unit vertical spacing.
- Group related labels in a VGroup; FadeOut the whole group before a new scene.
- Long text → abbreviate, reduce font_size, or split with `\n`.
- Always fully FadeOut a scene's objects before starting the next scene, or use MovingCameraScene to pan to a fresh canvas.

## FONT HIERARCHY (adjust to content length)
TITLE 64-46 > TEXT 40-36 > LABEL 32-28 > DESC 24.
`get_graph_label` takes a mobject: `axes.get_graph_label(graph, label=MathTex(r"x^2", font_size=24))`.

## API RULES (v0.20 — these cause most crashes)
- `from manim import *` and `import numpy as np` always.
- Create not ShowCreation; axes.plot() not get_graph().
- Opacity/stroke NOT in constructor → `.set_stroke(opacity=...)` / `.set_fill(...)` after. (fill_opacity in constructor OK.)
- Position: `.move_to(ORIGIN)` / `.center()` (no `.to_center()`); `.next_to()`, `.arrange()`, `.to_corner()`, `.to_edge()` all valid.
- Dashed: `DashedVMobject(m, num_dashes=50)` or `DashedLine(a, b)` (no dash_length kwarg in constructor).
- Per-axis config inside Axes: `x_axis_config={...}`, `y_axis_config={...}`. `background_line_style`/`axis_config` only inside Axes/NumberPlane.
- Custom colors as hex: `LIGHT_BLUE = "#87CEFA"`. Use UL/UR/DL/DR (not UP_LEFT); UP/DOWN/LEFT/RIGHT/ORIGIN valid.
- Updaters take dt: `def upd(mob, dt): ...`.
- Reference last item in a VGroup: `group[-1]` (no `last_mobject`).
- Define every font-size constant before use (e.g. TEXT_SIZE = 28).
- MathTex always raw string; Text() for words, MathTex() for math.

## STYLE
Box-based elements for arrays/nodes. Highlight comparisons (CYAN/YELLOW stroke), swaps (PINK/RED flash with `path_arc` for cinematic jumps), sorted (GREEN). Use `LaggedStart` for sequential reveals. Deep/dark background colors `#0B0F19` preferred for neon contrast. Show a final result.

## REFERENCE TEMPLATE (study structure; adapt, don't copy verbatim)
```python
from manim import *
import numpy as np

class UltimateBubbleSort(MovingCameraScene):
    def construct(self):
        # Deep space dark background for glowing colors to pop
        self.camera.background_color = BLACK
        
        # Color Palette
        NEON_CYAN = "#00F0FF"
        NEON_PINK = "#FF0055"
        NEON_GREEN = "#00FF66"
        DARK_BLUE = "#111827"

        # Helper function for generating beautiful boxes
        def make_box(val):
            box = RoundedRectangle(
                corner_radius=0.2, width=1.2, height=1.2, 
                stroke_color=BLUE_D, stroke_width=3,
                fill_color=DARK_BLUE, fill_opacity=0.8
            )
            num = Text(str(val), font_size=36, weight=BOLD, color=WHITE)
            return VGroup(box, num)

        # =========================================================
        # PHASE 1: THE SCATTER TITLE INTRO
        # =========================================================
        
        TITLE_SIZE = 64
        title = Text("Bubble Sort", font_size=TITLE_SIZE, color=WHITE, weight=BOLD).move_to(ORIGIN)
        
        self.play(Write(title, run_time=1.5))
        self.wait(1)
        
        self.play(
            LaggedStart(
                *[
                    letter.animate.shift(
                        np.array([np.random.uniform(-3, 3), np.random.uniform(-3, 3), 0])
                    ).scale(0.5).set_opacity(0)
                    for letter in title
                ],
                lag_ratio=0.05,
                run_time=2
            )
        )
        self.wait(0.5)

        # =========================================================
        # PHASE 2: THE CONCEPT EXPLANATION
        # =========================================================
        
        concept_title = Text("Concept: Compare & Swap", font_size=40, color=NEON_CYAN).to_edge(UP, buff=1)
        self.play(FadeIn(concept_title, shift=DOWN*0.3))

        ex_left = make_box(8)
        ex_right = make_box(3)
        example_group = VGroup(ex_left, ex_right).arrange(RIGHT, buff=0.5).move_to(ORIGIN)
        
        self.play(FadeIn(example_group, shift=UP))
        
        focus_box = SurroundingRectangle(example_group, color=NEON_CYAN, corner_radius=0.2, buff=0.2)
        compare_text = Text("8 > 3 ? (Yes)", font_size=28, color=NEON_CYAN).next_to(focus_box, DOWN)
        
        self.play(Create(focus_box), Write(compare_text))
        self.wait(1)

        self.play(
            focus_box.animate.set_color(NEON_PINK),
            compare_text.animate.become(Text("Swap!", font_size=28, color=NEON_PINK).next_to(focus_box, DOWN)),
            ex_left[0].animate.set_stroke(NEON_PINK, width=5),
            ex_right[0].animate.set_stroke(NEON_PINK, width=5)
        )
        
        self.play(
            ex_left.animate(path_arc=-PI/1.5).move_to(ex_right.get_center()),
            ex_right.animate(path_arc=-PI/1.5).move_to(ex_left.get_center()),
            run_time=1.2,
            rate_func=smooth
        )
        self.wait(1)

        # =========================================================
        # PHASE 3: THE MAIN ARRAY
        # =========================================================
        
        camera_target = DOWN * 10
        self.play(
            self.camera.frame.animate.move_to(camera_target),
            run_time=2, rate_func=rate_functions.ease_in_out_sine
        )

        values = [42, 23, 14, 35, 8]
        elements = VGroup(*[make_box(v) for v in values]).arrange(RIGHT, buff=0.3).move_to(camera_target)
        
        array_title = Text("Sorting the Array", font_size=40, weight=BOLD).next_to(elements, UP, buff=1.5)
        self.play(Write(array_title), LaggedStart(*[FadeIn(e, scale=0.5) for e in elements], lag_ratio=0.1))
        self.wait(1)

        n = len(values)
        for p in range(n - 1):
            for i in range(n - p - 1):
                self.play(
                    elements[i][0].animate.set_stroke(NEON_CYAN, width=5).set_fill(opacity=1),
                    elements[i+1][0].animate.set_stroke(NEON_CYAN, width=5).set_fill(opacity=1),
                    run_time=0.3
                )
                self.wait(0.2)

                if values[i] > values[i+1]:
                    self.play(
                        elements[i][0].animate.set_stroke(NEON_PINK),
                        elements[i+1][0].animate.set_stroke(NEON_PINK),
                        elements[i].animate.scale(1.1),
                        elements[i+1].animate.scale(1.1),
                        run_time=0.2
                    )
                    
                    pi, pj = elements[i].get_center(), elements[i+1].get_center()
                    
                    self.play(
                        elements[i].animate(path_arc=-PI/2).move_to(pj), 
                        elements[i+1].animate(path_arc=-PI/2).move_to(pi), 
                        run_time=0.5
                    )
                    
                    self.play(
                        elements[i].animate.scale(1/1.1),
                        elements[i+1].animate.scale(1/1.1),
                        run_time=0.2
                    )
                    
                    elements.submobjects[i], elements.submobjects[i+1] = elements.submobjects[i+1], elements.submobjects[i]
                    values[i], values[i+1] = values[i+1], values[i]

                self.play(
                    elements[i][0].animate.set_stroke(BLUE_D, width=3).set_fill(opacity=0.8),
                    elements[i+1][0].animate.set_stroke(BLUE_D, width=3).set_fill(opacity=0.8), 
                    run_time=0.2
                )
            
            locked_element = elements[n-p-1]
            self.play(
                locked_element[0].animate.set_stroke(NEON_GREEN, width=4).set_fill("#064E3B", opacity=1), 
                run_time=0.4
            )
            
        self.play(
            elements[0][0].animate.set_stroke(NEON_GREEN, width=4).set_fill("#064E3B", opacity=1), 
            run_time=0.4
        )

        # =========================================================
        # PHASE 4: THE FINALE
        # =========================================================
        
        self.play(ApplyWave(elements, amplitude=0.3, time_width=1), run_time=1.5)
        done = Text("Array Sorted!", font_size=40, weight=BOLD, color=NEON_GREEN).next_to(elements, DOWN, buff=1)
        
        cx = VGroup(
            Text("Time: ", font_size=24, color=WHITE),
            MathTex(r"O(n^2)", font_size=28, color=NEON_CYAN),
            Text("  |  Space: ", font_size=24, color=WHITE),
            MathTex(r"O(1)", font_size=28, color=NEON_CYAN)
        ).arrange(RIGHT, buff=0.1).next_to(done, DOWN, buff=0.3)

        self.play(Write(done))
        self.play(FadeIn(cx, shift=UP*0.2))
        self.wait(3)

        # Clean up
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.5)
</COMPUTER_DATASTRUCTURE_RULES>
"""

PHYSICS = r"""
<PHYSICS_SCENE_RULES>
Generate a Manim v0.20+ physics visualization.

## DESIGN SEQUENCE (mandatory order)
1. Title at ORIGIN center → Write → fade out (LaggedStart letter-scatter encouraged).
2. Axes after title fades. Relevant axes only, no grid unless needed. Integers; 2 decimals if needed.
3. Equations/parameters in a corner via `.to_corner(UL/UR/DL/DR, buff=...)`. Fade out if no space.
4. Draw the trajectory/field/object, then animate motion, then highlight key points.
5. 5% margin all edges. Background BLACK unless asked.

## SUPPORTED
Projectile/trajectory motion, pendulums, waves, force/vector diagrams, fields, MoveAlongPath animations, parametric paths.

## FONT HIERARCHY (adjust to length)
TITLE 46 > EQUATION 30-36 > LABEL 26-28 > DESC 22-24.

## CORE API (v0.20)
- Plot: `axes.plot(f, x_range=[...], color=...)`. Parametric path: `axes.plot_parametric_curve(lambda t: np.array([x(t), y(t), 0]), t_range=[a,b,step], color=...)`.
- Motion: `MoveAlongPath(dot, path)` with `rate_func=linear`.
- Point mapping: `axes.c2p(x, y)`; reverse `axes.p2c(point)` returns 2D for Axes (unpack 2, not 3).
- Labels: create axes first, then `axes.get_x_axis_label(MathTex("x"))`. Axis numbers/font via `axis_config={"include_numbers": True, "font_size": 24, "decimal_number_config": {"num_decimal_places": 0}}` — NOT as separate kwargs.
- Bars: `BarChart(values=..., y_range=[...])`. Line graph: `axes.plot_line_graph(x_values=..., y_values=..., line_color=...)` (no vertex_dots kwarg; add Dots manually).
- NumberLine: `NumberLine(x_range=[...], length=..., font_size=24)` then `.shift(...)` (no position= / axis_config).

## CONSTRUCTOR RULES (most crashes)
- stroke opacity NOT in constructor → `.set_stroke(opacity=...)` after. (fill_opacity in constructor OK.)
- `background_line_style`/`axis_config`/per-axis `x_axis_config` only inside Axes.
- Dashed: `DashedVMobject(m, num_dashes=50)` (no dash_length kwarg).
- `from manim import *` + `import numpy as np` always. UL/UR/DL/DR (not UP_LEFT). Custom colors hex.
- Position: `.move_to(ORIGIN)`/`.center()` (no to_center). to_corner/to_edge/next_to all valid.

## LaTeX (physics has lots of these failures)
- All MathTex raw strings. Plain words → Text(), math → MathTex(), never mixed.
- NEVER put `°` inside MathTex → use `^\circ`. e.g. `MathTex(rf"\theta = {angle}^\circ")`.
- In f-string MathTex, escape literal braces: `\text{{ m/s}}`.
- Units: `MathTex(rf"v_0 = {v0}\,\text{{m/s}}")`.

## STYLE (cinematic physics)
- Glow title (layered stroked copy). Fading TracedPath trail behind moving objects (dissipating_time≈0.6). Live always_redraw velocity/force vectors that update with motion. Dashed marker lines to apex/key points. Emphasize with Indicate/Flash. Ground line for grounding. Color-code: trajectory YELLOW, launch GREEN, peak ORANGE, landing PURPLE. ≤4-5 colors. Holds ≥1.5s.
- Axis labels (get_x/y_axis_label) sit at the axis ENDS. Do NOT place data labels (Range, landing, etc.) near the same end — they collide. Put the range/landing label ABOVE the landing point (UP, shifted LEFT), and keep every label inside the frame (push back if near an edge).

## REFERENCE TEMPLATE (study; adapt, don't copy verbatim)
```python
from manim import *
import numpy as np

class ProjectileMotion(Scene):
    def construct(self):
        self.camera.background_color = "#0a0a12"
        TITLE, EQ, LBL, DESC = 46, 30, 26, 22

        v0, angle, g = 20, 60, 9.8
        theta = angle * DEGREES
        v0x, v0y = v0*np.cos(theta), v0*np.sin(theta)
        t_max = 2*v0y/g
        range_x = v0x*t_max
        max_h = v0y**2/(2*g)

        # 1. Glow title -> scatter fade
        title = Text("Projectile Motion", font_size=TITLE, color=WHITE, weight=BOLD)
        glow = Text("Projectile Motion", font_size=TITLE, weight=BOLD).set_color(YELLOW).set_stroke(width=12, opacity=0.25)
        self.play(FadeIn(glow, scale=1.3), Write(title), run_time=1.6); self.wait(1)
        self.play(LaggedStart(*[l.animate.shift(np.array([np.random.uniform(-2,2), np.random.uniform(-2,2),0])).scale(0.5).set_opacity(0) for l in VGroup(*title, *glow)], lag_ratio=0.08, run_time=1.8))

        # 2. Axes + ground
        axes = Axes(
            x_range=[0,40,5], y_range=[0,20,5],
            x_length=config.frame_width*0.65, y_length=config.frame_height*0.55,
            axis_config={"include_numbers": True, "font_size": 20, "decimal_number_config": {"num_decimal_places": 0}},
        ).move_to(ORIGIN).shift(RIGHT*0.6 + DOWN*0.4)
        x_lab = axes.get_x_axis_label(Text("Distance (m)", font_size=LBL))
        y_lab = axes.get_y_axis_label(Text("Height (m)", font_size=LBL))
        ground = Line(axes.c2p(0,0), axes.c2p(40,0), color=GREY_B, stroke_width=2)
        self.play(Create(axes), Write(x_lab), Write(y_lab), Create(ground), run_time=1.5)

        # 3. Equations corner
        eqs = VGroup(
            MathTex(r"x(t)=v_0\cos(\theta)\,t", font_size=EQ, color=TEAL),
            MathTex(r"y(t)=v_0\sin(\theta)\,t-\tfrac{1}{2}gt^2", font_size=EQ, color=TEAL),
        ).arrange(DOWN, buff=0.3, aligned_edge=LEFT).to_corner(UL, buff=0.4)
        self.play(Write(eqs), run_time=1.5)

        # 4. Trajectory
        path = axes.plot_parametric_curve(
            lambda t: np.array([v0x*t, v0y*t - 0.5*g*t*t, 0]),
            t_range=[0, t_max, 0.01], color=YELLOW,
        )
        self.play(Create(path), run_time=2, rate_func=smooth)

        # 5. Glowing ball + trail + live velocity vector
        tt = ValueTracker(0.0)
        def ball_point():
            t = tt.get_value()
            return axes.c2p(v0x*t, v0y*t - 0.5*g*t*t)
        ball = always_redraw(lambda: Dot(ball_point(), radius=0.12, color=RED))
        trail = TracedPath(ball_point, stroke_color=ORANGE, stroke_width=5, dissipating_time=0.6)
        def vel_vector():
            t = tt.get_value()
            vx, vy = v0x, v0y - g*t
            start = ball_point()
            end = start + np.array([vx, vy, 0])*0.06
            return Arrow(start, end, color=GREEN, buff=0, stroke_width=4)
        vel = always_redraw(vel_vector)
        self.add(trail)
        self.play(FadeIn(ball), FadeIn(vel), run_time=0.4)
        self.play(tt.animate.set_value(t_max), run_time=4, rate_func=linear)
        self.play(FadeOut(vel), run_time=0.3)

        # 6. Key points + apex line
        peak_pt = axes.c2p(v0x*(v0y/g), max_h)
        apex_line = DashedLine(axes.c2p(v0x*(v0y/g), 0), peak_pt, color=ORANGE, stroke_width=2)
        peak = Dot(peak_pt, color=ORANGE, radius=0.1)
        peak_lab = Text(f"Max Height: {max_h:.1f} m", font_size=DESC, color=ORANGE).next_to(peak, UP, buff=0.3)
        land = Dot(axes.c2p(range_x, 0), color=PURPLE, radius=0.1)
        land_lab = Text(f"Range: {range_x:.1f} m", font_size=DESC, color=PURPLE).next_to(land, UR, buff=0.2)
        self.play(Create(apex_line), FadeIn(peak), Write(peak_lab), run_time=0.8)
        self.play(Indicate(peak, color=ORANGE), run_time=0.6)
        self.play(FadeIn(land), Write(land_lab), run_time=0.8)
        self.play(Flash(land, color=PURPLE, num_lines=12), run_time=0.8)

        # 7. Parameters corner (^\circ, not °)
        params = VGroup(
            MathTex(rf"v_0 = {v0}\,\text{{m/s}}", font_size=EQ-2),
            MathTex(rf"\theta = {angle}^\circ", font_size=EQ-2),
            MathTex(rf"g = {g}\,\text{{m/s}}^2", font_size=EQ-2),
        ).arrange(DOWN, buff=0.25, aligned_edge=LEFT).to_corner(UR, buff=0.4)
        self.play(FadeIn(params, shift=LEFT), run_time=1)
        self.wait(2)
```
</PHYSICS_SCENE_RULES>
"""

STATISTICS = r"""
<STATISTICS_SCENE_RULES>
Generate a Manim v0.20+ statistical visualization.

## DESIGN SEQUENCE (mandatory order)
1. Title at ORIGIN center → Write → fade out (LaggedStart letter-scatter encouraged).
2. Axes/chart after title fades. Relevant axes only, no grid unless needed. Integers; 2 decimals if needed.
3. Legend/formula (mean, SD, etc.) in a corner via `.to_corner(...)`. Fade out if no space.
4. Draw the chart, then dynamic highlight of a key value.
5. 5% margin all edges. Background BLACK unless asked.

## SUPPORTED
BarChart, scatter, line plot, histogram, pie/donut (AnnularSector), boxplot (manual).

## FONT HIERARCHY (adjust to length)
TITLE 46 > EQUATION 32-36 > LABEL 24-28 > DESC 22.

## CLIPPING / OVERLAP (the #1 visual bug — obey)
- Axis labels (get_x/y_axis_label) sit at the axis ENDS. Do NOT place data labels (value/peak/range) near the same end — they collide. Put data labels ABOVE their point (UP, shifted away from edges).
- Keep every label inside the frame; if near an edge, shift it back. Keep charts ≤70% frame width.
- Degree symbol: use `^\circ` inside MathTex, never literal `°`. In Text() a literal °C is OK.

## CORE API (v0.20)
- `BarChart(values=..., bar_names=..., y_range=[lo,hi,step], bar_colors=[...])` (no bar_spacing). Bars: `chart.bars[i]`.
- Line graph: `axes.plot_line_graph(x_values=..., y_values=..., line_color=...)` (no vertex_dots; add Dots manually).
- Point mapping: `axes.c2p(x, y)`; `axes.p2c(point)` returns 2D for Axes (unpack 2).
- Axis numbers/font/decimals via `axis_config={"include_numbers": True, "font_size": 24, "decimal_number_config": {"num_decimal_places": 0}}`.
- Pie/donut: loop `AnnularSector(outer_radius=.., inner_radius=.., angle=.., start_angle=..)`, accumulate start_angle.
- Grow bars: `GrowFromEdge(bars, edge=DOWN, lag_ratio=0.1)` (no GrowFromBottom).

## CONSTRUCTOR RULES (most crashes)
- stroke opacity NOT in constructor → `.set_stroke(opacity=...)` after. (fill_opacity in constructor OK.)
- `axis_config`/`background_line_style` only inside Axes/NumberPlane.
- Dashed: `DashedVMobject(m, num_dashes=50)` (no dash_length kwarg).
- `from manim import *` + `import numpy as np` always. UL/UR/DL/DR (not UP_LEFT). Custom colors hex.
- Position: `.move_to(ORIGIN)`/`.center()` (no to_center). to_corner/to_edge/next_to all valid.

## STYLE (cinematic stats)
Glow title (layered stroked copy). Grow bars from the baseline with LaggedStart. Highlight key bar/point with SurroundingRectangle + Indicate/Flash. Value labels above each bar. Smooth color palette (≤4-5). Holds ≥1.5s.

## REFERENCE TEMPLATE (study; adapt, don't copy verbatim)
```python
from manim import *
import numpy as np

class StatsBarChart(Scene):
    def construct(self):
        self.camera.background_color = "#0a0a12"
        TITLE, EQ, LBL = 46, 32, 26

        # 1. Glow title -> scatter fade
        title = Text("Sales by Category", font_size=TITLE, color=WHITE, weight=BOLD)
        glow = Text("Sales by Category", font_size=TITLE, weight=BOLD).set_color(TEAL).set_stroke(width=12, opacity=0.25)
        self.play(FadeIn(glow, scale=1.3), Write(title), run_time=1.6); self.wait(1)
        self.play(LaggedStart(*[l.animate.shift(np.array([np.random.uniform(-2,2), np.random.uniform(-2,2),0])).scale(0.5).set_opacity(0) for l in VGroup(*title, *glow)], lag_ratio=0.08, run_time=1.8))

        # 2. Bar chart
        data = [5, 8, 2, 6]
        cats = ["A", "B", "C", "D"]
        chart = BarChart(
            values=data, bar_names=cats,
            y_range=[0, max(data)+2, 1],
            x_length=config.frame_width*0.65, y_length=config.frame_height*0.55,
            bar_colors=["#4C9BE0", "#5BD68A", "#E06B6B", "#E0A24C"],
        ).center().shift(DOWN*0.3)

        # grow bars from baseline
        self.play(Create(chart.x_axis), Create(chart.y_axis), run_time=1)
        self.play(GrowFromEdge(chart.bars, edge=DOWN, lag_ratio=0.15), run_time=1.5)

        # value labels above each bar
        val_labels = VGroup(*[
            Text(str(v), font_size=22, color=WHITE).next_to(bar, UP, buff=0.15)
            for v, bar in zip(data, chart.bars)
        ])
        self.play(LaggedStart(*[FadeIn(l, shift=UP*0.2) for l in val_labels], lag_ratio=0.1), run_time=1)

        # 3. Stats legend (corner)
        mean = np.mean(data)
        legend = MathTex(rf"\text{{Mean}} = {mean:.1f}", font_size=EQ, color=WHITE).to_corner(UR, buff=0.4)
        self.play(Write(legend), run_time=1)

        # 4. Highlight tallest bar
        i = int(np.argmax(data))
        box = SurroundingRectangle(chart.bars[i], color=YELLOW, buff=0.05)
        tag = Text("Top", font_size=22, color=YELLOW).next_to(val_labels[i], UP, buff=0.15)
        self.play(Create(box), FadeIn(tag), run_time=0.8)
        self.play(Indicate(chart.bars[i], color=YELLOW), run_time=0.8)
        self.play(Flash(chart.bars[i].get_top(), color=YELLOW, num_lines=12), run_time=0.8)
        self.wait(2)

        # 5. Cleanup
        self.play(*[FadeOut(m) for m in [chart, val_labels, legend, box, tag]], run_time=1.2)
        self.wait(1)
```
</STATISTICS_SCENE_RULES>
"""