if __name__ == "__main__":
	import os
	import sys
	os.chdir(os.path.split(os.path.realpath(sys.argv[0]))[0])
	# The script won't work unless the file is run in a directory with
	# extension folders.
	import yaml

	from contextdocparser import ContextDocParser
	from cascadingmenumaker import CascadingMenuMaker
	
	condocp = ContextDocParser(open(sys.argv[1],'r'),os.path.realpath(__file__))
	if sys.argv[2] == "install":
		condocp.install()
		sys.exit(0)
	elif sys.argv[2] == "remove":
		condocp.remove()
		sys.exit(0)
	elif sys.argv[2] == "run":
		condocp.run()
		casman = CascadingMenuMaker(condocp.out,condocp.documentObject)