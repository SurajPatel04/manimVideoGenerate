from manim import *
import numpy as np

class ZoomRotateSurface(ThreeDScene):
    def construct(self):
        # Your 3D surface with z = sin(x) * cos(y)
        surface = Surface(
            lambda u, v: [u, v, np.sin(u) * np.cos(v)],
            u_range=[-PI, PI],
            v_range=[-PI, PI],
            resolution=(20, 20),
            fill_color=BLUE,
            fill_opacity=0.8,
            stroke_color=WHITE
        )

        # Add to the scene
        self.add(surface)

        # Set initial camera
        self.camera.frame.set_theta(0)
        self.camera.frame.set_phi(PI / 4)
        self.camera.frame.set_focal_distance(7)

        # Trackers for animation
        theta_tracker = ValueTracker(0)
        distance_tracker = ValueTracker(7)

        # Update function for the camera
        def update_camera(mob):
            mob.set_theta(theta_tracker.get_value())
            mob.set_phi(PI / 4)
            mob.set_focal_distance(distance_tracker.get_value())

        self.camera.frame.add_updater(update_camera)

        # Animate
        self.play(
            theta_tracker.animate
