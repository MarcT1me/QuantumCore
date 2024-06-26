#version 330 core

layout (location = 0) out vec4 fragColor;

in vec2 uv_0;
in vec3 normal;
in vec3 fragPos;

// light
struct Light {
    vec3 position;
    vec3 Ia;
    vec3 Id;
    vec3 Is;
    int size;
};
uniform int lights_source_size;
uniform Light lights_source[20];

// poligon color variable
uniform sampler2D u_texture_0;
uniform vec3 camPos;

uniform float gamma;


vec4 getLight(inout vec4 color) {
    // Standard variable
    vec3 Normal = normalize(normal);
    vec3 ambient = vec3(0, 0, 0);
    vec3 deffuse = vec3(0, 0, 0);
    vec3 specular = vec3(0, 0, 0);

    // Calculate light
    for(int i = 0; i < lights_source_size; i++) {
        // this iteration Light
        Light light = lights_source[i];

        // Ambient
        ambient = max(light.Ia, ambient);

        // Diffuse
        vec3 lightDir = normalize((light.position) - fragPos);
        float diff = max(0, dot(lightDir, Normal));
        deffuse = max(diff * light.Id, deffuse);

        // Specular
        vec3 viewDir = normalize(camPos - fragPos);
        vec3 reflectDir = reflect(-lightDir, Normal);
        float spec = pow(max(dot(viewDir, reflectDir), 0),  light.size);
        specular = max(spec * light.Is, specular);
    };

    return color * vec4(ambient + deffuse + specular, 1.0);
}


void main() {
    vec4 color  = texture(u_texture_0, uv_0);

    color = pow(color, vec4(gamma));
    color = getLight(color);
    color = pow(color, 1/vec4(gamma));

    fragColor = color;
}
