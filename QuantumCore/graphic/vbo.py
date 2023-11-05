# graphics
import moderngl

# math
import numpy as np

# other
import pywavefront
import glob
from copy import copy
from loguru import logger

# engine elements imports
import QuantumCore.graphic
# engine config import
from QuantumCore.data.config import __ENGINE_FOLDER__, NEAR


class VBO:
    def __init__(self) -> None:
        """ All VBO`s of the application itself. """

        # VBO array
        self.VBOs: dict[str: BaseVBO] = {
            'Cube': CubeVBO()
        }
        self.service_VBOs: dict[str: BaseVBO] = {
            # 'skybox': SkyBoxVBO(),
            # 'advanced_skybox': AdvancedSkyBoxVBO(),
            # 'interface': AdvancedInterfaceVBO()
        }

        # load custom VBO`s
        for name, (form, atr, f_path, m_ext, t_ext) in CustomVBO_name.items():
            self.VBOs[name] = CustomVBO(formats=form, attributes=atr, path=f_path, ext=m_ext)

    def __destroy__(self) -> None: [vbo.__destroy__() for vbo in self.VBOs.values()]


class BaseVBO:
    def __init__(self) -> None:
        """ Base VBO variable. """
        self.ctx = copy(QuantumCore.window.context)

        self.vbo = self.__get_vbo__()

        # Shader variable
        self.format: str = 'None'
        self.attributes: list = [None]

    """ Static, Property and other mandatory methods """
    @staticmethod
    def _get_data_(vertices, indices) -> np.array: ...  # ...
    
    def _get_vertex_data_(self) -> np.array: return  # .obj file
    
    def __get_vbo__(self) -> moderngl.Context.buffer:
        """ Buffer and get vertex in vbo type """
        vbo = self.ctx.buffer(self._get_vertex_data_())
        return vbo
    
    def __destroy__(self) -> None: self.vbo.release()


class CubeVBO(BaseVBO):
    def __init__(self) -> None:
        """ Just cube with texture. """
        super().__init__()

        # Shader variable
        self.formats: str = '2f 3f 3f'
        self.attributes: list = ['in_texcoord_0', 'in_normal', 'in_position']

    """ Static, Property and other mandatory methods """
    @staticmethod
    def _get_data_(vertices, indices) -> np.array:
        data = [vertices[ind] for triangle in indices for ind in triangle]
        return np.array(data, dtype='f4')

    def _get_vertex_data_(self) -> np.hstack:
        vertices = [(-1, -1,  1), (1,  -1,  1), (1,  1,  1), (-1, 1,  1),
                    (-1,  1, -1), (-1, -1, -1), (1, -1, -1), (1,  1, -1)]
        indices = [(0, 2, 3), (0, 1, 2),
                   (1, 7, 2), (1, 6, 7),
                   (6, 5, 4), (4, 7, 6),
                   (3, 4, 5), (3, 5, 0),
                   (3, 7, 4), (3, 2, 7),
                   (0, 6, 1), (0, 5, 6)]
        vertex_data = self._get_data_(vertices, indices)

        tex_coord = [(0, 0), (1, 0), (1, 1), (0, 1)]
        tex_coord_indices = [(0, 2, 3), (0, 1, 2),
                             (0, 2, 3), (0, 1, 2),
                             (0, 1, 2), (2, 3, 0),
                             (2, 3, 0), (2, 0, 1),
                             (0, 2, 3), (0, 1, 2),
                             (3, 1, 2), (3, 0, 1)]
        tex_coord_data = self._get_data_(tex_coord, tex_coord_indices)

        normals = [(0,  0,  1) * 6,
                   (1,  0,  0) * 6,
                   (0,  0, -1) * 6,
                   (-1, 0,  0) * 6,
                   (0,  1,  0) * 6,
                   (0, -1,  0) * 6]
        normals = np.array(normals, dtype='f4').reshape(36, 3)

        vertex_data = np.hstack([normals, vertex_data])
        vertex_data = np.hstack([tex_coord_data, vertex_data])

        return vertex_data


# in development
class SkyBoxVBO(BaseVBO):
    def __init__(self) -> None:
        super().__init__()

        # Shader variable
        self.formats: str = '3f'
        self.attributes: list = ['in_position']

    """ Static, Property and other mandatory methods """
    @staticmethod
    def _get_data_(vertices, indices) -> np.array:
        data = [vertices[ind] for triangle in indices for ind in triangle]
        return np.array(data, dtype='f4')

    def _get_vertex_data_(self) -> np.array:
        vertices = [(-1, -1, 1), (1,  -1,  1), (1,  1,  1), (-1, 1,  1),
                    (-1, 1, -1), (-1, -1, -1), (1, -1, -1), (1,  1, -1)]

        indices = [(0, 2, 3), (0, 1, 2),
                   (1, 7, 2), (1, 6, 7),
                   (6, 5, 4), (4, 7, 6),
                   (3, 4, 5), (3, 5, 0),
                   (3, 7, 4), (3, 2, 7),
                   (0, 6, 1), (0, 5, 6)]
        vertex_data = self._get_data_(vertices, indices)
        vertex_data = np.flip(vertex_data, 1).copy(order='C')

        return vertex_data


# in development
class AdvancedSkyBoxVBO(BaseVBO):

    __z: int = 0.9999  # z cord in shader cords system

    def __init__(self) -> None:
        super().__init__()

        # Shader variable
        self.formats: str = '3f'
        self.attributes: list = ['in_position']

    def _get_vertex_data_(self) -> np.array:
        vertices = [(-1, -1, self.__z), (3, -1, self.__z), (-1, 3, self.__z)]
        vertex_data = np.array(vertices, dtype='f4')
        return vertex_data


class AdvancedInterfaceVBO(BaseVBO):

    __z: int = NEAR+0.001  # z cord in shader cords system

    def __init__(self) -> None:
        super().__init__()

        # Shader variable
        self.formats: str = '2f 2f'
        self.attributes: list = ['vert', 'texcoord']

    def _get_vertex_data_(self) -> np.array:
        vertices = [(-1, -1, self.__z), (3, -1, self.__z), (-1, 3, self.__z)]
        vertex_data = np.array(vertices, dtype='f2')
        return vertex_data


class CustomVBO(BaseVBO):
    """ Namelist your VBO`s.

    accounting VBO:
     * CustomVBO_name['some name'] = (variable formats, OpenGL attributes, obj path, obj ext, texture path, texture ext)


    # custom VBO`s init.
    for name, (form, atr, f_path, f_ext, t_ext) in CustomVBO.name.items():
        self.VBOs[name] = CustomVBO(app, formats=form, attributes=atr)

    * !!! attention: init before Mash class !!!
    """
    name: dict[str: tuple[str, tuple[str], str, str, str]] = dict()

    def __init__(self, *, formats, attributes, path, ext) -> None:
        """ NOT USE THIS INITIALIZATION;

          * !!! attention: add our models before Mash class !!!

         """

        self.obj_file_name: str = self.__get_obj_file_name__(path=path, ext=ext)  # needed for vertex_data in init
        # inheritance by class
        super().__init__()

        # Shader variable
        self.formats: str = formats
        self.attributes: list = attributes
        logger.debug('CustomVBO - load\n')

    @staticmethod
    def __get_obj_file_name__(path, ext) -> str:
        """ get name custom model """
        logger.info(rf'    search model: {path}/*.{ext}')
        f_list = glob.glob(rf'{path}/*.{ext}')
        f_list.append(rf'{__ENGINE_FOLDER__}/data/models/cat/20430_Cat_v1_NEW.obj')
        return f_list[0]

    def _get_vertex_data_(self) -> np.array:
        obj = pywavefront.Wavefront(self.obj_file_name)
        Material = obj.materials.popitem()[1]
        Vertex = Material.vertices
        vertex_data = np.array(Vertex, dtype='f4')
        return vertex_data


CustomVBO_name = CustomVBO.name
