# This FUTURE file reports a side branch for project code changes.

## BRANCH ASSIGNMENT
In this branch, the work with graphics is changing, the API is simplified and the logic of initializing the graphics class is complicated (now it happens in a separate engine object).

## CHANGES:
1. [x] Working with the window is placed in a separate [class](QuantumCore/graphic/__init__.py)
2. [x] simplification of working with graphics and shortening of references to engine objects
3. [x] adding the ability to create an [interface](QuantumCore/graphic/interface.py)
4. [x] separation of service shaders and scene shaders
5. [x] Simplification of the API for working with the base class of the engine
6. [ ] separation of engine files
7. [ ] adding an improved tool to add an interface