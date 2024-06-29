# graphic
import pygame

# math
import glm
import numpy as np

# engine elements imports
from QuantumCore.data.config import FAR
from QuantumCore.model import ExtendedBaseModel, Cube, MetaData
import QuantumCore.time


class MovingCube(Cube):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.rotate_speed = .05
    
    def update(self) -> None:
        time = QuantumCore.time.list_['cube animation']*0.5
        # rotate
        self.metadata.rot.x += glm.radians(glm.cos(time)*QuantumCore.time.delta*self.rotate_speed)
        self.metadata.rot.y += glm.radians(glm.sin(time)*QuantumCore.time.delta*self.rotate_speed)
        self.metadata.rot.z += glm.radians(glm.cos(time)*QuantumCore.time.delta*self.rotate_speed)
        # matrix update
        super().update()
    
    def light_update(self) -> None: super().update()


class Cat(ExtendedBaseModel):
    def __init__(self, metadata: MetaData = None, *, vao_id='Cat', tex_id='Cat',
                 pos=(0, 0, 0), rot=(0, 0, 0), scale=(1, 1, 1), render_area=FAR, sav=False
                 ) -> None:
        super().__init__(
            metadata if metadata is not None else MetaData(
                pos=self.combine_vector(pos, (0, 1, 0), sav=sav),
                rot=self.combine_vector(rot, (-90, 0, 0), sav=sav),
                scale=scale,
                object_id=self.name(),
                vao_id=vao_id,
                tex_id=tex_id
            ),
            render_area=render_area
        )
        
        self.speed: float = .05
    
    def update(self) -> None:
        velocity = self.speed*QuantumCore.time.delta
        keys = pygame.key.get_pressed()
        if keys[pygame.K_KP8]:
            self.metadata.pos += velocity*self._vec_x
        if keys[pygame.K_KP5]:
            self.metadata.pos -= velocity*self._vec_x
        if keys[pygame.K_KP6]:
            self.metadata.pos += velocity*self._vec_z
        if keys[pygame.K_KP_4]:
            self.metadata.pos -= velocity*self._vec_z
        if keys[pygame.K_KP_PLUS]:
            self.metadata.pos += velocity*self._vec_y
        if keys[pygame.K_KP_MINUS]:
            self.metadata.pos -= velocity*self._vec_y
        
        velocity /= 5
        if keys[pygame.K_KP7]:
            self.metadata.rot -= velocity*self._vec_z
        if keys[pygame.K_KP9]:
            self.metadata.rot += velocity*self._vec_z
        
        if keys[pygame.K_RCTRL] or keys[pygame.K_LCTRL]:
            self.speed = 0.03
        else:
            self.speed = 0.01
        
        # matrix update
        super().update()
    
    def light_update(self) -> None: super().update()


class WoodenWatchTower(ExtendedBaseModel):
    def __init__(self, metadata: MetaData = None, *, vao_id='WoodenWatchTower', tex_id='WoodenWatchTower',
                 pos=(0, 0, 0), rot=(0, 0, 0), scale=(1, 1, 1), render_area=FAR, sav=False
                 ) -> None:
        super().__init__(
            metadata if metadata is not None else MetaData(
                pos=self.combine_vector(pos, (0, -1, 0), sav=sav),
                rot=self.combine_vector(rot, (0, 0, 0), sav=sav),
                scale=scale,
                object_id=self.name(),
                vao_id=vao_id,
                tex_id=tex_id
            ),
            render_area=render_area
        )


class Earth(ExtendedBaseModel):
    def __init__(self, metadata: MetaData = None, *, vao_id='Earth', tex_id='Earth',
                 pos=(0, 0, 0), rot=(0, 0, 0), scale=(1, 1, 1), render_area=FAR, sav=False
                 ) -> None:
        super().__init__(
            metadata if metadata is not None else MetaData(
                pos=self.combine_vector(pos, (0, 0, 0), sav=sav),
                rot=self.combine_vector(rot, (0, 0, 0), sav=sav),
                scale=scale,
                object_id=self.name(),
                vao_id=vao_id,
                tex_id=tex_id
            ),
            render_area=render_area
        )
        
        self.rotate_speed = 0.01
    
    def update(self) -> None:
        self.metadata.rot.y += glm.radians(self.rotate_speed*QuantumCore.time.delta)
        
        super().update()
    
    def light_update(self) -> None: super().update()
