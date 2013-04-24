menubar
=======


class Menubar
-------------


.. method:: Menubar.__init__(parent)

   Create the menubar widget and submenus. 

   | ``parent: Parent widget.``


.. method:: Menubar.set_sensitive(plugin, boolean)

   .. warning:: no doctring or additional documentation, too bad.


class Menu
----------


.. method:: Menu.__init__(menubar, parent, name, label)

   Create a menu. 

   | ``menubar: The parent menubar to append in.``
   | ``name: The menu name as string.``
   | ``label: The menu title as string.``


.. method:: Menu.dump(addlost=False)

   Filter sort list, dump to menu, and push to config. 


.. method:: Menu.istag(string)

   .. warning:: no doctring or additional documentation, too bad.


.. method:: Menu.item(plugin)

   Create a new item into menu. 

   | ``plugin: The plugin instance associated.``