# context-menu-maker

A program that makes Windows context menus from YAML files. It's extremely 
customizable, and easy to use.

![Demo Image](https://cloud.githubusercontent.com/assets/7797957/23379972/018fb536-fd07-11e6-8fc2-0787d84af43f.png)

## Install

Just download the contents of this repository and place them in a location that
shouldn't change much. I used  `C:\Python36\Scripts\context-menu-maker`.

## Usage

### Example

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
When installed, right clicking on a folder and then clicking on a button
entitled "Settings" would produce a context menu that looks like this:

![Example Image](https://cloud.githubusercontent.com/assets/7797957/23379902/abb01cc8-fd06-11e6-9575-155931b27e4d.png)

### Syntax

#### Header

Each menu descriptor file always includes a 'name', 'title', and 'exists' 
field at the top.

##### Name

The 'name' field describes the internal name that the menu shall assume in Windows.
It's used for placing the correct registry keys. Give it a simple name 
(preferably without spaces)

##### Title

This field describes the external name (or, rather, 'verb' as given by MSDN) 
that your context menu will use. It's the name that shows up in Explorer's context menu.

##### Exists

This field is a bit more complicated. It describes if your context menu will show up 
depending on what you click on/where you click. For example:
`exists: [^allfiles]` would tell Explorer that your context menu can be triggered off
of any file (the context menu produced by right clicking a file will have your menu
on it). This does not include directories.

There are multiple things that you can put in your exists section; here they are:

| Name | Location |
|------|----------|
|^allfiles|Every file type|
|^desktop|Files on the desktop|
|^directory|Not sure, but it's in the registry. Will have to figure out what this does.|
|^directoryba|Same as above, but the background.|
|^folder|Any folder|
|^folderba|The background of an open folder window|
|^drive|Any drive|
|^driveba|The background of an open drive window|
|^everything|All of the above|

Additionally, you can specify single file types that you wish to include: 
`exists: [doc, pdf, jpg]`

##### Icon

This field provides an icon that will be shown in the context menu; note that it _cannot_
use a handler (mentioned later); it must be a pointer to a file containing the icon that 
you wish to use.

#### Handlers

Handlers is a term I've used to describe a piece of code that modifies the menu in a specific way.
Vague, I know. Here's an example:

```yaml
icon:
	handler: exefile
    executable: 'C:\Windows\System32\regedit.exe'
```

It uses a handler called "exefile", which pulls an icon from an executable file. It has different
functionality than the default icon field behavior, which normally loads an icon from a
given file.

Handlers are useful when an action is more efficiently completed by using a method other
than the default behavior.

#### Tree

Creating nested context menus is done by traversing the `tree` field in the .yml file.
Items in the tree can have actions (an action object), or another tree (a submenu). You can name them
whatever you want; the program doesn't use the name.

##### Objects

Objects in the tree have properties that must be fulfulled in order for the object
to display correctly. These properties can use certain handlers that provide resources
in certain ways. For example, an icon handler might take an icon from a provided .exe
file. Using handlers helps create better customizability and gives the user a lot of
power to create their own options easily.

In the tree, objects are defined as sub-fields:
```yaml
tree:
	object-action:
    	...
    object-submenu:
    	tree:
        	object-action-nested:
            	...
            object-submenu-nested:
            	...
```

##### Action objects

These objects are displayed as buttons in the context menu; pressing them launches an action,
as opposed to displaying a submenu. To make an action, one must add an object with a field entitled
`action`:
```yaml
tree:
	object-action:
    	action: 'C:\Windows\System32\regedit.exe'
        ...
```

An action can have a _handler_ associated with it. For more information on handlers, jump to the
"handlers" section above.

##### Submenu objects

Submenu objects are simpler. They must contain a `tree` field, which, in turn, includes other
objects, be they actions or more submenus:
```yaml
tree:
	object-submenu:
    	tree:
        	object-action:
            	...
            object-submenu:
            	tree:
                	...
```

#### Shared properties

The `title` field and the `icon` (optional) field can be used on both submenu and action objects.
The `title` field gives an external name to the object (the name that the end user will see in
the context menu), and the `icon` field obviously gives the icon to be used for that particular object.

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

To uninstall a context menu, simply run the install command and substitute 
"install" with "remove".

```cmd
C:\path_to_python\python.exe C:\path_to_main.py C:\path_to_yml_file remove
```

To test a context menu:

```cmd
C:\path_to_python\python.exe C:\path_to_main.py C:\path_to_yml_file run
```
