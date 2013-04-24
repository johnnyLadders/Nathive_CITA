colorbar
========


class Colorbar
--------------


.. method:: Colorbar.__init__(parent)

   Create the colorbar. 


.. method:: Colorbar.getpalette()

   Get palette from file, return Python list. 


.. method:: Colorbar.item(hexcolor)

   Put a color in the colorbar. 

   | ``hexcolor: hexadecimal color like 57ABFF.``


.. method:: Colorbar.clicked(widget, event, hexcolor)

   Callback for each color. 

   | ``widget: Callback gtkwidget.``
   | ``event: Callback gtkevent.``
   | ``hexcolor: hexadecimal color like 57ABFF.``