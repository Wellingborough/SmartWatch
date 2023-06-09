import sys

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
    
    disp_text = "Hello Mark!!"
            
    (x, y, width, height, dx, dy) = ctx.text_extents(disp_text)

    ctx.move_to(120 - width/2, 120)
    ctx.show_text(disp_text)
    
    # Update image on display
    disp.ShowImage(Image.frombuffer('RGBA', (240, 240), surface.get_data(), 'raw', 'RGBA', 0, 1))
            
except IOError as e:
    print(e)    
