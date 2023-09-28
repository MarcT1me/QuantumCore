#version 330 core

layout (location = 0) out vec4 fragColor;


in vec2 uv_0;
in vec3 normal;
in vec3 fragPos;

vec3 color = vec3(0, 0, 0);

struct Light {
    vec3 position;
    vec3 Ia;
    vec3 Id;
    vec3 Is;
    int size;
};

uniform Light light;
uniform Light light2;
uniform Light light3;
uniform Light light4;
// textures
uniform sampler2D u_texture_0;
uniform vec3 camPos;


vec3 getLight(vec3 color) {
    vec3 Normal = normalize(normal);

    // ambient light
    vec3 ambient = light.Ia;
    vec3 ambient2 = light2.Ia;
    vec3 ambient3 = light3.Ia;
    vec3 ambient4 = light4.Ia;

    // difuse light
    vec3 lightDir = normalize((light.position) - fragPos);
    vec3 lightDir2 = normalize((light2.position) - fragPos);
    vec3 lightDir3 = normalize((light3.position) - fragPos);
    vec3 lightDir4 = normalize((light4.position) - fragPos);

    float diff = max(0, dot(lightDir, Normal));
    float diff2 = max(0, dot(lightDir2, Normal));
    float diff3 = max(0, dot(lightDir3, Normal));
    float diff4 = max(0, dot(lightDir4, Normal));

    vec3 deffuse = max((diff * light.Id), max((diff2 * light2.Id), max((diff3 * light3.Id), (diff4 * light4.Id))));

    // specular light
    vec3 viewDir = normalize(camPos - fragPos);
    vec3 reflectDir = reflect(-lightDir, Normal);
    int size = light.size;
    float spec = pow(max(dot(viewDir, reflectDir), 0), size);

    vec3 viewDir2 = normalize(camPos - fragPos);
    vec3 reflectDir2 = reflect(-lightDir2, Normal);
    int size2 = light2.size;
    float spec2 = pow(max(dot(viewDir2, reflectDir2), 0), size2);

    vec3 viewDir3 = normalize(camPos - fragPos);
    vec3 reflectDir3 = reflect(-lightDir3, Normal);
    int size3 = light3.size;
    float spec3 = pow(max(dot(viewDir3, reflectDir3), 0), size3);

    vec3 viewDir4 = normalize(camPos - fragPos);
    vec3 reflectDir4 = reflect(-lightDir4, Normal);
    int size4 = light4.size;
    float spec4 = pow(max(dot(viewDir4, reflectDir4), 0), size4);

    vec3 specular = max(spec * light.Is, max(spec2 * light2.Is, max(spec3 * light3.Is, spec4 * light4.Is)));

    return color * (max(ambient, max(ambient2, max(ambient3, ambient4))) + deffuse + specular);
}


void main() {

    if(gl_FrontFacing){
        vec3 color = texture(u_texture_0, uv_0).rgb;

        color = getLight(color);
        fragColor = vec4(color, 1.0);
    };
}
