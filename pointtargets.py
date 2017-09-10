from cairocffi import Context
import math

class PointTargets:
    def __init__(self):
        self.color = None
        self.position = None
        self.point_diameter_initial = None
        self.point_diameter_delta = None
        self.point_diameter_final = None
        self.point_diameter_check_is_greater = None
        self.point_margin = None
        self.target_width = None

        self.set_source_rgb(0, 0, 0)
        self.set_position(0, 0)
        self.set_point_size(0.5, -0.001, 0.001)
        self.set_point_margin(1)
        self.set_target_width(5)
        pass

    def set_source_rgb(self, red: float, green: float, blue: float) -> 'PointTargets':
        self.color = (red, green, blue)
        return self

    def set_position(self, x: float, y: float) -> 'PointTargets':
        self.position = (x, y)
        return self

    def set_point_size(self, initial: float, delta: float, final: float) -> 'PointTargets':

        if (initial > final and delta >= 0) or (initial < final and delta <= 0):
            raise RecursionError('arguments with lead to recursion')

        self.point_diameter_initial = initial
        self.point_diameter_delta = delta
        self.point_diameter_final = final

        if initial > final:
            self.point_diameter_check_is_greater = True
        else:
            self.point_diameter_check_is_greater = False

        return self

    def set_point_margin(self, margin: float) -> 'PointTargets':
        self.point_margin = margin
        return self

    def set_target_width(self, width: float) -> 'PointTargets':
        self.target_width = width
        return self

    def draw_circles(self, ctx: Context) -> None:
        self.draw(ctx, False)

    def draw_squares(self, ctx: Context) -> None:
        self.draw(ctx, True)
        pass

    def draw(self, ctx: Context, square: bool) -> None:
        point_diameter_current = self.point_diameter_initial

        ctx.set_source_rgb(self.color[0], self.color[1], self.color[2])

        points_per_row = math.floor(self.target_width / self.point_margin)
        i = 0

        while (
                    (self.point_diameter_check_is_greater and point_diameter_current > self.point_diameter_final) or
                    (not self.point_diameter_check_is_greater and point_diameter_current < self.point_diameter_final)
        ):

            col = i % points_per_row
            row = math.floor(i / points_per_row)
            x = self.position[0] + col * self.point_margin + self.point_margin / 2
            y = self.position[1] + row * self.point_margin + self.point_margin / 2

            radius = point_diameter_current / 2

            if square:
                ctx.move_to(x - radius, y - radius)
                ctx.line_to(x + radius, y - radius)
                ctx.line_to(x + radius, y + radius)
                ctx.line_to(x - radius, y + radius)
                ctx.fill()
            else:
                ctx.arc(x, y, radius, 0, 2 * math.pi)
                ctx.fill()

            i += 1
            point_diameter_current += self.point_diameter_delta

    def draw_labels(self, ctx: Context) -> None:
        point_diameter_current = self.point_diameter_initial
        text_height_room = 0

        ctx.set_source_rgb(self.color[0], self.color[1], self.color[2])

        points_per_row = math.floor(self.target_width / self.point_margin)
        i = 0

        while (
                    (self.point_diameter_check_is_greater and point_diameter_current > self.point_diameter_final) or
                    (not self.point_diameter_check_is_greater and point_diameter_current < self.point_diameter_final)
        ):

            col = i % points_per_row
            row = math.floor(i / points_per_row)
            x = self.position[0] + col * self.point_margin + self.point_margin / 2
            y = self.position[1] + row * self.point_margin + self.point_margin / 2

            first_point_diameter_in_row = point_diameter_current
            last_point_diameter_in_row = point_diameter_current + self.point_diameter_delta * (points_per_row - 1)
            print(first_point_diameter_in_row)
            print(last_point_diameter_in_row)

            if text_height_room > 2:
                ctx.move_to(x + 0, y)
                ctx.line_to(x + 2, y)
                ctx.stroke()
                self.draw_text(ctx, "{0:.3f} - {1:.3f}".format(first_point_diameter_in_row, last_point_diameter_in_row) + " mm", x + 3, y, 2)
                text_height_room = 0

            i += points_per_row
            point_diameter_current += self.point_diameter_delta * points_per_row
            text_height_room += self.point_margin

    @staticmethod
    def draw_text(ctx: Context, text: str, x: float, y: float, scale: float):
        original = ctx.get_matrix()
        ctx.translate(x, y)
        ctx.scale(scale / 10) # Default font size is 10 mm (1cm)
        ctx.show_text(text)
        ctx.set_matrix(original)