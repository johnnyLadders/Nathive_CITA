config
======


class Config
------------


.. method:: Config.__init__()

   Set config path and load it. 


.. method:: Config.valid_attributes(plugin)

   Search all valid (config-able) attributes into instance. 

   | ``plugin: Plugin instance.``
   | ``RETURNS: String list with attribute names.``


.. method:: Config.push_from_plugin(plugin)

   .. warning:: no doctring or additional documentation, too bad.


.. method:: Config.push_from_all_plugins()

   .. warning:: no doctring or additional documentation, too bad.


.. method:: Config.push_to_plugin(plugin)

   .. warning:: no doctring or additional documentation, too bad.


.. method:: Config.save()

   Export current config to hard-drive 


.. method:: Config.get(section, option)

   Get a string from config rule. 

   | ``section: Config rule group.``
   | ``option: Config rule name.``


.. method:: Config.getint(section, option)

   Get an int from config rule. 

   | ``section: Config rule group.``
   | ``option: Config rule name.``


.. method:: Config.set(section, option, value)

   Set an string in config rule. 

   | ``section: Config rule group.``
   | ``option: Config rule name.``
   | ``value: New value to set.``


.. method:: Config.options(section)

   Returns a list of options available in the specified section. 

   | ``section: Config rule group.``