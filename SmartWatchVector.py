import os
import sys
from time import sleep
from datetime import datetime
from math import radians, cos, sin, pi

import logging
import spidev as SPI
sys.path.append("..")
from lib import LCD_1inch28
from PIL import Image, ImageDraw, ImageFont
import cairo

import threading


# Raspberry Pi pin configuration:
RST = 27
DC = 25
BL = 18

bus = 0 
device = 0

mode = 0

logging.basicConfig(level=logging.DEBUG)

backlight = 0

class timeHand:
    def __init__(self, handType, handStyle):
        self.handType = handType
        self.handStyle = "Simple"
        self.centre_x = 120
        self.centre_y = 120
        
        if self.handType == 'Second':
            self.length = 90
            self.start_x = self.centre_x
            self.start_y = self.centre_y
            self.unit_count = 60
            self.width = 2
            self.cap = cairo.LINE_CAP_BUTT
            self.colour = (1, 0, 0)
        elif self.handType == 'Minute':
            self.length = 95
            self.start_x = self.centre_x
            self.start_y = self.centre_y
            self.unit_count = 60
            self.width = 3
            self.end_width = 8
            self.cap = cairo.LINE_CAP_ROUND
            self.colour = (1, 1, 1)
        elif self.handType == 'Hour':
            self.length = 70
            self.start_x = self.centre_x
            self.start_y = self.centre_y
            self.unit_count = 12
            self.width = 3
            self.end_width = 8
            self.cap = cairo.LINE_CAP_ROUND
            self.colour = (1, 1, 1)
        else:
            self.length = 0
    
    def tick():
        pass
    
    def draw(self, this_context):
        stamp = datetime.now()
        if self.handType == 'Second':
            self.units = stamp.second
            #print("Seconds: " + str(self.units))
        elif self.handType == 'Minute':
            self.units = stamp.minute
            #print("Minutes: " + str(self.units))
        elif self.handType == 'Hour':
            self.units = stamp.hour
            #print("Hours: " + str(self.units))
        else:
            print("Unknown handtype: " + self.handType)
            
        angle_degrees = self.units * (360/self.unit_count)
        
        if self.handType == 'Hour':
            angle_degrees += stamp.minute/2
        elif self.handType == 'Minute':
            angle_degrees += stamp.second/12

        angle_radians = radians(angle_degrees)
        
            
        hand_end_x = self.start_x + (self.length * cos((angle_radians - pi/2)))
        hand_end_y = self.start_y + (self.length * sin((angle_radians - pi/2)))

        this_context.move_to(self.start_x, self.start_y)
        this_context.line_to(int(hand_end_x), int(hand_end_y))

        this_context.set_source_rgb(*self.colour)
        this_context.set_line_width(self.width)
        this_context.stroke()
        
        # for Hour and Minute hands, add a thicker section
        if self.handType == 'Hour' or self.handType == 'Minute':
            hand_mid_x = self.start_x + (self.length/4 * cos((angle_radians - pi/2)))
            hand_mid_y = self.start_y + (self.length/4 * sin((angle_radians - pi/2)))
            #this_context.move_to(hand_mid_x, hand_mid_y)
            #this_context.line_to(int(hand_end_x), int(hand_end_y))
            this_context.move_to(int(hand_end_x), int(hand_end_y))
            this_context.line_to(hand_mid_x, hand_mid_y)

            this_context.set_source_rgb(*self.colour)
            this_context.set_line_width(self.end_width)
            this_context.set_line_cap(self.cap)

        if self.handType == 'Second':
            hand_end_x = self.start_x + (self.length/6 * cos((angle_radians - 3*pi/2)))
            hand_end_y = self.start_y + (self.length/6 * sin((angle_radians - 3*pi/2)))
            this_context.move_to(self.start_x, self.start_y)
            this_context.line_to(int(hand_end_x), int(hand_end_y))

            this_context.set_source_rgb(*self.colour)
            this_context.set_line_width(self.width)
            
        this_context.stroke()

        
class datePanel:
    def __init__(self, dateStyle):
        self.dateStyle = "Simple"
    
    def draw(image):
        dateString = "S M T W T F S"
        draw = ImageDraw.Draw(this_image)
        pass
    
def get_kb_input(this_queue):
    while True:
        this_queue.append(sys.stdin.read(1))
        
try:
    kb_queue = []
    kb_thread = threading.Thread(target=get_kb_input, args=(kb_queue,))
    kb_thread.daemon = True
    kb_thread.start()
    
    disp = LCD_1inch28.LCD_1inch28()

    # Initialize library.
    disp.Init()
    
    # Clear display.
    disp.clear()

    surface = cairo.ImageSurface(cairo.FORMAT_RGB24, 240, 240)
    ctx = cairo.Context(surface)

    secHand = timeHand('Second', 'Simple')
    minHand = timeHand('Minute', 'Simple')
    hourHand = timeHand('Hour', 'Simple')
    
    
    while True:
        if backlight == 0:
            backlight = 1
        else:
            backlight = 0
            
        if len(kb_queue):
            print("Keyboard input received")
            char1 = kb_queue.pop(0)
            char2 = kb_queue.pop(0)
            if char1 == '1':
                mode = 1
            elif char1 == '0':
                mode = 0
            
        # Clear the drawing context - set the background to dark grey
        # Note that we treat the display as a large square, but the
        # physical display is a circle cut from that square.
        ctx.rectangle(0, 0, 240, 240)
        ctx.set_source_rgb(0.1, 0.1, 0.1)
        ctx.fill()
        
        if mode == 0:
            # Now draw the 12, 3, 6, and 9 indicators - we have to split
            # this into two sections, otherwise the Cairo fill does
            # interesting stuff...
            ctx.arc(120, 10, 4, 0, 2*pi)
            ctx.arc(120, 230, 4, 0, 2*pi)
            ctx.set_source_rgb(1, 1, 0)
            ctx.fill()
            
            ctx.arc(230, 120, 4, 0, 2*pi)
            ctx.arc(10, 120, 4, 0, 2*pi)
            ctx.set_source_rgb(1, 1, 0)
            ctx.fill()


            # Draw minute, hour, and seconds hand on image
            minHand.draw(ctx)
            hourHand.draw(ctx)
            secHand.draw(ctx)

            # draw the centre 'hub'
            ctx.arc(120, 120, 4, 0, 2*pi)
            ctx.set_source_rgb(0, 0, 1)
            ctx.fill()
            
        elif mode == 1:
            ctx.set_source_rgb(1, 1, 1)
            ctx.set_font_size(60.0)
            ctx.select_font_face("Quicksand",
                                 cairo.FONT_SLANT_NORMAL,
                                 cairo.FONT_WEIGHT_NORMAL)
            
            stamp = datetime.now()
            
            disp_text = format(stamp.hour, '02d')+":"+ \
                        format(stamp.minute, '02d')
            
            (x, y, width, height, dx, dy) = ctx.text_extents(disp_text)

            ctx.move_to(120 - width/2, 120)
            ctx.show_text(disp_text)

            ctx.set_font_size(30.0)
            disp_text = str(stamp.day)+" "+ \
                          stamp.strftime("%b")+" "+ \
                          str(stamp.year)

            (x, y, width, height, dx, dy) = ctx.text_extents(disp_text)

            ctx.move_to(120 - width/2, 160)
            ctx.show_text(disp_text)
            
            # temporary - move this to a separate class
            seconds = stamp.second
            angle_degrees = seconds * 6
            angle_radians = radians(angle_degrees)
            xp = 120 + (115*cos((angle_radians-pi/2)))
            yp = 120 + (115*sin((angle_radians-pi/2)))
            ctx.arc(xp, yp, 4, 0, 2*pi)
            red = 1
            green = 1
            blue = 0
            ctx.set_source_rgb(red, green, blue)
            ctx.fill()
            for trailer in range(59):
                red = red/1.1
                green = green/1.1
                trailer_seconds = (seconds - trailer) % 60
                angle_degrees = trailer_seconds * 6
                angle_radians = radians(angle_degrees)
                xp = 120 + (115*cos((angle_radians-pi/2)))
                yp = 120 + (115*sin((angle_radians-pi/2)))
                ctx.arc(xp, yp, 4, 0, 2*pi)
                ctx.set_source_rgb(red, green, blue)
                ctx.fill()
            

        # Update image on display
        disp.ShowImage(Image.frombuffer('RGBA', (240, 240), surface.get_data(), 'raw', 'RGBA', 0, 1))
        sleep(0.1)
        
            
except IOError as e:
    logging.info(e)    
except KeyboardInterrupt:
    disp.module_exit()
    logging.info("quit:")
    exit()