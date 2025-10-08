TEXT="""
<Text Scenes Rule Only>

## Mandatory

1. Always follow Code and Design Example
2. Never use .next_to() before VGroup.arrange() - always arrange groups first
3. Equation should write like this MathTex(r"2x - 1 = 2 \Rightarrow x = \tfrac{3}{2}", font_size=32)

## Code and Design Example
```python
from manim import *

class FunctionalEquationSlide(Scene):
    def construct(self):
        # === Title Slide ===
        title = Text("Functional Equation Problem", font_size=50, color=YELLOW)
        self.play(FadeIn(title, scale=1.2))
        self.wait(2)
        self.play(FadeOut(title, shift=UP))

        # === Slide 1: Given Equation ===
        slide1_title = Text("Given Equation", font_size=40, color=YELLOW)
        eq_text = MathTex(r"f(2x - 1) + f(2) = 4x - 1", font_size=44)
        target = Text("Find the value of  ", font_size=32)
        f4 = MathTex(r"f(4)", font_size=40, color=BLUE)
        target_group = VGroup(target, f4).arrange(RIGHT, buff=0.1)
        group1 = VGroup(slide1_title, eq_text, target_group).arrange(DOWN, buff=0.5)
        self.play(Write(group1))
        self.wait(3)
        self.play(FadeOut(group1))

        # === Slide 2: Step 1 – Find f(2) ===
        step1_title = Text("Step 1: Find the constant term f(2)", font_size=38, color=YELLOW)
        eq1 = MathTex(r"f(2x-1) + f(2) = 4x - 1", font_size=34)
        sub_eq = MathTex(r"2x - 1 = 2 \Rightarrow x = \tfrac{3}{2}", font_size=32)
        calc = MathTex(
            r"f(2) + f(2) = 6 - 1 \\[4pt]"
            r"2f(2) = 5 \\[4pt]"
            r"f(2) = \tfrac{5}{2}",
            font_size=32
        )
        group2 = VGroup(step1_title, eq1, sub_eq, calc).arrange(DOWN, buff=0.4)
        self.play(Write(group2))
        self.wait(3)
        self.play(FadeOut(group2))

        # === Slide 3: Step 2 – Determine general form f(t) ===
        step2_title = Text("Step 2: Determine the general form of f(t)", font_size=38, color=YELLOW)
        eq2 = MathTex(r"f(2x-1) + \tfrac{5}{2} = 4x - 1", font_size=32)
        isolate = MathTex(r"f(2x-1) = 4x - \tfrac{7}{2}", font_size=32)
        sub_t = MathTex(
            r"t = 2x - 1 \Rightarrow x = \tfrac{t+1}{2}", font_size=32
        )
        form = MathTex(
            r"f(t) = 4\left(\tfrac{t+1}{2}\right) - \tfrac{7}{2} = 2t - \tfrac{3}{2}",
            font_size=34, color=GREEN
        )
        group3 = VGroup(step2_title, eq2, isolate, sub_t, form).arrange(DOWN, buff=0.4)
        self.play(Write(group3))
        self.wait(3)
        self.play(FadeOut(group3))

        # === Slide 4: Step 3 – Calculate f(4) ===
        step3_title = Text("Step 3: Calculate f(4)", font_size=38, color=YELLOW)
        eq3 = MathTex(
            r"f(4) = 2(4) - \tfrac{3}{2} = \tfrac{13}{2}",
            font_size=40, color=GREEN
        )
        decimal = Text("Or equivalently, f(4) = 6.5", font_size=32, color=BLUE)
        group4 = VGroup(step3_title, eq3, decimal).arrange(DOWN, buff=0.5)
        self.play(Write(group4))
        self.wait(3)
        self.play(FadeOut(group4))

        # === Slide 5: Alternative Method ===
        alt_title = Text("Alternative Method (Direct Substitution)", font_size=36, color=YELLOW)
        sub_x = MathTex(r"2x - 1 = 4 \Rightarrow x = \tfrac{5}{2}", font_size=32)
        eq_alt = MathTex(r"f(4) + f(2) = 9", font_size=32)
        sub_f2 = MathTex(
            r"f(4) + \tfrac{5}{2} = 9 \\[4pt]"
            r"f(4) = \tfrac{13}{2}",
            font_size=32, color=GREEN
        )
        group5 = VGroup(alt_title, sub_x, eq_alt, sub_f2).arrange(DOWN, buff=0.4)
        self.play(Write(group5))
        self.wait(3)
        self.play(FadeOut(group5))

        # === Final Slide: Answer ===
        final_title = Text("Final Answer", font_size=46, color=YELLOW)
        ans = MathTex(r"f(4) = \tfrac{13}{2} = 6.5", font_size=48, color=BLUE)
        group_final = VGroup(final_title, ans).arrange(DOWN, buff=0.5)
        self.play(FadeIn(group_final, shift=UP))
        self.wait(4)
        self.play(FadeOut(group_final))
```
<Text Scenes Rule Only/>
"""

GRAPH2D = """
<2D Graph Scenes Rule Only>

## Mandatory way to design

1. Title: Always at the center (never top). Must appear first and then fade out with a smooth animation (e.g., FadeOut, LaggedStart, star-burst effect). Do not include the equation in the title.
2. Axes: Create axes immediately after title fades.
3. Numbers: Use integers mostly; if needed, then 2 decimal precision. Do not include "π" value in the axes.
4. Axes style: Show only the central axes (no grid). Draw only the x-axis if needed, and only the y-axis if needed.
5. Equation: Place in corners (left, right, bottom-left, bottom-right). If no space → fade it out before graph. and do not include Equation in the center
6. Margins: Leave a 5% gap at the top, bottom, left, and right edges.
7. The background color should be black by default unless the user requests a different color. Note: Do not change anything else.
8. Sequence: Title (center + fade out) → Axes → Equation (adaptive placement or fade) → Graph.


### Deprecated → New (Manim v0.19+)

---

## Common Deprecated → New

* `to_edge(...)` still works, but prefer `.next_to()` for finer control.
* `to_corner(...)` → use `.align_on_border(...)`.
* `axes.to_center()` → use `axes.move_to(ORIGIN)` or `axes.center()`.
* `shift(x*RIGHT)` still valid.
* `scale_in_place(factor)` → use `.scale(factor, about_point=...)`.
* `fade_in` / `fade_out` methods → use animations: `FadeIn(mobj)` / `FadeOut(mobj)`.
* `ShowCreation(mobj)`  → `Create(mobj)`.
* `Write(mobj, run_time=...)`  still valid.
* `Transform(m1, m2)`  still valid.
* `SurroundingRectangle(..., buff=0.1)`  still valid.
* `.start_point or .end_point` -> use `.get_start()` or `.get_end()`.

---

## Axes / Graphs

* `axes.get_graph(f, ...)` → deprecated. Use `axes.plot(f, x_range=[...], color=...)`.

* `axes.get_area(f, ...)` → still valid for one function. For two functions use `FillBetween(...)`.

* `NumberPlane.get_graph(...)` → does not exist. Use `plane.plot(...)`.

* `add_coordinates()` → still valid.

* `axes.get_tangent_line(graph, x=..., line_length=...)` → does not exist. Use `TangentLine(graph, alpha, length=...)` where `alpha ∈ [0,1]`. To map `x` to `alpha`, use helpers like `axes.i2gp`.

* `axes.get_vertical_line(x_val=...)` wrong → invalid. Correct: `axes.get_vertical_line(point, **kwargs)`.
  (use `axes.c2p(x_value, y_value)` or `axes.i2gp(x_value, graph)` to get the point).

* `axes.y_axis_labels` wrong → no attribute. Use `axes.get_axis_labels()`.

* `y_axis_config` must be passed explicitly inside `Axes(...)`, not accessed as an attribute afterwards.

* `axes.get_x_axis_label(...)` and `axes.get_y_axis_label(...)` → still valid, but prefer `axes.get_axis_labels(x_label, y_label)` for paired labels.

---

## Colors / Styles

- `stroke_width` → still valid.
- `stroke_opacity=...` in constructor → not allowed. Use `.set_stroke(opacity=...)`.
- `fill_opacity=...` in constructor → still valid.
- `line_arg_dict` → deprecated.  Use: 
  - `axis_config={...}` → for styling axes 
  - `background_line_style={...}` → **only inside Axes or NumberPlane**.
- `stroke_dash_length` → not valid. Use `DashedLine(...)` or `DashedVMobject(...)`.

---

## Text / Labels

* `TextMobject(...)` → use `Tex(...)`.
* `TexMobject(...)` → use `Tex(...)`.
* `edge_buffer` argument (e.g., in `Text`) → not valid. Replace with `.next_to(..., buff=...)` or `.align_on_border(...)`.
* `Text(..., t2c=...)` → still valid. 
* `t2s` (text-to-style) → replaced by `.set_color_by_t2s()`.

---

## Shapes

* `ArcBetweenPoints(..., radius=...)` → `ArcBetweenPoints(..., angle=...)`.
* `Sector(inner_radius=...)` → replaced with `AnnularSector(inner_radius=...)`.

---

## NumberLine

* `NumberLine(default_numbers_to_display=...)` → removed. Use `include_numbers=True` and control with `numbers_to_include=[...]` or `decimal_number_config={...}`.
* `exclude_zero_from_default_numbers` → removed. Must explicitly control numbers via `numbers_to_include`.

---

## Camera / Scene

* `ThreeDScene.set_camera_orientation(...)` → still valid.
* `self.camera.animate.set(phi=..., theta=...)` → replaces old `self.move_camera(...)`.
* `self.set_camera_orientation(...)` → replaces old `set_camera_position(...)`.
* `self.set_camera_orientation(phi=..., theta=...)` → still valid; `gamma` is no longer supported.


---

## Geometry / Mobject Methods

* `.start_point` / `.end_point` → replaced with `.get_start()` / `.get_end()`.
* `.point_from_proportion(alpha)` → still valid.
* `scale_in_place(factor)` → deprecated. Use `.scale(factor, about_point=...)`.
* `.fade_in` / `.fade_out` (methods) → removed. Use `FadeIn(mobj)` / `FadeOut(mobj)` animations.
* `next_to(...)` → still valid and preferred over `to_edge(...)` for finer control.
* `to_corner(...)` → replaced with `.align_on_border(...)`.
* `.center()` or `.move_to(ORIGIN)` → replaces older `.to_center()`.
* `rotate(angle, axis=...)` → still valid.
* `.get_midpoint()` → preferred over manual midpoint calculations.
* `.get_vertices()` → still valid for polygons.
* `.copy()` → still valid.

## Summary of New Errors Fixed

* `TypeError: Mobject.__getattr__.<locals>.getter() got an unexpected keyword argument 'length'` → use `line_length`.
* `TypeError: Mobject.__getattr__.<locals>.getter() got an unexpected keyword argument 'x_val'` → use `x`.
* `TypeError: Mobject.__getattr__.<locals>.getter() got an unexpected keyword argument 'edge_buffer'` → replace with `.next_to(..., buff=...)`.
* `AttributeError: Axes object has no attribute 'y_axis_labels'` → use `axes.get_axis_labels()`.
* `AttributeError: NumberLine object has no attribute 'default_numbers_to_display'` → use `include_numbers=True` with `numbers_to_include`.
* `TypeError: ... got an unexpected keyword argument 'stroke_opacity'` → set via `.set_stroke(opacity=...)`.
* `AttributeError: NumberLine has no attribute 'exclude_zero_from_default_numbers'` → must use `numbers_to_include`.
* `TypeError: ... got an unexpected keyword argument 'gamma'` → camera no longer supports gamma.
* `NameError: name 'UP_LEFT' is not defined` → Use `UL` (UP + LEFT), `UR`, `DL`, `DR` instead.

### Font Size Rules (Hierarchy — Never Violate)
```python
TITLE_SIZE = 46          # Largest - for main titles
EQUATION_SIZE = 36       # Smaller than title - for math equations
LABEL_SIZE = 28          # Smaller than equation - for axis labels
DESC_SIZE = 24           # Smallest - for descriptions

Text(...) →  font_size works.
MathTex(...) →  font_size works.
Axes(..., axis_config={"font_size": ...}) →  font_size works.
axes.get_graph_label(...) →  font_size not allowed. Use: axes.get_graph_label(graph, label=MathTex(r"x^2", font_size=24))
```

### Mandatory Spacing Rules
```python
TOP_BUFFER = config.frame_height * 0.05      # 5% space from top
BOTTOM_BUFFER = config.frame_height * 0.05   # 5% space from bottom
LEFT_BUFFER = config.frame_width * 0.05      # 5% space from left
RIGHT_BUFFER = config.frame_width * 0.05     # 5% space from right
```
## Mandatory avoid these 

1. NameError: name 'LIGHT_BLUE' is not defined
    Use valid built-ins (from manim):
    from manim import BLUE, GREEN, TEAL, YELLOW, RED, ORANGE, PURPLE
    Or define your own shades:
    LIGHT_BLUE = "#87CEFA"   # hex for light sky blue
    LIGHT_GREEN = "#90EE90"  # hex for light green

    Then your code works:
    self.play(f1.animate.set_color(LIGHT_BLUE).set_opacity(0.4))

    
2. Mobject.__getattr__.<locals>.getter() got an unexpected keyword argument 'color'
    Fix: Import form the manim 
    from manim import Scene, MathTex, Axes, Write, WHITE
    or
    from manim import *

3. NameError: name 'BOTTOM' is not defined
    Fix: UP, DOWN, LEFT, RIGHT, ORIGIN are valid.

4. NameError: name 'WiggleOutThenIn' is not defined
    At the top of your script add:
    from manim import *
    or,
    from manim import Scene, Axes, MathTex, FadeIn, WiggleOutThenIn

5.  Mobject.__getattr__.<locals>.getter() got an unexpected keyword argument 'x_range'
    Fix: graph_sin_x = plane.plot(lambda x: np.sin(x), x_range=[-7, 7], color=BLUE)

6. TypeError: Mobject.__init__() got an unexpected keyword argument 'line_arg_dict'
    Fix: replace it with:
    background_line_style={...}
    Use axis_config={...} for Axes.

7. Error Message: Found `stroke_opacity` set in the constructor for `envelope_pos` and `envelope_neg`. According to the validation rules, opacity-related parameters should not be set in the constructor; use `.set_stroke(opacity=...)` or `.set_opacity()` after creation.

8. TypeError: Mobject.__init__() got an unexpected keyword argument 'stroke_dash_length'
    Fix: 
    # Option A: directly make dashed
    line1 = DashedLine(LEFT, RIGHT, dash_length=0.2, num_dashes=20)


    # Option B: wrap an existing object
    base = Line(LEFT, RIGHT)
    line2 = DashedVMobject(base, dash_length=0.2, num_dashes=20)


9. AttributeError: Axes object has no attribute 'to_center'
    Fix: 
    axes.move_to(ORIGIN)
    # or
    axes.center()

10. TypeError: Mobject.__init__() got an unexpected keyword argument 'background_line_style'
    Fix:
    background_line_style is only valid in NumberPlane or Axes, not in general Mobject.
    So you must pass it when constructing axes/plane, like this:

    axes = Axes(
        x_range=[-5, 5],
        y_range=[-3, 3],
        axis_config={"color": BLUE},              # style for main axes
        background_line_style={                   # style for grid lines
            "stroke_color": GREY,
            "stroke_width": 1,
            "stroke_opacity": 0.5,
        }
    )

11. Mobject.__getattr__.<locals>.getter() got an unexpected keyword argument 'length'
    Fix: axes.get_tangent_line(graph_sin, x_tracker.get_value(), line_length=3)

12. TypeError: Mobject.__init__() got an unexpected keyword argument 'x_axis_config'
    Axes does not accept x_axis_config or y_axis_config as keyword arguments at the top level of Axes(...)
    Fix:
    axes = Axes(
    x_range=[-5, 5, 1],
    y_range=[-3, 3, 1],
    axis_config={"font_size": 24},
    )

    or, if you need separate configs:

    axes = Axes(
        x_range=[-5, 5, 1],
        y_range=[-3, 3, 1],
        x_axis_config={"font_size": 24},
        y_axis_config={"font_size": 30},
    )

13. AxisError: axis 1 is out of bounds for array of dimension 1
    fix:
    curve1 = axes.plot_parametric_curve(
        lambda t: (x_func1(t), y_func1(t)),
        t_range=[0, 2*np.pi, 0.01],
        color=BLUE
    )

14. AttributeError: MathTex object has no attribute 'is_about_to_overlap' is_about_to_overlap() doesn’t exist in ManimCE.

15. Mobject.__getattr__.<locals>.getter() got an unexpected keyword argument 't_range'
    Fix:
    curve = axes.plot_parametric_curve(
        lambda t: np.array([t, np.sin(t), 0]),
        t_range=[-PI, PI, 0.05],
        color=BLUE
    )

16. AttributeError: ParametricFunction object has no attribute 'x_to_alpha'
    Fix: x_to_alpha works only on Axes.plot, not on ParametricFunction.
    tangent_line = always_redraw(
        lambda: TangentLine(graph_sin, x=x_tracker.get_value(), length=4)
    )

17. AttributeError: Axes object has no attribute 'x_to_proportion'
    In new Manim (v0.19+), Axes has no x_to_proportion.
    Fix: 
    tangent_line = always_redraw(
        lambda: TangentLine(graph_sin, x=x_tracker.get_value(), length=4)
    )

18. TypeError: Mobject.__init__() got an unexpected keyword argument 'dash_length'
    Fix: 
    envelope_pos_graph = axes.plot(lambda x: np.sin(x), x_range=[-7,7], color=BLUE)
    envelope_pos = DashedVMobject(envelope_pos_graph)
    envelope_pos.set_dash(dash_length=0.1, dashed_ratio=0.5)

19. IndexError: list index out of range
    use a tiny visible placeholder, e.g.:

    MathTex(r"\;", font_size=LABEL_SIZE)  # thin space
    # or
    MathTex(r"0", font_size=LABEL_SIZE)

20. AttributeError: MathTex object has no attribute 'bounding_box'
    Fix: use properties or new methods:

    mobj.width
    mobj.height
    mobj.get_center()
    mobj.get_bounding_box_vertices()

21. TypeError: Mobject.__init__() got an unexpected keyword argument 'number_constructor_kwargs'
    Fix: remove it and customize numbers after creation:
    axes = Axes(x_range=[-2.5*np.pi, 2.5*np.pi, np.pi/2], y_range=[-1.5, 1.5, 0.5])
    for x_val in axes.x_axis.numbers:
        x_val.set_color(BLUE)

22. NameError: name 'FillBetween' is not defined
    FillBetween isn’t auto-imported in v0.19+.
    Fix: 
    Add this line:
    from manim.mobject.graphing.utils import FillBetween
    Or use axes.get_area() as an alternative.

23. TypeError: Mobject.__init__() got an unexpected keyword argument 'color_map'
    Fix:

    surface = Surface(..., resolution=(30,30))
    surface.set_style(fill_color=BLUE, fill_opacity=0.7)

    For gradient:
    surface.set_fill_by_value(axes=axes, colors=[(BLUE,-1),(GREEN,0),(RED,1)])

24. NameError: name 'ParametricSurface' is not defined
    Fix:
    NameError: name 'ParametricSurface' is not defined
    
25. TypeError: Mobject.__init__() got an unexpected keyword argument 'res_u'
    Error comes from res_u / res_v → not valid in v0.19.
    Fix:
    resolution=(20, 20)

26. TypeError: Mobject.__init__() got an unexpected keyword argument 'dash_length'
    Fix for current version: use num_dashes instead:
    envelope_pos = DashedVMobject(envelope_pos_graph, num_dashes=50, dashed_ratio=0.5)
    envelope_neg = DashedVMobject(envelope_neg_graph, num_dashes=50, dashed_ratio=0.5)

27. AttributeError: 'Camera' object has no attribute 'frame'
    Fix:
    step2_title.to_edge(UP, buff=TOP_BUFFER)
    
## ANIMATION SEQUENCE (MANDATORY ORDER)

### STEP 1: Title in center only
title = Text("Your Title Here", font_size=TITLE_SIZE)
title.move_to(ORIGIN)   # center of screen

self.play(Write(title, run_time=1.5))
self.wait(3)


```
### **STEP 2: Axes (No Grid, With Margins)**
```python
# Calculate usable space
usable_width = config.frame_width - (LEFT_BUFFER + RIGHT_BUFFER)
usable_height = config.frame_height * 0.65

# Create axes
axes = Axes(
    x_range=[-1, 10, 1],
    y_range=[-1, 3, 1],
    x_length=usable_width,
    y_length=usable_height,
    axis_config={
        "include_numbers": True,
        "font_size": 24,
        "decimal_number_config": {"num_decimal_places": 0}
    }
)


# Apply margins
axes.next_to(title, DOWN, buff=AFTER_TITLE_GAP)

# Decimal place override (for fractional steps)
if x_step < 1:
    axes.x_axis.decimal_number_config["num_decimal_places"] = 2
if y_step < 1:
    axes.y_axis.decimal_number_config["num_decimal_places"] = 2

# Animate axes
self.play(Create(axes))

### **STEP 3: Equation (Adaptive Placement with Fallback)**
- Place equation below top with a 5% gap.
- If no space available → show equation temporarily then fade it out.
- Try to place **left, right, bottom-left, or bottom-right or bottom of the edges if eqation is bigger depending on space.
- equation = MathTex(r"y = f(x)", font_size=EQUATION_SIZE)

# Try placements in order:
# 1. Left
# 2. Right 
# 3. Bottom-left
# 4. Bottom-right
# If nothing fits → fade out

eq_width = eq.width
eq_height = eq.height

positions = [
    lambda: eq.next_to(axes, LEFT, buff=0.3).align_to(axes, UP),
    lambda: eq.next_to(axes, RIGHT, buff=0.3).align_to(axes, UP),
    lambda: eq.to_edge(DOWN, buff=BOTTOM_BUFFER).to_edge(LEFT, buff=LEFT_BUFFER),
    lambda: eq.to_edge(DOWN, buff=BOTTOM_BUFFER).to_edge(RIGHT, buff=RIGHT_BUFFER),
]


for pos in positions:
    pos()
    left_ok = eq.get_left()[0] >= -config.frame_width/2 + LEFT_BUFFER
    right_ok = eq.get_right()[0] <= config.frame_width/2 - RIGHT_BUFFER
    bottom_ok = eq.get_bottom()[1] >= -config.frame_height/2 + BOTTOM_BUFFER
    top_ok = eq.get_top()[1] <= config.frame_height/2 - TOP_BUFFER

    if left_ok and right_ok and bottom_ok and top_ok:
        self.play(Write(eq))
        equation_placed = True
        break

if not equation_placed:
    self.play(Write(eq))
    self.wait(1)
    self.play(FadeOut(eq))



```

### **STEP 4: Plot Graph**
```python
graph = axes.plot(
    lambda x: your_function(x),
    x_range=[min, max],
    color=BLUE
)
self.play(Create(graph))
```
---

## QUICK TEMPLATE
```python
from manim import *
import numpy as np
import random

class Animation_84c7b8ca(Scene):
    def construct(self):
        # ===== CONSTANTS =====
        TITLE_SIZE = 46
        EQUATION_SIZE = 36
        LABEL_SIZE = 28

        TOP_BUFFER = config.frame_height * 0.01
        BOTTOM_BUFFER = config.frame_height * 0.05
        LEFT_BUFFER = config.frame_width * 0.05
        RIGHT_BUFFER = config.frame_width * 0.05
        AFTER_TITLE_GAP = config.frame_height * 0.05

        self.camera.background_color = BLACK

        # ===== STEP 1: Title in center =====
        title = Text("Derivative & Tangent Line", font_size=TITLE_SIZE, color=WHITE)
        title.move_to(ORIGIN)

        # Title appear
        self.play(Write(title, run_time=1.5))
        self.wait(3)

        # Custom "star explosion" fade out
        self.play(
            LaggedStart(
                *[
                    letter.animate.shift(
                        np.array([random.uniform(-2, 2), random.uniform(-2, 2), 0])
                    ).scale(0.5).set_opacity(0)
                    for letter in title
                ],
                lag_ratio=0.1,
                run_time=2
            )
        )

        # ===== STEP 2: Axes =====
        usable_width = config.frame_width - (LEFT_BUFFER + RIGHT_BUFFER)
        usable_height = config.frame_height * 0.65

        axes = Axes(
            x_range=[-7, 7, 1],
            y_range=[-2, 2, 1],
            x_length=usable_width,
            y_length=usable_height,
            axis_config={
                "include_numbers": True,
                "font_size": 24,
                "decimal_number_config": {"num_decimal_places": 0},
            },
            x_axis_config={"numbers_to_include": [-6, -4, -2, 0, 2, 4, 6]},
            y_axis_config={"numbers_to_include": [-1, 0, 1]},
        )

        axes.center()
        self.play(Create(axes, run_time=2))

        # ===== STEP 3: Equation =====
        equation = MathTex(r"y = \sin(x)", font_size=EQUATION_SIZE, color=WHITE)

        positions = [
            lambda: equation.next_to(axes, LEFT, buff=0.3).align_to(axes, UP),
            lambda: equation.next_to(axes, RIGHT, buff=0.3).align_to(axes, UP),
            lambda: equation.to_edge(DL, buff=BOTTOM_BUFFER).to_edge(LEFT, buff=LEFT_BUFFER),
            lambda: equation.to_edge(DR, buff=BOTTOM_BUFFER).to_edge(RIGHT, buff=RIGHT_BUFFER),
        ]

        equation_placed = False
        for pos_func in positions:
            pos_func()
            if (
                equation.get_left()[0] >= -config.frame_width/2 + LEFT_BUFFER and
                equation.get_right()[0] <= config.frame_width/2 - RIGHT_BUFFER and
                equation.get_bottom()[1] >= -config.frame_height/2 + BOTTOM_BUFFER and
                equation.get_top()[1] <= config.frame_height/2 - TOP_BUFFER
            ):
                self.play(Write(equation, run_time=1))
                equation_placed = True
                break

        if not equation_placed:
            equation.move_to(ORIGIN)
            self.play(Write(equation, run_time=1))
            self.wait(1)
            self.play(FadeOut(equation))

        # ===== STEP 4: Plot Graph =====
        def f(x):
            return np.sin(x)

        graph_sin = axes.plot(f, x_range=[-7, 7], color=BLUE)
        self.play(Create(graph_sin, run_time=2))

        # ===== STEP 5: Dynamic Elements =====
        x_tracker = ValueTracker(-7)

        moving_dot = always_redraw(
            lambda: Dot(point=axes.i2gp(x_tracker.get_value(), graph_sin), color=RED, radius=0.08)
        )

        tangent_line = always_redraw(
            lambda: TangentLine(
                graph_sin,
                alpha=(x_tracker.get_value() - axes.x_range[0]) / (axes.x_range[1] - axes.x_range[0]),
                length=4,
                color=YELLOW
            )
        )

        vertical_line = always_redraw(
            lambda: DashedLine(
                axes.c2p(x_tracker.get_value(), 0),
                axes.i2gp(x_tracker.get_value(), graph_sin),
                color=GREY_A,
                dash_length=0.1
            )
        )

        x_label_group = always_redraw(
            lambda: VGroup(
                MathTex("x = ", font_size=LABEL_SIZE, color=GREEN),
                DecimalNumber(x_tracker.get_value(), num_decimal_places=2, font_size=LABEL_SIZE, color=GREEN)
            ).arrange(RIGHT, buff=0.1).next_to(axes.c2p(x_tracker.get_value(), 0), DOWN, buff=0.2)
        )

        slope_label_group = always_redraw(
            lambda: VGroup(
                MathTex(r"m = \cos(x) = ", font_size=LABEL_SIZE, color=YELLOW),
                DecimalNumber(np.cos(x_tracker.get_value()), num_decimal_places=2, font_size=LABEL_SIZE, color=YELLOW)
            ).arrange(RIGHT, buff=0.1).to_edge(UR, buff=RIGHT_BUFFER)
        )

        self.play(
            FadeIn(moving_dot),
            FadeIn(tangent_line),
            FadeIn(vertical_line),
            FadeIn(x_label_group),
            FadeIn(slope_label_group),
            run_time=0.5
        )

        # ===== STEP 6: Animate Movement =====
        self.play(x_tracker.animate.set_value(7), run_time=10, rate_func=linear)

        # ===== STEP 7: Clean Up =====
        self.play(
            FadeOut(axes),
            FadeOut(equation),
            FadeOut(graph_sin),
            FadeOut(moving_dot),
            FadeOut(tangent_line),
            FadeOut(vertical_line),
            FadeOut(x_label_group),
            FadeOut(slope_label_group),
            run_time=1
        )
        self.wait(1)


```

<2D Graph Scenes Rule Only/>
"""

GRAPH3D="""
<3D Scenes and Graph Rule Only>

## Animation Sequence (Mandatory Order)

1. Title: Always at the top. Do not include the equation in the title.
2. Axes: Create axes immediately after the title.
3. Use integers mostly if needed then use 2 decimal precision.
4. Only show central axes (no grid).
5. Equation: Placed below title or in corners (left, right, bottom-left, bottom-right). If no space → fade it out before graph.
7. Margins: Leave a 5% gap at the bottom, left, and right edges.
8. Sequence: Title → Axes → Equation (adaptive) → Graph.


### Font Size Rules (Hierarchy — Never Violate)
```python
TITLE_SIZE = 46          # Largest - for main titles
EQUATION_SIZE = 36       # Smaller than title - for math equations
LABEL_SIZE = 28          # Smaller than equation - for axis labels
DESC_SIZE = 24           # Smallest - for descriptions

Text(...) →  font_size works.
MathTex(...) →  font_size works.
Axes(..., axis_config={"font_size": ...}) →  font_size works.
axes.get_graph_label(...) →  font_size not allowed. Use: axes.get_graph_label(graph, label=MathTex(r"x^2", font_size=24))
```

### Mandatory Spacing Rules
```python
TOP_BUFFER = config.frame_height * 0.01      # 1% space from top
BOTTOM_BUFFER = config.frame_height * 0.05   # 5% space from bottom
LEFT_BUFFER = config.frame_width * 0.05      # 5% space from left
RIGHT_BUFFER = config.frame_width * 0.05     # 5% space from right
AFTER_TITLE_GAP = config.frame_height * 0.05 # 5% gap after title

## Critical Fixes for Text Placement, Safe Zone, and Overlap

1. **Fixed-Frame Text**
   * All text (titles, equations, annotations) **must** use `add_fixed_in_frame_mobjects()` **before** any camera orientation or movement.
   * This locks text to the 2D screen and keeps it facing the viewer regardless of 3D camera rotation.
   ```python
   self.add_fixed_in_frame_mobjects(title, equation)
   ```

2. **Horizontal Safe Zone**
   * Reserve the top 30% of the frame for all fixed-frame text. No 3D object should enter this zone.
   ```python
   SAFE_Y = config.frame_height * 0.3   # top 30% reserved for text
   ```
   * Push surfaces downward if necessary:
   ```python
   surface.move_to([0, -SAFE_Y/2, 0])
   ```

3. **Locked Screen Placement**
   * Set both x and y screen coordinates to ensure equations remain only in the horizontal safe band.
   ```python
   equation.move_to([
       -config.frame_width/2 + 0.5,
        config.frame_height/2 - 0.5,
        0
   ])
   ```

4. **Adaptive Overlap Checks**
   * After each 3D element creation, check for collisions and automatically move or hide equations:
   ```python
   def avoid_overlap(eq, obj, pad=0.3):
       if eq.get_left()[0] < obj.get_right()[0] + pad:
           eq.to_edge(LEFT).shift(UP*2)
       if eq.get_top()[1] < obj.get_top()[1] + pad:
           self.play(FadeOut(eq))
   ```

5. **Pre-Rotation Fade**
   * Fade out equations before any camera rotations or complex slice additions, then fade back in when motion stops.
   ```python
   self.play(FadeOut(equation)) # rotate camera or add big elements
   self.play(FadeIn(equation))
   ```



---

## Some error you need to avoid
1 nNameError: name Cuboid is not defined: Fix
    Shape you need  Manim class  Example
    Standard cube   Cube        Cube(side_length=2)
    Rectangular box Prism       Prism(dimensions=[2,1,3])

2. Mobject.__getattr__.<locals>.getter() takes 1 positional argument but 2 were given
    Fix: call it with no args, e.g. 
    mobj.get_center()

3. latex error converting to dvi
    Fix:
    Use pure math mode or split into two Tex parts. For example:
    Option 1 (all math mode, no \textbf):
    title = Tex(r"3D Surface: $z = \sin(x)\cos(y)$", font_size=48, color=WHITE)
    
    Option 2 (use Tex with two parts, bold handled separately):
    title = Tex(r"\textbf{3D Surface: }", r"$z = \sin(x)\cos(y)$", font_size=48, color=WHITE)

4. 'ThreeDCamera' object has no attribute 'animate'
    Fix:
    ThreeDCamera has no .animate. Use move_camera(...) or set_camera_orientation(...) in a ThreeDScene.

5. Unexpected argument None passed to Scene.play().
    Check every object inside self.play(...) → make sure they are real Animations/Mobjects, not None.
    For example:
    x_label = axes.get_x_axis_label(MathTex("x")) 
    y_label = axes.get_y_axis_label(MathTex("f(x)"))
    self.play(Write(x_label), Write(y_label))  

6. TypeError: manim.mobject.text.numbers.DecimalNumber() got multiple values for keyword argument 'font_size'
    Fix:

    Use it only once:
    DecimalNumber(3.14, num_decimal_places=2, font_size=48)
    Or set later:

    num = DecimalNumber(3.14)
    num.set(font_size=48)

7. TypeError: Mobject.__getattr__.<locals>.getter() got an unexpected keyword argument 'x_range'
    Axes, NumberPlane accept x_range, y_range.
    axes = Axes(x_range=[-5, 5], y_range=[-3, 3])  



## Multi-Element 3D Visualizations

**For complex scenes with multiple 3D components (surfaces + slices + volumes + annotations):**

* Use progressive transparency hierarchy:
  - Base surface: `opacity=0.6`
  - Cross-sections/slices: `opacity=0.4`
  - Volume elements/Riemann boxes: `opacity=0.3`

* Layer elements with visual priority:
  - Main surface → Cross-sections → Volume elements → Annotations

* Fade out equations temporarily during complex element additions:
```python
self.play(FadeOut(equations))
# Add complex 3D elements
self.play(FadeIn(equations))
```

* Position dynamic text to avoid 3D element bounding boxes
* Check for overlaps after each new 3D element addition

---

## Dynamic Equation Management

**For equations that change during animation:**

* Start equations at safe elevated position to avoid overlap:
```python
equations.to_edge(LEFT).shift(UP*2)  # Higher placement
```

* Monitor 3D element growth and adjust equation position:
```python
if surface.height > 4 or len(3d_elements) > 3:
    equations.shift(UP*0.5)
```

* Use `Transform` for equation updates, not new objects:
```python
new_equation = MathTex(r"new_formula", font_size=36)
new_equation.move_to(equations.get_center())
self.play(Transform(equations, new_equation))
```

* Implement bounds checking after updates:
```python
if equations.get_top()[1] < 3.5 and overlaps_with_3d(equations, surface):
    equations.to_edge(LEFT).shift(UP*3)
```

---

## Cross-Section and Slice Management

**For visualizations showing slices or cross-sections:**

* Calculate slice spacing to prevent overlap:
```python
num_slices = 10
slice_spacing = surface_width / (num_slices + 1)
```

* Use distinct colors for different slice types:
  - XY-plane slices: `BLUE`
  - XZ-plane slices: `GREEN`
  - Integration bound slices: `ORANGE`

* Animate slice appearance progressively:
```python
for slice in slices:
    self.play(Create(slice), run_time=0.3)
    self.wait(0.1)
```

* Group slices for collective operations:
```python
slice_group = VGroup(*slices)
self.play(slice_group.animate.set_opacity(0.3))
```

---

## Riemann Sum and Volume Visualization

**For double/triple integrals with volume elements:**

* Volume boxes must use high transparency:
```python
box = Cube()
box.set_fill_opacity(0.3)
box.set_stroke_opacity(0.6)
```

* Position boxes within calculated integration bounds
* Stagger appearance to maintain clarity:
```python
self.play(
    AnimationGroup(*[Create(box) for box in volume_boxes], lag_ratio=0.05),
    run_time=3
)
```

* Use wireframe mode for interior visibility:
```python
box.set_stroke(WHITE, width=1)
box.set_fill(BLUE, opacity=0.2)
```

---

## Adaptive Content Management

* Check 3D scene complexity before displaying all elements:
```python
total_elements = len([surface, *slices, *volumes, axes])
if total_elements > 5:
    # Fade out equations during main visualization
    self.play(FadeOut(equations), run_time=0.5)
```

* If 3D object exceeds 60% of frame space, fade out supplementary text:
```python
frame_w, frame_h = config.frame_width, config.frame_height
if surface.width > frame_w * 0.6 or surface.height > frame_h * 0.6:
    self.play(FadeOut(equations), run_time=1)
    self.wait(0.5)
```

* Keep title visible at all times - only fade equations and bottom text

---

## Title First Appearance

* Always animate the **main title first** before any other elements
* Use `Write(title)` or `FadeIn(title)` animation
* Adjust font sizes proportionally - reduce if many elements needed
* Keep descriptive text fixed using `add_fixed_in_frame_mobjects(...)`
* Group related text in `VGroup` with clear vertical spacing

---

## Main Title

* Center horizontally at top: `title.to_edge(UP, buff=0.3)`
* No equations in title text
* Bold style: `Tex(r"\\textbf{Title Text}", font_size=48)`
* Leave 0.3-0.5 units space beneath title for other elements

---

## Equations / Descriptive Text

**Without title:**
* Position at top corner: `to_edge(LEFT)` or `to_edge(RIGHT)`
* Shift down slightly: `.shift(DOWN*0.2)`

**With title:**
* Position below title: `next_to(title, DOWN, buff=0.3).to_edge(LEFT)`
* Maintain horizontal distance from center to avoid 3D object overlap
* **For multi-element scenes:** Position higher: `to_edge(LEFT).shift(UP*2)`

**Equations may be faded out if:**
* 3D object requires full frame visibility
* Multiple 3D elements create visual clutter
* Dynamic updates cause temporary overlap

---

## Space Management Rules

**Priority order:**
1. Title (always visible)
2. Main 3D object
3. Secondary 3D elements (slices, volumes)
4. Equations
5. Bottom text

**If space limited:**
* Fade elements in reverse priority order
* Maintain clean visual hierarchy
* Large/complex objects take precedence

---

## Frame Boundaries and Safety

* Leave comfortable margins between text and frame edges
* Keep x, y, z axis lengths proportional for balanced objects
* All fixed text must stay within visible boundaries
* Use `add_fixed_in_frame_mobjects()` for ALL text elements

---

## Axes & Camera Rotation

* Use `ThreeDAxes` with 3D objects
* Group axes with objects: `VGroup(object, axes)` for synchronized rotation
* Draw and label x, y, z axes for clarity
* Center 3D surfaces at `ORIGIN`
* Choose camera orientation keeping entire object visible

---

## Camera Configuration

* Standard orientation: `self.set_camera_orientation(phi=75*DEGREES, theta=-45*DEGREES, distance=8)`
* Adjust distance for object size:
  - Small objects: `distance=6-8`
  - Large objects: `distance=10-12`
  - Multi-element scenes: `distance=12-15`
* Ensure no clipping throughout animations

---

## Extra Text / Graph Descriptions

* Position at bottom: `to_edge(DOWN, buff=0.4)`
* Use smaller font: 28-32pt
* Apply `add_fixed_in_frame_mobjects(bottom_text)`
* Leave adequate spacing from 3D objects
* Fade out if 3D object becomes too large

---

## Object Creation and Styling

**Never set opacity in constructors:**

**WRONG:**
```python
Surface(..., fill_opacity=0.8, stroke_opacity=0.5)
```

**CORRECT:**
```python
surface = Surface(...)
surface.set_fill_opacity(0.8)
surface.set_stroke_opacity(0.5)
```

---

## 3D Object Positioning

* Always center at `ORIGIN`
* Scale to fit bounds: typically -5 to 5 in each dimension
* Ensure visibility from camera angle
* Group related elements for synchronized transformations

---

## Text Management in 3D

* ALL text uses `add_fixed_in_frame_mobjects()`
* Position before adding to fixed frame
* Verify readability from camera angle
* Font size hierarchy: Title(48) > Equations(36) > Descriptions(30)

---

## Animation Timing

* Title: 1-2 seconds
* Equations: 2-3 seconds
* Axes: 1-2 seconds
* 3D object: 3-5 seconds
* Additional elements (slices/volumes): 0.3 seconds each without lag
* Rotations: 4-6 seconds with `rate_func=linear`
* Fade operations: 1 second

---

## LaTeX and Mathematical Expressions

* Use raw strings: `MathTex(r"x^2")`
* Escape curly braces in prompts: `\\textbf{title}`
* Group equations: `VGroup().arrange(DOWN, buff=0.2)`
* Ensure proper rendering

---

## Validation Checklist

All text uses `add_fixed_in_frame_mobjects()`  
3D objects centered at `ORIGIN`  
Camera distance appropriate for scene complexity  
Title animated first, then equations, axes, object  
No opacity in constructors  
Complex scenes trigger equation fade-out  
All elements within frame boundaries  
Text readable throughout animations  
Multi-element transparency hierarchy applied  
Dynamic equations positioned to avoid overlaps  

---

## Common 3D Layout Issues Prevention

* **Text rotation:** Use fixed frame positioning
* **Object clipping:** Adjust camera distance and scaling
* **Equation overlap:** Implement adaptive fade-out and repositioning
* **Axis misalignment:** Group axes with objects
* **Title overcrowding:** Fade non-essential text
* **Multi-element confusion:** Use transparency hierarchy
* **Dynamic text overlap:** Reposition equations as scene evolves

---

## Complete Example

```python
from manim import *
import numpy as np


class Animation_ea6da621(ThreeDScene):
    def construct(self):
        # Step 1: Set up the 3D scene.
        self.camera.background_color = BLACK
        self.set_camera_orientation(phi=75 * DEGREES, theta=-45 * DEGREES, distance=10)

        # Axes
        axes = ThreeDAxes(
            x_range=[-3.14, 3.14, 1.57],
            y_range=[-3.14, 3.14, 1.57],
            z_range=[-2, 2, 1],
            x_length=7,
            y_length=7,
            z_length=4,
        )
        x_label = axes.get_x_axis_label("x")
        y_label = axes.get_y_axis_label("y")
        z_label = axes.get_z_axis_label("z")
        
        # Title (fixed to camera) - Start invisible
        title = Tex(r"\textbf{3D Surface Plot}", font_size=48)
        title.set_opacity(0)  # Make invisible initially
        self.add_fixed_in_frame_mobjects(title)
        title.to_edge(UP)

        # Equation (fixed to camera) - Start invisible
        equation = MathTex(r"f(x, y) = \sin(x) + \cos(y)", font_size=36)
        equation.set_opacity(0)  # Make invisible initially
        self.add_fixed_in_frame_mobjects(equation)
        equation.next_to(title, DOWN, buff=0.4).to_edge(LEFT)

        # Bottom description (fixed to camera) - Start invisible
        bottom_description = Tex(r"Function: $f(x, y) = \sin(x) + \cos(y)$", font_size=30)
        bottom_description.set_opacity(0)  # Make invisible initially
        self.add_fixed_in_frame_mobjects(bottom_description)
        bottom_description.to_edge(DOWN, buff=0.3)

        # --- Animate text appearance with fade-in effect ---
        self.play(title.animate.set_opacity(1), run_time=1)
        self.play(equation.animate.set_opacity(1), run_time=2)
        self.play(bottom_description.animate.set_opacity(1), run_time=1)
        self.wait(1)

        # --- Show axes & labels ---
        self.play(Create(axes), run_time=2)
        self.play(Write(x_label), Write(y_label), Write(z_label))
        self.wait(1)

        # --- Now animate the surface ---
        surface = Surface(
            lambda u, v: np.array([u, v, np.sin(u) + np.cos(v)]),
            u_range=[-3.14, 3.14],
            v_range=[-3.14, 3.14],
            resolution=(40, 40)
        )
        surface.set_style(fill_color=BLUE_D, fill_opacity=0.8, stroke_color=BLUE_E)
        surface.move_to(ORIGIN)

        self.play(Create(surface), run_time=3)
        self.wait(1)

        # --- Rotate whole group (surface + axes + labels) ---
        group = VGroup(surface, axes, x_label, y_label, z_label)
        self.play(Rotate(group, angle=TAU, axis=Z_AXIS, run_time=6, rate_func=linear))
        self.wait(2)

```
<3D Scenes and Graph Rule Only/>

"""

COMPUTER_DATASTRUCTURE="""
<Computer Data Structure Rule Only>
### Mandatory Structure
1. **Title Placement**: Always centered (not top). Must appear first, then fade out completely before any new object or text appears. Avoid including equations or expressions in the title.
2. **Numeric Formatting**: Prefer integers; if decimals are needed, use two-decimal precision. Avoid π or symbolic constants in numeric labels.
3. **Text Placement**: Place texts near screen corners (UL, UR, DL, DR) or top edge, maintaining a 5% screen margin. Ensure texts do not overlap any existing objects; if overlap occurs, fade the text out instead of repositioning unsafely.
4. **Margin Enforcement**: Maintain 5% margin on all screen sides — top, bottom, left, and right.
5. **Graph/Object**: Object should not overlap with the text or anything maintain 1% gap
5. **Scene Sequence**: Must follow this strict order → **Title → FadeOut → Text (Adaptive) → Graph/Object**. No parallel animation that interrupts this order.

---

### 🚨 OVERLAP PREVENTION CHECKLIST (MANDATORY)

#### Rule 1: Sequential Text Display at Same Location
**If multiple texts need to appear in the same location:**

```python
# CORRECT - Sequential with complete fadeout
text1 = Text("First Message", font_size=TEXT_SIZE)
text1.move_to([0, 3, 0])
self.play(FadeIn(text1), run_time=0.5)
self.wait(1.5)
self.play(FadeOut(text1), run_time=0.5)
self.wait(0.2)  # Buffer time

text2 = Text("Second Message", font_size=TEXT_SIZE)
text2.move_to([0, 3, 0])  # Same position as text1
self.play(FadeIn(text2), run_time=0.5)
self.wait(1.5)
self.play(FadeOut(text2), run_time=0.5)

**Timing Pattern:**
```
FadeIn(0.5s) → Wait(1.5s) → FadeOut(0.5s) → Buffer(0.2s) → Next Text
```

**RULE: One location = One text at a time. Previous must fade out completely before next appears.**

---

#### Rule 2: Corner Distribution for Simultaneous Texts
**If multiple texts must be visible simultaneously:**

```python
# CORRECT - Distributed to corners
text1 = Text("DFS Preorder", font_size=TEXT_SIZE)
text1.to_corner(UL, buff=0.5)  # Upper-Left

text2 = Text("Traversal: Left→Right", font_size=TEXT_SIZE)
text2.to_corner(UR, buff=0.5)  # Upper-Right

text3 = Text("Stack: [1, 2, 4]", font_size=TEXT_SIZE)
text3.to_corner(DL, buff=0.5)  # Down-Left

text4 = Text("Visited: [1]", font_size=TEXT_SIZE)
text4.to_corner(DR, buff=0.5)  # Down-Right

self.play(
    FadeIn(text1), FadeIn(text2), 
    FadeIn(text3), FadeIn(text4),
    run_time=1
)


---

#### Rule 3: Vertical Stacking (Alternative)
**For top-aligned multiple texts:**

```python
TOP_BUFFER = config.frame_height * 0.05
VERTICAL_SPACING = 0.8  # Minimum 8% screen height

top_y = config.frame_height/2 - TOP_BUFFER

text1 = Text("Line 1", font_size=TEXT_SIZE)
text1.move_to([0, top_y, 0])

text2 = Text("Line 2", font_size=TEXT_SIZE)
text2.move_to([0, top_y - VERTICAL_SPACING, 0])  # Stack below

text3 = Text("Line 3", font_size=TEXT_SIZE)
text3.move_to([0, top_y - 2*VERTICAL_SPACING, 0])  # Stack below

self.play(FadeIn(text1), FadeIn(text2), FadeIn(text3), run_time=1)
```

---

#### Rule 4: Object-Text Collision Detection
**Before placing any text, verify no collision with graph/object:**

```python
# CORRECT - Check bounding boxes
graph_top = graph.get_top()[1]
graph_bottom = graph.get_bottom()[1]
graph_left = graph.get_left()[0]
graph_right = graph.get_right()[0]

# Place text safely above graph
label_y = graph_top + 0.5  # 0.5 unit gap
label = Text("Graph Label", font_size=LABEL_SIZE)
label.move_to([0, label_y, 0])

# Verify no overlap
if label.get_bottom()[1] > graph_top:
    # Safe - no overlap
    self.play(FadeIn(label))
else:
    # Overlap detected - reposition or fade out conflicting object
    label.move_to([0, graph_top + 1, 0])
```

**Minimum Gap Rules:**
- Text ↔ Graph: 1% screen height = `config.frame_height * 0.01`
- Text ↔ Text: 8% screen height = `config.frame_height * 0.08`
- Text ↔ Edge: 5% margin from screen border

---

#### Rule 5: Dynamic Text Abbreviation
**If text is too long and causes overlap:**

```python
# CORRECT - Abbreviate or reduce font
original_text = "Depth First Search Preorder Traversal (Recursive)"

# Option A: Abbreviate
short_text = Text("DFS Preorder (Recursive)", font_size=TEXT_SIZE)

# Option B: Reduce font dynamically
if len(original_text) > 30:
    font_size = TEXT_SIZE * 0.8  # 80% of original
else:
    font_size = TEXT_SIZE

label = Text(original_text, font_size=font_size)

# Option C: Multi-line
label = Text(
    "Depth First Search\nPreorder Traversal", 
    font_size=TEXT_SIZE,
    line_spacing=1.2
)
```

---

#### Rule 6: Pre-Animation Overlap Check
**Always verify positions before animating:**

```python
def check_overlap(obj1, obj2, min_gap=0.1):
    # Check if two objects overlap with minimum gap
    box1 = obj1.get_bounding_box_vertices()
    box2 = obj2.get_bounding_box_vertices()
    
    # Get bounds
    obj1_right = box1[2][0]
    obj1_left = box1[0][0]
    obj1_top = box1[1][1]
    obj1_bottom = box1[0][1]
    
    obj2_right = box2[2][0]
    obj2_left = box2[0][0]
    obj2_top = box2[1][1]
    obj2_bottom = box2[0][1]
    
    # Check horizontal overlap
    h_overlap = not (obj1_right + min_gap < obj2_left or 
                     obj2_right + min_gap < obj1_left)
    
    # Check vertical overlap
    v_overlap = not (obj1_top + min_gap < obj2_bottom or 
                     obj2_top + min_gap < obj1_bottom)
    
    return h_overlap and v_overlap

# Usage
text1 = Text("Label 1", font_size=TEXT_SIZE).move_to([0, 2, 0])
text2 = Text("Label 2", font_size=TEXT_SIZE).move_to([0, 2, 0])

if check_overlap(text1, text2):
    # Collision detected - use sequential display
    self.play(FadeIn(text1), run_time=0.5)
    self.wait(1)
    self.play(FadeOut(text1), run_time=0.5)
    self.play(FadeIn(text2), run_time=0.5)
else:
    # Safe to show simultaneously
    self.play(FadeIn(text1), FadeIn(text2), run_time=0.5)
```

---

#### Rule 7: Group Management for Complex Scenes
**Use VGroup to manage related objects:**

```python
# CORRECT - Group and manage together
top_labels = VGroup()

label1 = Text("Method: DFS", font_size=TEXT_SIZE)
label1.to_corner(UL, buff=0.5)
top_labels.add(label1)

label2 = Text("Order: Preorder", font_size=TEXT_SIZE)
label2.to_corner(UR, buff=0.5)
top_labels.add(label2)

# Show all together
self.play(FadeIn(top_labels), run_time=1)

# Clear all together before next scene
self.play(FadeOut(top_labels), run_time=0.5)
self.wait(0.2)

# Now safe to add new labels
new_label = Text("New Scene", font_size=TEXT_SIZE)
new_label.to_corner(UL, buff=0.5)
self.play(FadeIn(new_label), run_time=0.5)
```

---

#### Rule 8: Scene Transition Protocol
**Between major scene changes:**

```python
# CORRECT - Complete fadeout before new scene
# Scene 1: Show graph with labels
graph = ...
labels = VGroup(label1, label2, label3)
self.play(Create(graph), FadeIn(labels))
self.wait(2)

# Transition: Clear everything
self.play(
    FadeOut(graph), 
    FadeOut(labels),
    run_time=1
)
self.wait(0.5)  # Buffer

# Scene 2: New content (no overlap risk)
new_graph = ...
new_labels = VGroup(new_label1, new_label2)
self.play(Create(new_graph), FadeIn(new_labels))
```

---

### OVERLAP PREVENTION SUMMARY

**MUST DO:**
1. Sequential display if same location (FadeOut → Wait → FadeIn)
2. Corner distribution if simultaneous (UL, UR, DL, DR)
3. Vertical stacking with 8% spacing minimum
4. 1% gap between text and graph/objects
5. 5% margin from screen edges
6. Complete fadeout before scene transitions
7. Group related objects with VGroup
8. Abbreviate long text to prevent overflow

---

### Deprecated → New (Manim v0.19+)

---

## Common Deprecated → New

* `to_edge(...)` still works, but prefer `.next_to()` for finer control.
* `to_corner(...)` → use `.align_on_border(...)`.
* `axes.to_center()` → use `axes.move_to(ORIGIN)` or `axes.center()`.
* `shift(x*RIGHT)` still valid.
* `scale_in_place(factor)` → use `.scale(factor, about_point=...)`.
* `fade_in` / `fade_out` methods → use animations: `FadeIn(mobj)` / `FadeOut(mobj)`.
* `ShowCreation(mobj)`  → `Create(mobj)`.
* `Write(mobj, run_time=...)`  still valid.
* `Transform(m1, m2)`  still valid.
* `SurroundingRectangle(..., buff=0.1)`  still valid.
* `.start_point or .end_point` -> use `.get_start()` or `.get_end()`.

---

## Colors / Styles

- `stroke_width` → still valid.
- `stroke_opacity=...` in constructor → not allowed. Use `.set_stroke(opacity=...)`.
- `fill_opacity=...` in constructor → still valid.
- `line_arg_dict` → deprecated.  Use: 
  - `axis_config={...}` → for styling axes 
  - `background_line_style={...}` → **only inside Axes or NumberPlane**.
- `stroke_dash_length` → not valid. Use `DashedLine(...)` or `DashedVMobject(...)`.

---

## Text / Labels

* `TextMobject(...)` → use `Tex(...)`.
* `TexMobject(...)` → use `Tex(...)`.
* `edge_buffer` argument (e.g., in `Text`) → not valid. Replace with `.next_to(..., buff=...)` or `.align_on_border(...)`.
* `Text(..., t2c=...)` → still valid. 
* `t2s` (text-to-style) → replaced by `.set_color_by_t2s()`.

---

## Shapes

* `ArcBetweenPoints(..., radius=...)` → `ArcBetweenPoints(..., angle=...)`.
* `Sector(inner_radius=...)` → replaced with `AnnularSector(inner_radius=...)`.

---

## NumberLine

* `NumberLine(default_numbers_to_display=...)` → removed. Use `include_numbers=True` and control with `numbers_to_include=[...]` or `decimal_number_config={...}`.
* `exclude_zero_from_default_numbers` → removed. Must explicitly control numbers via `numbers_to_include`.

---

## Camera / Scene

* `ThreeDScene.set_camera_orientation(...)` → still valid.
* `self.camera.animate.set(phi=..., theta=...)` → replaces old `self.move_camera(...)`.
* `self.set_camera_orientation(...)` → replaces old `set_camera_position(...)`.
* `self.set_camera_orientation(phi=..., theta=...)` → still valid; `gamma` is no longer supported.


---

## Geometry / Mobject Methods

* `.start_point` / `.end_point` → replaced with `.get_start()` / `.get_end()`.
* `.point_from_proportion(alpha)` → still valid.
* `scale_in_place(factor)` → deprecated. Use `.scale(factor, about_point=...)`.
* `.fade_in` / `.fade_out` (methods) → removed. Use `FadeIn(mobj)` / `FadeOut(mobj)` animations.
* `next_to(...)` → still valid and preferred over `to_edge(...)` for finer control.
* `to_corner(...)` → replaced with `.align_on_border(...)`.
* `.center()` or `.move_to(ORIGIN)` → replaces older `.to_center()`.
* `rotate(angle, axis=...)` → still valid.
* `.get_midpoint()` → preferred over manual midpoint calculations.
* `.get_vertices()` → still valid for polygons.
* `.copy()` → still valid.

## Summary of New Errors Fixed

* `TypeError: Mobject.__getattr__.<locals>.getter() got an unexpected keyword argument 'length'` → use `line_length`.
* `TypeError: Mobject.__getattr__.<locals>.getter() got an unexpected keyword argument 'x_val'` → use `x`.
* `TypeError: Mobject.__getattr__.<locals>.getter() got an unexpected keyword argument 'edge_buffer'` → replace with `.next_to(..., buff=...)`.
* `AttributeError: Axes object has no attribute 'y_axis_labels'` → use `axes.get_axis_labels()`.
* `AttributeError: NumberLine object has no attribute 'default_numbers_to_display'` → use `include_numbers=True` with `numbers_to_include`.
* `TypeError: ... got an unexpected keyword argument 'stroke_opacity'` → set via `.set_stroke(opacity=...)`.
* `AttributeError: NumberLine has no attribute 'exclude_zero_from_default_numbers'` → must use `numbers_to_include`.
* `TypeError: ... got an unexpected keyword argument 'gamma'` → camera no longer supports gamma.
* `NameError: name 'UP_LEFT' is not defined` → Use `UL` (UP + LEFT), `UR`, `DL`, `DR` instead.

### Font Size Rules (adjustable based on content length)
TITLE_SIZE = 46       # not fixed, can change based on title length
TEXT_SIZE = 36    # not fixed, can change based on TEXT_SIZE length
LABEL_SIZE = 28       # not fixed, can change based on axis label length
DESC_SIZE = 24        # not fixed, can change based on description length

Text(...) →  font_size works.
MathTex(...) →  font_size works.
Axes(..., axis_config={"font_size": ...}) →  font_size works.
axes.get_graph_label(...) →  font_size not allowed. Use: axes.get_graph_label(graph, label=MathTex(r"x^2", font_size=24))
```

### Mandatory Spacing Rules
```python
TOP_BUFFER = config.frame_height * 0.05      # 5% space from top
BOTTOM_BUFFER = config.frame_height * 0.05   # 5% space from bottom
LEFT_BUFFER = config.frame_width * 0.05      # 5% space from left
RIGHT_BUFFER = config.frame_width * 0.05     # 5% space from right
```
## Mandatory avoid these 

1. NameError: name 'LIGHT_BLUE' is not defined
    Use valid built-ins (from manim):
    from manim import BLUE, GREEN, TEAL, YELLOW, RED, ORANGE, PURPLE
    Or define your own shades:
    LIGHT_BLUE = "#87CEFA"   # hex for light sky blue
    LIGHT_GREEN = "#90EE90"  # hex for light green

    Then your code works:
    self.play(f1.animate.set_color(LIGHT_BLUE).set_opacity(0.4))

    
2. Mobject.__getattr__.<locals>.getter() got an unexpected keyword argument 'color'
    Fix: Import form the manim 
    from manim import Scene, MathTex, Axes, Write, WHITE
    or
    from manim import *

3. NameError: name 'BOTTOM' is not defined
    Fix: UP, DOWN, LEFT, RIGHT, ORIGIN are valid.

4. NameError: name 'WiggleOutThenIn' is not defined
    At the top of your script add:
    from manim import *
    or,
    from manim import Scene, Axes, MathTex, FadeIn, WiggleOutThenIn

5.  Mobject.__getattr__.<locals>.getter() got an unexpected keyword argument 'x_range'
    Fix: graph_sin_x = plane.plot(lambda x: np.sin(x), x_range=[-7, 7], color=BLUE)

6. TypeError: Mobject.__init__() got an unexpected keyword argument 'line_arg_dict'
    Fix: replace it with:
    background_line_style={...}
    Use axis_config={...} for Axes.

7. Error Message: Found `stroke_opacity` set in the constructor for `envelope_pos` and `envelope_neg`. According to the validation rules, opacity-related parameters should not be set in the constructor; use `.set_stroke(opacity=...)` or `.set_opacity()` after creation.

8. TypeError: Mobject.__init__() got an unexpected keyword argument 'stroke_dash_length'
    Fix: 
    # Option A: directly make dashed
    line1 = DashedLine(LEFT, RIGHT, dash_length=0.2, num_dashes=20)


    # Option B: wrap an existing object
    base = Line(LEFT, RIGHT)
    line2 = DashedVMobject(base, dash_length=0.2, num_dashes=20)


9. AttributeError: Axes object has no attribute 'to_center'
    Fix: 
    axes.move_to(ORIGIN)
    # or
    axes.center()

10. TypeError: Mobject.__init__() got an unexpected keyword argument 'background_line_style'
    Fix:
    background_line_style is only valid in NumberPlane or Axes, not in general Mobject.
    So you must pass it when constructing axes/plane, like this:

    axes = Axes(
        x_range=[-5, 5],
        y_range=[-3, 3],
        axis_config={"color": BLUE},              # style for main axes
        background_line_style={                   # style for grid lines
            "stroke_color": GREY,
            "stroke_width": 1,
            "stroke_opacity": 0.5,
        }
    )

11. Mobject.__getattr__.<locals>.getter() got an unexpected keyword argument 'length'
    Fix: axes.get_tangent_line(graph_sin, x_tracker.get_value(), line_length=3)

12. TypeError: Mobject.__init__() got an unexpected keyword argument 'x_axis_config'
    Axes does not accept x_axis_config or y_axis_config as keyword arguments at the top level of Axes(...)
    Fix:
    axes = Axes(
    x_range=[-5, 5, 1],
    y_range=[-3, 3, 1],
    axis_config={"font_size": 24},
    )

    or, if you need separate configs:

    axes = Axes(
        x_range=[-5, 5, 1],
        y_range=[-3, 3, 1],
        x_axis_config={"font_size": 24},
        y_axis_config={"font_size": 30},
    )

13. AxisError: axis 1 is out of bounds for array of dimension 1
    fix:
    curve1 = axes.plot_parametric_curve(
        lambda t: (x_func1(t), y_func1(t)),
        t_range=[0, 2*np.pi, 0.01],
        color=BLUE
    )

14. AttributeError: MathTex object has no attribute 'is_about_to_overlap' is_about_to_overlap() doesn't exist in ManimCE.

15. Mobject.__getattr__.<locals>.getter() got an unexpected keyword argument 't_range'
    Fix:
    curve = axes.plot_parametric_curve(
        lambda t: np.array([t, np.sin(t), 0]),
        t_range=[-PI, PI, 0.05],
        color=BLUE
    )

16. AttributeError: ParametricFunction object has no attribute 'x_to_alpha'
    Fix: x_to_alpha works only on Axes.plot, not on ParametricFunction.
    tangent_line = always_redraw(
        lambda: TangentLine(graph_sin, x=x_tracker.get_value(), length=4)
    )

17. AttributeError: Axes object has no attribute 'x_to_proportion'
    In new Manim (v0.19+), Axes has no x_to_proportion.
    Fix: 
    tangent_line = always_redraw(
        lambda: TangentLine(graph_sin, x=x_tracker.get_value(), length=4)
    )

18. TypeError: Mobject.__init__() got an unexpected keyword argument 'dash_length'
    Fix: 
    envelope_pos_graph = axes.plot(lambda x: np.sin(x), x_range=[-7,7], color=BLUE)
    envelope_pos = DashedVMobject(envelope_pos_graph)
    envelope_pos.set_dash(dash_length=0.1, dashed_ratio=0.5)

19. IndexError: list index out of range
    use a tiny visible placeholder, e.g.:

    MathTex(r"\;", font_size=LABEL_SIZE)  # thin space
    # or
    MathTex(r"0", font_size=LABEL_SIZE)

20. AttributeError: MathTex object has no attribute 'bounding_box'
    Fix: use properties or new methods:

    mobj.width
    mobj.height
    mobj.get_center()
    mobj.get_bounding_box_vertices()

21. TypeError: Mobject.__init__() got an unexpected keyword argument 'number_constructor_kwargs'
    Fix: remove it and customize numbers after creation:
    axes = Axes(x_range=[-2.5*np.pi, 2.5*np.pi, np.pi/2], y_range=[-1.5, 1.5, 0.5])
    for x_val in axes.x_axis.numbers:
        x_val.set_color(BLUE)

22. NameError: name 'FillBetween' is not defined
    FillBetween isn't auto-imported in v0.19+.
    Fix: 
    Add this line:
    from manim.mobject.graphing.utils import FillBetween
    Or use axes.get_area() as an alternative.

23. TypeError: Mobject.__init__() got an unexpected keyword argument 'color_map'
    Fix:

    surface = Surface(..., resolution=(30,30))
    surface.set_style(fill_color=BLUE, fill_opacity=0.7)

    For gradient:
    surface.set_fill_by_value(axes=axes, colors=[(BLUE,-1),(GREEN,0),(RED,1)])

24. NameError: name 'ParametricSurface' is not defined
    Fix:
    NameError: name 'ParametricSurface' is not defined
    
25. TypeError: Mobject.__init__() got an unexpected keyword argument 'res_u'
    Error comes from res_u / res_v → not valid in v0.19.
    Fix:
    resolution=(20, 20)

26. TypeError: Mobject.__init__() got an unexpected keyword argument 'dash_length'
    Fix for current version: use num_dashes instead:
    envelope_pos = DashedVMobject(envelope_pos_graph, num_dashes=50, dashed_ratio=0.5)
    envelope_neg = DashedVMobject(envelope_neg_graph, num_dashes=50, dashed_ratio=0.5)

27. AttributeError: 'Camera' object has no attribute 'frame'
    Fix:
    step2_title.to_edge(UP, buff=TOP_BUFFER)

28. AttributeError: VGroup object has no attribute 'last_mobject'
    Fix:
    Use this output_num_mobj.next_to(output_numbers_group[-1], RIGHT, buff=0.5)

    
## ANIMATION SEQUENCE (MANDATORY ORDER)

### STEP 1: Title in center only
title = Text("Your Title Here", font_size=TITLE_SIZE)
title.move_to(ORIGIN)   # center of screen

self.play(Write(title, run_time=1.5))
self.wait(3)

## QUICK STATISTICS TEMPLATE
```python
from manim import *
import numpy as np

class BubbleSortAnimation(Scene):
    def construct(self):
        # ===== CONSTANTS =====
        TITLE_SIZE = 46
        TEXT_SIZE = 36
        LABEL_SIZE = 28
        DESC_SIZE = 24

        TOP_BUFFER = config.frame_height * 0.05
        BOTTOM_BUFFER = config.frame_height * 0.05
        LEFT_BUFFER = config.frame_width * 0.05
        RIGHT_BUFFER = config.frame_width * 0.05

        self.camera.background_color = "#0a0a0a"

        # ===== STEP 1: Display the title =====
        title = Text("Bubble Sort Algorithm", font="Montserrat", font_size=TITLE_SIZE, color=WHITE, weight=BOLD)
        title.move_to(ORIGIN)

        self.play(Write(title, run_time=1.5))
        self.wait(1)

        # Fade out title
        self.play(FadeOut(title), run_time=1)
        self.wait(0.5)

        # ===== STEP 2: Setup description and array =====
        top_y = config.frame_height/2 - TOP_BUFFER

        # Description text at top
        desc_text = Text(
            "Compare adjacent elements and swap if in wrong order",
            font="Montserrat",
            font_size=DESC_SIZE,
            color="#87CEFA"
        )
        desc_text.move_to([0, top_y - 0.4, 0])

        # Pass counter
        pass_text = Text("Pass: 0", font="Montserrat", font_size=TEXT_SIZE, color="#90EE90", weight=BOLD)
        pass_text.move_to([0, top_y - 1.2, 0])

        self.play(Write(desc_text), run_time=1)
        self.play(Write(pass_text), run_time=0.5)
        self.wait(0.5)

        # ===== STEP 3: Create the array =====
        array_values = [64, 34, 25, 12, 22, 11, 90]
        array_elements = []
        
        def create_array_element(value, position):
            # Create a box with number insid
            box = Rectangle(width=1.0, height=1.0, stroke_color="#4682B4", fill_color="#1e3a5f", fill_opacity=0.8)
            number = Text(str(value), font="Montserrat", font_size=30, color=WHITE, weight=BOLD)
            element = VGroup(box, number)
            element.move_to(position)
            return element, value

        # Position array in center
        array_start_x = -3.5
        array_y = 0
        spacing = 1.2

        for i, val in enumerate(array_values):
            pos = [array_start_x + i * spacing, array_y, 0]
            element, value = create_array_element(val, pos)
            array_elements.append(element)

        # Show array
        self.play(
            LaggedStart(*[FadeIn(elem) for elem in array_elements], lag_ratio=0.1),
            run_time=1.5
        )
        self.wait(1)

        # ===== STEP 4: Bubble Sort Algorithm =====
        n = len(array_values)
        
        for pass_num in range(n - 1):
            # Update pass counter
            self.play(
                pass_text.animate.become(
                    Text(f"Pass: {pass_num + 1}", font="Montserrat", font_size=TEXT_SIZE, color="#90EE90", weight=BOLD).move_to(pass_text.get_center())
                ),
                run_time=0.3
            )
            self.wait(0.3)

            for i in range(n - pass_num - 1):
                # Highlight elements being compared
                self.play(
                    array_elements[i][0].animate.set_stroke(color=YELLOW, width=4),
                    array_elements[i + 1][0].animate.set_stroke(color=YELLOW, width=4),
                    run_time=0.3
                )
                
                # Show comparison with symbols
                val1 = array_values[i]
                val2 = array_values[i + 1]
                
                # Position for comparison text (above the elements)
                comp_y = array_elements[i].get_center()[1] + 1.5
                comp_x = (array_elements[i].get_center()[0] + array_elements[i + 1].get_center()[0]) / 2
                
                if val1 > val2:
                    comparison = MathTex(f"{val1}", ">", f"{val2}", font_size=32, color=WHITE)
                    comparison.move_to([comp_x, comp_y, 0])
                    comparison[1].set_color("#FF6347")  # Red for greater than
                else:
                    comparison = MathTex(f"{val1}", r"\leq", f"{val2}", font_size=32, color=WHITE)
                    comparison.move_to([comp_x, comp_y, 0])
                    comparison[1].set_color("#90EE90")  # Green for less than or equal
                
                self.play(Write(comparison), run_time=0.3)
                self.wait(0.3)

                # Compare values
                if array_values[i] > array_values[i + 1]:
                    # Flash red for swap
                    self.play(
                        array_elements[i][0].animate.set_fill(color="#8B0000", opacity=0.9),
                        array_elements[i + 1][0].animate.set_fill(color="#8B0000", opacity=0.9),
                        run_time=0.2
                    )
                    
                    # Add "SWAP" label
                    swap_label = Text("SWAP", font="Montserrat", font_size=24, color="#FF6347", weight=BOLD)
                    swap_label.move_to([comp_x, comp_y - 0.6, 0])
                    self.play(FadeIn(swap_label), run_time=0.2)
                    
                    # Swap animation
                    elem1_pos = array_elements[i].get_center()
                    elem2_pos = array_elements[i + 1].get_center()
                    
                    # Move elements
                    self.play(
                        array_elements[i].animate.move_to(elem2_pos + UP * 0.5),
                        array_elements[i + 1].animate.move_to(elem1_pos + DOWN * 0.5),
                        run_time=0.4
                    )
                    self.play(
                        array_elements[i].animate.move_to(elem2_pos),
                        array_elements[i + 1].animate.move_to(elem1_pos),
                        run_time=0.4
                    )
                    
                    # Swap in list
                    array_elements[i], array_elements[i + 1] = array_elements[i + 1], array_elements[i]
                    array_values[i], array_values[i + 1] = array_values[i + 1], array_values[i]
                    
                    # Reset colors and remove labels
                    self.play(
                        array_elements[i][0].animate.set_fill(color="#1e3a5f", opacity=0.8).set_stroke(color="#4682B4", width=2),
                        array_elements[i + 1][0].animate.set_fill(color="#1e3a5f", opacity=0.8).set_stroke(color="#4682B4", width=2),
                        FadeOut(comparison),
                        FadeOut(swap_label),
                        run_time=0.2
                    )
                else:
                    # Flash green for no swap
                    self.play(
                        array_elements[i][0].animate.set_fill(color="#006400", opacity=0.9),
                        array_elements[i + 1][0].animate.set_fill(color="#006400", opacity=0.9),
                        run_time=0.2
                    )
                    
                    # Add "NO SWAP" label
                    no_swap_label = Text("NO SWAP", font="Montserrat", font_size=24, color="#90EE90", weight=BOLD)
                    no_swap_label.move_to([comp_x, comp_y - 0.6, 0])
                    self.play(FadeIn(no_swap_label), run_time=0.2)
                    self.wait(0.2)
                    
                    # Reset colors and remove labels
                    self.play(
                        array_elements[i][0].animate.set_fill(color="#1e3a5f", opacity=0.8).set_stroke(color="#4682B4", width=2),
                        array_elements[i + 1][0].animate.set_fill(color="#1e3a5f", opacity=0.8).set_stroke(color="#4682B4", width=2),
                        FadeOut(comparison),
                        FadeOut(no_swap_label),
                        run_time=0.2
                    )
                
                self.wait(0.1)

            # Mark sorted element (last element in this pass)
            sorted_index = n - pass_num - 1
            self.play(
                array_elements[sorted_index][0].animate.set_fill(color="#228B22", opacity=0.9).set_stroke(color="#32CD32", width=3),
                run_time=0.3
            )
            self.wait(0.3)

        # Mark first element as sorted (it's sorted by default after all passes)
        self.play(
            array_elements[0][0].animate.set_fill(color="#228B22", opacity=0.9).set_stroke(color="#32CD32", width=3),
            run_time=0.3
        )
        self.wait(0.5)

        # ===== STEP 5: Final message =====
        sorted_text = Text("Array Sorted!", font="Montserrat", font_size=TEXT_SIZE, color="#FFD700", weight=BOLD)
        sorted_text.move_to([0, array_y - 2, 0])
        
        self.play(Write(sorted_text), run_time=1)
        self.wait(1)

        # Complexity info
        complexity_text = Text(
            "Time Complexity: O(n²)  |  Space Complexity: O(1)",
            font="Montserrat",
            font_size=DESC_SIZE,
            color="#87CEFA"
        )
        complexity_text.move_to([0, array_y - 2.8, 0])
        
        self.play(Write(complexity_text), run_time=1)
        self.wait(2)

        # ===== STEP 6: Cleanup =====
        self.play(
            FadeOut(VGroup(*array_elements)),
            FadeOut(desc_text),
            FadeOut(pass_text),
            FadeOut(sorted_text),
            FadeOut(complexity_text),
            run_time=1.5
        )
        self.wait(1)
```
<Computer Data Structure Rule Only/>
"""

PHYSICS = """
<Physics Visualization Rule Only>
## Mandatory way to design

1. Title: Always at the center (never top). Must appear first and then fade out with a smooth animation (e.g., FadeOut, LaggedStart, star-burst effect).
2. Axes: Create axes immediately after title fades. Show only relevant axes (x, y) with margins.
3. Numbers: Use integers mostly; if needed, 2 decimal precision.
4. Axes style: No grid unless needed. Include only numbers required for visualization.
5. Legend / Equation: Place formula, mean, variance, or legend in corners. If no space → fade out temporarily.
6. Margins: Leave a 5% gap at edges.
7. Sequence: Title → Axes → Legend/Formula → Graph → Dynamic Highlight.

## Graph Types Supported
- BarChart
- Scatter Plot
- Line Plot (from dataset)
- Histogram
- Boxplot (manual construction)
- etc

### Deprecated → New (Manim v0.19+)

---

## Common Deprecated → New

* `to_edge(...)` still works, but prefer `.next_to()` for finer control.
* `to_corner(...)` → use `.align_on_border(...)`.
* `axes.to_center()` → use `axes.move_to(ORIGIN)` or `axes.center()`.
* `shift(x*RIGHT)` still valid.
* `scale_in_place(factor)` → use `.scale(factor, about_point=...)`.
* `fade_in` / `fade_out` methods → use animations: `FadeIn(mobj)` / `FadeOut(mobj)`.
* `ShowCreation(mobj)`  → `Create(mobj)`.
* `Write(mobj, run_time=...)`  still valid.
* `Transform(m1, m2)`  still valid.
* `SurroundingRectangle(..., buff=0.1)`  still valid.
* `.start_point or .end_point` -> use `.get_start()` or `.get_end()`.

---

## Axes / Graphs

* `axes.get_graph(f, ...)` → deprecated. Use `axes.plot(f, x_range=[...], color=...)`.

* `axes.get_area(f, ...)` → still valid for one function. For two functions use `FillBetween(...)`.

* `NumberPlane.get_graph(...)` → does not exist. Use `plane.plot(...)`.

* `add_coordinates()` → still valid.

* `axes.get_tangent_line(graph, x=..., line_length=...)` → does not exist. Use `TangentLine(graph, alpha, length=...)` where `alpha ∈ [0,1]`. To map `x` to `alpha`, use helpers like `axes.i2gp`.

* `axes.get_vertical_line(x_val=...)` wrong → invalid. Correct: `axes.get_vertical_line(point, **kwargs)`.
  (use `axes.c2p(x_value, y_value)` or `axes.i2gp(x_value, graph)` to get the point).

* `axes.y_axis_labels` wrong → no attribute. Use `axes.get_axis_labels()`.

* `y_axis_config` must be passed explicitly inside `Axes(...)`, not accessed as an attribute afterwards.

* `axes.get_x_axis_label(...)` and `axes.get_y_axis_label(...)` → still valid, but prefer `axes.get_axis_labels(x_label, y_label)` for paired labels.

---

## Colors / Styles

- `stroke_width` → still valid.
- `stroke_opacity=...` in constructor → not allowed. Use `.set_stroke(opacity=...)`.
- `fill_opacity=...` in constructor → still valid.
- `line_arg_dict` → deprecated.  Use: 
  - `axis_config={...}` → for styling axes 
  - `background_line_style={...}` → **only inside Axes or NumberPlane**.
- `stroke_dash_length` → not valid. Use `DashedLine(...)` or `DashedVMobject(...)`.

---

## Text / Labels

* `TextMobject(...)` → use `Tex(...)`.
* `TexMobject(...)` → use `Tex(...)`.
* `edge_buffer` argument (e.g., in `Text`) → not valid. Replace with `.next_to(..., buff=...)` or `.align_on_border(...)`.
* `Text(..., t2c=...)` → still valid. 
* `t2s` (text-to-style) → replaced by `.set_color_by_t2s()`.

---

## Shapes

* `ArcBetweenPoints(..., radius=...)` → `ArcBetweenPoints(..., angle=...)`.
* `Sector(inner_radius=...)` → replaced with `AnnularSector(inner_radius=...)`.

---

## NumberLine

* `NumberLine(default_numbers_to_display=...)` → removed. Use `include_numbers=True` and control with `numbers_to_include=[...]` or `decimal_number_config={...}`.
* `exclude_zero_from_default_numbers` → removed. Must explicitly control numbers via `numbers_to_include`.

---

## Camera / Scene

* `ThreeDScene.set_camera_orientation(...)` → still valid.
* `self.camera.animate.set(phi=..., theta=...)` → replaces old `self.move_camera(...)`.
* `self.set_camera_orientation(...)` → replaces old `set_camera_position(...)`.
* `self.set_camera_orientation(phi=..., theta=...)` → still valid; `gamma` is no longer supported.


---

## Geometry / Mobject Methods

* `.start_point` / `.end_point` → replaced with `.get_start()` / `.get_end()`.
* `.point_from_proportion(alpha)` → still valid.
* `scale_in_place(factor)` → deprecated. Use `.scale(factor, about_point=...)`.
* `.fade_in` / `.fade_out` (methods) → removed. Use `FadeIn(mobj)` / `FadeOut(mobj)` animations.
* `next_to(...)` → still valid and preferred over `to_edge(...)` for finer control.
* `to_corner(...)` → replaced with `.align_on_border(...)`.
* `.center()` or `.move_to(ORIGIN)` → replaces older `.to_center()`.
* `rotate(angle, axis=...)` → still valid.
* `.get_midpoint()` → preferred over manual midpoint calculations.
* `.get_vertices()` → still valid for polygons.
* `.copy()` → still valid.

## Summary of New Errors Fixed

* `TypeError: Mobject.__getattr__.<locals>.getter() got an unexpected keyword argument 'length'` → use `line_length`.
* `TypeError: Mobject.__getattr__.<locals>.getter() got an unexpected keyword argument 'x_val'` → use `x`.
* `TypeError: Mobject.__getattr__.<locals>.getter() got an unexpected keyword argument 'edge_buffer'` → replace with `.next_to(..., buff=...)`.
* `AttributeError: Axes object has no attribute 'y_axis_labels'` → use `axes.get_axis_labels()`.
* `AttributeError: NumberLine object has no attribute 'default_numbers_to_display'` → use `include_numbers=True` with `numbers_to_include`.
* `TypeError: ... got an unexpected keyword argument 'stroke_opacity'` → set via `.set_stroke(opacity=...)`.
* `AttributeError: NumberLine has no attribute 'exclude_zero_from_default_numbers'` → must use `numbers_to_include`.
* `TypeError: ... got an unexpected keyword argument 'gamma'` → camera no longer supports gamma.
* `NameError: name 'UP_LEFT' is not defined` → Use `UL` (UP + LEFT), `UR`, `DL`, `DR` instead.


## Font Size Rules (adjustable based on content length)
TITLE_SIZE = 46       # not fixed, can change based on title length
EQUATION_SIZE = 36    # not fixed, can change based on formula/legend length
LABEL_SIZE = 28       # not fixed, can change based on axis label length
DESC_SIZE = 24        # not fixed, can change based on description length

```

## Mandatory Spacing Rules
```python
TOP_BUFFER = config.frame_height * 0.05
BOTTOM_BUFFER = config.frame_height * 0.05
LEFT_BUFFER = config.frame_width * 0.05
RIGHT_BUFFER = config.frame_width * 0.05
AFTER_TITLE_GAP = config.frame_height * 0.05
```

### Mandatory Spacing Rules
```python
TOP_BUFFER = config.frame_height * 0.05      # 5% space from top
BOTTOM_BUFFER = config.frame_height * 0.05   # 5% space from bottom
LEFT_BUFFER = config.frame_width * 0.05      # 5% space from left
RIGHT_BUFFER = config.frame_width * 0.05     # 5% space from right
```
## Mandatory avoid these errors when create a manim code

1. NameError: name 'LIGHT_BLUE' is not defined
    Use valid built-ins (from manim):
    from manim import BLUE, GREEN, TEAL, YELLOW, RED, ORANGE, PURPLE
    Or define your own shades:
    LIGHT_BLUE = "#87CEFA"   # hex for light sky blue
    LIGHT_GREEN = "#90EE90"  # hex for light green

    Then your code works:
    self.play(f1.animate.set_color(LIGHT_BLUE).set_opacity(0.4))

    
2. Mobject.__getattr__.<locals>.getter() got an unexpected keyword argument 'color'
    Fix: Import form the manim 
    from manim import Scene, MathTex, Axes, Write, WHITE
    or
    from manim import *

3. NameError: name 'BOTTOM' is not defined
    Fix: UP, DOWN, LEFT, RIGHT, ORIGIN are valid.

4. NameError: name 'WiggleOutThenIn' is not defined
    At the top of your script add:
    from manim import *
    or,
    from manim import Scene, Axes, MathTex, FadeIn, WiggleOutThenIn

5.  Mobject.__getattr__.<locals>.getter() got an unexpected keyword argument 'x_range'
    Fix: graph_sin_x = plane.plot(lambda x: np.sin(x), x_range=[-7, 7], color=BLUE)

6. TypeError: Mobject.__init__() got an unexpected keyword argument 'line_arg_dict'
    Fix: replace it with:
    background_line_style={...}
    Use axis_config={...} for Axes.

7. Error Message: Found `stroke_opacity` set in the constructor for `envelope_pos` and `envelope_neg`. According to the validation rules, opacity-related parameters should not be set in the constructor; use `.set_stroke(opacity=...)` or `.set_opacity()` after creation.

8. TypeError: Mobject.__init__() got an unexpected keyword argument 'stroke_dash_length'
    Fix: 
    # Option A: directly make dashed
    line1 = DashedLine(LEFT, RIGHT, dash_length=0.2, num_dashes=20)


    # Option B: wrap an existing object
    base = Line(LEFT, RIGHT)
    line2 = DashedVMobject(base, dash_length=0.2, num_dashes=20)


9. AttributeError: Axes object has no attribute 'to_center'
    Fix: 
    axes.move_to(ORIGIN)
    # or
    axes.center()

10. TypeError: Mobject.__init__() got an unexpected keyword argument 'background_line_style'
    Fix:
    background_line_style is only valid in NumberPlane or Axes, not in general Mobject.
    So you must pass it when constructing axes/plane, like this:

    axes = Axes(
        x_range=[-5, 5],
        y_range=[-3, 3],
        axis_config={"color": BLUE},              # style for main axes
        background_line_style={                   # style for grid lines
            "stroke_color": GREY,
            "stroke_width": 1,
            "stroke_opacity": 0.5,
        }
    )

11. Mobject.__getattr__.<locals>.getter() got an unexpected keyword argument 'length'
    Fix: axes.get_tangent_line(graph_sin, x_tracker.get_value(), line_length=3)

12. TypeError: Mobject.__init__() got an unexpected keyword argument 'x_axis_config'
    Axes does not accept x_axis_config or y_axis_config as keyword arguments at the top level of Axes(...)
    Fix:
    axes = Axes(
    x_range=[-5, 5, 1],
    y_range=[-3, 3, 1],
    axis_config={"font_size": 24},
    )

    or, if you need separate configs:

    axes = Axes(
        x_range=[-5, 5, 1],
        y_range=[-3, 3, 1],
        x_axis_config={"font_size": 24},
        y_axis_config={"font_size": 30},
    )

13. AxisError: axis 1 is out of bounds for array of dimension 1
    fix:
    curve1 = axes.plot_parametric_curve(
        lambda t: (x_func1(t), y_func1(t)),
        t_range=[0, 2*np.pi, 0.01],
        color=BLUE
    )

14. AttributeError: MathTex object has no attribute 'is_about_to_overlap' is_about_to_overlap() doesn’t exist in ManimCE.

15. Mobject.__getattr__.<locals>.getter() got an unexpected keyword argument 't_range'
    Fix:
    curve = axes.plot_parametric_curve(
        lambda t: np.array([t, np.sin(t), 0]),
        t_range=[-PI, PI, 0.05],
        color=BLUE
    )

16. AttributeError: ParametricFunction object has no attribute 'x_to_alpha'
    Fix: x_to_alpha works only on Axes.plot, not on ParametricFunction.
    tangent_line = always_redraw(
        lambda: TangentLine(graph_sin, x=x_tracker.get_value(), length=4)
    )

17. AttributeError: Axes object has no attribute 'x_to_proportion'
    In new Manim (v0.19+), Axes has no x_to_proportion.
    Fix: 
    tangent_line = always_redraw(
        lambda: TangentLine(graph_sin, x=x_tracker.get_value(), length=4)
    )

18. TypeError: Mobject.__init__() got an unexpected keyword argument 'dash_length'
    Fix: 
    envelope_pos_graph = axes.plot(lambda x: np.sin(x), x_range=[-7,7], color=BLUE)
    envelope_pos = DashedVMobject(envelope_pos_graph)
    envelope_pos.set_dash(dash_length=0.1, dashed_ratio=0.5)

19. IndexError: list index out of range
    use a tiny visible placeholder, e.g.:

    MathTex(r"\;", font_size=LABEL_SIZE)  # thin space
    # or
    MathTex(r"0", font_size=LABEL_SIZE)

20. AttributeError: MathTex object has no attribute 'bounding_box'
    Fix: use properties or new methods:

    mobj.width
    mobj.height
    mobj.get_center()
    mobj.get_bounding_box_vertices()

21. TypeError: Mobject.__init__() got an unexpected keyword argument 'number_constructor_kwargs'
    Fix: remove it and customize numbers after creation:
    axes = Axes(x_range=[-2.5*np.pi, 2.5*np.pi, np.pi/2], y_range=[-1.5, 1.5, 0.5])
    for x_val in axes.x_axis.numbers:
        x_val.set_color(BLUE)

22. NameError: name 'FillBetween' is not defined
    FillBetween isn’t auto-imported in v0.19+.
    Fix: 
    Add this line:
    from manim.mobject.graphing.utils import FillBetween
    Or use axes.get_area() as an alternative.

23. TypeError: Mobject.__init__() got an unexpected keyword argument 'color_map'
    Fix:

    surface = Surface(..., resolution=(30,30))
    surface.set_style(fill_color=BLUE, fill_opacity=0.7)

    For gradient:
    surface.set_fill_by_value(axes=axes, colors=[(BLUE,-1),(GREEN,0),(RED,1)])

24. NameError: name 'ParametricSurface' is not defined
    Fix:
    NameError: name 'ParametricSurface' is not defined
    
25. TypeError: Mobject.__init__() got an unexpected keyword argument 'res_u'
    Error comes from res_u / res_v → not valid in v0.19.
    Fix:
    resolution=(20, 20)

26. TypeError: Mobject.__init__() got an unexpected keyword argument 'dash_length'
    Fix for current version: use num_dashes instead:
    envelope_pos = DashedVMobject(envelope_pos_graph, num_dashes=50, dashed_ratio=0.5)
    envelope_neg = DashedVMobject(envelope_neg_graph, num_dashes=50, dashed_ratio=0.5)

27. AttributeError: 'ManimConfig' object has no attribute 'camera'
    Fix:
        self.camera.frame_width
        self.camera.frame_height
    Or better, just use
    legend.to_edge(UR, buff=TOP_BUFFER)

28. TypeError: Mobject.__getattr__.<locals>.getter() got an unexpected keyword argument 'num_decimal_places'
    Fix:
    axes = Axes(
    x_range=[0, 10, 1],
    y_range=[0, 5, 1],
    x_length=7,
    y_length=4,
    axis_config={
        "include_numbers": True,
        "font_size": LABEL_SIZE,
        "decimal_number_config": {"num_decimal_places": 0}  # <-- set here
    }
)

29. TypeError: Mobject.__getattr__.<locals>.getter() got an unexpected keyword argument 'font_size'
    Fix: Set the tick label styles when constructing the axes, using axis_config and decimal_number_config:
    axes = Axes(
    x_range=[0, 10, 1],
    y_range=[0, 5, 1],
    x_length=7,
    y_length=4,
    axis_config={
        "include_numbers": True,
        "font_size": LABEL_SIZE,                 # font size for all tick labels
        "decimal_number_config": {"num_decimal_places": 0},  # decimal precision
        "color": WHITE                           # color of numbers
    }
)

30. TypeError: Mobject.__init__() got an unexpected keyword argument 'vertex_dots'
    Fix:
    line_graph = axes.plot_line_graph(
        x_values=x_values,
        y_values=y_values,
        line_color=BLUE,
    )

    If you want dots at each vertex, you need to add them manually using Dot objects. For example:
    dots = VGroup(*[
    Dot(axes.coords_to_point(x, y))
    for x, y in zip(x_values, y_values)
])
self.play(FadeIn(dots))

31. ValueError: not enough values to unpack (expected 3, got 2)
    Fix:
    Change this line:
        x_axis_coord, _, _ = axes.p2c(dot.get_center())

    to
        x_axis_coord, _ = axes.p2c(dot.get_center())

32. TypeError: Mobject.__init__() got an unexpected keyword argument 'bar_spacing'
    Fix:
    chart = BarChart(
        values=sales_values,
        y_range=[0, 300, 50],
        y_length=config.frame_height * 0.6,
        x_length=config.frame_width * 0.8,
        # bar_spacing removed
    )

33. NameError: name 'WiggleOutThenIn' is not defined
    Fix:
    Replace with a built-in animation, e.g.:

    self.play(sectors[0].animate.shift(UP*0.2).scale(1.1), run_time=1.5)
    self.play(sectors[0].animate.shift(DOWN*0.2).scale(0.91), run_time=1.5)

34. NameError: name 'GrowFromBottom' is not defined
    Fix:
    self.play(GrowFromEdge(all_bars, edge=DOWN, lag_ratio=0.1), run_time=2)

35. TypeError: Mobject.__init__() got an unexpected keyword argument 'axis_config'
    Fix: pass style arguments directly.
    number_line = NumberLine(x_range=[0,10,1], length=12, color=WHITE, stroke_width=2)

36. ValueError: latex error converting to dvi
    Fixes:
    Use double braces {{ and }} for LaTeX inside f-strings.
    Replace ° with ^\circ.
    Example:

    param_L = MathTex(f"$L = {L:.1f} \\text{{ m}}$", font_size=LABEL_SIZE)
    param_g = MathTex(f"$g = {g:.1f} \\text{{ m/s}}^2$", font_size=LABEL_SIZE)
    param_theta0 = MathTex(f"$\\theta_0 = {theta0_deg}^\\circ$", font_size=LABEL_SIZE)

## QUICK STATISTICS TEMPLATE
```
python
from manim import *
import numpy as np

class ProjectileMotion(Scene):
    def construct(self):
        # Font sizes (adjustable based on content)
        TITLE_SIZE = 46
        EQUATION_SIZE = 30
        LABEL_SIZE = 26
        DESC_SIZE = 22
        
        # Spacing rules
        TOP_BUFFER = config.frame_height * 0.05
        BOTTOM_BUFFER = config.frame_height * 0.05
        LEFT_BUFFER = config.frame_width * 0.05
        RIGHT_BUFFER = config.frame_width * 0.05
        
        # Physics parameters
        v0 = 20  # initial velocity (m/s)
        angle = 60  # launch angle (degrees)
        g = 9.8  # gravity (m/s^2)
        
        # Convert to radians
        theta = angle * DEGREES
        
        # Calculate trajectory parameters
        v0x = v0 * np.cos(theta)
        v0y = v0 * np.sin(theta)
        t_max = 2 * v0y / g  # time of flight
        range_x = v0x * t_max  # horizontal range
        max_height = (v0y ** 2) / (2 * g)  # maximum height
        
        # Step 1: Title at center with star explosion fade out
        title = Text("Projectile Motion", font_size=TITLE_SIZE, color=WHITE)
        title.move_to(ORIGIN)
        
        # Title appear
        self.play(Write(title, run_time=1.5))
        self.wait(1.5)
        
        # Custom "star explosion" fade out
        self.play(
            LaggedStart(
                *[
                    letter.animate.shift(
                        np.array([np.random.uniform(-2, 2), np.random.uniform(-2, 2), 0])
                    ).scale(0.5).set_opacity(0)
                    for letter in title
                ],
                lag_ratio=0.1,
                run_time=2
            )
        )
        
        # Step 2: Create axes
        axes = Axes(
            x_range=[0, 40, 5],
            y_range=[0, 20, 5],
            x_length=config.frame_width * 0.65,
            y_length=config.frame_height * 0.55,
            axis_config={
                "include_numbers": True,
                "font_size": LABEL_SIZE - 6,
                "decimal_number_config": {"num_decimal_places": 0}
            }
        )
        
        # Position axes with margins - shift right and down to avoid overlaps
        axes.move_to(ORIGIN).shift(RIGHT * 0.8 + DOWN * 0.5)
        
        # Axis labels - position carefully
        x_label = MathTex(r"Distance(m)", font_size=LABEL_SIZE)
        x_label.next_to(axes.x_axis, DOWN, buff=0.5).shift(RIGHT * 1.5)
        
        y_label = MathTex(r"Height(m)", font_size=LABEL_SIZE)
        y_label.next_to(axes.y_axis, LEFT, buff=0.4).shift(UP * 1)
        
        self.play(Create(axes), Write(x_label), Write(y_label), run_time=1.5)
        self.wait(0.5)
        
        # Step 3: Display equations in top-left corner
        equation1 = MathTex(
            r"x(t) = v_0 \cos(\theta) \cdot t",
            font_size=EQUATION_SIZE
        )
        equation2 = MathTex(
            r"y(t) = v_0 \sin(\theta) \cdot t - \frac{1}{2}gt^2",
            font_size=EQUATION_SIZE
        )
        
        equations = VGroup(equation1, equation2).arrange(DOWN, buff=0.3, aligned_edge=LEFT)
        equations.to_corner(UL, buff=TOP_BUFFER)
        
        self.play(Write(equations), run_time=1.5)
        self.wait(0.5)
        
        # Step 4: Draw trajectory
        # Create parametric curve for trajectory
        path = axes.plot_parametric_curve(
            lambda t: np.array([v0x * t, v0y * t - 0.5 * g * t * t, 0]),
            t_range=[0, t_max, 0.01],
            color=YELLOW
        )
        
        self.play(Create(path), run_time=3, rate_func=linear)
        self.wait(0.5)
        
        # Step 5: Add projectile and animate motion
        projectile = Dot(axes.c2p(0, 0), radius=0.12, color=RED)
        self.play(FadeIn(projectile))
        
        # Animate projectile along path
        self.play(
            MoveAlongPath(projectile, path),
            run_time=4,
            rate_func=linear
        )
        self.wait(0.5)
        
        # Step 6: Highlight key points with careful positioning
        # Launch point
        launch_dot = Dot(axes.c2p(0, 0), color=GREEN, radius=0.1)
        launch_label = Text("Launch", font_size=DESC_SIZE, color=GREEN)
        launch_label.next_to(launch_dot, DOWN + LEFT, buff=0.3)
        
        # Maximum height point
        t_peak = v0y / g
        peak_x = v0x * t_peak
        peak_dot = Dot(axes.c2p(peak_x, max_height), color=ORANGE, radius=0.1)
        peak_label = Text(f"Max Height: {max_height:.1f}m", font_size=DESC_SIZE, color=ORANGE)
        peak_label.next_to(peak_dot, UP, buff=0.4)
        
        # Landing point
        landing_dot = Dot(axes.c2p(range_x, 0), color=PURPLE, radius=0.1)
        landing_label = Text(f"Range: {range_x:.1f}m", font_size=DESC_SIZE, color=PURPLE)
        landing_label.next_to(landing_dot, DOWN + RIGHT, buff=0.3)
        
        self.play(
            FadeIn(launch_dot), Write(launch_label),
            run_time=0.8
        )
        self.wait(0.3)
        
        self.play(
            FadeIn(peak_dot), Write(peak_label),
            run_time=0.8
        )
        self.wait(0.3)
        
        self.play(
            FadeIn(landing_dot), Write(landing_label),
            run_time=0.8
        )
        self.wait(0.5)
        
        # Step 7: Display parameters in top-right corner
        params = VGroup(
            MathTex(rf"v_0 = {v0} \text{{ m/s}}", font_size=EQUATION_SIZE - 2),
            MathTex(rf"\theta = {angle}°", font_size=EQUATION_SIZE - 2),
            MathTex(rf"g = {g} \text{{ m/s}}^2", font_size=EQUATION_SIZE - 2)
        ).arrange(DOWN, buff=0.25, aligned_edge=LEFT)
        
        params.to_corner(UR, buff=TOP_BUFFER)
        
        self.play(FadeIn(params, shift=LEFT), run_time=1)
        self.wait(2)
        
        # Final pause
        self.wait(1)
```
<Physics Visualization Rule Only/>
"""

STATISTICS = """
<Statistical Visualization Rule Only>
## Mandatory way to design (Statistics Adapted)

1. Title: Always at the center (never top). Must appear first and then fade out with a smooth animation (e.g., FadeOut, LaggedStart, star-burst effect).
2. Axes: Create axes immediately after title fades. Show only relevant axes (x, y) with margins.
3. Numbers: Use integers mostly; if needed, 2 decimal precision.
4. Axes style: No grid unless needed. Include only numbers required for visualization.
5. Legend / Equation: Place formula, mean, variance, or legend in corners. If no space → fade out temporarily.
6. Margins: Leave a 5% gap at edges.
7. Sequence: Title → Axes → Legend/Formula → Graph → Dynamic Highlight.

## Graph Types Supported
- BarChart
- Scatter Plot
- Line Plot (from dataset)
- Histogram
- Boxplot (manual construction)
- etc

### Deprecated → New (Manim v0.19+)

---

## Common Deprecated → New

* `to_edge(...)` still works, but prefer `.next_to()` for finer control.
* `to_corner(...)` → use `.align_on_border(...)`.
* `axes.to_center()` → use `axes.move_to(ORIGIN)` or `axes.center()`.
* `shift(x*RIGHT)` still valid.
* `scale_in_place(factor)` → use `.scale(factor, about_point=...)`.
* `fade_in` / `fade_out` methods → use animations: `FadeIn(mobj)` / `FadeOut(mobj)`.
* `ShowCreation(mobj)`  → `Create(mobj)`.
* `Write(mobj, run_time=...)`  still valid.
* `Transform(m1, m2)`  still valid.
* `SurroundingRectangle(..., buff=0.1)`  still valid.
* `.start_point or .end_point` -> use `.get_start()` or `.get_end()`.

---

## Axes / Graphs

* `axes.get_graph(f, ...)` → deprecated. Use `axes.plot(f, x_range=[...], color=...)`.

* `axes.get_area(f, ...)` → still valid for one function. For two functions use `FillBetween(...)`.

* `NumberPlane.get_graph(...)` → does not exist. Use `plane.plot(...)`.

* `add_coordinates()` → still valid.

* `axes.get_tangent_line(graph, x=..., line_length=...)` → does not exist. Use `TangentLine(graph, alpha, length=...)` where `alpha ∈ [0,1]`. To map `x` to `alpha`, use helpers like `axes.i2gp`.

* `axes.get_vertical_line(x_val=...)` wrong → invalid. Correct: `axes.get_vertical_line(point, **kwargs)`.
  (use `axes.c2p(x_value, y_value)` or `axes.i2gp(x_value, graph)` to get the point).

* `axes.y_axis_labels` wrong → no attribute. Use `axes.get_axis_labels()`.

* `y_axis_config` must be passed explicitly inside `Axes(...)`, not accessed as an attribute afterwards.

* `axes.get_x_axis_label(...)` and `axes.get_y_axis_label(...)` → still valid, but prefer `axes.get_axis_labels(x_label, y_label)` for paired labels.

---

## Colors / Styles

- `stroke_width` → still valid.
- `stroke_opacity=...` in constructor → not allowed. Use `.set_stroke(opacity=...)`.
- `fill_opacity=...` in constructor → still valid.
- `line_arg_dict` → deprecated.  Use: 
  - `axis_config={...}` → for styling axes 
  - `background_line_style={...}` → **only inside Axes or NumberPlane**.
- `stroke_dash_length` → not valid. Use `DashedLine(...)` or `DashedVMobject(...)`.

---

## Text / Labels

* `TextMobject(...)` → use `Tex(...)`.
* `TexMobject(...)` → use `Tex(...)`.
* `edge_buffer` argument (e.g., in `Text`) → not valid. Replace with `.next_to(..., buff=...)` or `.align_on_border(...)`.
* `Text(..., t2c=...)` → still valid. 
* `t2s` (text-to-style) → replaced by `.set_color_by_t2s()`.

---

## Shapes

* `ArcBetweenPoints(..., radius=...)` → `ArcBetweenPoints(..., angle=...)`.
* `Sector(inner_radius=...)` → replaced with `AnnularSector(inner_radius=...)`.

---

## NumberLine

* `NumberLine(default_numbers_to_display=...)` → removed. Use `include_numbers=True` and control with `numbers_to_include=[...]` or `decimal_number_config={...}`.
* `exclude_zero_from_default_numbers` → removed. Must explicitly control numbers via `numbers_to_include`.

---

## Camera / Scene

* `ThreeDScene.set_camera_orientation(...)` → still valid.
* `self.camera.animate.set(phi=..., theta=...)` → replaces old `self.move_camera(...)`.
* `self.set_camera_orientation(...)` → replaces old `set_camera_position(...)`.
* `self.set_camera_orientation(phi=..., theta=...)` → still valid; `gamma` is no longer supported.


---

## Geometry / Mobject Methods

* `.start_point` / `.end_point` → replaced with `.get_start()` / `.get_end()`.
* `.point_from_proportion(alpha)` → still valid.
* `scale_in_place(factor)` → deprecated. Use `.scale(factor, about_point=...)`.
* `.fade_in` / `.fade_out` (methods) → removed. Use `FadeIn(mobj)` / `FadeOut(mobj)` animations.
* `next_to(...)` → still valid and preferred over `to_edge(...)` for finer control.
* `to_corner(...)` → replaced with `.align_on_border(...)`.
* `.center()` or `.move_to(ORIGIN)` → replaces older `.to_center()`.
* `rotate(angle, axis=...)` → still valid.
* `.get_midpoint()` → preferred over manual midpoint calculations.
* `.get_vertices()` → still valid for polygons.
* `.copy()` → still valid.

## Summary of New Errors Fixed

* `TypeError: Mobject.__getattr__.<locals>.getter() got an unexpected keyword argument 'length'` → use `line_length`.
* `TypeError: Mobject.__getattr__.<locals>.getter() got an unexpected keyword argument 'x_val'` → use `x`.
* `TypeError: Mobject.__getattr__.<locals>.getter() got an unexpected keyword argument 'edge_buffer'` → replace with `.next_to(..., buff=...)`.
* `AttributeError: Axes object has no attribute 'y_axis_labels'` → use `axes.get_axis_labels()`.
* `AttributeError: NumberLine object has no attribute 'default_numbers_to_display'` → use `include_numbers=True` with `numbers_to_include`.
* `TypeError: ... got an unexpected keyword argument 'stroke_opacity'` → set via `.set_stroke(opacity=...)`.
* `AttributeError: NumberLine has no attribute 'exclude_zero_from_default_numbers'` → must use `numbers_to_include`.
* `TypeError: ... got an unexpected keyword argument 'gamma'` → camera no longer supports gamma.
* `NameError: name 'UP_LEFT' is not defined` → Use `UL` (UP + LEFT), `UR`, `DL`, `DR` instead.


## Font Size Rules (adjustable based on content length)
TITLE_SIZE = 46       # not fixed, can change based on title length
EQUATION_SIZE = 36    # not fixed, can change based on formula/legend length
LABEL_SIZE = 28       # not fixed, can change based on axis label length
DESC_SIZE = 24        # not fixed, can change based on description length

```

## Mandatory Spacing Rules
```python
TOP_BUFFER = config.frame_height * 0.05
BOTTOM_BUFFER = config.frame_height * 0.05
LEFT_BUFFER = config.frame_width * 0.05
RIGHT_BUFFER = config.frame_width * 0.05
AFTER_TITLE_GAP = config.frame_height * 0.05
```

### Mandatory Spacing Rules
```python
TOP_BUFFER = config.frame_height * 0.05      # 5% space from top
BOTTOM_BUFFER = config.frame_height * 0.05   # 5% space from bottom
LEFT_BUFFER = config.frame_width * 0.05      # 5% space from left
RIGHT_BUFFER = config.frame_width * 0.05     # 5% space from right
```
## Mandatory avoid these errors when create a manim code

1. NameError: name 'LIGHT_BLUE' is not defined
    Use valid built-ins (from manim):
    from manim import BLUE, GREEN, TEAL, YELLOW, RED, ORANGE, PURPLE
    Or define your own shades:
    LIGHT_BLUE = "#87CEFA"   # hex for light sky blue
    LIGHT_GREEN = "#90EE90"  # hex for light green

    Then your code works:
    self.play(f1.animate.set_color(LIGHT_BLUE).set_opacity(0.4))

    
2. Mobject.__getattr__.<locals>.getter() got an unexpected keyword argument 'color'
    Fix: Import form the manim 
    from manim import Scene, MathTex, Axes, Write, WHITE
    or
    from manim import *

3. NameError: name 'BOTTOM' is not defined
    Fix: UP, DOWN, LEFT, RIGHT, ORIGIN are valid.

4. NameError: name 'WiggleOutThenIn' is not defined
    At the top of your script add:
    from manim import *
    or,
    from manim import Scene, Axes, MathTex, FadeIn, WiggleOutThenIn

5.  Mobject.__getattr__.<locals>.getter() got an unexpected keyword argument 'x_range'
    Fix: graph_sin_x = plane.plot(lambda x: np.sin(x), x_range=[-7, 7], color=BLUE)

6. TypeError: Mobject.__init__() got an unexpected keyword argument 'line_arg_dict'
    Fix: replace it with:
    background_line_style={...}
    Use axis_config={...} for Axes.

7. Error Message: Found `stroke_opacity` set in the constructor for `envelope_pos` and `envelope_neg`. According to the validation rules, opacity-related parameters should not be set in the constructor; use `.set_stroke(opacity=...)` or `.set_opacity()` after creation.

8. TypeError: Mobject.__init__() got an unexpected keyword argument 'stroke_dash_length'
    Fix: 
    # Option A: directly make dashed
    line1 = DashedLine(LEFT, RIGHT, dash_length=0.2, num_dashes=20)


    # Option B: wrap an existing object
    base = Line(LEFT, RIGHT)
    line2 = DashedVMobject(base, dash_length=0.2, num_dashes=20)


9. AttributeError: Axes object has no attribute 'to_center'
    Fix: 
    axes.move_to(ORIGIN)
    # or
    axes.center()

10. TypeError: Mobject.__init__() got an unexpected keyword argument 'background_line_style'
    Fix:
    background_line_style is only valid in NumberPlane or Axes, not in general Mobject.
    So you must pass it when constructing axes/plane, like this:

    axes = Axes(
        x_range=[-5, 5],
        y_range=[-3, 3],
        axis_config={"color": BLUE},              # style for main axes
        background_line_style={                   # style for grid lines
            "stroke_color": GREY,
            "stroke_width": 1,
            "stroke_opacity": 0.5,
        }
    )

11. Mobject.__getattr__.<locals>.getter() got an unexpected keyword argument 'length'
    Fix: axes.get_tangent_line(graph_sin, x_tracker.get_value(), line_length=3)

12. TypeError: Mobject.__init__() got an unexpected keyword argument 'x_axis_config'
    Axes does not accept x_axis_config or y_axis_config as keyword arguments at the top level of Axes(...)
    Fix:
    axes = Axes(
    x_range=[-5, 5, 1],
    y_range=[-3, 3, 1],
    axis_config={"font_size": 24},
    )

    or, if you need separate configs:

    axes = Axes(
        x_range=[-5, 5, 1],
        y_range=[-3, 3, 1],
        x_axis_config={"font_size": 24},
        y_axis_config={"font_size": 30},
    )

13. AxisError: axis 1 is out of bounds for array of dimension 1
    fix:
    curve1 = axes.plot_parametric_curve(
        lambda t: (x_func1(t), y_func1(t)),
        t_range=[0, 2*np.pi, 0.01],
        color=BLUE
    )

14. AttributeError: MathTex object has no attribute 'is_about_to_overlap' is_about_to_overlap() doesn’t exist in ManimCE.

15. Mobject.__getattr__.<locals>.getter() got an unexpected keyword argument 't_range'
    Fix:
    curve = axes.plot_parametric_curve(
        lambda t: np.array([t, np.sin(t), 0]),
        t_range=[-PI, PI, 0.05],
        color=BLUE
    )

16. AttributeError: ParametricFunction object has no attribute 'x_to_alpha'
    Fix: x_to_alpha works only on Axes.plot, not on ParametricFunction.
    tangent_line = always_redraw(
        lambda: TangentLine(graph_sin, x=x_tracker.get_value(), length=4)
    )

17. AttributeError: Axes object has no attribute 'x_to_proportion'
    In new Manim (v0.19+), Axes has no x_to_proportion.
    Fix: 
    tangent_line = always_redraw(
        lambda: TangentLine(graph_sin, x=x_tracker.get_value(), length=4)
    )

18. TypeError: Mobject.__init__() got an unexpected keyword argument 'dash_length'
    Fix: 
    envelope_pos_graph = axes.plot(lambda x: np.sin(x), x_range=[-7,7], color=BLUE)
    envelope_pos = DashedVMobject(envelope_pos_graph)
    envelope_pos.set_dash(dash_length=0.1, dashed_ratio=0.5)

19. IndexError: list index out of range
    use a tiny visible placeholder, e.g.:

    MathTex(r"\;", font_size=LABEL_SIZE)  # thin space
    # or
    MathTex(r"0", font_size=LABEL_SIZE)

20. AttributeError: MathTex object has no attribute 'bounding_box'
    Fix: use properties or new methods:

    mobj.width
    mobj.height
    mobj.get_center()
    mobj.get_bounding_box_vertices()

21. TypeError: Mobject.__init__() got an unexpected keyword argument 'number_constructor_kwargs'
    Fix: remove it and customize numbers after creation:
    axes = Axes(x_range=[-2.5*np.pi, 2.5*np.pi, np.pi/2], y_range=[-1.5, 1.5, 0.5])
    for x_val in axes.x_axis.numbers:
        x_val.set_color(BLUE)

22. NameError: name 'FillBetween' is not defined
    FillBetween isn’t auto-imported in v0.19+.
    Fix: 
    Add this line:
    from manim.mobject.graphing.utils import FillBetween
    Or use axes.get_area() as an alternative.

23. TypeError: Mobject.__init__() got an unexpected keyword argument 'color_map'
    Fix:

    surface = Surface(..., resolution=(30,30))
    surface.set_style(fill_color=BLUE, fill_opacity=0.7)

    For gradient:
    surface.set_fill_by_value(axes=axes, colors=[(BLUE,-1),(GREEN,0),(RED,1)])

24. NameError: name 'ParametricSurface' is not defined
    Fix:
    NameError: name 'ParametricSurface' is not defined
    
25. TypeError: Mobject.__init__() got an unexpected keyword argument 'res_u'
    Error comes from res_u / res_v → not valid in v0.19.
    Fix:
    resolution=(20, 20)

26. TypeError: Mobject.__init__() got an unexpected keyword argument 'dash_length'
    Fix for current version: use num_dashes instead:
    envelope_pos = DashedVMobject(envelope_pos_graph, num_dashes=50, dashed_ratio=0.5)
    envelope_neg = DashedVMobject(envelope_neg_graph, num_dashes=50, dashed_ratio=0.5)

27. AttributeError: 'ManimConfig' object has no attribute 'camera'
    Fix:
        self.camera.frame_width
        self.camera.frame_height
    Or better, just use
    legend.to_edge(UR, buff=TOP_BUFFER)

28. TypeError: Mobject.__getattr__.<locals>.getter() got an unexpected keyword argument 'num_decimal_places'
    Fix:
    axes = Axes(
    x_range=[0, 10, 1],
    y_range=[0, 5, 1],
    x_length=7,
    y_length=4,
    axis_config={
        "include_numbers": True,
        "font_size": LABEL_SIZE,
        "decimal_number_config": {"num_decimal_places": 0}  # <-- set here
    }
)

29. TypeError: Mobject.__getattr__.<locals>.getter() got an unexpected keyword argument 'font_size'
    Fix: Set the tick label styles when constructing the axes, using axis_config and decimal_number_config:
    axes = Axes(
    x_range=[0, 10, 1],
    y_range=[0, 5, 1],
    x_length=7,
    y_length=4,
    axis_config={
        "include_numbers": True,
        "font_size": LABEL_SIZE,                 # font size for all tick labels
        "decimal_number_config": {"num_decimal_places": 0},  # decimal precision
        "color": WHITE                           # color of numbers
    }
)

30. TypeError: Mobject.__init__() got an unexpected keyword argument 'vertex_dots'
    Fix:
    line_graph = axes.plot_line_graph(
        x_values=x_values,
        y_values=y_values,
        line_color=BLUE,
    )

    If you want dots at each vertex, you need to add them manually using Dot objects. For example:
    dots = VGroup(*[
    Dot(axes.coords_to_point(x, y))
    for x, y in zip(x_values, y_values)
])
self.play(FadeIn(dots))

31. ValueError: not enough values to unpack (expected 3, got 2)
    Fix:
    Change this line:
        x_axis_coord, _, _ = axes.p2c(dot.get_center())

    to
        x_axis_coord, _ = axes.p2c(dot.get_center())

32. TypeError: Mobject.__init__() got an unexpected keyword argument 'bar_spacing'
    Fix:
    chart = BarChart(
        values=sales_values,
        y_range=[0, 300, 50],
        y_length=config.frame_height * 0.6,
        x_length=config.frame_width * 0.8,
        # bar_spacing removed
    )

33. NameError: name 'WiggleOutThenIn' is not defined
    Fix:
    Replace with a built-in animation, e.g.:

    self.play(sectors[0].animate.shift(UP*0.2).scale(1.1), run_time=1.5)
    self.play(sectors[0].animate.shift(DOWN*0.2).scale(0.91), run_time=1.5)

34. NameError: name 'GrowFromBottom' is not defined
    Fix:
    self.play(GrowFromEdge(all_bars, edge=DOWN, lag_ratio=0.1), run_time=2)

## QUICK STATISTICS TEMPLATE

## Bar Plot
```python
from manim import *
import numpy as np

class StatisticsGraph(Scene):
    def construct(self):
        # ===== CONSTANTS =====
        TITLE_SIZE = 46
        EQUATION_SIZE = 36
        LABEL_SIZE = 28
        TOP_BUFFER = config.frame_height * 0.05
        BOTTOM_BUFFER = config.frame_height * 0.05
        LEFT_BUFFER = config.frame_width * 0.05
        RIGHT_BUFFER = config.frame_width * 0.05

        self.camera.background_color = BLACK

        # ===== STEP 1: Title =====
        title = Text("Statistics Visualization", font_size=TITLE_SIZE, color=WHITE)
        title.move_to(ORIGIN)
        self.play(Write(title, run_time=1.5))
        self.wait(2)

        self.play(
            LaggedStart(
                *[letter.animate.shift([np.random.uniform(-1,1), np.random.uniform(-1,1),0]).scale(0.5).set_opacity(0) for letter in title],
                lag_ratio=0.1,
                run_time=2
            )
        )

        # ===== STEP 2: Bar Chart =====
        data = [5, 8, 2, 6]
        categories = ["A", "B", "C", "D"]

        chart = BarChart(
            values=data,
            bar_names=categories,
            y_range=[0, max(data)+2, 1],
            x_length=config.frame_width * 0.7,
            y_length=config.frame_height * 0.6,
            bar_width=0.6,
            bar_colors=[BLUE, GREEN, RED, ORANGE]
        )
        chart.center()
        
        # ===== STEP 3: Legend / Formula =====
        legend = MathTex(r"\text{Mean} = 5, \text{SD} = 2", font_size=EQUATION_SIZE, color=WHITE)
        legend.to_edge(UR, buff=TOP_BUFFER)
        
        self.play(Create(chart))
        self.play(Write(legend, run_time=1))

        # ===== STEP 4: Dynamic Highlight =====
        highlight = SurroundingRectangle(chart.bars[1], color=YELLOW, buff=0.1)
        self.play(Create(highlight))

        # ===== STEP 5: Clean Up =====
        self.wait(2)
        self.play(FadeOut(chart), FadeOut(legend), FadeOut(highlight))
        self.wait(1)
```

## Pie Chart
```python
from manim import *

class PieChartExample(Scene):
    def construct(self):
        self.camera.background_color = BLACK
              
        # Data: 3 slices
        values = [45, 30, 25]
        colors = [BLUE, GREEN, ORANGE]
        
        # Create pie chart
        sectors = VGroup()
        start_angle = 90 * DEGREES
        
        for value, color in zip(values, colors):
            angle = (value / 100) * TAU
            sector = AnnularSector(
                outer_radius=2.0,
                inner_radius=0,
                angle=angle,
                start_angle=start_angle,
                color=color,
                fill_opacity=0.8,
                stroke_color=WHITE,
                stroke_width=3
            )
            sectors.add(sector)
            start_angle += angle
        
        self.play(Create(sectors), run_time=2)
        self.wait(2)
        
        self.play(FadeOut(sectors))
        self.wait(1)
```

## Donut shape chart
```python
from manim import *

class DonutChartExample(Scene):
    def construct(self):
        self.camera.background_color = BLACK
        
        # Data: 3 slices
        values = [45, 30, 25]
        colors = [BLUE, GREEN, ORANGE]
        
        # Create donut chart
        sectors = VGroup()
        start_angle = 90 * DEGREES
        
        for value, color in zip(values, colors):
            angle = (value / 100) * TAU
            sector = AnnularSector(
                outer_radius=2.0,
                inner_radius=1.0,
                angle=angle,
                start_angle=start_angle,
                color=color,
                fill_opacity=0.8,
                stroke_color=WHITE,
                stroke_width=3
            )
            sectors.add(sector)
            start_angle += angle
        
        self.play(Create(sectors), run_time=2)
        self.wait(2)
        
        self.play(FadeOut(sectors))
        self.wait(1)
```

## Line Plot
```python
from manim import *
import numpy as np

class TemperatureLinePlot(Scene):
    def construct(self):
        # ===== CONSTANTS =====
        TITLE_SIZE = 46
        EQUATION_SIZE = 32
        LABEL_SIZE = 24
        TOP_BUFFER = config.frame_height * 0.08
        BOTTOM_BUFFER = config.frame_height * 0.08
        LEFT_BUFFER = config.frame_width * 0.08
        RIGHT_BUFFER = config.frame_width * 0.08

        self.camera.background_color = BLACK

        # ===== STEP 1: Title =====
        title = Text("Weekly Temperature Changes", font_size=TITLE_SIZE, color=WHITE)
        title.move_to(ORIGIN)
        self.play(Write(title, run_time=1.5))
        self.wait(2)

        self.play(
            LaggedStart(
                *[letter.animate.shift([np.random.uniform(-1,1), np.random.uniform(-1,1),0]).scale(0.5).set_opacity(0) for letter in title],
                lag_ratio=0.1,
                run_time=2
            )
        )

        # ===== STEP 2: Temperature Data =====
        # Week 1-4 temperature data (in Celsius)
        weeks = [1, 2, 3, 4]
        temperatures = [22, 25, 20, 27]  # Weekly average temperatures
        
        # ===== STEP 3: Create Axes =====
        axes = Axes(
            x_range=[0, 5, 1],
            y_range=[15, 30, 5],
            x_length=config.frame_width * 0.7,
            y_length=config.frame_height * 0.6,
            axis_config={
                "include_numbers": True,
                "font_size": LABEL_SIZE,
                "color": WHITE
            },
            tips=False
        )
        axes.center().shift(DOWN * 0.3)
        
        # Add axis labels
        x_label = Text("Week", font_size=LABEL_SIZE).next_to(axes.x_axis, DOWN, buff=0.5)
        y_label = Text("Temperature (°C)", font_size=LABEL_SIZE).next_to(axes.y_axis, LEFT, buff=0.7).rotate(PI/2)
        
        self.play(Create(axes), Write(x_label), Write(y_label), run_time=2)
        
        # ===== STEP 4: Legend =====
        legend = VGroup(
            Text("Average Weekly Temperature", font_size=EQUATION_SIZE, color=BLUE),
            Text("Month: January 2025", font_size=EQUATION_SIZE-4, color=GRAY)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        legend.to_corner(UR, buff=0.5)
        self.play(Write(legend, run_time=1))
        
        # ===== STEP 5: Plot Points =====
        points = [axes.coords_to_point(w, t) for w, t in zip(weeks, temperatures)]
        dots = VGroup(*[Dot(point, color=RED, radius=0.08) for point in points])
        temp_labels = VGroup()
        
        # Animate dots appearing one by one
        for i, dot in enumerate(dots):
            self.play(FadeIn(dot, scale=0.5), run_time=0.5)
            # Add temperature label above each dot
            temp_label = Text(f"{temperatures[i]}°C", font_size=LABEL_SIZE-4, color=YELLOW)
            temp_label.next_to(dot, UP, buff=0.2)
            temp_labels.add(temp_label)
            self.play(Write(temp_label, run_time=0.3))
            self.wait(0.3)
        
        # ===== STEP 6: Draw Line Connecting Points =====
        # Create line segments between consecutive points
        lines = VGroup()
        for i in range(len(points) - 1):
            line = Line(points[i], points[i+1], color=BLUE, stroke_width=4)
            lines.add(line)
        
        self.play(Create(lines, lag_ratio=0.3), run_time=2)
        self.wait(1)
        
        # ===== STEP 7: Highlight Highest Temperature =====
        max_temp_idx = temperatures.index(max(temperatures))
        highlight = Circle(radius=0.15, color=GREEN, stroke_width=5)
        highlight.move_to(dots[max_temp_idx])
        
        highlight_label = Text("Highest", font_size=LABEL_SIZE-4, color=GREEN)
        highlight_label.next_to(highlight, RIGHT, buff=0.4)
        
        self.play(Create(highlight), Write(highlight_label), run_time=1)
        self.wait(2)
        
        # ===== STEP 8: Show Temperature Trend Arrow =====
        if temperatures[-1] > temperatures[0]:
            trend_text = Text("Warming Trend ↗", font_size=EQUATION_SIZE-4, color=RED)
        elif temperatures[-1] < temperatures[0]:
            trend_text = Text("Cooling Trend ↘", font_size=EQUATION_SIZE-4, color=BLUE)
        else:
            trend_text = Text("Stable Trend →", font_size=EQUATION_SIZE-4, color=WHITE)
        
        trend_text.to_corner(UR, buff=0.5).shift(DOWN * 2.5)
        self.play(Write(trend_text, run_time=1))
        self.wait(2)
        
        # ===== STEP 9: Clean Up =====
        self.play(
            FadeOut(axes),
            FadeOut(x_label),
            FadeOut(y_label),
            FadeOut(legend),
            FadeOut(dots),
            FadeOut(temp_labels),
            FadeOut(lines),
            FadeOut(highlight),
            FadeOut(highlight_label),
            FadeOut(trend_text),
            run_time=1.5
        )
        self.wait(1)
```
<Statistical Visualization Rule Only/>
"""