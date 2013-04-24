layer
=====


class Layer
-----------


.. method:: Layer.__init__(name, path, width=0, height=0, fill=False)

   Create the layer. 


.. method:: Layer.update_pointer()

   Update the pixbuf pointer. 


.. method:: Layer.get_rowstride()

   .. warning:: no doctring or additional documentation, too bad.


.. method:: Layer.overwrite_from_path(path)

   .. warning:: no doctring or additional documentation, too bad.


.. method:: Layer.overwrite_from_data(data)

   .. warning:: no doctring or additional documentation, too bad.


.. method:: Layer.overwrite_from_pixbuf(pixbuf)

   .. warning:: no doctring or additional documentation, too bad.


.. method:: Layer.composite(mode, dest, x, y, area_x, area_y, area_w, area_h)

   Composite the given area of the layer into the destination. 

   | ``mode: Composite mode as int, 0=copy, 1=over, 2=subtractive.``
   | ``dest: Destination layer object, or layer-like object.``
   | ``x: Offset in X axis of the layer into the destination.``
   | ``y: Offset in X axis of the layer into the destination.``
   | ``area_x: Action area X coordinate (in dest scope).``
   | ``area_y: Action area Y coordinate (in dest scope).``
   | ``area_w: Action area rectangle width.``
   | ``area_h: Action area rectangle height.``


.. method:: Layer.clear(x, y, width, height)

   Clear (fill) the given area with black and opaque pixels. 