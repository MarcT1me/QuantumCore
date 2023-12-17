# QuantumCore - graphic Engine
###### _Just **PyQC**_
\
ㅤ
Game Engine in Python ( **[Pygame](https://pypi.org/project/pygame/), [OpenGL](https://www.opengl.org/)**, _[Bullet Physics](https://pybullet.org/wordpress/), [Cython](https://cython.org/)_ ) \
<img alt="main image" height="256" src="F:\project\QuantumCore\QuantumCore\data\QuantumCore.png" width="256"/>
\
ㅤ
## Engine
This is an engine whose main language is **Python**. The project implements three-dimensional space and graphics, which are
rendered via  **OpenGL**, or just **GLSL**. The engine uses many other libraries to make it easier to work with.\
The optimization in the project is bad, as is the graphics, but the first is a consequence of the language and the second
is the lack of good shaders.

## Project details:
The engine is based on its own implementation, its own implementation of three-dimensional space. Rendering takes place through
the creation and use of shaders on GLSL, all information is transmitted to them through classes [моделей](QuantumCore/model.py)
The main language of the engine is **Python**, it is used for initialization _[VBO](QuantumCore/graphic/vbo.py),
[CAMERA](QuantumCore/graphic/camera.py), [LIGHT](QuantumCore/graphic/light.py)_. The rendering is based on the Modernlib
library, based on OpenGL. The language itself helps to create [.frag](QuantumCore/data/shaders/automaton/unilight.frag) and
[.vert](QuantumCore/data/shaders/automaton/unilight.vert). This will help me use your GPU to increase performance and graphics
quality. Currently, work is underway to improve the API and improve the internal classes of the engine. There are already
provided for the user [widgets](QuantumCore/widgets.py) (button, additional window, soon the input field),
[error screen](QuantumCore/messages/err_screen.py), [loading screen](QuantumCore/messages/loading_screen.py).  Do not forget
that the PyGame library is also at the heart of the project, which makes it easier to use some functions both in terms of
their use and in terms of documentation

### Requirements:
  * PyGame;
  * ModernGL;
  * Numpy;
  * PyGlm;
  * PyWaveFront;

### Compile:
Compile command: `pyinstaller --name "Quantum Game v0.4.4" --icon="QuantumCore/data/QuantumCore.ico" --add-data "C:/Program Files/Python311/Lib/site-packages/moderngl;moderngl" --add-data "C:/Program Files/Python311/Lib/site-packages/glcontext;glcontext" --add-data "F:/project/QuantumCore/core/elements/entities.py;entities" main.pyw`\
Eclipse the python version, icon name and game version to your own before using. After compile - copy all data in directory
(textures, models, game data and other). In the future it will work through a separate engine function
ㅤ
#### screenshots:
> 1. light: [after add 2 and more light source](QuantumCore/data/Screenshots/intermediateV1.png);
> 2. model loader: [3 loaded models in scene](QuantumCore/data/Screenshots/model_loader.png);
