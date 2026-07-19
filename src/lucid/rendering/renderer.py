"""
    
    Personal engine built on Pygame and ECS.

    This file is a part of the lucid-engine
    project and distributed under MIT license.
    https://github.com/kadir014/lucid-engine

"""

import struct

import moderngl

from lucid.models import Transform, Sprite


def create_buffer(
        ctx: moderngl.Context,
        data: list[float | int]
        ) -> moderngl.Buffer:
    """ Create buffer object from single-dtype array. """

    dtype = "f" if isinstance(data[0], float) else "I"
    return ctx.buffer(struct.pack(f"{len(data)}{dtype}", *data))


class Renderer:
    def __init__(self) -> None:
        self.context = moderngl.create_context(require=460)
        self.context.enable(moderngl.BLEND)

        self._vbo = create_buffer(
            self.context, [-0.5, 0.5, 0.5, 0.5, -0.5, -0.5, 0.5, -0.5]
        )
        self._uvbo = create_buffer(
            self.context, [0.0, 1.0, 1.0, 1.0, 0.0, 0.0, 1.0, 0.0]
        )
        self._ibo = create_buffer(self.context, [0, 1, 2, 1, 2, 3])

        self.instance_buffer = self.context.buffer(reserve=1024 * 1024, dynamic=True)

        vsh_source = """
#version 460

in vec2 in_position;
in vec2 in_uv;

in vec2 ins_position;
in float ins_rotation;
in vec2 ins_scale;
in vec2 ins_size;
in float ins_alpha;
in vec4 ins_tint;

out vec2 v_uv;
flat out float v_alpha;
flat out vec4 v_tint;

uniform vec2 u_resolution;

void main() {
    // Convert the unit quad [-0.5, 0.5] into sprite-sized pixels.
    vec2 local = in_position * ins_size * ins_scale;

    // Rotate around the center.
    float c = cos(ins_rotation);
    float s = sin(ins_rotation);
    vec2 rotated = vec2(
        local.x * c - local.y * s,
        local.x * s + local.y * c
    );

    // Move into world space (pixels).
    vec2 world = rotated + ins_position;

    // Convert pixel coordinates to opengl NDC.
    vec2 ndc = (world / u_resolution) * 2.0 - 1.0;

    // Convert from pygame origin to opengl origin.
    ndc.y = -ndc.y;

    gl_Position = vec4(ndc, 0.0, 1.0);

    v_uv = in_uv;
    v_alpha = ins_alpha;
    v_tint = ins_tint;
}
"""

        fsh_source = """
#version 460

in vec2 v_uv;
flat in float v_alpha;
flat in vec4 v_tint;

out vec4 f_color;

uniform sampler2D s_texture;

void main() {
    vec4 color = texture(s_texture, v_uv);

    color = mix(color, vec4(v_tint.rgb, color.a), v_tint.a);

    f_color = vec4(color.rgb, color.a * v_alpha);
}
"""

        self.program = self.context.program(
            vertex_shader=vsh_source, fragment_shader=fsh_source
        )

        self.vao = self.context.vertex_array(
            self.program,
            (
                (self._vbo, "2f", "in_position"),
                (self._uvbo, "2f", "in_uv"),
                (
                    self.instance_buffer,
                    "2f 1f 2f 2f 1f 4f /i",
                    "ins_position",
                    "ins_rotation",
                    "ins_scale",
                    "ins_size",
                    "ins_alpha",
                    "ins_tint",
                ),
            ),
            self._ibo
        )

        self.sprite_batches: dict[str, list[tuple[Transform, Sprite]]] = {}

    def batch_sprite(self, xform: Transform, sprite: Sprite, group: str) -> None:
        if group not in self.sprite_batches:
            self.sprite_batches[group] = []

        self.sprite_batches[group].append((xform, sprite))

    def render(self, window_resolution: tuple[int, int]) -> None:
        self.program["u_resolution"] = window_resolution

        self.context.clear(1.0, 1.0, 1.0, 1.0)

        inv255 = 1.0 / 255.0

        for group in self.sprite_batches:
            n_sprites = len(self.sprite_batches[group])

            for i, sprite_pair in enumerate(self.sprite_batches[group]):
                fmt = "12f"
                size = struct.calcsize(fmt)
                xform, sprite = sprite_pair
                data = struct.pack(
                    fmt,
                    xform.position.x,
                    xform.position.y,
                    xform.rotation,
                    xform.scale.x,
                    xform.scale.y,
                    sprite.texture.texture.width,
                    sprite.texture.texture.height,
                    sprite.alpha,
                    sprite.tint_color.r * inv255,
                    sprite.tint_color.g * inv255,
                    sprite.tint_color.b * inv255,
                    sprite.tint_alpha
                )
                
                self.instance_buffer.write(data, i * size)

            # Sprites are grouped by texture, so every sprite share the same texture
            self.sprite_batches[group][0][1].texture.texture.use()

            self.vao.render(instances=n_sprites)

        self.sprite_batches.clear()