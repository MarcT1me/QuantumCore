# graphics
import pygame

# other
import glm
from dataclasses import dataclass, field

# engine elements imports
from QuantumCore.data import config
import QuantumCore.time


class OldCamera:

    __up = glm.vec3(0, 1, 0)
    __right = glm.vec3(1, 0, 0)
    __forward = glm.vec3(0, 0, -1)
    
    def __init__(self, pos=(0, 0, 4), yaw: float = 0, pitch: float = 0, speed=0.01) -> None:
        """ Camera init """
        self._aspect_ratio: float = config.SCREEN_size[0] / config.SCREEN_size[1]

        """ orientation in space """
        self.position = glm.vec3(pos)
        self.attach_object: QuantumCore = None  # attach a camera to an object

        self.yaw: float = yaw
        self.pitch: float = pitch

        self.speed: float = speed
        
        """ Graphic matrices """
        self.m_view: glm.mat4 = self.__get_view_matrix
        self.m_proj: glm.mat4 = self._get_projection_matrix_

    def update(self) -> None:
        """ update camera """
        self.move() if self.attach_object is None else self._use_attach_()
        self._rotate_()
        self.__update_camera_vectors()
        self.m_view = self.__get_view_matrix

    def _rotate_(self) -> None:
        """ rotate FOV """
        rel_x, rel_y = pygame.mouse.get_rel()

        # calculate camera rotate vectors
        self.yaw += rel_x * config.sensitivity
        self.pitch -= rel_y * config.sensitivity
        self.pitch = max(-90, min(90, self.pitch))

    def __update_camera_vectors(self):
        """ orientation in space """
        yaw, pitch = glm.radians(self.yaw), glm.radians(self.pitch)

        # calculate xz vector
        self.__forward.x = glm.cos(yaw) * glm.cos(pitch)
        self.__forward.y = glm.sin(pitch)
        self.__forward.z = glm.sin(yaw) * glm.cos(pitch)

        # use vectors
        self.__forward = glm.normalize(self.__forward)
        self.__right = glm.normalize(glm.cross(self.__forward, glm.vec3(0, 1, 0)))
        self.__up = glm.normalize(glm.cross(self.__right, self.__forward))

    def move(self) -> None:
        """ move in space; if camera not attach """
        velocity = self.speed * QuantumCore.time.delta
        keys = pygame.key.get_pressed()

        # move
        if keys[pygame.K_w]:
            self.position += self.__forward * velocity
        if keys[pygame.K_s]:
            self.position -= self.__forward * velocity
        if keys[pygame.K_a]:
            self.position -= self.__right * velocity
        if keys[pygame.K_d]:
            self.position += self.__right * velocity
        if keys[pygame.K_SPACE]:
            self.position += self.__up * velocity
        if keys[pygame.K_c]:
            self.position -= self.__up * velocity

        # run (speed up)
        if keys[pygame.K_LCTRL]:
            self.speed = 0.03
        else:
            self.speed = 0.01

    """ Property and necessarily methods """
    def _use_attach_(self) -> None: self.position = glm.vec3(self.attach_object.pos)

    @property
    def __get_view_matrix(self) -> glm.mat4: return glm.lookAt(self.position, self.position + self.__forward, self.__up)

    @property
    def _get_projection_matrix_(self) -> glm.mat4: return glm.perspective(glm.radians(config.FOV),
                                                                          self._aspect_ratio, config.NEAR, config.FAR)


class Camera:

    __up = glm.vec3(0, 1, 0)
    __right = glm.vec3(1, 0, 0)
    __forward = glm.vec3(0, 0, -1)
    
    
    @dataclass
    class Snap:
        pos: tuple[float, float, float] = field(init=True)
        
        yaw: float
        pitch: float
        
        attach_object_id: int = field(init=True, default=None)
        
        def __post_init__(self):
            self.pos = glm.vec3(self.pos)
    
    def __init__(self, data: Snap = Snap(pos=(0, 0, 4), yaw = 0, pitch= 0), speed=0.01) -> None:
        """ Camera init """
        self._aspect_ratio: float = config.SCREEN_size[0] / config.SCREEN_size[1]

        self.data: Camera.Snap = data
        self.speed: float = speed
        
        """ Graphic matrices """
        self.m_view: glm.mat4 = self.__get_view_matrix
        self.m_proj: glm.mat4 = self._get_projection_matrix_

    def update(self) -> None:
        """ update camera """
        self.move()
        self._rotate_()
        self.__update_camera_vectors()
        self.m_view = self.__get_view_matrix

    def _rotate_(self) -> None:
        """ rotate FOV """
        rel_x, rel_y = pygame.mouse.get_rel()

        # calculate camera rotate vectors
        self.data.yaw += rel_x * config.sensitivity
        self.data.pitch -= rel_y * config.sensitivity
        self.pitch = max(-90, min(90, self.data.pitch))

    def __update_camera_vectors(self):
        """ orientation in space """
        yaw, pitch = glm.radians(self.data.yaw), glm.radians(self.pitch)

        # calculate xz vector
        self.__forward.x = glm.cos(yaw) * glm.cos(pitch)
        self.__forward.y = glm.sin(pitch)
        self.__forward.z = glm.sin(yaw) * glm.cos(pitch)

        # use vectors
        self.__forward = glm.normalize(self.__forward)
        self.__right = glm.normalize(glm.cross(self.__forward, glm.vec3(0, 1, 0)))
        self.__up = glm.normalize(glm.cross(self.__right, self.__forward))

    def move(self) -> None:
        """ move in space; if camera not attach """
        velocity = self.speed * QuantumCore.time.delta
        keys = pygame.key.get_pressed()

        # move
        if keys[pygame.K_w]:
            self.data.pos += self.__forward * velocity
        if keys[pygame.K_s]:
            self.data.pos -= self.__forward * velocity
        if keys[pygame.K_a]:
            self.data.pos -= self.__right * velocity
        if keys[pygame.K_d]:
            self.data.pos += self.__right * velocity
        if keys[pygame.K_SPACE]:
            self.data.pos += self.__up * velocity
        if keys[pygame.K_c]:
            self.data.pos -= self.__up * velocity

        # run (speed up)
        if keys[pygame.K_LCTRL]:
            self.speed = 0.03
        else:
            self.speed = 0.01

    @property
    def __get_view_matrix(self) -> glm.mat4:
        return glm.lookAt(self.data.pos, self.data.pos + self.__forward, self.__up)

    @property
    def _get_projection_matrix_(self) -> glm.mat4:
        return glm.perspective(glm.radians(config.FOV),
                               self._aspect_ratio, config.NEAR, config.FAR)


camera: Camera = None
