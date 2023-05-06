import sys
import math
import time

sys.path.append("..")
from lib import LCD_1inch28
from PIL import Image
import cairo

try:
    disp = LCD_1inch28.LCD_1inch28()

    # Initialize library.
    disp.Init()
    
    # Clear display.
    disp.clear()

    # Create a new drawing surface
    surface = cairo.ImageSurface(cairo.FORMAT_RGB24, 240, 240)
    ctx = cairo.Context(surface)

    # Write "Hello World" in the centre of the drawing surface
    ctx.set_source_rgb(1, 1, 1)
    ctx.set_font_size(30.0)
    ctx.select_font_face("Quicksand",
                          cairo.FONT_SLANT_NORMAL,
                          cairo.FONT_WEIGHT_NORMAL)
    
    disp_text = "Hello World"
    disp1_text = "Hello"
    disp2_text = "World"
            
    (x, y, width, height, dx, dy) = ctx.text_extents(disp_text)

    #
    # Float the word "Hello" in from the top
    # Float the word "World" in from the bottom
    # Magic number warning...  This is just a demo!
    #
    for y in range(20, 120):
        ctx.set_source_rgb(0, 0, 0)
        ctx.rectangle(0, 0, 240, 240)
        ctx.fill()
        ctx.set_source_rgb(1, 1, 1)
        ctx.move_to(120 - width/2, y)
        ctx.show_text(disp1_text)
        ctx.move_to(200 - width/2, 238-y)
        ctx.show_text(disp2_text)
        
        # Update image on display
        disp.ShowImage(Image.frombuffer('RGBA', (240, 240), surface.get_data(), 'raw', 'RGBA', 0, 1))
    
    #
    # Give the user a couple of seconds to admire this display
    #
    time.sleep(2)
    
    #
    # Spin a square into the screen...
    # Change colour as we go.
    #
    for side in range(1, 60, 2):
        ctx.set_source_rgb(0, 0, 0)
        ctx.rectangle(0, 0, 240, 240)
        ctx.fill()
        ctx.set_source_rgb(side/100, side/100, 1-(side/100))
        ctx.rectangle(120+side, 20+side, side, side)
        ctx.fill()
        ctx.rotate(1*math.pi/180)
        
        # Update image on display
        disp.ShowImage(Image.frombuffer('RGBA', (240, 240), surface.get_data(), 'raw', 'RGBA', 0, 1))
    #
    # Give the user a few seconds to admire this display
    #
    time.sleep(5)
    
            
except IOError as e:
    print(e)    
