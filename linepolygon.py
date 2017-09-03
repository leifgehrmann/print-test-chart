from cairocffi import Context


class LinePolygon:
    def __init__(self):
        self.color = None
        self.position = None
        self.line_width_initial = None
        self.line_width_delta = None
        self.line_width_final = None
        self.line_width_check_is_greater = None
        self.target_width = None

        self.set_source_rgb(0, 0, 0)
        self.set_position(0, 0)
        self.set_line_width(1, -0.01, 0.05)
        self.set_target_width(20)
        pass

    def set_source_rgb(self, red: float, green: float, blue: float) -> 'LinePolygon':
        self.color = (red, green, blue)
        return self

    def set_position(self, x: float, y: float) -> 'LinePolygon':
        self.position = (x, y)
        return self

    def set_line_width(self, initial: float, delta: float, final: float) -> 'LinePolygon':

        if (initial > final and delta >= 0) or (initial < final and delta <= 0):
            raise RecursionError('arguments with lead to recursion')

        self.line_width_initial = initial
        self.line_width_delta = delta
        self.line_width_final = final

        if initial > final:
            self.line_width_check_is_greater = True
        else:
            self.line_width_check_is_greater = False

        return self

    def set_target_width(self, width: float) -> 'LinePolygon':
        self.target_width = width
        return self

    def draw_lines(self, ctx: Context) -> None:
        self.draw(ctx, False)

    def draw_polygons(self, ctx: Context) -> None:
        self.draw(ctx, True)
        pass

    def draw(self, ctx: Context, polygon: bool) -> None:
        line_width_current = self.line_width_initial

        ctx.set_source_rgb(self.color[0], self.color[1], self.color[2])

        x_start = self.position[0]
        x_end = x_start + self.target_width
        y = self.position[1]

        while (
                    (self.line_width_check_is_greater and line_width_current > self.line_width_final) or
                    (not self.line_width_check_is_greater and line_width_current < self.line_width_final)
        ):
            ctx.set_line_width(line_width_current)
            y += line_width_current / 2

            if polygon:
                ctx.move_to(x_start, y - line_width_current / 2)
                ctx.line_to(x_end, y - line_width_current / 2)
                ctx.line_to(x_end, y + line_width_current / 2)
                ctx.line_to(x_start, y + line_width_current / 2)
                ctx.fill()
            else:
                ctx.move_to(x_start, y)
                ctx.line_to(x_end, y)
                ctx.stroke()

            # Add the white space
            y += line_width_current

            # prepare next line width
            y += line_width_current / 2
            line_width_current += self.line_width_delta

    def draw_labels(self, ctx: Context):
        ctx.set_line_width(0.1)

        line_width_current = self.line_width_initial
        text_height_room  = 0

        ctx.set_source_rgb(self.color[0], self.color[1], self.color[2])

        x = self.position[0]
        y = self.position[1]

        while (
                    (self.line_width_check_is_greater and line_width_current > self.line_width_final) or
                    (not self.line_width_check_is_greater and line_width_current < self.line_width_final)
        ):
            y += line_width_current / 2
            text_height_room += line_width_current / 2

            # Draw the line annotating the row
            if text_height_room > 2:
                ctx.move_to(x + 0, y)
                ctx.line_to(x + 2, y)
                ctx.stroke()
                self.draw_text(ctx, "{0:.2f}".format(line_width_current) + " mm", x + 3, y, 2)
                text_height_room = 0

            # Add the white space
            y += line_width_current
            text_height_room += line_width_current

            # prepare next line width
            y += line_width_current / 2
            text_height_room += line_width_current / 2
            line_width_current += self.line_width_delta

    @staticmethod
    def draw_text(ctx: Context, text: str, x: float, y: float, scale: float):
        original = ctx.get_matrix()
        ctx.translate(x, y)
        ctx.scale(scale / 10) # Default font size is 10 mm (1cm)
        ctx.show_text(text)
        ctx.set_matrix(original)
