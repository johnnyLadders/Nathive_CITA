Project Contents:
	Nathive_CITA - My modified version of the project
		*This Can also be found at my github page (jhhegler)

	original source - A directory containing the original Nathive project

		nathive-0.924.tgz - The Archive Downloaded From the Nathive
				    website, containing the project source		
		nathive - An unarchived directory containing the original
			  project source

	README.txt - This File

	Note:I have not been able to successfully build or run nathive
	on any system other than Linux.  

Dependencies:
	There are several dependencies, all of which are sub/co-dependencies
	of python-scipy.  So, if you install scipy, nathive will work. If
	you're reading this from my virtual box Ubuntu, I've already installed
	scipy.  Otherwise, if you'd like to install scipy on Ubuntu:
		
		"sudo apt-get install python-scipy"
	
	To install scipy on other systems, you'll need to follow the 
	instructions on the scipy website.

Building Nathive:
	From inside of top level directory(Hegler_Capstone):
		
		To Build my Capstone Version of Nathive, call:
			$ cd Nathive_CITA
			$ make

		To Build the unmodified version of native, call:
			$ cd original\ source/nathive
			$ make

Running Nathive:
	Once the cython and c libraries have built successfully, call:

		$ python nathive.py


Generating Diffs:
	The Main Source Files that I edited were:
		Brush.py -- (nathive.plugins)
		Layer.py -- (nathive.lib)
		Brush.cy -- (nathive.plugins)
		Core.cy --- (nathive.lib)
		Main.py --- (nathive.gui)
		
	The Source Files that I created are:
		colorDictionary.py -- (nathive.plugins)

	To generate diffs for these files, call the following commands from
	the top directory (Hegler_Capstone)

	Brush.py:
		diff Nathive_CITA/nathive/plugins/brush.py original\ source/nathive/nathive/plugins/brush.py

	Layer.py: 
		diff Nathive_CITA/nathive/lib/layer.py original\ source/nathive/nathive/lib/layer.py

	Brush.cy:
		diff Nathive_CITA/nathive/plugins/brush.cy original\ source/nathive/nathive/plugins/brush.cy

	Core.cy:
		diff Nathive_CITA/nathive/lib/core.cy original\ source/nathive/nathive/lib/core.cy

	Gui Main:
		diff Nathive_CITA/nathive/gui/main.py original\ source/nathive/nathive/gui/main.py

	ColorDictionary.py
		Since Color Dictionary is a new file you cannot diff it with the
		original.  However, Color Dictionary is an extension of another
		class called colorBar.py.  To generate the diff between color
		dictionary and colorbar, call:
			$diff Nathive_CITA/nathive/gui/colorDictionary.py original\ source/nathive/nathive/gui/colorbar.py


