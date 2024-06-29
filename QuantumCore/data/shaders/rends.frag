#version 330 core

/* pipeline variables */
layout (location = 0) out vec4 fragColor;
in vec2 uv0;

/* uniforms */
uniform sampler2D u_renderSurface;


void main() {
    /* Entry point */
    vec4 tex = texture(u_renderSurface, uv0);
    fragColor = tex;
}
