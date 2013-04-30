#!/usr/bin/env python
#coding=utf-8

# Nathive (and this file) is free software: you can redistribute it and/or
# modify it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or newer.
#
# You should have received a copy of the GNU General Public License along with
# this file. If not, see <http://www.gnu.org/licenses/>.


import gtk
import math

from nathive.lib.plugin import *
from nathive.lib.layer import Layer
from nathive.libc import brush
from nathive.gui import utils as gutils
from nathive.gui.multiwidget import *
from nathive.libc import core




class Brush(PluginTool):

    def __init__(self):

        # Subclass it.
        PluginTool.__init__(self)

        # Plugin attributes.
        self.name = 'brush'
        self.author = 'nathive-dev'
        self.icon = 'tool-brush.png'

        # Setting up the plugin.
        self.brush = None
        self.layer = None
        self.default()
        main.config.push_to_plugin(self)

        #pregenerated softness mask
        self.softnessMask = []

        # Init apply limits (left, top, right, bottom).
        self.apply = [0, 0, 0, 0]

        # Able simple overriding for subclassed plugins like eraser.
        self.composite_mode = 1
        self.color_updated_todo = main.color.updated_todo

        self.count = 0


    def enable(self):

        self.color_updated_todo.append(self.new_color)
        self.new()


    def disable(self):

        self.color_updated_todo.remove(self.new_color)
        hud = main.documents.active.canvas.hud
        hud.remove_cursor()


    def default(self):

        self.shape = 1
        self.size = 100
        self.opacity = 100
        self.soft = 100
        self.spacing = 0


    def update(self):

        self.gui_shape.set_value(self.shape)
        self.gui_size.set_value(self.size)
        self.gui_opacity.set_value(self.opacity)
        self.gui_soft.set_value(self.soft)
        self.gui_spacing.set_value(self.spacing)
        self.new()


    @property
    def color(self):
        """Redirect self.color to global color value to able
        simple overriding in subclassed plugins like eraser."""

        return main.color.rgb


    def set_then_new(self, variable, value):

        setattr(self, variable, value)
        self.new()


    def new(self):
        

        del(self.brush)
        self.brush = Layer('brush', None, self.size, self.size)
        

        brush.new(
            self.brush.pointer,
            True,
            self.shape,
            self.size,
            self.opacity,
            self.soft,
            self.color[0],
            self.color[1],
            self.color[2])
            
        #regenerate pre computed softness mask
        self.generateSoftnessMask()

        if not main.documents.active: return
        hud = main.documents.active.canvas.hud
        fixed_size = self.size - ((self.size * (self.soft/2) / 100) / 2)
        if self.shape == 0: hud.set_cursor('square', fixed_size)
        elif self.shape == 1: hud.set_cursor('circle', fixed_size)
        


    def new_color(self):
        """Change brush color with no opacity re-calculation for better
        performance at color change."""

        brush.new(
            self.brush.pointer,
            False,
            0,
            self.size,
            0,
            0,
            self.color[0],
            self.color[1],
            self.color[2])


    def button_primary(self, x, y, ux, uy):

        main.documents.active.actions.begin('layer-content')
        self.layer = main.documents.active.layers.active
        self.motion_primary(x, y, ux, uy)
        
    def motion_primary(self, x, y, ux, uy):

        # Update apply limits.
        if not self.apply[0] or x < self.apply[0]: self.apply[0] = x
        if not self.apply[1] or y < self.apply[1]: self.apply[1] = y
        if not self.apply[2] or x > self.apply[2]: self.apply[2] = x
        if not self.apply[3] or y > self.apply[3]: self.apply[3] = y

        # Set apply coordinates.
        x = x - (self.size / 2)
        y = y - (self.size / 2)

        
        #add color to color dictionary
        CD = main.gui.colorDictionary
        setItem = getattr(CD,'addAndShowNewColor')
        setItem(main.color.hex)
        
        #update pixel data
        self.updatePixData(x, y)

        # Brush.
        self.brush.composite(
            self.composite_mode,
            self.layer,
            x - self.layer.xpos,
            y - self.layer.ypos,
            x - self.layer.xpos,
            y - self.layer.ypos,
            self.brush.width,
            self.brush.height)

        # Redraw expired area.
        main.documents.active.canvas.redraw(
            x,
            y,
            self.size,
            self.size,
            True,
            True)


    def release_primary(self):

        # Calc apply area rectangle.
        area = [
            self.apply[0] - (self.brush.width/2),
            self.apply[1] - (self.brush.height/2),
            self.apply[2] + (self.brush.width) - self.apply[0],
            self.apply[3] + (self.brush.height) - self.apply[1]]

        # Apply layer offset.
        layer = main.documents.active.layers.active
        area[0] -= layer.xpos
        area[1] -= layer.ypos

        # End action and reset area vars.
        main.documents.active.actions.end(area)
        self.apply = [0, 0, 0, 0]


    def button_secondary(self, x, y, ux, uy):

        self.resizing_root = [x, y]


    def motion_secondary(self, x, y, ux, uy):

        root_x, root_y = self.resizing_root
        rel_x = root_x - x
        rel_y = root_y - y
        self.size += rel_y - rel_x
        self.resizing_root = [x, y]
        if self.size < 1: self.size = 1
        if self.size > 100: self.size = 100
        if gtk.events_pending(): return
        hud = main.documents.active.canvas.hud
        hud.create_cursor()
        hud.move_cursor(x, y)
        hud.dump_cursor()
        self.gui_size.set_value(self.size, True)


    def gui(self):

        self.box = gtk.VBox(False, 0)

        self.gui_shape = MultiWidgetToggle(
            self.box,
            _('Shape'),
            ['square', 'circle'],
            self.shape,
            lambda x: self.set_then_new('shape', x))

        gutils.separator(self.box)

        self.gui_size = MultiWidgetSpin(
            self.box,
            _('Size'),
            True,
            1,
            100,
            self.size,
            self.updateSize)

        self.gui_soft = MultiWidgetSpin(
            self.box,
            _('Smoothing'),
            True,
            0,
            100,
            self.soft,
            self.updateSoftness)

        self.gui_opacity = MultiWidgetSpin(
            self.box,
            _('Opacity'),
            True,
            1,
            100,
            self.opacity,
            self.updateOpacity)

        gutils.separator(self.box)

        self.gui_spacing = MultiWidgetCombo(
            self.box,
            _('Spacing'),
            ['not ported'],
            self.spacing,
            lambda x: None)

        return self.box
    
    def updatePixData(self, mouseX, mouseY):
        
        #foreground xOffset
        xOff = mouseX
        
        #foreground yOffset
        yOff = mouseY
        
        #foreground xEnd (must be <= layer width)
        xEnd = xOff + self.size
        xEnd = xEnd if(xEnd < self.layer.width) else self.layer.width
        
        #foreground yEnd (must be <= layer height)
        yEnd = yOff + self.size
        yEnd = yEnd if(yEnd < self.layer.height) else self.layer.height

  
        #Actual Row Number
        rowNum = 0
        
        #get Color Index
        colorIndex = main.gui.colorDictionary.palette.index(main.color.hex)
        
        #iterate through relevant pixels
        for row in range(yOff,yEnd):
            #Actual Column Number
            columnNum = 0

            for column in range(xOff,xEnd):
                
                #retrieve pre-calculated opacity
                pixelSoftness = self.getPixelSoftness(rowNum,columnNum)
                
                #handle for this column
                thisColumn = self.layer.pixData[row][column]
                
                #handle for brush opacity
                brushOpacity = self.opacity
                
                              
                
                #only add if some opacity exists
                if(pixelSoftness != 0):
                    
                    #if column not empty and last element is the same color as current
                    if((len(thisColumn) != 0) and
                        (thisColumn[-1][0] == colorIndex)):
                            
                        #handle for this colorEntry
                        thisEntry = thisColumn[-1]

                        #combine opacity
                        combinedOpacity = core.getOverAlpha(float(pixelSoftness),float(thisEntry[1]))

                        #if their combined opacities == 255 --> remove the rest of the array and add
                        if(combinedOpacity == 255):
                            thisColumn = [[colorIndex, 255, brushOpacityy/100.0]]

                        #else update old opacity
                        else:
                            thisEntry[1] = combinedOpacity
                            thisEntry[2] = (thisColumn[-1][2] + brushOpacity/100.0)
                            if(thisEntry[2] > 1.0): thisEntry[2] = 1.0


                    #else just append
                    else:
                        thisColumn.append([colorIndex,pixelSoftness, brushOpacity/100.0])

                #increment column number
                columnNum = columnNum + 1
            
            #increment row number
            rowNum = rowNum + 1
        
    def updateSoftness(self,softness):
        self.soft = int(softness)
        self.new()

    
    def updateOpacity(self,opacity):
        self.opacity = int(opacity)
        self.new()

    
    def updateSize(self,size):
        self.size = int(size)
        self.pixBufFromPixData()
        self.new()

        
        
#    def generateSoftnessMask(self):
#        #clear old mask
#        self.softnessMask = []
#                
#        for row in range(self.size):
#            
#            #Create Temporary Row To Hold Column Mask Values
#            tempRow = []
#            for column in range(self.size):
#                
#                #radius
#                radius = self.size/2.0
#                
#                #distance in columns (x)
#                distX = column - radius + 1.0
#                
#                #distance in rows (y)
#                distY = row - radius + 1.0
#                
#                #dist
#                dist = int(math.sqrt((distX ** 2) + (distY ** 2)))
#                
#                print "distance: " + str(dist)
#                print "radius: " + str(radius)
#
#                #dist = sqrt( (dist_x*dist_x) + (dist_y*dist_y) )
#
#                
#                #Calculate Softness for the relative row and column
#                #then store it in a new array (column) and append the array to
#                #the row
#                tempSoftness = brush.getSoftness(radius , dist, self.opacity, self.soft)
#                
#                if(not(tempSoftness is None)):
#                    tempSoftness = ord(tempSoftness)
#                else:
#                    tempSoftness = 0
#                    
##                #convert to float between 0 and 1
##                tempSoftness = (tempSoftness/255.0)
#                
#                #add column to row
#                tempRow.append([tempSoftness])
#                
#                
#            
#            #Append Temporary Row to softnessMask
#            self.softnessMask.append(tempRow)

    def generateSoftnessMask(self):
                
            #new layer
            tempLayer = Layer('tempLayer', None, self.size, self.size)
    
            brush.new(
            tempLayer.pointer,
            True,
            self.shape,
            self.size,
            self.opacity,
            self.soft,
            self.color[0],
            self.color[1],
            self.color[2])
            
            #get pixBuf array
            tempPixelArray = tempLayer.pixbuf.get_pixels_array()
            
            #init softnessArray
            self.softnessMask = []
            
            for row in tempPixelArray:
                tempRow = []
                for column in row:
                    tempRow.append([column[3]])
                    
                self.softnessMask.append(tempRow)
                
            
    #returns the precomputed softness for a pixels position
    def getPixelSoftness(self,row,column):
        return self.softnessMask[row][column][0]
    
    def pixBufFromPixData(self):
        pass
#        #get pixbuf array
#        pixBufArray = self.layer.pixbuf.get_pixels_array()
#        
#        for  i in range(self.brush.height):
#            for j in range(self.brush.width):
#                for k in range(3):
#                    pixBufArray[i][j][k] = 0
#                pixBufArray[i][j][3] = self.getPixelSoftness(i,j)
#                print self.getPixelSoftness(i,j) * 255
#                    
#        # Redraw expired area.
#        self.layer.pixbuf = gtk.gdk.pixbuf_new_from_array(pixBufArray, gtk.gdk.COLORSPACE_RGB, 8)
#
#        main.documents.active.canvas.redraw_all()
#        main.documents.active.actions.end([0,0,699,699])
#        
#        

    def compositeRBG(self,lowerValue,upperValue,upperValueOpacity):
        #algorithm for compositing two 8bit color channel values
        compositedChannel = (upperValueOpacity * upperValue) + ((1 - upperValueOpacity) * lowerValue)
        return compositedChannel