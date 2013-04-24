shortcuts
=========


class Shortcuts
---------------


.. method:: Shortcuts.__init__()

   Create the shortcuts manager instance. 


.. method:: Shortcuts.load_from_config()

   Load all shortcut entries from config and store it as Shortcut instances in items dict. 


.. method:: Shortcuts.save_to_config()

   .. warning:: no doctring or additional documentation, too bad.


.. method:: Shortcuts.callback_decode(callback)

   Get a shortcut callback in config format and return it as real cb. 

   | ``callback: Shortcut callback string in 'type:name' format.``
   | ``RETURNS: Real callback function.``


.. method:: Shortcuts.push()

   Update (really create each time) the GTK window shortcuts list from stored shortcut instances. 


class Shortcut
--------------


.. method:: Shortcut.__init__(key, mask, callback)

   Create the shortcut instance. 