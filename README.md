# context-menu-maker

A program that makes Windows context menus from YAML files. It's extremely 
customizable, and easy to use.

## Install

Just download the contents of this repository and place them in a location that
shouldn't change much.

## Usage

### Writing .yml context menus

Consider the following snippet:

```yaml
name: 'settings'
title: 'Settings'
exists: [^folder]
tree:
	control-panel:
    	title: 'Control Panel'
        icon:
        	handler: 'exefile'
            executable: 'control.exe'
        action: 'control.exe'
    other-options:
    	title: 'Other...'
        icon: 'C:\insert_icon_file_here.ico'
        tree:
        	reg:
            	title: 'Registry Editor'
                icon:
                	handler: 'exefile'
                    executable: 'regedit.exe'
                action: 'regedit.exe'
```
When installed, this would produce a context menu that looks like this:



### Installation
Context menus are installed once, and can always be uninstalled.

To install a context menu from a .yml file, run at an administrative command
prompt:

```cmd
C:\path_to_python\python.exe C:\path_to_main.py C:\path_to_yml_file install
```

To install the example .yml, the command would be something like this
(at least, for me):

```cmd
C:\Python36\python.exe C:\Python36\Scripts\context-menu-maker\main.py C:\Users\me\context-menus\example.yml install
```

To uninstall a .yml context menu, simply run the above command and substitute 
"install" with "remove".

```cmd
C:\path_to_python\python.exe C:\path_to_main.py C:\path_to_yml_file install
```

To test a context menu:

```cmd
C:\path_to_python\python.exe C:\path_to_main.py C:\path_to_yml_file run
```
