document
========


class Document
--------------


.. method:: Document.__init__(path, width=0, height=0)

   Create a document instance from file or totally new. 

   | ``path: Path of the requested image.``
   | ``width: If no path given, width of new document.``
   | ``height: If no path given, height of new document.``


.. method:: Document.configure(width, height)

   .. warning:: no doctring or additional documentation, too bad.


.. method:: Document.set_path(path)

   Set a new path for the document, usually when is saved in other site. 

   | ``path: The new path, must be absolute.``


.. method:: Document.set_mime_from_format(format)

   Set a new mime type converting the passed format string. 

   | ``format: File format string like 'png'.``


.. method:: Document.set_dimensions(width, height)

   .. warning:: no doctring or additional documentation, too bad.


.. method:: Document.export(path, format, quality=None)

   .. warning:: no doctring or additional documentation, too bad.