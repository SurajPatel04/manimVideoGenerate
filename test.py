from manim import *
import numpy as np

class Surface3DExample(ThreeDScene):
    def construct(self):
        # Set up axes
        axes = ThreeDAxes(
            x_range=[-3, 3, 1],
            y_range=[-3, 3, 1],
            z_range=[-1, 1, 0.5],
            x_length=6,
            y_length=6,
            z_length=2
        )

        # Define the surface function
        def surface_func(u, v):
            x = u
            y = v
            z = np.sin(x) * np.cos(y)
            return np.array([x, y, z])

        # Create the surface
        surface = Surface(
            surface_func,
            u_range=[-3, 3],
            v_range=[-3, 3],
            resolution=(30, 30),
            checkerboard_colors=[BLUE_D, BLUE_E],
        )

        # Add axes and surface
        self.add(axes, surface)

        # Set initial camera orientation
        self.set_camera_orientation(phi=75 * DEGREES, theta=-45 * DEGREES)

        # Animate camera rotation and zoom
        self.begin_ambient_camera_rotation(rate=0.3)  # rotates around z-axis
        self.play(self.camera.frame.animate.set(width=axes.x_length * 1.2))
        self.wait(5)  # animation duration
        self.stop_ambient_camera_rotation()

