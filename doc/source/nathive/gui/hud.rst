hud
===


class Hud
---------


.. method:: Hud.__init__(canvas)

   Hud object initialization. 

   | ``canvas: The parent canvas object.``


.. method:: Hud.get_item(image)

   Returns the hud item object for given image. 

   | ``image: A gtk image widget.``
   | ``RETURNS: The hud item object that store the given image.``


.. method:: Hud.add(image, x=0, y=0, offset_x=0, offset_y=0)

   Create and append a basic hud item object with the given properties. 

   | ``image: A gtk image widget.``
   | ``x: Coordinate in x axis.``
   | ``y: Coordinate in y axis.``
   | ``offset_x: Correction amount in x axis.``
   | ``offset_y: Correction amount in y axis.``
   | ``RETURNS: The created hud item object.``


.. method:: Hud.add_from_name(name, x=0, y=0, offset_x=0, offset_y=0)

   Create and append a basic hud item object using the given filename. 

   | ``name: A file name with extension to load from the img folder.``
   | ``x: Coordinate in x axis.``
   | ``y: Coordinate in y axis.``
   | ``offset_x: Correction amount in x axis.``
   | ``offset_y: Correction amount in y axis.``
   | ``RETURNS: The created hud item object.``


.. method:: Hud.remove(item)

   Remove the given hud item object. 

   | ``item: Am hud item object.``


.. method:: Hud.set_cursor(shape, size)

   Configure the hud cursor properties to create it. 

   | ``shape: A string with the shape name, currently 'square' or 'circle'.``
   | ``size: Cursor real size in pixels.``


.. method:: Hud.move_cursor(x, y)

   Move the hud cursor to the given coordinates. 

   | ``x: Coordinate in x axis.``
   | ``y: Coordinate in y axis.``


.. method:: Hud.hide_cursor()

   Hide hud cursor temporally, like in handscroll. 


.. method:: Hud.show_cursor()

   Show the hud cursor again after a temporally hide. 


.. method:: Hud.remove_cursor(totally=True)

   Remove the current hud cursor, if the totally argument is given as False the hud cursor will be still configurated with the old properties and ready to be created again. 


.. method:: Hud.create_cursor()

   Create the hud cursor image (cairo based), after this the hud cursor is ready to be dumped. 


.. method:: Hud.set_area(area)

   Create the hud area image with the given area dimensions, after this the hud is ready to be dumped. 

   | ``area: Dimension rectangle as 4-item list.``


.. method:: Hud.move_area(x, y)

   Move the area to the given coordinates. 

   | ``x: Coordinate in x axis.``
   | ``y: Coordinate in y axis.``


.. method:: Hud.remove_area()

   Remove area hud item. 


.. method:: Hud.draw_circle(context, size)

   Draw a b&w circle in the given cairo context. 

   | ``context: A pycairo context object.``
   | ``size: Requested size for the circle in pixels.``


.. method:: Hud.draw_rectangle(context, width, height, offset_x=0, offset_y=0)

   Draw a b&w square in the given cairo context. 

   | ``context: A pycairo context object.``
   | ``width: Requested width for the square in pixels.``
   | ``height: Requested height for the square in pixels.``
   | ``offset_x: Initial deviation at x axis in pixels.``
   | ``offset_y: Initial deviation at y axis in pixels.``


.. method:: Hud.dump()

   Dump each basic (tracked child) hud item to sandbox. 


.. method:: Hud.dump_cursor()

   Dump the hud cursor to sandbox. 


class HudItem
-------------


.. method:: HudItem.__init__(image, x=0, y=0, offset_x=0, offset_y=0)

   Hud item object initialization. 

   | ``image: A gtk image widget.``
   | ``x: Coordinate in x axis.``
   | ``y: Coordinate in y axis.``
   | ``offset_x: Correction amount in x axis.``
   | ``offset_y: Correction amount in y axis.``


.. method:: HudItem.move(x, y)

   Set hud item new coordinates. 

   | ``x: Coordinate in x axis.``
   | ``y: Coordinate in y axis.``


.. method:: HudItem.set_display(display)

   Set the hud item display state, True to show, False to hide. until the dump process is called. 

   | ``display: New display state as boolean.``