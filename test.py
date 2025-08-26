from manim import *

class WaveInterference(Scene):
    def construct(self):
        """
        Animates the interference of two sine waves traveling towards each other.
        It shows both constructive and destructive interference patterns.
        """
        # Layout Plan:
        # 1. A title will be placed at the top of the screen (to_edge(UP)).
        # 2. A set of axes will be centered on the screen to plot the waves.
        # 3. Two traveling sine waves will be plotted on these axes in different colors (BLUE, RED).
        # 4. A third, resultant wave (the sum of the two) will be plotted on the same axes in a distinct color (YELLOW).
        # 5. Labels for each wave type will be positioned on the top left to avoid overlap with the animation.

        # --- Scene Setup ---
        self.camera.background_color = BLACK

        title = Text("Wave Interference").to_edge(UP)
        self.play(Write(title))

        # Create axes for the waves
        axes = Axes(
            x_range=[-4 * PI, 4 * PI, PI],
            y_range=[-2.5, 2.5, 1],
            x_length=12,
            y_length=5,
            axis_config={"color": WHITE},
            x_axis_config={"numbers_to_include": np.arange(-4 * PI, 4 * PI + PI, 2*PI),
                           "numbers_with_elongated_ticks": np.arange(-4 * PI, 4 * PI + PI, 2*PI),
                           "decimal_number_config": {"num_decimal_places": 0}},
            tips=False,
        ).add_coordinates()
        
        # Add labels for axes
        y_label = axes.get_y_axis_label("Amplitude")
        x_label = axes.get_x_axis_label("Position")
        axes_labels = VGroup(x_label, y_label)

        self.play(Create(axes), Write(axes_labels))
        self.wait(1)

        # --- Wave and Animation Setup ---
        # ValueTracker to animate the progression of time
        time = ValueTracker(0)

        # Define the two traveling waves and the resultant wave
        wave1 = always_redraw(
            lambda: axes.plot(
                lambda x: np.sin(x - time.get_value()), 
                x_range=[-4 * PI, 4 * PI], 
                color=BLUE
            )
        )

        wave2 = always_redraw(
            lambda: axes.plot(
                lambda x: np.sin(x + time.get_value()), 
                x_range=[-4 * PI, 4 * PI], 
                color=RED
            )
        )
        
        resultant_wave = always_redraw(
            lambda: axes.plot(
                lambda x: np.sin(x - time.get_value()) + np.sin(x + time.get_value()),
                x_range=[-4 * PI, 4 * PI],
                color=YELLOW
            )
        )
        
        # --- Create Labels for Waves ---
        label_wave1 = MathTex(r"\sin(x - t)", color=BLUE).next_to(axes, UP, buff=0.2).align_to(axes, LEFT)
        label_wave2 = MathTex(r"\sin(x + t)", color=RED).next_to(label_wave1, RIGHT, buff=0.5)
        label_resultant = MathTex(r"\text{Resultant Wave}", color=YELLOW).next_to(label_wave2, RIGHT, buff=0.5)
        
        labels = VGroup(label_wave1, label_wave2, label_resultant)
        self.play(Write(labels))

        # Add all waves to the scene
        self.add(wave1, wave2, resultant_wave)

        # --- Animate the Interference ---
        # Animate the 'time' ValueTracker to make the waves move
        self.play(
            time.animate.set_value(8 * PI),
            run_time=10,
            rate_func=linear
        )
        self.wait(2)

        # --- Final Fade Out ---
        self.play(
            FadeOut(wave1),
            FadeOut(wave2),
            FadeOut(resultant_wave),
            FadeOut(labels),
            FadeOut(axes),
            FadeOut(axes_labels),
            FadeOut(title)
        )
        self.wait()