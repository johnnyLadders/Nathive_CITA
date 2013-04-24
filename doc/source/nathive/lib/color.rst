color
=====


class Color
-----------


.. method:: Color.__init__()

   Create the color management object at program start. 


.. method:: Color.set_color_from_rgb(rgb)

   Set the foreground color from rgb values. 

   | ``rgb: Python 3-item list with values from 0 to 255.``


.. method:: Color.set_color_from_hsv(hsv)

   Set the foreground color from hsv values. 

   | ``hsv: Python 3-item list with values from 0 to 255.``


.. method:: Color.set_color_from_hex(hexa)

   Set the foreground color from an hexadecimal string. 

   | ``hexa: A string of six chars defining a color in hexadecimal format.``


.. method:: Color.set_rgb_component(value, index)

   Compose a new rgb color by changing one of its component, then set the foreground color with the new rgb values. 

   | ``value: The new component value as int from 0 to 255.``
   | ``index: The component to change as int from 0(red) to 2(blue).``


.. method:: Color.set_hsv_component(value, index)

   Compose a new hsv color by changing one of its component, then set the foreground color with the new hsv values. 

   | ``value: The new component value as int.``
   | ``index: The component to change as int from 0(hue) to 2(value).``


.. method:: Color.set_hex(hexa)

   Evaluate an hexadecimal string and set the foreground color. 

   | ``hexa: A valid hexadecimal string of six chars.``


.. method:: Color.update_external()

   Call every function in the todo stack. 


.. method:: Color.clear()

   Restore the color to defaults, just black. 