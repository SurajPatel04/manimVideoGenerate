from manim import *
import numpy as np
from scipy.special import zeta

class RiemannZeta3D(ThreeDScene):
    def construct(self):
        """
        Creates a 3D visualization of the Riemann zeta function's magnitude,
        highlights its zeros on the critical line, and animates camera movement.
        """
        # 1. Setup Axes
        axes = ThreeDAxes(
            x_range=[-20, 20, 5],
            y_range=[-20, 20, 5],
            z_range=[0, 4, 1],
            x_length=12,
            y_length=12,
            z_length=5,
        )
        x_label = axes.get_x_axis_label(Tex("Im(s)"), direction=RIGHT) # Imaginary part on x-axis
        y_label = axes.get_y_axis_label(Tex("Re(s)"), direction=UP)    # Real part on y-axis
        z_label = axes.get_z_axis_label(Tex("|ζ(s)|"), direction=OUT)
        axis_labels = VGroup(x_label, y_label, z_label)

        # Title for the animation
        title = Tex("The Riemann Zeta Function |ζ(s)| in the Complex Plane").to_corner(UL)
        self.add_fixed_in_frame_mobjects(title)

        # 2. Define the Zeta Function Surface
        def zeta_func(x, y):
            # Complex number s = y + ix (mapping Re to y-axis, Im to x-axis)
            s = y + 1j * x
            # Calculate the magnitude of zeta(s)
            # Clip the value to avoid extreme peaks for better visualization
            return np.clip(np.abs(zeta(s)), 0, 4)

        surface = Surface(
            lambda u, v: axes.c2p(u, v, zeta_func(u, v)),
            u_range=[-20, 20],
            v_range=[-2, 2], # Focusing on the interesting strip
            resolution=(100, 32),
            fill_opacity=0.8,
            checkerboard_colors=[BLUE_D, BLUE_E],
        )

        # 3. Define the Critical Line and Zeros
        # The critical line is where Re(s) = 0.5
        critical_line = DashedLine(
            start=axes.c2p(-20, 0.5, 0),
            end=axes.c2p(20, 0.5, 0),
            color=RED,
            stroke_width=6,
        )
        critical_line_label = Tex("Critical Line (Re(s) = 0.5)", color=RED).scale(0.7)
        critical_line_label.next_to(axes.c2p(0, 0.5, 1.5), OUT, buff=0.2)
        
        # First three non-trivial zeros (approximate values)
        zeros_coords = [
            14.135,
            21.022,
            25.011,
        ]
        
        zero_points = VGroup()
        zero_labels = VGroup()

        for i, im_val in enumerate(zeros_coords):
            # Create a sphere at the zero's location on the critical line
            point = Sphere(
                center=axes.c2p(im_val, 0.5, 0),
                radius=0.15,
                color=YELLOW,
                fill_opacity=1
            )
            # Create a label for the zero
            label = MathTex(f"z_{i+1}", color=YELLOW).scale(0.8)
            label.next_to(point, OUT, buff=0.3)
            
            zero_points.add(point)
            zero_labels.add(label)

        # 4. Set Initial Camera Position
        self.set_camera_orientation(phi=75 * DEGREES, theta=15 * DEGREES, zoom=0.75)

        # 5. Animation Sequence
        self.play(Write(title))
        self.play(Create(axes), Write(axis_labels), run_time=2)
        self.wait()

        self.play(
            Create(surface),
            Create(critical_line),
            Write(critical_line_label),
            run_time=4
        )
        self.wait()

        self.play(
            LaggedStart(*[GrowFromCenter(p) for p in zero_points]),
            LaggedStart(*[Write(l) for l in zero_labels]),
            run_time=3,
        )
        self.wait()

        # Begin ambient rotation
        self.begin_ambient_camera_rotation(rate=0.1, about="phi")
        self.wait(5)
        
        # Dynamically zoom into the first zero
        self.play(
            self.camera.frame.animate.move_to(zero_points[0].get_center()).set(width=10),
            run_time=4,
            animation_config={"easing": ease_in_out_sine"}
        )
        self.wait(5)

        # Pan and zoom to the third zero
        self.play(
            self.camera.frame.animate.move_to(zero_points[2].get_center()).set(width=12),
            run_time=5,
            animation_config={"easing": ease_in_out_sine"}
        )
        self.wait(5)

        # Zoom out to see the whole scene again
        self.play(
            self.camera.frame.animate.move_to(ORIGIN).set(width=30),
            run_time=4
        )
        self.wait(5)
        
        self.stop_ambient_camera_rotation()
        self.wait(2)