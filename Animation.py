import cairo
from lib import LCD_1inch28
from PIL import Image, ImageDraw, ImageFont

disp = LCD_1inch28.LCD_1inch28()

# Initialize library.
disp.Init()

# Clear display.
disp.clear()

#
# Set target height and width for SmartWatch display
# in pixels
#
targetWidth = 240
targetHeight = 240

numCharizardImages = 47

while (True):
    for i in range(numCharizardImages):
        #
        # Load source image, get height and width
        # in pixels
        # NB - each frame is numbered using two digits, hence the
        # need for the format(i, '02d') call...
        # 0=use this as the leading char 
        # 2=fill to this minimum length
        #
        filename = "Charizard/frame_" + format(i,'02d') + "_delay-0.04s.png"
        #print(filename)
        
        img = cairo.ImageSurface.create_from_png(filename)
        width = img.get_width()
        height = img.get_height()
        #print("Original image width: ", width)
        #print("Original image height: ", height)

        #
        # Calculate a scaling factor - use a single value to
        # maintain aspect ratio of original image
        #
        factor = 1.0

        if width > height:
            factor = width/targetWidth
        else:
            factor = height/targetHeight
        #print("Scaling factor: ", factor)


        imgpat = cairo.SurfacePattern(img)

        #
        # Scale factor of 1.0 = 100%
        # Scale factor of 2.0 = 50%
        # Scale factor of 0.25 = 400%
        #
        scaler = cairo.Matrix()
        scaler.scale(factor, factor)
        imgpat.set_matrix(scaler)

        #set resampling filter
        imgpat.set_filter(cairo.FILTER_BEST)

        canvas = cairo.ImageSurface(cairo.FORMAT_ARGB32,targetWidth,targetHeight)
        ctx = cairo.Context(canvas)

        ctx.set_source(imgpat)
        ctx.paint()

        #canvas.write_to_png("out.png")

        disp.ShowImage(Image.frombuffer('RGBA', (240, 240), canvas.get_data(), 'raw', 'RGBA', 0, 1))

