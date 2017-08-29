# print-test-chart
A practical test chart for testing printer resolution/accuracy/quality

The quality of printed output can be very different depending on the software and hardware used. While there are plenty of resources for testing printer alignment, I haven't found good resources for testing resolution, or other properties like aliasing.

Resolution is often measured by test charts listed in [this wikipedia article](https://en.wikipedia.org/wiki/Optical_resolution#Measuring_optical_resolution). The charts are intended to test sensors, but can also be used to crudely test printer resolution. It's a more qualitative approach to measuring the resolution rather than the quantitative DPI that a printer can claim to print.

This project generates a PDF that can be printed to analyse the resolution and other qualities or a printer. It'll cover line, polygon, text graphics.
