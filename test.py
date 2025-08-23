from manim import *
import numpy as np

class FourierSeriesApprox(Scene):
    def construct(self):
        # Axes
        axes = Axes(
            x_range=[-2*PI, 2*PI, PI/2],
            y_range=[-1.5, 1.5, 0.5],
            axis_config={"color": WHITE},
        )
        labels = axes.get_axis_labels(x_label="x", y_label="f(x)")
        self.play(Create(axes), Write(labels))

        # Original square wave (target function)
        def square_wave(x):
            return 1 if (x % (2*PI)) < PI else -1

        square_graph = axes.plot(lambda x: square_wave(x), color=GRAY)
        self.play(Create(square_graph))

        # Fourier series function
        def fourier_series(x, n_terms):
            result = 0
            for n in range(1, n_terms+1, 2):  # odd terms only
                result += (4/PI) * (1/n) * np.sin(n*x)
            return result

        # Term counts to show
        term_counts = [1, 3, 5, 10]
        colors = [BLUE, GREEN, YELLOW, RED]

        # Animate successive approximations
        for n, c in zip(term_counts, colors):
            approx_graph = axes.plot(lambda x: fourier_series(x, n), color=c)
            label = Tex(f"N = {n} terms").to_corner(UL).scale(0.7)

            self.play(Create(approx_graph), Write(label))
            self.wait(2)
            self.play(FadeOut(label))

        self.wait(3)
