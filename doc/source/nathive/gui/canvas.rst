canvas
======


class Canvas
------------


.. method:: Canvas.__init__(document)

   Create canvas and show it. 

   | ``document: Parent document object.``


.. method:: Canvas.allocate_cb(widget, event)

   .. warning:: no doctring or additional documentation, too bad.


.. method:: Canvas.layout_reverse()

   Reverse the layout children order, it is a way to keep the hud items over the sandbox despite the lack of a z-index system in the layout and fixed gtk widgets. 


.. method:: Canvas.enter_cb(widget, event)

   To do when the user moves the mouse into the eventbox. 

   | ``widget: Root widget.``
   | ``event: Emited event object.``


.. method:: Canvas.leave_cb(widget, event)

   To do when the user moves the mouse out of the eventbox. 

   | ``widget: Root widget.``
   | ``event: Emited event object.``


.. method:: Canvas.key_cb(widget, event)

   To do when the user press a key. 

   | ``widget: Root widget.``
   | ``event: Emited event object.``


.. method:: Canvas.button_cb(widget, event)

   To do when the user click a mouse button over the eventbox. 

   | ``widget: Root widget.``
   | ``event: Emited event object.``


.. method:: Canvas.motion_cb(widget, event)

   To do when the user move the mouse over the eventbox. 

   | ``widget: Root widget.``
   | ``event: Emited event object.``


.. method:: Canvas.release_cb(widget, event)

   To do when the user release a mouse button. 

   | ``widget: Root widget.``
   | ``event: Emited event object.``


.. method:: Canvas.handscroll(x, y)

   Perform a freehand scroll in relation to the click root position. 

   | ``x: The motion coordinate in x axis.``
   | ``y: The motion coordinate in y axis.``


.. method:: Canvas.zoom_cb(widget, event)

   To do when the user uses the mouse scroll over the eventbox. 

   | ``widget: Root widget.``
   | ``event: Emited event object.``


.. method:: Canvas.redraw(x, y, width, height, propagate=True, timing=False)

   Redraw an outdated area in the displayed image. 

   | ``x: The x coordinate of upper-left corner of rectangle.``
   | ``y: The y coordinate of upper-left corner of rectangle.``
   | ``width: The width of rectangle.``
   | ``height: The height of rectangle.``
   | ``propagate: Boolean to redraw or not the related sandbox area.``
   | ``timing: Boolean to use or not the redraw timing system.``


.. method:: Canvas.redraw_all(propagate=True)

   Redraw the displayed image completely. 

   | ``propagate: Boolean to redraw or not the related sandbox area.``


.. method:: Canvas.redraw_step(x, y, width, height, recursion=True)

   Redraw an outdated area in the displayed image step by step. 

   | ``x: The x coordinate of upper-left corner of rectangle.``
   | ``y: The y coordinate of upper-left corner of rectangle.``
   | ``width: The width of rectangle.``
   | ``height: The height of rectangle.``


.. method:: Canvas.redraw_all_step(recursion=True)

   Redraw the displayed image completely step by step. 