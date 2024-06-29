#version 330 core

/* shader attributes */
layout (location = 0) in vec3 in_position;
layout (location = 1) in vec2 in_texCoord;
out vec2 uv0;

void main() {
    /* Entry point */
    uv0 = in_texCoord;
    gl_Position = vec4(in_position, 1.0);
}
