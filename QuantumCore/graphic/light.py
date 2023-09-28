
# math
import glm


class Light:
    def __init__(self, *, pos=(3, 3, -3), color=(1, 1, 1), size=32, ambient=0.1, diffuse=0.8, specular=1.0) -> None:
        self.color = glm.vec3(color)
        # instances
        self.position = glm.vec3(pos)
        self.Ia = ambient * self.color
        self.Id = diffuse * self.color
        self.Is = specular * self.color
        self.size = size


lights_list: list = [Light()]
