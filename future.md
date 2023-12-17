# This FUTURE file reports a side branch for project code changes.

## BRANCH ASSIGNMENT
>>>>>>>  ## Future Branch
>>>>>>>  ##### game version: 0.5.5
>>>>>>>  ##### Engine version: 0.11.6

In this branch, the data structure of the model in the engine is removed and changed. Now this happens through a separate [MetaData](QuantumCore/model.py) class. In addition, the approach to storing all objects in the scene is changing.

## CHANGES:
1. [x] adding and adding to a separate data class about the camera and models
2. [x] changing the initialization of the model
3. [x] changing the fields of the model class
4. [x] changing position calculations
5. [x] changing the loading of objects into the [scene](QuantumCore/scene.py)
6. [x] changing the download of the [saves](GameData/saves) file
7. [x] changes in the approach to storing models and their abbreviations in the scene
