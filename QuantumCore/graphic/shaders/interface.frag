#version 330 core

uniform sampler2D interface_texture;
uniform vec3 colorkey;

in vec2 uvs;
out vec4 f_color;

void main() {
    vec2 sample_pos = uvs;
    vec4 tex = texture(interface_texture, sample_pos);

    float alpha = tex.a-0.2;
    vec3 tex_rgb = tex.rgb;

    if (tex_rgb == vec3(colorkey)) {
        alpha = 0.0;
    };
    f_color = vec4(tex_rgb, alpha);
}
