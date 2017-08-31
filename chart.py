import cairocffi as cairo
from shapely.geometry import polygon, linestring

mm_in_an_inch = 25.4
pdf_inch = 72  # Standard "pixels" per inch in cairo is 72. Changing the scale later will correct this.
canvas_size_width = 210  # A4 in mm
canvas_size_height = 297  # A4 in mm

# Coordinates should be transformed from the OSM parser
pdf_size_width = canvas_size_width * pdf_inch / mm_in_an_inch
pdf_size_height = canvas_size_height * pdf_inch / mm_in_an_inch
surface = cairo.PDFSurface("chart.pdf", pdf_size_width, pdf_size_height)
ctx = cairo.Context(surface)

ctx.scale(pdf_inch / mm_in_an_inch, pdf_inch / mm_in_an_inch)  # Normalizing the canvas so that units are in mm

ctx.set_source_rgb(0, 0, 0)
ctx.set_line_width(1)
ctx.move_to(0, 0)
ctx.line_to(canvas_size_width, canvas_size_height)
ctx.stroke()

surface.flush()
surface.finish()
