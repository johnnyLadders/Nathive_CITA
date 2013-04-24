openraster
==========


class OpenRaster
----------------


.. method:: OpenRaster.__init__(path, mode='r')

   Create a new OpenRaster instance pointing to a disk location. 

   | ``path: File absulute location.``
   | ``mode: Read or write mode as unique char string.``


.. method:: OpenRaster.check()

   Check if the current path is a valid openraster file. 


.. method:: OpenRaster.get_size()

   Retrieve the openraster file width and height. 

   | ``RETURNS: A tuple with the width and height.``


.. method:: OpenRaster.load(document)

   Load the openraster file contents into the given document. 

   | ``document: A document object, usually empty.``


.. method:: OpenRaster.save(document)

   Dump the given document contents to a new openraster file, this operation will overwrite files in the current path. 

   | ``document: A document object to dump.``