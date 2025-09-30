I want to create an application to create color ramps. Its called "Color Ramp". A color ramp is
defined by 5 RGB colors which define a color transition from the first color to the last. The
application has a current color ramp which, by default, is displayed as a table. The color ramp can
be edited or reset to the default. RBG colors are edited in decimal. The color ramp is rendered in a
rectangle below the color ramp display. From left to right, render a a two-pixel-wide rectangle. The
color of the rectangle is determined by the middle-point of the pixel on the rectangle. The
left-most pixel is the first color ramp color. The right-most pixel is the last color ramp color.
The color of the first 1/5 of pixels is determined by interpolating the RGB values from color 1 to
color 2. The color of the next 1/5 of pixels is determined by interpolating the RGB values of color
2 and color 3.
