#version 330 core

in vec2 uvs;
out vec4 f_color;

uniform sampler2D interfaceTexture;
uniform float globalAlpha = 1.0;
uniform vec3 colorkey = vec3(0.0);
uniform bool useColorkey = false;

void main() {
    vec4 tex = texture(interfaceTexture, uvs);

    if (tex.rgb == colorkey && useColorkey) {
        f_color = tex * 0.0;
    } else {
        f_color = tex * globalAlpha;
    }
}
