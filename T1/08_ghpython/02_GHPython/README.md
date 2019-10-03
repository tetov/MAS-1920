# Rhinocommon / Grasshopper / GHPython

## Web Resources

* [Essential Mathmatics for Computational Design](https://www.rhino3d.com/download/rhino/6/essentialmathematics/)
* [Rhino Developer Docs - Guides](https://developer.rhino3d.com/guides/)
* [Rhino API (Application Programming Interface)](https://developer.rhino3d.com/api/RhinoCommon/html/R_Project_RhinoCommon.htm)
* [RhinoPython 101 Primer](https://www.rhino3d.com/download/IronPython/5.0/RhinoPython101)
* [Grasshopper Tutorials](https://www.grasshopper3d.com/page/tutorials-1)

## Scripting in Rhino

Rhino uses Python version 2.7. More specifically: it uses IronPython which brings together the Python langauge and the .NET framework. A disadvantage of IronPython is that it cannot be used in a straightforward way with plugins such as *matplotlib, numpy or scipy*. 

## RhinoCommon

RhinoCommon is a crossplatform SDK (Software Development Kit) that can be used from within Windows, Mac, Grasshopper etc. The 'common'part of the name means that it can be used across Rhino platforms. It is a low-level programming environment which is based on the .NET framework that is underlying to Rhino. It gives you full access to the .NET framework, meaning you are able to access all of Rhino's functions.

![Rhino Structure](https://developer.rhino3d.com/images/rhino-technology-overview-01.png)

## RhinoScriptSyntax

RhinoScriptSyntax is a module which is written as a Python implementation of RhinoScript. If you are familiar with RhinoScript then this module will be familar to you. Many (but not all) functions of Rhino can easily be accessed through this module. 