from manim import *

class KadaneAlgorithmScene(Scene):
    def construct(self):
        # Array and initial variables
        arr = [-2, 1, -3, 4, -1, 2, 1, -5, 4]
        max_current = arr[0]
        max_global = arr[0]

        # Create visual array as squares with numbers
        squares = VGroup(*[
            Square(side_length=1).set_fill(WHITE, opacity=0.5).set_stroke(BLACK, 2)
            for _ in arr
        ]).arrange(RIGHT, buff=0.1).to_edge(UP)

        numbers = VGroup(*[Text(str(x)) for x in arr])
        for sq, num in zip(squares, numbers):
            num.move_to(sq.get_center())

        self.play(*[Create(sq) for sq in squares], *[Write(num) for num in numbers])
        self.wait(1)

        # Initial step text
        step_text = Text(f"max_current = {max_current}, max_global = {max_global}").next_to(squares, DOWN)
        self.play(Write(step_text))
        self.wait(1)

        # Iterate through array
        for i in range(1, len(arr)):
            prev_max_current = max_current
            max_current = max(arr[i], max_current + arr[i])
            max_global = max(max_global, max_current)

            # Highlight current element
            highlight = squares[i].copy().set_fill(YELLOW, opacity=0.5)
            self.play(FadeIn(highlight, scale=1.2))

            # Update step text
            step_text_new = Text(
                f"Step {i}: max_current = max({arr[i]}, {prev_max_current}+{arr[i]}) = {max_current}, "
                f"max_global = {max_global}"
            ).next_to(squares, DOWN)
            self.play(ReplacementTransform(step_text, step_text_new))
            step_text = step_text_new
            self.wait(1)

            # Remove highlight
            self.play(FadeOut(highlight))

        # Highlight the final maximum subarray (indices 3 to 6)
        final_highlight = VGroup(*[squares[j].copy().set_fill(GREEN, opacity=0.5) for j in range(3, 7)])
        self.play(FadeIn(final_highlight, scale=1.2))
        final_text = Text("Maximum Subarray Sum = 6 (from [4, -1, 2, 1])").next_to(squares, DOWN)
        self.play(Write(final_text))
        self.wait(3)
