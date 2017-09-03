import cairocffi as cairo
from shapely.geometry import polygon, linestring
from linepolygon import LinePolygon

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

lp = LinePolygon()
lp.set_position(20,20)
lp.draw_lines(ctx)
lp.set_position(40,20)
lp.draw_polygons(ctx)
lp.set_position(60,20)
lp.draw_labels(ctx)

surface.flush()
surface.finish()
