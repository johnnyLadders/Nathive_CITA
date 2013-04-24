tabs
====


class Tabs
----------


.. method:: Tabs.__init__(parent)

   Create notebook at program start. 

   | ``parent: Parent widget.``


.. method:: Tabs.switched(widget, child, index)

   Callback function when a tab is selected. 

   | ``widget: Call widget.``
   | ``child: Widget contained in selected tab.``
   | ``index: Int index of selected tab.``


.. method:: Tabs.reordered(widget, child, index)

   Callback function when a tab is reordered, 

   | ``widget: all widget.``
   | ``child: unused widget contained in selected tab.``
   | ``index: Int index of selected tab.``


.. method:: Tabs.update_title(document)

   Update the tab title. 

   | ``document: The document instance related with the tab.``


.. method:: Tabs.update_all_titles()

   Update all tab titles. 


.. method:: Tabs.short_title(title)

   Return a shortest version for tab title based on config rule. 

   | ``title: The title string to short.``
   | ``RETURNS: A shortest version of title or the same if not exceed.``


.. method:: Tabs.append(document)

   Append the given document as a new tab in the notebook. 

   | ``document: A document instance to append.``