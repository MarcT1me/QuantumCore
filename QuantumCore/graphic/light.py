
# math
import glm


class Light:
    def __init__(self, *, color=(1, 1, 1), pos=(3, 3, -3),
                 ambient=0.1, diffuse=0.8, specular=1.0, size=32) -> None:
        self.color = glm.vec3(color)
        # instances
        self.position = glm.vec3(pos)
        self.Ia: glm.vec3 = ambient * self.color
        self.Id: glm.vec3 = diffuse * self.color
        self.Is: glm.vec3 = specular * self.color
        self.size: int = size


lights_list: dict[hash: Light] = [{0: Light()},]
