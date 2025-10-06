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
# Manim 2D Graph Animation Rules (v0.19+)

## Core Design Principles

### Mandatory Structure
1. **Title Placement**: Always centered (not top). Must appear first, then fade out completely before any new object or text appears. Avoid including equations or expressions in the title.
2. **Numeric Formatting**: Prefer integers; if decimals are needed, use two-decimal precision. Avoid π or symbolic constants in numeric labels.
3. **Text Placement**: Place texts near screen corners (UL, UR, DL, DR) or top edge, maintaining a 5% screen margin. Ensure texts do not overlap any existing objects; if overlap occurs, fade the text out instead of repositioning unsafely.
4. **Margin Enforcement**: Maintain 5% margin on all screen sides — top, bottom, left, and right.
5. **Scene Sequence**: Must follow this strict order → **Title → FadeOut → Text (Adaptive) → Graph/Object**. No parallel animation that interrupts this order.

---

## Mandatory Error Prevention Rules

### 1. **IndexError: too many indices for array**
Occurs when `.align_to()` is used on whitespace-only `Text` objects.

**Root Cause**: Empty or space-only `Text` lacks coordinate points.

**Correct Usage:**
```python
result_text = Text("X", font_size=LABEL_SIZE, color=TEAL)
result_text.next_to(label, DOWN, buff=0.2)
result_text.set_opacity(0)  # Hide until first Transform
```

**Never use:**
```python
text = Text(" ").next_to(label).align_to(label)
```

### 2. **ValueError: operands could not be broadcast together**
When moving 2D points to 3D context, extend tuple:
```python
circle.move_to((*data['pos'], 0))
```

### 3. **NameError: Parallel undefined**
Use:
```python
self.play(AnimationGroup(*animations, lag_ratio=0))
```

### 4. **AttributeError: Camera missing frame_x_radius**
Replace with:
```python
visited_label.align_to(-self.camera.frame_width/2 + LEFT_BUFFER, LEFT)
```

### 5. **NameError: CENTER_Y undefined**
Replace with `0` or `ORIGIN[1]`.

### 6. **TypeError: VMobject.set_points() invalid arguments**
Fix:
```python
top_arrow.animate.put_start_and_end_on(start_point, end_point)
```

### 7. **NameError: BOTTOM undefined**
Replace with:
```python
.to_edge(DOWN, buff=BOTTOM_BUFFER)
```

### 8. **Overlap Prevention System**
Always define `self.visible_objects = []` at start.

#### Helper Functions:
```python
def check_overlap(obj1, obj2, buffer=0.3):
    try:
        box1 = obj1.get_bounding_box()
        box2 = obj2.get_bounding_box()
        return not (
            box1[1] < box2[0] - buffer or
            box1[0] > box2[1] + buffer or
            box1[3] < box2[2] - buffer or
            box1[2] > box2[3] + buffer
        )
    except:
        return False
```

```python
def place_text_safely(text, existing_objects, preferred_positions=None):
    if preferred_positions is None:
        preferred_positions = [
            ('top_left', lambda: text.to_edge(UL, buff=0.3)),
            ('top_right', lambda: text.to_edge(UR, buff=0.3)),
            ('bottom_left', lambda: text.to_edge(DL, buff=0.3)),
            ('bottom_right', lambda: text.to_edge(DR, buff=0.3)),
        ]
    for _, func in preferred_positions:
        func()
        in_bounds = (
            text.get_left()[0] >= -config.frame_width/2 + 0.3 and
            text.get_right()[0] <= config.frame_width/2 - 0.3 and
            text.get_bottom()[1] >= -config.frame_height/2 + 0.3 and
            text.get_top()[1] <= config.frame_height/2 - 0.3
        )
        overlap = any(check_overlap(text, obj) for obj in existing_objects)
        if in_bounds and not overlap:
            return True
    return False
```

#### Usage Example:
```python
self.visible_objects = []
self.play(Create(boxes))
self.visible_objects.append(boxes)

status = Text("State: q0", font_size=DESC_SIZE)
if place_text_safely(status, self.visible_objects):
    self.play(Write(status))
    self.visible_objects.append(status)
else:
    status.move_to(ORIGIN)
    self.play(Write(status))
    self.wait(0.5)
    self.play(FadeOut(status))
```

---

## Spacing & Font Size Constants
```python
TITLE_SIZE = 46
TEXT_SIZE = 36
LABEL_SIZE = 28
DESC_SIZE = 24

TOP_BUFFER = config.frame_height * 0.05
BOTTOM_BUFFER = config.frame_height * 0.05
LEFT_BUFFER = config.frame_width * 0.05
RIGHT_BUFFER = config.frame_width * 0.05
AFTER_TITLE_GAP = config.frame_height * 0.05
```

---

## Modern vs Deprecated Syntax
| Deprecated | Updated (v0.19+) |
|-------------|------------------|
| `ShowCreation()` | `Create()` |
| `TextMobject` / `TexMobject` | `Tex()` / `MathTex()` |
| `scale_in_place()` | `.scale(..., about_point=...)` |
| `UP_LEFT` | `UL` (also UR, DL, DR) |

**Color Rules:** Use only Manim’s named colors or hex codes.
**Opacity Rules:** Use `.set_stroke(opacity=...)` after creation.

---

## Text & Label Practices
- Use proper `font_size` constants.
- Avoid raw pixel scaling.
- Maintain visibility contrast (no dim text on dark background).

---

## Mandatory Animation Order

1. **Title (Center, FadeOut)**
```python
title = Text("Your Title", font_size=TITLE_SIZE)
title.move_to(ORIGIN)
self.play(Write(title))
self.wait(1)
self.play(FadeOut(title))
```

2. **Adaptive Text Placement (After Title FadeOut)**
```python
func_text = Text("y = f(x)", font_size=TEXT_SIZE)
positions = [UL, UR, DL, DR]
placed = False
for pos in positions:
    func_text.to_edge(pos, buff=TOP_BUFFER)
    if within_bounds(func_text):
        self.play(Write(func_text))
        placed = True
        break
if not placed:
    func_text.move_to(ORIGIN)
    self.play(Write(func_text))
    self.wait(0.5)
    self.play(FadeOut(func_text))
```

3. **Graph or Object Rendering**
```python
self.play(Create(graph))
```

---

## Key Checklist
-- Always `from manim import *`
-- Maintain font hierarchy (Title > Text > Label > Desc)
-- Enforce 5% screen margins
-- Use adaptive placement for text
-- Replace deprecated syntax
-- Avoid object overlap
-- Use correct color and opacity handling
-- Apply proper animation order

## QUICK TEMPLATE
```python
from manim import *
import numpy as np
import random

class BubbleSortAnimation(Scene):
    def construct(self):
        # ===== CONSTANTS =====
        TITLE_SIZE = 46
        DESC_SIZE = 24
        NUMBER_SIZE = 36
        BOX_SIZE = 0.9

        self.camera.background_color = "#0a0a0a"

        # ===== STEP 1: Title =====
        title = Text("Bubble Sort Visualization", font_size=TITLE_SIZE, color=WHITE, weight=BOLD)
        title.move_to(ORIGIN)

        self.play(Write(title, run_time=1.5))
        self.wait(1)

        # Star-burst fadeout
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

        # ===== STEP 2: Create Array with Boxes =====
        array_values = [5, 3, 8, 4, 2, 7, 6]
        
        boxes = VGroup()
        numbers = VGroup()
        indices = VGroup()

        # Create boxes with numbers
        for i, val in enumerate(array_values):
            # Create box
            box = Square(
                side_length=BOX_SIZE,
                fill_color=BLUE,
                fill_opacity=0.3,
                stroke_color=WHITE,
                stroke_width=3
            )
            
            # Number inside box
            number = Text(str(val), font_size=NUMBER_SIZE, color=WHITE, weight=BOLD)
            
            # Index below box
            index = Text(f"[{i}]", font_size=22, color=GRAY)
            
            boxes.add(box)
            numbers.add(number)
            indices.add(index)

        # Arrange boxes
        boxes.arrange(RIGHT, buff=0.3)
        boxes.move_to(ORIGIN)
        
        # Position numbers and indices
        for i in range(len(array_values)):
            numbers[i].move_to(boxes[i].get_center())
            indices[i].next_to(boxes[i], DOWN, buff=0.2)

        # Animate creation
        self.play(
            LaggedStart(*[Create(box) for box in boxes], lag_ratio=0.1),
            LaggedStart(*[Write(number) for number in numbers], lag_ratio=0.1),
            LaggedStart(*[FadeIn(index) for index in indices], lag_ratio=0.1),
            run_time=2
        )
        self.wait(1)

        # Status texts
        status = Text("Starting Bubble Sort...", font_size=DESC_SIZE, color=WHITE).to_edge(UP, buff=0.3)
        pass_text = Text("", font_size=22, color=YELLOW).next_to(status, DOWN, buff=0.3)
        comparison_text = Text("", font_size=22, color=ORANGE).next_to(pass_text, DOWN, buff=0.2)
        
        self.play(Write(status))
        self.add(pass_text, comparison_text)
        self.wait(0.5)

        # Pointer for j only
        j_pointer = Arrow(start=UP*0.5, end=DOWN*0.2, color=YELLOW, buff=0.1, stroke_width=6)
        j_label = Text("j", font_size=28, color=YELLOW, weight=BOLD)
        
        # Bracket to show sorted region
        sorted_bracket = None
        sorted_label = None

        # ===== STEP 3: Bubble Sort with Detailed Animation =====
        n = len(array_values)

        for i in range(n):
            # Update pass information
            new_pass = Text(
                f"Pass {i+1}/{n}: Comparing elements from index 0 to {n-i-2}",
                font_size=22, color=YELLOW
            ).next_to(status, DOWN, buff=0.3)
            self.play(Transform(pass_text, new_pass), run_time=0.5)
            
            # Show sorted region bracket if there are sorted elements
            if i > 0:
                # Create bracket over sorted region
                sorted_start = boxes[n-i].get_right()
                sorted_end = boxes[n-1].get_left()
                
                new_bracket = BraceBetweenPoints(
                    sorted_start + DOWN*0.8,
                    sorted_end + DOWN*0.8,
                    direction=DOWN,
                    color=GREEN
                )
                new_label = Text("Sorted", font_size=20, color=GREEN).next_to(new_bracket, DOWN, buff=0.1)
                
                if sorted_bracket is None:
                    self.play(Create(new_bracket), Write(new_label), run_time=0.5)
                    sorted_bracket = new_bracket
                    sorted_label = new_label
                else:
                    self.play(
                        Transform(sorted_bracket, new_bracket),
                        Transform(sorted_label, new_label),
                        run_time=0.5
                    )
            
            for j in range(n - i - 1):
                # Update comparison text
                new_comp = Text(
                    f"Comparing index [{j}] = {numbers[j].text} with [{j+1}] = {numbers[j+1].text}",
                    font_size=22, color=ORANGE
                ).next_to(pass_text, DOWN, buff=0.2)
                self.play(Transform(comparison_text, new_comp), run_time=0.4)

                # Show j pointer
                j_pointer.next_to(boxes[j], UP, buff=0.2)
                j_label.next_to(j_pointer, UP, buff=0.1)
                if i == 0 and j == 0:
                    self.play(GrowArrow(j_pointer), Write(j_label), run_time=0.4)
                else:
                    self.play(
                        j_pointer.animate.next_to(boxes[j], UP, buff=0.2),
                        j_label.animate.next_to(j_pointer, UP, buff=0.1),
                        run_time=0.4
                    )

                box1 = boxes[j]
                box2 = boxes[j + 1]
                num1 = numbers[j]
                num2 = numbers[j + 1]

                # Highlight comparison
                self.play(
                    box1.animate.set_fill(YELLOW, opacity=0.6).set_stroke(YELLOW, width=4),
                    box2.animate.set_fill(YELLOW, opacity=0.6).set_stroke(YELLOW, width=4),
                    run_time=0.3
                )
                self.wait(0.3)

                if int(num1.text) > int(num2.text):
                    # Show swap action
                    swap_text = Text(
                        f"SWAP! {num1.text} > {num2.text}, swapping positions",
                        font_size=22, color=RED
                    ).next_to(pass_text, DOWN, buff=0.2)
                    self.play(Transform(comparison_text, swap_text), run_time=0.4)

                    # Change to swap color
                    self.play(
                        box1.animate.set_fill(RED, opacity=0.6).set_stroke(RED, width=4),
                        box2.animate.set_fill(RED, opacity=0.6).set_stroke(RED, width=4),
                        run_time=0.2
                    )

                    # Calculate swap positions
                    box1_target = boxes[j+1].get_center()
                    box2_target = boxes[j].get_center()

                    # Swap animation - lift, swap, lower
                    self.play(
                        box1.animate.shift(UP * 0.8),
                        num1.animate.shift(UP * 0.8),
                        box2.animate.shift(UP * 0.8),
                        num2.animate.shift(UP * 0.8),
                        run_time=0.3
                    )
                    
                    self.play(
                        box1.animate.move_to(box1_target + UP * 0.8),
                        num1.animate.move_to(box1_target + UP * 0.8),
                        box2.animate.move_to(box2_target + UP * 0.8),
                        num2.animate.move_to(box2_target + UP * 0.8),
                        run_time=0.5
                    )
                    
                    self.play(
                        box1.animate.move_to(box1_target),
                        num1.animate.move_to(box1_target),
                        box2.animate.move_to(box2_target),
                        num2.animate.move_to(box2_target),
                        run_time=0.3
                    )

                    # Update references after swap
                    boxes[j], boxes[j+1] = boxes[j+1], boxes[j]
                    numbers[j], numbers[j+1] = numbers[j+1], numbers[j]

                else:
                    no_swap_text = Text(
                        f"No swap: {num1.text} ≤ {num2.text}, already in order",
                        font_size=22, color=GREEN
                    ).next_to(pass_text, DOWN, buff=0.2)
                    self.play(Transform(comparison_text, no_swap_text), run_time=0.4)
                    self.wait(0.3)

                # Reset color
                self.play(
                    box1.animate.set_fill(BLUE, opacity=0.3).set_stroke(WHITE, width=3),
                    box2.animate.set_fill(BLUE, opacity=0.3).set_stroke(WHITE, width=3),
                    run_time=0.3
                )

            # Mark element as sorted
            sorted_text = Text(
                f"Position {n-i-1} now sorted!",
                font_size=22, color=GREEN
            ).next_to(pass_text, DOWN, buff=0.2)
            self.play(Transform(comparison_text, sorted_text), run_time=0.4)
            self.play(
                boxes[n-i-1].animate.set_fill(GREEN, opacity=0.5).set_stroke(GREEN, width=4),
                run_time=0.5
            )
            self.wait(0.5)

        # First element is also sorted
        self.play(
            boxes[0].animate.set_fill(GREEN, opacity=0.5).set_stroke(GREEN, width=4),
            run_time=0.5
        )
        
        # Update bracket to cover all elements
        if sorted_bracket:
            final_bracket = BraceBetweenPoints(
                boxes[0].get_right() + DOWN*0.8,
                boxes[n-1].get_left() + DOWN*0.8,
                direction=DOWN,
                color=GREEN
            )
            final_label = Text("All Sorted", font_size=20, color=GREEN).next_to(final_bracket, DOWN, buff=0.1)
            self.play(
                Transform(sorted_bracket, final_bracket),
                Transform(sorted_label, final_label),
                run_time=0.5
            )

        # ===== STEP 4: Final Message =====
        self.play(FadeOut(j_pointer), FadeOut(j_label), run_time=0.4)
        if sorted_bracket:
            self.play(FadeOut(sorted_bracket), FadeOut(sorted_label), run_time=0.4)
        
        final_status = Text(
            "Array is now SORTED!", 
            font_size=DESC_SIZE+4, 
            color=GREEN,
            weight=BOLD
        ).to_edge(UP, buff=0.3)
        self.play(Transform(status, final_status), FadeOut(pass_text), FadeOut(comparison_text), run_time=0.5)
        
        # Victory animation
        self.play(
            *[box.animate.scale(1.15).set_fill(GOLD, opacity=0.7).set_stroke(GOLD, width=5) for box in boxes],
            run_time=0.6
        )
        self.play(
            *[box.animate.scale(1/1.15) for box in boxes],
            run_time=0.6
        )
        self.wait(2)

        # ===== STEP 5: Clean Up =====
        self.play(
            FadeOut(boxes),
            FadeOut(numbers),
            FadeOut(indices),
            FadeOut(status),
            run_time=1.5
        )
        self.wait(1)
        
```
<Computer Data Structure Rule Only/>
"""

PHYSICS = """
<Physics Visualization Rule Only>
## Mandatory way to design

1. Title: Always at the center (never top). Must appear first and then fade out with a smooth animation (e.g., FadeOut, LaggedStart, star-burst effect). Do not include the equation in the title.
2. Axes: Create axes immediately after title fades.
3. Numbers: Use integers mostly; if needed, then 2 decimal precision. Do not include "π" value in the axes.
4. Axes style: Show only central axes (no grid).
5. Equation: Place in corners (left, right, bottom-left, bottom-right). If no space → fade it out before graph. and do not include Equation in the center
6. Margins: Leave a 5% gap at the top, bottom, left, and right edges.
7. Sequence: Title (center + fade out) → Axes → Equation (adaptive placement or fade) → Graph.


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

### Font Size Rules (adjustable based on content length)
TITLE_SIZE = 46       # not fixed, can change based on title length
EQUATION_SIZE = 36    # not fixed, can change based on formula/legend length
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
## Mandatory avoid these errors 

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

27. TypeError: CoordinateSystem._get_axis_label() got an unexpected keyword argument 'font_size'
    Fix (two options):
    Option 1 — Set font size after creation
    x_label = axes.get_x_axis_label("x (m)")
    y_label = axes.get_y_axis_label("y (m)")
    x_label.set_font_size(LABEL_SIZE)
    y_label.set_font_size(LABEL_SIZE)

    Option 2 — Wrap in MathTex
    x_label = axes.get_x_axis_label(MathTex("x (m)", font_size=LABEL_SIZE))
    y_label = axes.get_y_axis_label(MathTex("y (m)", font_size=LABEL_SIZE))

28. ValueError: latex error converting to dvi.
    Fix:
    equation2 = MathTex(r"x = x_0 + v_0 t + \frac{1}{2} a t^2")

29. AttributeError: NumberLine object has no attribute 'c2p'
    fix:
    Use number_line.n2p() instead of c2p()


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

class Animation_64cd9ba5(Scene):
    def construct(self):
        # ===== CONSTANTS =====
        TITLE_SIZE = 46
        EQUATION_SIZE = 30
        LABEL_SIZE = 24

        TOP_BUFFER = config.frame_height * 0.08
        BOTTOM_BUFFER = config.frame_height * 0.08
        LEFT_BUFFER = config.frame_width * 0.08
        RIGHT_BUFFER = config.frame_width * 0.08
        
        # Physics constants
        g = 9.8  # acceleration due to gravity, m/s²
        v0 = 15  # initial velocity magnitude, m/s
        angle_deg = 60  # launch angle, degrees
        angle_rad = np.deg2rad(angle_deg)
        vx0 = v0 * np.cos(angle_rad)  # initial x-velocity
        vy0 = v0 * np.sin(angle_rad)  # initial y-velocity
        t_max = (2 * vy0) / g  # total time of flight
        max_x_val = vx0 * t_max  # maximum horizontal distance
        max_y_val = (vy0**2) / (2 * g)  # maximum vertical height

        self.camera.background_color = BLACK

        # ===== STEP 1: Title Display and Fade Out =====
        title = Text("Projectile Motion", font_size=TITLE_SIZE, color=WHITE)
        title.move_to(ORIGIN)

        self.play(Write(title, run_time=1.5))
        self.wait(3)

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

        # ===== STEP 2: Axes Creation and Positioning =====
        x_range_val_calc = max_x_val * 1.2
        y_range_val_calc = max_y_val * 1.5

        x_range = [0, max(5, round(x_range_val_calc)), 5]
        y_range = [0, max(5, round(y_range_val_calc)), 5]

        # Make graph smaller - 70% of available space
        axes = Axes(
            x_range=x_range,
            y_range=y_range,
            x_length=(config.frame_width - LEFT_BUFFER - RIGHT_BUFFER) * 0.7,
            y_length=(config.frame_height - BOTTOM_BUFFER - TOP_BUFFER) * 0.7,
            axis_config={
                "include_numbers": True,
                "font_size": LABEL_SIZE,
                "decimal_number_config": {"num_decimal_places": 0},
                "color": WHITE
            },
            x_axis_config={"label_direction": DOWN},
            y_axis_config={"label_direction": LEFT},
        )
        
        # Position axes with more buffer
        target_origin_point = np.array([
            -config.frame_width/2 + LEFT_BUFFER * 1.5,
            -config.frame_height/2 + BOTTOM_BUFFER * 1.5,
            0
        ])
        axes.shift(target_origin_point - axes.c2p(0,0))

        x_label = axes.get_x_axis_label("x (m)", edge=DOWN, direction=DOWN)
        y_label = axes.get_y_axis_label("y (m)", edge=LEFT, direction=LEFT)
        axes_labels = VGroup(x_label, y_label)

        self.play(Create(axes), Create(axes_labels), run_time=2)

        # ===== STEP 3: Equation Display in Top-Right =====
        equation_text = MathTex(
            r"x(t) = (v_0 \cos \theta) t",
            r"y(t) = (v_0 \sin \theta) t - \frac{1}{2} g t^2",
            font_size=EQUATION_SIZE,
            color=WHITE
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3)

        # Position in top-right corner with proper buffer
        equation_text.to_corner(UR, buff=0.5)

        self.play(Write(equation_text, run_time=1))

        # ===== STEP 4: Initial Velocity Vector and Angle =====
        initial_velocity_vec = Arrow(
            start=axes.c2p(0,0),
            end=axes.c2p(vx0 * 0.7, vy0 * 0.7),
            color=ORANGE,
            max_stroke_width_to_length_ratio=0.1,
            buff=0
        )

        v0_label = MathTex(r"v_0", font_size=LABEL_SIZE, color=ORANGE)
        v0_label.next_to(initial_velocity_vec, UP+RIGHT, buff=0.1)

        angle_arc = Arc(
            radius=0.8,
            start_angle=0,
            angle=angle_rad,
            arc_center=axes.c2p(0,0),
            color=ORANGE
        )

        angle_label = MathTex(r"\theta", font_size=LABEL_SIZE, color=ORANGE)
        angle_label.next_to(angle_arc, RIGHT * 0.5 + UP * 0.5, buff=0.1) 

        initial_launch_elements = VGroup(initial_velocity_vec, v0_label, angle_arc, angle_label)

        self.play(GrowFromPoint(initial_launch_elements, axes.c2p(0,0)), run_time=1.5)

        # ===== STEP 5: Projectile Path and Moving Projectile =====
        def path_function(t):
            x = vx0 * t
            y = vy0 * t - 0.5 * g * t**2
            return axes.c2p(x, y)

        projectile_path = ParametricFunction(
            path_function,
            t_range=[0, t_max, 0.01],
            color=BLUE,
            stroke_width=4
        )

        t_tracker = ValueTracker(0)

        projectile_dot = always_redraw(
            lambda: Dot(point=path_function(t_tracker.get_value()), color=RED, radius=0.15)
        )

        self.play(Create(projectile_path, run_time=2))
        self.play(FadeIn(projectile_dot, run_time=0.5))

        # ===== STEP 6: Instantaneous Velocity and Gravity Vectors, and Time Label =====
        inst_velocity_vec = always_redraw(
            lambda: Arrow(
                start=projectile_dot.get_center(),
                end=projectile_dot.get_center() + (
                    lambda: (
                        velocity_vector_at_t := axes.c2p(vx0, vy0 - g * t_tracker.get_value()) - axes.c2p(0,0),
                        normalized_velocity_vector := velocity_vector_at_t / np.linalg.norm(velocity_vector_at_t) if np.linalg.norm(velocity_vector_at_t) != 0 else np.array([0., 0., 0.]),
                        scaled_velocity_vector := normalized_velocity_vector * 2
                    )[2]
                )(),
                color=YELLOW,
                max_stroke_width_to_length_ratio=0.1,
                buff=0
            )
        )

        inst_velocity_label = always_redraw(
            lambda: MathTex(r"\vec{v}", font_size=LABEL_SIZE, color=YELLOW).next_to(inst_velocity_vec, UP, buff=0.1)
        )

        gravity_vec = always_redraw(
            lambda: Arrow(
                start=projectile_dot.get_center(),
                end=projectile_dot.get_center() + DOWN * 0.7,
                color=GREEN,
                max_stroke_width_to_length_ratio=0.1,
                buff=0
            )
        )

        gravity_label = always_redraw(
            lambda: MathTex(r"\vec{g}", font_size=LABEL_SIZE, color=GREEN).next_to(gravity_vec, DOWN, buff=0.1)
        )

        time_label_group = always_redraw(
            lambda: VGroup(
                MathTex(r"t = ", font_size=LABEL_SIZE, color=WHITE),
                DecimalNumber(t_tracker.get_value(), num_decimal_places=2, font_size=LABEL_SIZE, color=WHITE)
            ).arrange(RIGHT, buff=0.1).to_corner(DL, buff=0.5)
        )

        self.play(
            FadeIn(inst_velocity_vec),
            FadeIn(inst_velocity_label),
            FadeIn(gravity_vec),
            FadeIn(gravity_label),
            FadeIn(time_label_group),
            run_time=1
        )

        # ===== STEP 7: Animate Projectile Motion =====
        self.play(t_tracker.animate.set_value(t_max), run_time=t_max, rate_func=linear)

        # ===== STEP 8: Clean Up =====
        self.play(
            FadeOut(axes),
            FadeOut(axes_labels),
            FadeOut(equation_text),
            FadeOut(initial_launch_elements),
            FadeOut(projectile_path),
            FadeOut(projectile_dot),
            FadeOut(inst_velocity_vec),
            FadeOut(inst_velocity_label),
            FadeOut(gravity_vec),
            FadeOut(gravity_label),
            FadeOut(time_label_group),
            run_time=1.5
        )
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