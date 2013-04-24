toolbar
=======


class Toolbar
-------------


.. method:: Toolbar.__init__(parent)

   Create toolbar and buttons. 

   | ``parent: Parent widget.``


.. method:: Toolbar.dump(addlost=False)

   Filter sort list, dump to toolbar, and push to config. 


.. method:: Toolbar.item(toolname)

   Append toolbar buttons. 

   | ``toolname: Tool name to include in toolbar.``


.. method:: Toolbar.toggled(toolname)

   Callback function when some toolbar icon is selected. 

   | ``toolname: Asociated tool name to activate.``


.. method:: Toolbar.press(widget, event)

   Callback function that catch double-clicks in any button to show the tool propierties tab in the sidebar. 

   | ``widget: Call widget.``
   | ``event: Event data instance.``


.. method:: Toolbar.colorbox_update()

   Updates colorbox color when is outdated. 