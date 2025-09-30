GRAPH2D = """
<2D Graph Scenes Rule Only>

## Comon Error to avoid

1. CoordinateSystem._get_axis_label() got an unexpected keyword argument 'font_size'

    Fix: wrap the label in Text or MathTex with font_size, e.g.
    x_label = axes.get_x_axis_label(MathTex("x", font_size=28))
    y_label = axes.get_y_axis_label(MathTex("f(x)", font_size=28))

2. Error Message: Found non-raw strings in MathTex calls. Specifically, 'x' and 'f(x)' should be r'x' and r'f(x)' respectively to ensure proper LaTeX parsing. For example: MathTex(r"x", ...).

## Font Size Hierarchy (Mandatory)
```python
TITLE_SIZE = 46      # Maximum title size
EQUATION_SIZE = 36   # Equations must be smaller than title
LABEL_SIZE = 28      # Labels must be smaller than equations
DESC_SIZE = 24       # Descriptions smallest
```

## Edge Buffers (5% Mandatory)
```python
EDGE_BUFFER = 0.05
buff_left = config.frame_width * 0.05
buff_right = config.frame_width * 0.05
buff_bottom = config.frame_height * 0.05
```

## Decimal Precision (2 Places Only)
```python
# Axes
axes = Axes(
    x_range=[-5, 5, 1],
    y_range=[-3, 3, 1],
    axis_config={
        "include_numbers": True,
        "decimal_number_config": {"num_decimal_places": 2}
    }
)

# All numbers
point_label = Text(f"({x:.2f}, {y:.2f})", font_size=28)
value_text = Text(f"Value: {result:.2f}", font_size=24)
```

## Space Management - Fade Out Rule
**When space is insufficient, ALWAYS fade out equation before showing new elements:**
```python
# If adding complex elements and space is tight
self.play(FadeOut(equation))
self.play(Create(new_element))
# Optionally bring back later
self.play(FadeIn(equation))
```

## Animation Sequence (Mandatory)
1. Title (46pt) → 2. Equation (36pt) → 3. Axes → 4. Labels (28pt) → 5. Graph → 6. Transforms

## Standard Setup
```python
# Title
title = Text("Graph Title", font_size=46)
title.to_edge(UP, buff=0.3)
self.play(Write(title))

# Equation (smaller than title)
equation = MathTex(r"f(x) = x^2", font_size=36)
equation.to_edge(LEFT, buff=config.frame_width * 0.05).shift(UP*2)
self.play(Write(equation))

# Axes (with 5% margins)
axes = Axes(
    x_range=[-3, 3, 1],
    y_range=[-2, 2, 1],
    x_length=8,
    y_length=5,
    axis_config={
        "include_numbers": True,
        "decimal_number_config": {"num_decimal_places": 2}
    }
).move_to(ORIGIN)
axes.scale_to_fit_width(config.frame_width * 0.9)
self.play(Create(axes))

# Labels (smaller than equation)
x_label = axes.get_x_axis_label("x", font_size=28)
y_label = axes.get_y_axis_label("f(x)", font_size=28)
self.play(Write(x_label), Write(y_label))

# Graph
graph = axes.plot(lambda x: x**2, x_range=[-3, 3], color=BLUE)
self.play(Create(graph))
```

## Safe Positioning
```python
# Top-left with buffer
equation.to_corner(UL, buff=config.frame_width * 0.05)

# Bottom with buffer
description.to_edge(DOWN, buff=config.frame_height * 0.05)

# Right side with buffer
legend.to_edge(RIGHT, buff=config.frame_width * 0.05)
```

## Multi-Graph Colors
- Primary: `BLUE`
- Secondary: `GREEN`
- Reference: `YELLOW`
- Intersections: `RED`

```python
graph1 = axes.plot(func1, color=BLUE)
graph2 = axes.plot(func2, color=GREEN)
self.play(Create(graph1))
self.wait(0.5)
self.play(Create(graph2))
```

## Points with 2 Decimals
```python
x_val, y_val = 2.34, 5.48
point = Dot(axes.c2p(x_val, y_val), color=RED)
label = Text(f"({x_val:.2f}, {y_val:.2f})", font_size=28)
label.next_to(point, UR, buff=0.1)
```

## Area Visualization
```python
area = axes.get_area(graph, x_range=[a, b], color=BLUE, opacity=0.3)
self.play(Create(area))

# Area value with 2 decimals
area_value = calculate_area(graph, a, b)
area_text = Text(f"Area: {area_value:.2f}", font_size=24)
area_text.to_edge(DOWN, buff=config.frame_height * 0.05)
```

## Riemann Sums
```python
rects = axes.get_riemann_rectangles(
    graph, x_range=[a, b], dx=0.5, 
    color=BLUE, fill_opacity=0.5
)
self.play(Create(rects))

# Refinement
for dx in [1, 0.5, 0.25, 0.1]:
    new_rects = axes.get_riemann_rectangles(graph, dx=dx)
    self.play(Transform(rects, new_rects), run_time=1)
```

## Tangent Lines
```python
def get_tangent_line(axes, graph, x_val, length=3):
    point = axes.c2p(x_val, graph.underlying_function(x_val))
    slope = derivative_at(x_val)
    return Line(
        point + LEFT*length/2, 
        point + RIGHT*length/2, 
        color=RED
    )

tangent = get_tangent_line(axes, graph, x_val)
slope_text = Text(f"Slope: {slope:.2f}", font_size=24)
slope_text.to_corner(UR, buff=config.frame_width * 0.05)
```

## Moving Elements
```python
x_tracker = ValueTracker(x_start)

moving_dot = always_redraw(lambda:
    Dot(axes.c2p(
        x_tracker.get_value(),
        graph.underlying_function(x_tracker.get_value())
    ), color=RED)
)

coord_text = always_redraw(lambda:
    Text(
        f"({x_tracker.get_value():.2f}, "
        f"{graph.underlying_function(x_tracker.get_value()):.2f})",
        font_size=28
    ).next_to(moving_dot, UR)
)

self.play(x_tracker.animate.set_value(x_end), run_time=3)
```

## Transformations
```python
# Morphing graphs
graph2 = axes.plot(lambda x: np.sin(x), color=GREEN)
self.play(Transform(graph1, graph2), run_time=3)

# Scaling
self.play(graph.animate.scale(1.5), run_time=2)
```

## Parametric Curves
```python
curve = axes.plot_parametric_curve(
    lambda t: np.array([np.cos(t), np.sin(t), 0]),
    t_range=[0, 2*PI],
    color=PURPLE
)
```

## Piecewise Functions
```python
def piecewise(x):
    return x**2 if x < 0 else np.sqrt(x)

graph = axes.plot(piecewise, x_range=[-2, 4], use_smoothing=False)
```

## Discontinuous Functions
```python
graph1 = axes.plot(lambda x: 1/x, x_range=[-3, -0.1], color=BLUE)
graph2 = axes.plot(lambda x: 1/x, x_range=[0.1, 3], color=BLUE)
self.play(Create(graph1), Create(graph2))
```

## Legend
```python
legend = VGroup(
    Line(ORIGIN, RIGHT*0.5, color=BLUE),
    Text("f(x)", font_size=24),
    Line(ORIGIN, RIGHT*0.5, color=GREEN),
    Text("g(x)", font_size=24)
).arrange_in_grid(rows=2, cols=2, buff=0.2)
legend.to_corner(UR, buff=config.frame_width * 0.05)
```

## Dashed Reference Lines
```python
ref_line = DashedLine(
    axes.c2p(x_val, y_min),
    axes.c2p(x_val, y_max),
    color=YELLOW
)
```

## Gradient Fills
```python
area = axes.get_area(
    graph, 
    x_range=[a, b],
    color=[BLUE, GREEN],
    opacity=0.5
)
```

## Complete Example:
from manim import *

class Animation_6dd97c70(Scene):
    def construct(self):
        # Constants for font sizes and buffers
        TITLE_SIZE = 46
        EQUATION_SIZE = 36
        LABEL_SIZE = 28
        DESC_SIZE = 24

        EDGE_BUFFER = 0.05
        buff_left = config.frame_width * EDGE_BUFFER
        buff_right = config.frame_width * EDGE_BUFFER
        buff_bottom = config.frame_height * EDGE_BUFFER

        # Step 1: Scene setup
        self.camera.background_color = BLACK

        axes = Axes(
            x_range=[-4 * PI, 4 * PI, PI],
            y_range=[-1.5, 1.5, 0.5],
            x_length=12,
            y_length=5,
            axis_config={
                "include_numbers": True,
                "decimal_number_config": {"num_decimal_places": 2}
            },
            x_axis_config={"unit_size": 1.5},
            y_axis_config={"unit_size": 2}
        ).move_to(ORIGIN)
        axes.scale_to_fit_width(config.frame_width * 0.9)

        # Step 2: Display title
        title = Text("Phase Shift Animation", font_size=TITLE_SIZE, color=WHITE)
        title.to_edge(UP, buff=0.3)
        self.play(Write(title), run_time=1)

        # Step 3: Display equation
        equation = MathTex(r"y = \sin(x + t)", font_size=EQUATION_SIZE, color=WHITE)
        equation.to_edge(LEFT, buff=config.frame_width * 0.05).shift(UP*2)
        self.play(Write(equation), run_time=1)

        # Step 4: Animate axes and labels
        self.play(Create(axes), run_time=1.5)

        x_label_text = Text("x", font_size=LABEL_SIZE)
        x_label = axes.get_x_axis_label(x_label_text)
        y_label_text = Text("y", font_size=LABEL_SIZE)
        y_label = axes.get_y_axis_label(y_label_text)
        self.play(Write(x_label), Write(y_label), run_time=0.5)

        # Step 5: Initialize and animate the phase-shifted sine wave
        t_tracker = ValueTracker(0)

        graph = always_redraw(
            lambda: axes.plot(
                lambda x: np.sin(x + t_tracker.get_value()),
                x_range=[-4 * PI, 4 * PI],
                color=BLUE
            )
        )

        self.play(Create(graph), run_time=2)
        self.play(t_tracker.animate.set_value(4 * PI), run_time=8, rate_func=linear)
        self.wait(1)


## Critical Rules Summary
1. **Font Hierarchy**: Title(46) > Equation(36) > Label(28) > Desc(24)
2. **5% Edge Buffer**: All elements from left, right, bottom
3. **2 Decimal Places**: All numbers use `:.2f`
4. **Space Management**: Fade out equation if space needed
5. **Animation Order**: Title → Equation → Axes → Labels → Graph
6. **No Edge Clipping**: Scale to 90% width/height max
7. **Label Size**: Always smaller than equation size
8. **Equation Size**: Always smaller than title size

## Quick Checklist
- Title 46pt or less
- Equation 36pt, smaller than title
- Labels 28pt, smaller than equation
- 5% buffer from edges (left, right, bottom)
- All decimals show 2 places if needed otherwise use integer number
- Equation fades out if space tight
- Animation sequence correct
- Colors distinct and visible
- No text overlap
- All labels present
- LaTeX parsing. For example: MathTex(r"x", ...)

## Common Mistakes
1. Text too large (>46pt title)
2. Equation larger than title
3. Labels larger than equation
4. Elements touching screen edges
5. Wrong decimal places (not 2)
6. Keeping equation when space tight
7. Wrong animation order
8. Missing 5% buffers
9. Error Message: Found non-raw strings in MathTex calls. Specifically, 'x' and 'f(x)' should be r'x' and r'f(x)' respectively to ensure proper LaTeX parsing. For example: MathTex(r"x", ...)

<2D Graph Scenes Rule Only/>
"""

GRAPH3D="""
<3D Scenes and Graph Rule Only>

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

## Animation Sequence (Mandatory Order)

1. **Title First:** `self.play(Write(title))` – animate title before anything else.
2. **Equations Second:** `self.play(Write(equation))` – show mathematical context.
3. **Axes Third:** `self.play(Create(axes))` – establish coordinate system.
4. **3D Object Last:** `self.play(Create(surface))` – main visualization.
5. **Rotations/Movements:** Any camera or object rotations after all elements are visible.

---

## Some error you need to avoid
1 nNameError: name Cuboid is not defined: Fix
    Shape you need  Manim class  Example
    Standard cube   Cube        Cube(side_length=2)
    Rectangular box Prism       Prism(dimensions=[2,1,3])

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
* 3D object: 3-4 seconds
* Additional elements (slices/volumes): 0.3 seconds each with lag
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

## Complete Example: Multi-Element Scene

```python
from manim import *

class DoubleIntegralVisualization(ThreeDScene):
    def construct(self):
        self.camera.background_color = BLACK
        self.set_camera_orientation(phi=70*DEGREES, theta=-45*DEGREES, distance=12)
        
        # Step 1: Title
        title = Tex(r"\\textbf{Double Integral for Volume}", font_size=48)
        self.add_fixed_in_frame_mobjects(title)
        title.to_edge(UP)
        self.play(Write(title))
        self.wait(0.5)
        
        # Step 2: Equation (positioned higher for multi-element scene)
        equation = MathTex(
            r"V = \\int_0^1 \\int_0^1 (4 + (x^2 - y)) \\, dy \\, dx",
            font_size=32
        )
        self.add_fixed_in_frame_mobjects(equation)
        equation.to_edge(LEFT).shift(UP*2)  # Higher positioning
        self.play(Write(equation), run_time=2)
        
        # Step 3: Axes
        axes = ThreeDAxes(
            x_range=[0, 1.5, 0.5],
            y_range=[0, 1.5, 0.5],
            z_range=[0, 6, 2]
        )
        self.play(Create(axes), run_time=1.5)
        
        # Step 4: Main surface (with transparency for multi-element)
        surface = Surface(
            lambda u, v: np.array([u, v, 4 + (u**2 - v)]),
            u_range=[0, 1], v_range=[0, 1],
            resolution=(20, 20)
        )
        surface.set_fill_opacity(0.6)  # Semi-transparent for slices
        surface.set_stroke_opacity(0.3)
        surface.move_to(ORIGIN)
        
        self.play(Create(surface), run_time=3)
        self.wait(1)
        
        # Step 5: Cross-sectional slices (progressive appearance)
        slices = []
        for x in np.linspace(0.1, 0.9, 5):
            slice_rect = Polygon(
                axes.c2p(x, 0, 0),
                axes.c2p(x, 0, 4 + x**2),
                axes.c2p(x, 1, 4 + (x**2 - 1)),
                axes.c2p(x, 1, 0)
            )
            slice_rect.set_fill(BLUE, opacity=0.4)
            slice_rect.set_stroke(BLUE, width=2)
            slices.append(slice_rect)
        
        # Fade equation during slice display
        self.play(FadeOut(equation), run_time=0.5)
        
        # Show slices progressively
        for slice in slices:
            self.play(Create(slice), run_time=0.3)
        
        self.wait(1)
        
        # Step 6: Group for rotation
        group = VGroup(surface, axes, *slices)
        self.play(
            Rotate(group, angle=PI/3, axis=Z_AXIS, run_time=4, rate_func=linear)
        )
        
        # Bring back equation
        self.play(FadeIn(equation))
        self.wait(2)
```
<3D Scenes and Graph Rule Only/>

"""

COMPUTER_DATASTRUCTURE="""
<Computer Data Structure Rule Only>
**Rules for 2D Computer Data Structure Animations (Manim)**

0 *Important*
    Do not draw The grid and crosshair lines

1. **Enforce Frame Bounds in Code**
   Before rendering, inspect each mobject’s bounding box against the camera frame:

```python
frame_w, frame_h = config.frame_width, config.frame_height
safe_pad = 0.5

def inside_safe(mobj):
    x_min, y_min, _ = mobj.get_corner(DOWN + LEFT)
    x_max, y_max, _ = mobj.get_corner(UP + RIGHT)
    return (
        x_min >= -frame_w/2 + safe_pad and
        x_max <=  frame_w/2 - safe_pad and
        y_min >= -frame_h/2 + safe_pad and
        y_max <=  frame_h/2 - safe_pad
    )

for m in [title, visited_text, tree]:
    if not inside_safe(m):
        m.scale_to_fit_width(frame_w - 1.0)  # or reposition
```

This forces you to shrink or move anything that would overflow.

2. **Auto-Scaling Helpers**
   Use built-in helpers instead of guessing sizes:

```python
title.scale_to_fit_width(config.frame_width - 1.0)
```

This guarantees the title never exceeds the frame width.

3. **Progressive Reveal**
   If the scene is crowded, fade out the title or older elements before showing new ones:

```python
self.play(FadeIn(title))
self.wait(1)
self.play(FadeOut(title))
```

4. **Dynamic Font Sizing & Placement for Annotations (Visited Nodes)**

   * Always keep `visited_text` **below the diagram** with extra padding so it never overlaps with nodes or edges:

```python
visited_text.next_to(tree, DOWN, buff=1.0)
```

* If the tree is large, shrink or reposition the visited text dynamically:

```python
max_w = config.frame_width - 1.0
if visited_text.width > max_w:
    visited_text.scale_to_fit_width(max_w)
```

5. **Title Placement**

   * Always center the title horizontally:

```python
title.to_edge(UP)
```

* Ensure it remains inside the safe zone.

6. **Diagram Styling (Cool & Clear Visuals)**

   * Use **consistent node colors**: e.g., unvisited nodes = `BLUE_C`, current node = `YELLOW`, visited = `GREEN`.
   * Highlight active edges with brighter colors (`GREEN` or `ORANGE`).
   * Use **arrows** instead of plain lines for edges:

```python
Line(start, end, buff=0.2).add_tip(tip_length=0.2)
```

* Mark nodes with **circle outlines** and fill opacity for clarity.
* Add subtle shadows or glow (e.g., stroke width or contrasting edge colors) for emphasis.

7. **General Guidelines**

   * Use raw strings for LaTeX: `MathTex(r"x^2")`.
   * Ensure no unintended overlaps between mobjects.
   * Do not set opacity in the constructor; use `.set_opacity()` after creation.
   * Keep all objects within frame boundaries.
   * Ensure visited nodes and arrows are updated smoothly with animations (e.g., `self.play(FadeToColor(node, GREEN))`).

<Computer Data Structure Rule Only/>

"""

PHYSICS = """
<Physics Visualization Rule Only>
## Font Size Hierarchy (Dynamic Scaling)

```python
# Base sizes - scale down if content is complex
def get_font_sizes(content_complexity='medium'):
    if content_complexity == 'simple':
        return {
            'TITLE_SIZE': 48,
            'EQUATION_SIZE': 36,
            'LABEL_SIZE': 28,
            'DESC_SIZE': 24,
            'VARIABLE_SIZE': 20
        }
    elif content_complexity == 'medium':
        return {
            'TITLE_SIZE': 42,
            'EQUATION_SIZE': 32,
            'LABEL_SIZE': 24,
            'DESC_SIZE': 20,
            'VARIABLE_SIZE': 18
        }
    else:  # complex
        return {
            'TITLE_SIZE': 36,
            'EQUATION_SIZE': 28,
            'LABEL_SIZE': 22,
            'DESC_SIZE': 18,
            'VARIABLE_SIZE': 16
        }

# Rule: Title should always be largest, followed by equations, labels, descriptions
# If scene is crowded, use smaller base sizes
```

## Edge Buffers and Safe Zones

```python
EDGE_BUFFER = 0.05       # 5% buffer from all edges
TOP_SAFE_ZONE = 0.30     # Top 30% reserved for text in 3D scenes
buff_x = config.frame_width * EDGE_BUFFER
buff_y = config.frame_height * EDGE_BUFFER
```

## Decimal Precision (2 Places)

```python
force_text = Text(f"F = {force_value:.2f} N", font_size=LABEL_SIZE)
velocity_label = Text(f"v = {v:.2f} m/s", font_size=LABEL_SIZE)
field_text = Text(f"E = {E:.2f} V/m", font_size=DESC_SIZE)
```

## Frame Safety & Physics Object Scaling

```python
frame_w = config.frame_width
frame_h = config.frame_height

SAFE_MARGIN = 0.5
x_bounds = [-frame_w/2 + SAFE_MARGIN, frame_w/2 - SAFE_MARGIN]
y_bounds = [-frame_h/2 + SAFE_MARGIN, frame_h/2 - SAFE_MARGIN]

physics_object.scale_to_fit_width(frame_w * 0.8)
physics_object.scale_to_fit_height(frame_h * 0.7)
```

## Force Vector Management (CORRECTED)

```python
# Basic arrow syntax - NO tip_length in constructor
force_vector = Arrow(
    start=start_point,
    end=end_point,
    buff=0,
    color=RED,
    stroke_width=6
    # DO NOT USE: tip_length, max_tip_length_to_length_ratio
)

# Adjust tip after creation if needed
force_vector.tip.scale(0.8)  # Make tip smaller if needed

# Standard color coding
FORCE_COLOR = RED
VELOCITY_COLOR = BLUE
ACCELERATION_COLOR = ORANGE
DISPLACEMENT_COLOR = GREEN

# Vector labels
force_label = MathTex(r"\vec{F}", font_size=LABEL_SIZE, color=RED)
force_label.next_to(force_vector, UR, buff=0.2)
```

## 3D Arrows (CORRECTED)

```python
# For 3D scenes, use Arrow3D - NO tip_length or cone_height parameters
from manim import Arrow3D

arrow_3d = Arrow3D(
    start=start_point,
    end=end_point,
    color=RED
    # DO NOT USE: tip_length, cone_height, resolution
)

# Adjust appearance after creation
arrow_3d.set_color(RED)
arrow_3d.set_stroke(width=4)
```

## Field Visualization Layout

```python
max_field_lines = int((frame_w * frame_h) / 4)
field_line_density = min(requested_density, max_field_lines)

def get_field_color(field_strength, max_strength):
    normalized = min(field_strength / max_strength, 1.0)
    return interpolate_color(BLUE, RED, normalized)

field_equations = VGroup(
    MathTex(r"\vec{E} = k\frac{q}{r^2}", font_size=EQUATION_SIZE),
    MathTex(r"|\vec{E}| = {E_value:.2f}", font_size=DESC_SIZE)
).arrange(DOWN, buff=0.2)
field_equations.to_edge(LEFT, buff=buff_x).shift(DOWN*0.3)
```

## Wave Animation Positioning

```python
content_y = -0.5
wave_center = np.array([0, content_y, 0])
max_amplitude = min(frame_h/4, 2.0)

wave_params = VGroup(
    Text(f"λ = {wavelength:.2f} m", font_size=DESC_SIZE),
    Text(f"f = {frequency:.2f} Hz", font_size=DESC_SIZE),
    Text(f"v = {velocity:.2f} m/s", font_size=DESC_SIZE)
).arrange(DOWN, buff=0.15, aligned_edge=LEFT)
wave_params.to_corner(UR, buff=buff_x)
```

## Particle System Bounds

```python
orbit_radius = min(frame_w * 0.35, frame_h * 0.35)

collision_bounds = {
    'x_min': -frame_w/2 + 0.8,
    'x_max': frame_w/2 - 0.8,
    'y_min': -frame_h/2 + 0.8,
    'y_max': frame_h/2 - 0.8
}

# Particle trails with auto-fade (CORRECTED)
trajectory = TracedPath(
    particle.get_center,
    stroke_color=YELLOW,
    stroke_width=3,
    dissipating_time=2.0
)
self.add(trajectory)
```

## Physics Equation Placement with Space Management

```python
# Group equations and check available space
main_equations = VGroup(
    MathTex(r"F = ma", font_size=EQUATION_SIZE),
    MathTex(r"E = \frac{1}{2}mv^2", font_size=EQUATION_SIZE)
).arrange(DOWN, buff=0.2)
main_equations.to_edge(LEFT, buff=buff_x).shift(UP*1.5)

variable_defs = VGroup(
    MathTex(r"F: \text{Force}", font_size=VARIABLE_SIZE),
    MathTex(r"m: \text{Mass}", font_size=VARIABLE_SIZE)
).arrange(DOWN, buff=0.15, aligned_edge=LEFT)
variable_defs.next_to(main_equations, DOWN, buff=0.4)

# If space is limited, fade out less important elements
if physics_object.height > frame_h * 0.6:
    self.play(FadeOut(variable_defs), run_time=0.5)

constants = Text("g = 9.81 m/s²", font_size=DESC_SIZE)
constants.to_edge(DOWN, buff=buff_y).to_edge(RIGHT, buff=buff_x)
```

## 3D Physics Visualization (CORRECTED)

### Scene Setup Order

```python
from manim import *

class PhysicsScene3D(ThreeDScene):
    def construct(self):
        # Dynamic font sizing based on content
        sizes = get_font_sizes('medium')
        TITLE_SIZE = sizes['TITLE_SIZE']
        EQUATION_SIZE = sizes['EQUATION_SIZE']
        buff_x = config.frame_width * 0.05
        
        self.camera.background_color = BLACK
        
        # Step 1: Set camera orientation FIRST
        self.set_camera_orientation(
            phi=70*DEGREES, 
            theta=-45*DEGREES
        )
        
        # Step 2: Animate title FIRST
        title = Tex(r"\textbf{3D Physics Title}", font_size=TITLE_SIZE)
        self.add_fixed_in_frame_mobjects(title)
        title.to_edge(UP, buff=0.3)
        self.play(Write(title), run_time=1)
        
        # Step 3: Animate equations SECOND
        equations = MathTex(r"F = ma", font_size=EQUATION_SIZE)
        self.add_fixed_in_frame_mobjects(equations)
        equations.to_edge(LEFT, buff=buff_x).shift(UP*2)
        self.play(Write(equations), run_time=1.5)
        
        # Step 4: Create 3D axes (CORRECTED)
        axes = ThreeDAxes(
            x_range=[-5, 5, 1],
            y_range=[-5, 5, 1],
            z_range=[-5, 5, 1],
            x_length=6,
            y_length=6,
            z_length=6
        )
        
        # Step 5: Create physics objects at ORIGIN
        physics_object = Sphere(radius=0.5, color=BLUE)
        physics_object.move_to(ORIGIN)
        
        # Step 6: Animate 3D objects
        self.play(Create(axes), Create(physics_object), run_time=2)
```

### Fixed Text Elements (CRITICAL)

```python
# ALL text must use add_fixed_in_frame_mobjects BEFORE positioning
title = Text("Title", font_size=TITLE_SIZE)
self.add_fixed_in_frame_mobjects(title)
title.to_edge(UP, buff=0.3)

equations = MathTex(r"equation", font_size=EQUATION_SIZE)
self.add_fixed_in_frame_mobjects(equations)
equations.to_edge(LEFT, buff=buff_x).shift(UP*2)
```

### 3D Object Centering

```python
# Center at ORIGIN
pivot = Sphere(radius=0.1, color=GRAY).move_to(ORIGIN)
bob = Sphere(radius=0.3, color=RED).move_to([0, 0, -3])
```

### 3D Vector Fields (CORRECTED)

```python
max_3d_vectors = 200

# Use Arrow3D for 3D vectors - simplified syntax
start = axes.c2p(x, y, 0)
end = axes.c2p(x + dx, y + dy, dz)
arrow = Arrow3D(start, end, color=BLUE)

# NO tip_length, cone_height parameters
```

## Space Management & Fade Strategy

```python
# Check if elements overlap or exceed bounds
def check_space_available(new_element, existing_elements):
    for existing in existing_elements:
        if new_element.get_center()[1] - existing.get_center()[1] < 0.5:
            return False
    return True

# Fade out strategy when space is limited
if not check_space_available(new_text, [title, equations]):
    # Fade out least important element first
    self.play(FadeOut(variable_defs), run_time=0.5)
    self.wait(0.3)
    
# Then show new element
self.play(FadeIn(new_text), run_time=0.5)

# Progressive fade pattern
# Priority: Title (never fade) > Main equations > Labels > Descriptions
```

## Animation Timing for Physics

```python
TIMING = {
    'title': 1.0,
    'equation': 1.5,
    'force_application': 2.0,
    'wave_propagation': 3.0,
    'field_creation': 2.0,
    'particle_motion': 4.0,
    'rotation_3d': 4.0,
    'fade_transition': 0.5  # For space management
}

# Smooth force applications
self.play(
    force_vector.animate.shift(direction),
    run_time=TIMING['force_application'],
    rate_func=smooth
)

# Particle motion with ValueTracker (CORRECTED)
t_tracker = ValueTracker(0)
self.play(
    t_tracker.animate.set_value(10),
    run_time=TIMING['particle_motion'],
    rate_func=linear
)
```

## Critical API Corrections

### ThreeDAxes (CORRECT)

```python
axes = ThreeDAxes(
    x_range=[-5, 5, 1],
    y_range=[-5, 5, 1],
    z_range=[-5, 5, 1],
    x_length=6,
    y_length=6,
    z_length=6
)
# NOT: length=6  (parameter doesn't exist)
```

### Arrow/Arrow3D (CORRECT)

```python
# 2D Arrow
arrow = Arrow(start, end, color=RED, buff=0)
# NO: tip_length, max_tip_length_to_length_ratio parameters

# 3D Arrow
arrow_3d = Arrow3D(start, end, color=RED)
# NO: tip_length, cone_height, resolution parameters
```

### TracedPath (CORRECT)

```python
trajectory = TracedPath(
    obj.get_center,
    stroke_color=YELLOW,
    stroke_width=3,
    dissipating_time=2.0
)
self.add(trajectory)
# NO: stroke_opacity, max_num_points parameters
```

### ValueTracker (CORRECT)

```python
t_tracker = ValueTracker(0)
self.play(t_tracker.animate.set_value(10), run_time=3)

# In updater
def updater(mob, dt):
    current = t_tracker.get_value()
    t_tracker.set_value(current + dt)
# NO: increment() method
```

### Camera Rotation (CORRECT)

```python
# Rotate camera
self.begin_ambient_camera_rotation(rate=0.1)
self.wait(10)
self.stop_ambient_camera_rotation()

# Rotate objects
self.play(
    Rotate(group, angle=2*PI, axis=Z_AXIS),
    run_time=10,
    rate_func=linear
)
# NO: mobject parameter in begin_ambient_camera_rotation
```

## Quick Reference Checklist

✓ **Dynamic Font Sizes**: Adjust based on content complexity  
✓ **Title Priority**: Always largest, never fade out  
✓ **5% Edge Buffer**: All elements respect boundaries  
✓ **Decimal Format**: `.2f` for all physics values  
✓ **Vector Colors**: Force(RED), Velocity(BLUE), Accel(ORANGE)  
✓ **Arrow Syntax**: NO tip_length, cone_height parameters  
✓ **3D Text**: `add_fixed_in_frame_mobjects()` before positioning  
✓ **3D Origin**: Center physics objects at ORIGIN  
✓ **Animation Order**: Title → Equations → Axes → Objects  
✓ **Space Management**: Fade out less important elements when crowded  
✓ **API Corrections**: Use corrected syntax for all 3D elements

## Common Error Fixes

### Error: "unexpected keyword argument 'tip_length'"
```python
# WRONG
Arrow(start, end, tip_length=0.3)

# CORRECT
arrow = Arrow(start, end)
arrow.tip.scale(0.8)
```

### Error: "unexpected keyword argument 'cone_height'"
```python
# WRONG
Arrow3D(start, end, cone_height=0.2)

# CORRECT
Arrow3D(start, end)
```

### Error: ThreeDAxes length parameter
```python
# WRONG
ThreeDAxes(length=6)

# CORRECT
ThreeDAxes(x_length=6, y_length=6, z_length=6)
```
<Physics Visualization Rule Only/>
"""

STATISTICS = """
<Statistical Visualization Rule Only>
## CRITICAL 3D TEXT RULE
**ALL text in 3D scenes MUST be fixed to frame immediately after creation:**
```python
title = Tex(r"\textbf{Title}", font_size=48)
self.add_fixed_in_frame_mobjects(title)  # Prevents rotation
title.to_edge(UP, buff=0.2)
```

## COMMON ERRORS & FIXES

| Error | Cause | Solution |
|-------|-------|----------|
| TypeError: None in play() | Passing undefined objects | Check `if obj is not None` before animating |
| Text rotates in 3D | Not fixed to frame | Use `add_fixed_in_frame_mobjects(text)` |
| ThreeDCamera animate error | Camera isn't a Mobject | Use `self.move_camera()` or `self.camera.frame.animate` |
| Title overlaps chart | Chart too large | Scale chart or show title last |
| font_size in axis labels | Method doesn't accept it | Create `Tex("label", font_size=32)` first |
| Bars exceed frame | No scaling | Scale data to fit `max_height` |

## FRAME BOUNDS & SAFE ZONES

```python
# Frame dimensions
frame_w, frame_h = 14.22, 8.0
safe_x = (-7.0, 7.0)
safe_y = (-3.5, 3.5)

# Chart area (70% width, 60% height)
chart_w = frame_w * 0.7  # ~10
chart_h = frame_h * 0.6  # ~4.8

# Safe corner positions for 3D text
title.to_edge(UP, buff=0.2)           # Top center
legend.to_corner(UR, buff=0.4)        # Top right
x_label.to_corner(DL, buff=0.5)       # Bottom left
y_label.to_corner(DR, buff=0.5)       # Bottom right
z_label.to_edge(LEFT, buff=0.5).shift(UP*1.5)  # Left middle
```

## ANIMATION SEQUENCE

### Simple Scenes (< 5 elements)
1. Title first → 2. Axes/Chart → 3. Labels → 4. Legend

### Complex Scenes (> 5 elements)
1. Chart first (no title) → 2. Progressive data reveal → 3. Fade old elements → 4. Title last (if space)

### 3D Scenes
1. Set camera → 2. Title (fixed) → 3. Axes → 4. Labels (fixed, corners) → 5. Data (progressive) → 6. Legend (fixed) → 7. Rotate

## OBJECT CREATION RULES

**WRONG:**
```python
rect = Rectangle(width=2, height=1, fill_opacity=0.7)  # ❌
```

**CORRECT:**
```python
rect = Rectangle(width=2, height=1)
rect.set_fill(BLUE, opacity=0.7)
rect.set_stroke(WHITE, width=2)
```

## 📊 2D CHART TEMPLATES

### Bar Chart
```python
def create_bar_chart(data):
    max_height = frame_h * 0.6 * 0.8
    scale = max_height / max(data)
    
    bars = VGroup()
    for i, val in enumerate(data):
        bar = Rectangle(width=0.8, height=val*scale)
        bar.move_to([i*1.2, val*scale/2, 0])
        bar.set_fill(BLUE, opacity=0.7)
        bar.set_stroke(WHITE, width=2)
        bars.add(bar)
    
    bars.move_to([0, -0.3, 0])
    return bars
```

### Scatter Plot
```python
def create_scatter(x_data, y_data):
    axes = Axes(
        x_range=[min(x_data)*0.9, max(x_data)*1.1],
        y_range=[min(y_data)*0.9, max(y_data)*1.1],
        x_length=frame_w * 0.6,
        y_length=frame_h * 0.5
    )
    axes.move_to([0, -0.3, 0])
    
    point_size = max(0.05, min(0.15, 1.0/len(x_data)))
    points = VGroup(*[Dot(axes.c2p(x,y), radius=point_size) 
                      for x,y in zip(x_data, y_data)])
    return axes, points
```

## 3D VISUALIZATION TEMPLATE

```python
class Scene3D(ThreeDScene):
    def construct(self):
        self.camera.background_color = BLACK
        self.set_camera_orientation(phi=70*DEGREES, theta=-45*DEGREES, distance=10)
        
        # 1. TITLE (fixed to frame)
        title = Tex(r"\textbf{3D Visualization}", font_size=52)
        self.add_fixed_in_frame_mobjects(title)
        title.to_edge(UP, buff=0.2)
        
        # 2. AXES
        axes = ThreeDAxes(
            x_range=[0, 10, 2], y_range=[0, 10, 2], z_range=[0, 10, 2],
            x_length=6, y_length=6, z_length=5
        )
        
        # 3. AXIS LABELS (fixed to frame, positioned in corners)
        x_label = Tex(r"X Axis", font_size=36, color=BLUE)
        y_label = Tex(r"Y Axis", font_size=36, color=BLUE)
        z_label = Tex(r"Z Axis", font_size=36, color=RED)
        
        self.add_fixed_in_frame_mobjects(x_label, y_label, z_label)
        x_label.to_corner(DL, buff=0.5)
        y_label.to_corner(DR, buff=0.5)
        z_label.to_edge(LEFT, buff=0.5).shift(UP*1.5)
        
        # 4. DATA POINTS
        points = self.create_3d_points(axes)
        
        # 5. LEGEND (fixed to frame)
        legend = self.create_legend()
        self.add_fixed_in_frame_mobjects(legend)
        legend.to_corner(UR, buff=0.4)
        
        # 6. ANIMATE
        self.play(Write(title))
        self.play(Create(axes))
        self.play(Write(x_label), Write(y_label), Write(z_label))
        self.play(LaggedStart(*[GrowFromCenter(p) for p in points], lag_ratio=0.05))
        self.play(FadeIn(legend))
        
        # 7. CAMERA ROTATION
        self.begin_ambient_camera_rotation(rate=0.15)
        self.wait(5)
        self.stop_ambient_camera_rotation()
    
    def create_3d_points(self, axes):
        import numpy as np
        data = np.random.randn(20, 3) * 2 + 5
        points = VGroup()
        for point in data:
            sphere = Sphere(radius=0.15)
            sphere.move_to(axes.c2p(*point))
            sphere.set_color(BLUE)
            sphere.set_opacity(0.8)
            points.add(sphere)
        return points
    
    def create_legend(self):
        return VGroup(
            VGroup(
                Circle(radius=0.15, fill_opacity=0.8).set_color(BLUE),
                Tex(r"Data Points", font_size=28)
            ).arrange(RIGHT, buff=0.3)
        )
```

## CAMERA CONTROLS (3D)

```python
# Set initial position
self.set_camera_orientation(phi=70*DEGREES, theta=-45*DEGREES, distance=10)

# Animate camera movement
self.move_camera(phi=60*DEGREES, theta=30*DEGREES, run_time=2)

# Alternative: Using frame
self.play(self.camera.frame.animate.set_euler_angles(theta=-30*DEGREES, phi=60*DEGREES))

# Ambient rotation
self.begin_ambient_camera_rotation(rate=0.1)
self.wait(5)
self.stop_ambient_camera_rotation()

# Zoom
self.move_camera(distance=5, run_time=2)  # Zoom in
```

## VALIDATION & DEBUGGING

```python
def validate_scene(elements):
    # "Check all elements fit within safe bounds"
    for elem in elements:
        if elem is None:
            raise ValueError("Element is None")
        
        left, bottom, _ = elem.get_corner(DOWN + LEFT)
        right, top, _ = elem.get_corner(UP + RIGHT)
        
        if not (-7.0 <= left <= 7.0) or not (-7.0 <= right <= 7.0):
            raise ValueError(f"Element outside X bounds: {left}, {right}")
        if not (-3.5 <= bottom <= 3.5) or not (-3.5 <= top <= 3.5):
            raise ValueError(f"Element outside Y bounds: {bottom}, {top}")
```

## PROGRESSIVE REVEAL PATTERN

```python
def manage_complex_data(self, data_elements):
    # "Handle scenes with many elements"
    # Show first batch
    for elem in data_elements[:5]:
        self.play(Create(elem), run_time=0.2)
    
    # Fade and show remaining
    if len(data_elements) > 5:
        for i in range(5, len(data_elements), 5):
            self.play(FadeOut(VGroup(*data_elements[i-5:i])))
            for elem in data_elements[i:i+5]:
                self.play(Create(elem), run_time=0.2)
```

## BEST PRACTICES CHECKLIST

### 2D Scenes
- Calculate chart dimensions (70% width, 60% height)
- Position title at top with 0.3 buff
- Center chart considering title space
- Add legend in corner with 0.5 buff
- Validate bounds before rendering
- Use progressive reveal for > 10 elements

### 3D Scenes
- Set camera orientation first
- Fix all text to frame immediately
- Position text in safe corners (DL, DR, UR, LEFT)
- Maintain 1-unit separation from 3D objects
- Use progressive reveal for data
- Test camera rotation
- Never use `self.camera.animate`

### Animation
- Check for None objects before `play()`
- Use `LaggedStart` for multiple similar elements
- Set `run_time` proportional to complexity
- Add `wait()` at end for final view
- Fade out old content when adding new

## GOLDEN RULES

1. **3D text = Fixed to frame** (`add_fixed_in_frame_mobjects`)
2. **Text in corners** (UR, DL, DR for 3D labels)
3. **Check before animating** (`if obj is not None`)
4. **Scale to fit** (respect frame bounds)
5. **Progressive reveal** (fade old, show new)
6. **Priority order** (Data > Axes > Legend > Title)
7. **Camera first** (set orientation before objects)
8. **Style after creation** (`.set_fill()`, not constructor)
9. **Validate bounds** (x: ±7, y: ±3.5)
10. **Test rotation** (ensure text doesn't interfere)

<Statistical Visualization Rule Only/>
"""