# graphics
import pygame

# math
import glm

# engine elements imports
from QuantumCore.data import config
import QuantumCore.time


class Camera:
    def __init__(self, position=(0, 0, 4), yaw=0, pitch=0, speed=0.01) -> None:
        """ Camera init """
        self.aspect_ratio = config.SCREEN_size[0] / config.SCREEN_size[1]

        # orientation in space
        self.position = glm.vec3(position)

        self.up = glm.vec3(0, 1, 0)
        self.right = glm.vec3(1, 0, 0)
        self.forward = glm.vec3(0, 0, -1)

        self.yaw = yaw
        self.pitch = pitch

        self.speed = speed

        # view matrix
        self.m_view = self.__get_view_matrix__
        # projection matrix
        self.m_proj = self.__get_projection_matrix__

        # attach a camera to an object
        self.attach_object = None

    def update(self) -> None:
        """ update camera """

        # optional
        self.move() if self.attach_object is None else self.__use_attach__()
        self.__rotate__()

        # necessarily
        self.__update_camera_vectors__()
        self.m_view = self.__get_view_matrix__

    def __rotate__(self) -> None:
        """ rotate FOV """
        rel_x, rel_y = pygame.mouse.get_rel()

        # calculate camera rotate vectors
        self.yaw += rel_x * config.sensitivity
        self.pitch -= rel_y * config.sensitivity
        self.pitch = max(-90, min(90, self.pitch))

    def __update_camera_vectors__(self):
        """ orientation in space """
        yaw, pitch = glm.radians(self.yaw), glm.radians(self.pitch)

        # calculate xz vector
        self.forward.x = glm.cos(yaw) * glm.cos(pitch)
        self.forward.y = glm.sin(pitch)
        self.forward.z = glm.sin(yaw) * glm.cos(pitch)

        # use vectors
        self.forward = glm.normalize(self.forward)
        self.right = glm.normalize(glm.cross(self.forward, glm.vec3(0, 1, 0)))
        self.up = glm.normalize(glm.cross(self.right, self.forward))

    def move(self) -> None:
        """ move in space; if camera not attach """
        velocity = self.speed * QuantumCore.time.delta_time
        keys = pygame.key.get_pressed()

        # move
        if keys[pygame.K_w]:
            self.position += self.forward * velocity
        if keys[pygame.K_s]:
            self.position -= self.forward * velocity
        if keys[pygame.K_a]:
            self.position -= self.right * velocity
        if keys[pygame.K_d]:
            self.position += self.right * velocity
        if keys[pygame.K_SPACE]:
            self.position += self.up * velocity
        if keys[pygame.K_c]:
            self.position -= self.up * velocity

        # run (speed up)
        if keys[pygame.K_LCTRL]:
            self.speed = 0.03
        else:
            self.speed = 0.01

    """ Property and necessarily methods """
    def __use_attach__(self) -> None: self.position = glm.vec3(self.attach_object.pos)

    @property
    def __get_view_matrix__(self) -> glm.mat4: return glm.lookAt(self.position, self.position + self.forward, self.up)

    @property
    def __get_projection_matrix__(self) -> glm.mat4: return glm.perspective(glm.radians(config.FOV),
                                                                            self.aspect_ratio, config.NEAR, config.FAR)


camera: Camera = None
