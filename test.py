from manim import *
import numpy as np

class SineWaveTunnel(ThreeDScene):
    def construct(self):
        # Set initial camera orientation
        self.set_camera_orientation(phi=75 * DEGREES, theta=-45 * DEGREES)

        # Parameters for tunnel
        n_waves = 80       # number of sine rings
        wave_length = 0.5  # distance between rings
        radius = 3

        # Create sine-wave tunnel rings
        tunnel = VGroup()
        for i in range(n_waves):
            z = -i * wave_length
            ring = ParametricFunction(
                lambda t: np.array([
                    (radius + 0.5 * np.sin(3 * t + i * 0.3)) * np.cos(t),
                    (radius + 0.5 * np.sin(3 * t + i * 0.3)) * np.sin(t),
                    z
                ]),
                t_range=[0, TAU],
                color=interpolate_color(BLUE, PURPLE, i / n_waves),
                stroke_width=2
            )
            tunnel.add(ring)

        self.add(tunnel)

        # Animate tunnel moving towards camera (z shift)
        def update_tunnel(mob, dt):
            mob.shift([0, 0, 1 * dt])  # move forward
            # recycle rings to simulate infinite tunnel
            for ring in mob:
                if ring.get_center()[2] > 1:
                    ring.shift([0, 0, -n_waves * wave_length])
        
        tunnel.add_updater(update_tunnel)

        # Camera slow forward fly
        self.begin_ambient_camera_rotation(rate=0.05)  # slow rotation
        self.move_camera(phi=65*DEGREES, theta=-30*DEGREES, run_time=10)
        self.wait(10)
