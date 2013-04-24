#!/usr/bin/env python
#coding=utf-8

# Nathive (and this file) is free software: you can redistribute it and/or
# modify it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or newer.
#
# You should have received a copy of the GNU General Public License along with
# this file. If not, see <http://www.gnu.org/licenses/>.


import gtk

from nathive.gui.multiwidget import *


class ColorDictionary(object):
    """Define colorbar instance."""

    def __init__(self, parent):
        """Create the colorbar."""
        
        self.parent = parent

        # Colorbar properties.
        self.vbox = gtk.VBox(False, 0)
        self.vbox.set_size_request(100, False)
        self.vbox.set_border_width(5)
        self.name = "Color Dictionary"
        
        # Color Switch Fields
        self.toBeReplaced = ""
        self.newColor = ""

        # Get palette.
        self.palette = self.getpalette()

        # Put colors in palette.
        for color in self.palette:
            self.item(color)

        # Pack colorbar into parent widget and show.
        parent.pack_start(self.vbox, False, False, 0)
        self.vbox.show_all()


    def getpalette(self):
        """Get palette from file, return Python list."""

        palette = open('%s/colorDictionary.pal' % main.palpath).readlines()
        palette = [x.rstrip() for x in palette]
        return palette


    def item(self, hexcolor):
        """Put a color in the colorbar.
        @hexcolor: hexadecimal color like 57ABFF."""

        eventbox = gtk.EventBox()
        eventbox.set_size_request(20, False)
        color = gtk.gdk.color_parse('#' + hexcolor)
        eventbox.modify_bg(gtk.STATE_NORMAL, color)
        eventbox.connect('button-press-event', self.clicked, hexcolor)
        self.vbox.pack_start(eventbox, True, True, 0)


    def clicked(self, widget, event, hexcolor):
        
        if(event.type == gtk.gdk._2BUTTON_PRESS):
            
            #store widget to be used in response
            self.callingWidget = widget

            # Create dialog.
            self.dialog = gtk.Dialog("Replace #" + str(hexcolor))
            self.dialog.set_modal(True)
            self.dialog.set_resizable(False)
            self.box = gtk.VBox(False, 5)
            self.box.set_border_width(5)
            self.dialog.vbox.pack_start(self.box)

            #set the clicked hexColor "toBeReplaced"
            self.toBeReplaced = hexcolor

            #set new color to old color incase they don't change it
            #this will prevent value errors from being thrown
            self.newColor = hexcolor

            #Add color previews


            #color widget
            self.colorwidget = gtk.HBox(True, 0)

            #old label
            oldLabel = gtk.Label("Old:")
            oldLabel.set_alignment(0, 0.5)

            #old color frame
            self.oldColorframe = gtk.Frame()
            self.oldColorbox = gtk.EventBox()
            self.oldColorbox.set_size_request(40, 40)

            ##set old Color
            newGTKColor = gtk.gdk.color_parse('#' + self.toBeReplaced)
            self.oldColorbox.modify_bg(gtk.STATE_NORMAL, newGTKColor)
            self.oldColorframe.add(self.oldColorbox)

            #new label
            newLabel = gtk.Label("New:")
            newLabel.set_alignment(0, 0.5)

            #new color frame
            self.newColorframe = gtk.Frame()
            self.newColorbox = gtk.EventBox()
            self.newColorbox.set_size_request(40, 40)

            ##set new Color
            newGTKColor = gtk.gdk.color_parse('#' + self.toBeReplaced)
            self.newColorbox.modify_bg(gtk.STATE_NORMAL, newGTKColor)
            self.newColorframe.add(self.newColorbox)


            #pack dialog box
            #old
            self.colorwidget.pack_start(oldLabel, False, False, 0)
            self.colorwidget.pack_start(self.oldColorframe, False, False, 0)
            #new
            self.colorwidget.pack_start(newLabel, False, False, 0)
            self.colorwidget.pack_start(self.newColorframe, False, False, 0)
            self.box.pack_start(self.colorwidget, False, False, 0)

            #Create New Hex Color Input Box
            self.color_hex = MultiWidgetEntry(
                self.box,
                _('New Hex Color'),
                6,
                hexcolor,
                self.updateNewColor)


            # Connect.
            self.dialog.connect('response', self.response)
            self.dialog.connect('destroy', lambda x: self.quit())

            # Buttons (auto-connected by response).
            self.dialog.add_button('gtk-cancel', 1)
            self.dialog.add_button('Remove', 3)
            self.dialog.add_button('Replace', 2)

            # Show.
            self.dialog.show_all()
        else:
            
            #set project main color to new color
            main.color.set_hex(hexcolor)

    def addAndShowNewColor(self,hexcolor):
        """Put a color in the colorbar.
        @hexcolor: hexadecimal color like 57ABFF."""
        
        #If hexcolor isn't already in the colorDictionary
        if( not (hexcolor in self.palette)):
            #add to color Dictionary
            self.palette.append(hexcolor);
            
            #add color to color gui color palette
            self.item(hexcolor)
        
            #refresh gui
            self.vbox.show_all()
            
    def response(self, widget, response):
        """Response (buttons) callbacks.
        @widget: Call widget.
        @response: Response int."""

        if response == 1: self.quit()
        if response == 2: self.replaceColor()
        if response == 3: self.removeButton()
        
        
    def quit(self):
        """To do when the dialog is closed."""

        self.dialog.hide()
        self.dialog.destroy()
        
    def replaceColor(self):
        
        #Try except structure ensures that only valid hex values are used
        try:
            #This method will throw a value error if not valid hex
            newGTKColor = gtk.gdk.color_parse('#' + self.newColor)
            
            
            #remove old color from palette
            self.palette.remove(self.toBeReplaced)
            
            #only continue if newColor insn't already in palette
            if(not(self.newColor in self.palette)):
                #Change the Color of the Widget in the color dictionary
                self.callingWidget.modify_bg(gtk.STATE_NORMAL, newGTKColor)
                
                #Add the new color to the palette
                self.palette.append(self.newColor)
                
                #set project main color to new color
                main.color.set_hex(self.newColor)
            
            else:
                #only continue if new color is not the same as the old color
                if(self.newColor != self.toBeReplaced):
                    #only remove old color, new color is already in palette
                    self.removeSelectedColor()
                
                
            
        except:
            #Don't do anything
            pass
        
        #clear temp colors
        self.toBeReplaced = ""
        self.newColor = ""
        
        #close dialog
        self.quit()
        
    def updateNewColor(self,newColor):
        #set new color 
        self.newColor = newColor
        
        try:
            #update color box in dialog
            newGTKColor = gtk.gdk.color_parse('#' + newColor)
            self.newColorbox.modify_bg(gtk.STATE_NORMAL, newGTKColor)
        except:
            pass
    
    def removeSelectedColor(self):
        #If in palette
        if(self.toBeReplaced in self.palette):
            #remove from palette
            self.palette.remove(self.toBeReplaced)
        
        #only remove old color, new color is already in palette
        self.vbox.remove(self.callingWidget)

        #set project main color to new color
        main.color.set_hex(self.palette[-1])

        #refresh gui
        self.vbox.show_all()

    def removeButton(self):
        self.removeSelectedColor()
        #close dialog
        self.quit()
        
    def numColors(self):
        return len(self.palette)