# graphic
import pygame

# math
import glm
import numpy as np

# engine elements imports
from QuantumCore.data.config import FAR
from QuantumCore.model import ExtendedBaseModel, Cube
import QuantumCore.time


class MovingCube(Cube):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

    def update(self) -> None:

        m_model = glm.rotate(self.__get_model_matrix__(),
                             np.sin(self.app.time_list['cube animation'] * 0.5), glm.vec3(1, 0, 0))
        m_model = glm.rotate(m_model,
                             np.cos(self.app.time_list['cube animation'] * 0.5), glm.vec3(0, -1, 0))
        self.m_model = glm.rotate(m_model,
                                  np.sin(self.app.time_list['cube animation'] * 0.5), glm.vec3(0, 0, 1))

        super().update()

    def light_update(self) -> None: super().update()


class Cat(ExtendedBaseModel):
    def __init__(self, app, vao_name='cat', tex_id='cat',
                 pos=(0, 0, 0), rot=(0, 0, 0), scale=(1, 1, 1), ) -> None:

        super().__init__(app, vao_name, tex_id,
                         self.combine_vector(pos, [0, 1, 0]),
                         self.combine_vector(rot, (-90, 0, 0)),
                         scale, render_area=FAR)
        self.speed: float = .05

    def update(self) -> None:

        velocity = self.speed * QuantumCore.time.delta_time
        keys = pygame.key.get_pressed()
        if keys[pygame.K_i]:
            self.pos += velocity * self.__vec_x
        if keys[pygame.K_k]:
            self.pos -= velocity * self.__vec_x
        if keys[pygame.K_l]:
            self.pos += velocity * self.__vec_z
        if keys[pygame.K_j]:
            self.pos -= velocity * self.__vec_z
        if keys[pygame.K_m]:
            self.pos += velocity * self.__vec_y
        if keys[pygame.K_n]:
            self.pos -= velocity * self.__vec_y

        velocity /= 5
        if keys[pygame.K_DELETE]:
            self.rot -= velocity * self.__vec_z
        if keys[pygame.K_PAGEDOWN]:
            self.rot += velocity * self.__vec_z

        if keys[pygame.K_LCTRL]:
            self.speed = 0.03
        else:
            self.speed = 0.01
        
        if keys[pygame.K_TAB]:
            print(self.pos, self.rot)

        self.m_model = self.__get_model_matrix__()
        super().update()

    def light_update(self) -> None: super().update()


class WoodenWatchTower(ExtendedBaseModel):
    def __init__(self, app, vao_name='WoodenWatchTower', tex_id='WoodenWatchTower',
                 pos=(0, 0, 0), rot=(0, 0, 0), scale=(1, 1, 1)) -> None:

        super().__init__(app, vao_name, tex_id,
                         self.combine_vector(pos, (0, -0.55, 0)),
                         rot, scale, render_area=FAR)


class Earth(ExtendedBaseModel):
    def __init__(self, app, vao_name='earth', tex_id='earth',
                 pos=(0, 0, 0), rot=(0, 0, 0), scale=(1, 1, 1)) -> None:

        super().__init__(app, vao_name, tex_id, pos, rot, scale, render_area=FAR)

    def update(self) -> None:

        self.m_model = glm.rotate(self.__get_model_matrix__(),
                                  self.app.time_list['earth animation'] * 0.5, glm.vec3(0, 1, 0))

        super().update()

    def light_update(self) -> None: super().update()
