#!/usr/bin/env python3
"""Build a simple layered RGB PSD and preview from PNG assets and text layers."""
import argparse
import json
import struct
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


def u32(value):
    return struct.pack(">I", value)


def s32(value):
    return struct.pack(">i", value)


def s16(value):
    return struct.pack(">h", value)


def pascal_name(name):
    raw = name.encode("mac_roman", errors="replace")[:255]
    data = bytes([len(raw)]) + raw
    return data + b"\0" * ((4 - len(data) % 4) % 4)


def find_font(font):
    if font and Path(font).is_file():
        return str(font)
    candidates = [
        font,
        "C:/Windows/Fonts/msyh.ttc",
        "C:/Windows/Fonts/arial.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    ]
    for candidate in candidates:
        if candidate and Path(candidate).is_file():
            return candidate
    return None


def render_text(item):
    text = item["text"]
    font_path = find_font(item.get("font"))
    size = int(item.get("font_size", 48))
    font = ImageFont.truetype(font_path, size) if font_path else ImageFont.load_default()
    lines = text.split("\n")
    spacing = int(item.get("line_spacing", size // 5))
    probe = ImageDraw.Draw(Image.new("RGBA", (1, 1)))
    boxes = [probe.textbbox((0, 0), line or " ", font=font, stroke_width=int(item.get("stroke_width", 0))) for line in lines]
    line_h = max((b[3] - b[1] for b in boxes), default=size)
    line_w = max((b[2] - b[0] for b in boxes), default=1)
    x, y = int(item.get("x", 0)), int(item.get("y", 0))
    layer = Image.new("RGBA", (max(1, line_w + 8), max(1, len(lines) * (line_h + spacing) + 8)))
    draw = ImageDraw.Draw(layer)
    for i, (line, box) in enumerate(zip(lines, boxes)):
        align = item.get("align", "left")
        dx = 4 if align == "left" else (layer.width - (box[2] - box[0])) // 2 if align == "center" else layer.width - (box[2] - box[0]) - 4
        draw.text((dx - box[0], 4 + i * (line_h + spacing) - box[1]), line, font=font,
                  fill=item.get("color", "#ffffff"),
                  stroke_width=int(item.get("stroke_width", 0)),
                  stroke_fill=item.get("stroke_color", "#000000"))
    return layer, x, y


def load_layers(manifest_path):
    manifest_path = Path(manifest_path).resolve()
    data = json.loads(manifest_path.read_text(encoding="utf-8"))
    width, height = map(int, data["canvas"])
    if not (1 <= width <= 30000 and 1 <= height <= 30000):
        raise ValueError("PSD canvas dimensions must be between 1 and 30000 pixels")
    root = manifest_path.parent
    layers = []
    for item in data["layers"]:
        if "text" in item:
            image, x, y = render_text(item)
        else:
            source = Path(item["file"])
            source = source if source.is_absolute() else root / source
            image = Image.open(source).convert("RGBA")
            x, y = int(item.get("x", 0)), int(item.get("y", 0))
        if x < 0 or y < 0 or x + image.width > width or y + image.height > height:
            # Clip assets/text that extend beyond the canvas.
            left, top = max(0, -x), max(0, -y)
            right, bottom = min(image.width, width - x), min(image.height, height - y)
            image = image.crop((left, top, right, bottom))
            x, y = max(0, x), max(0, y)
        layers.append({"name": item["name"], "image": image, "x": x, "y": y})
    if not layers:
        raise ValueError("Manifest must contain at least one layer")
    return width, height, layers


def build_psd(width, height, layers, output, preview=None):
    composite = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    for layer in layers:
        composite.alpha_composite(layer["image"], (layer["x"], layer["y"]))
    if preview:
        composite.convert("RGB").save(preview)

    records, channel_data = [], []
    # Keep manifest order (bottom-to-top) so Photoshop stacks the background
    # below artwork and copy layers when it reads the records.
    for layer in layers:
        image = layer["image"]
        bbox = image.getbbox() or (0, 0, 1, 1)
        cropped = image.crop(bbox)
        left, top = layer["x"] + bbox[0], layer["y"] + bbox[1]
        right, bottom = left + cropped.width, top + cropped.height
        records.append(s32(top) + s32(left) + s32(bottom) + s32(right) + s16(4))
        for cid in (-1, 0, 1, 2):
            records.append(s16(cid) + u32(cropped.width * cropped.height + 2))
        name = pascal_name(layer["name"])
        unicode_raw = layer["name"].encode("utf-16-be")
        unicode_data = u32(len(unicode_raw) // 2) + unicode_raw + b"\0\0"
        unicode_name = b"8BIMluni" + u32(len(unicode_data)) + unicode_data
        extra = u32(0) + u32(0) + name + unicode_name
        # Visibility bit 1 is clear for visible layers; bit 3 is required by PSD 5+.
        records.append(b"8BIMnorm" + bytes([255, 0, 8, 0]) + u32(len(extra)) + extra)
        channels = cropped.split()
        channel_data.append(s16(0) + channels[3].tobytes())
        for channel in channels[:3]:
            channel_data.append(s16(0) + channel.tobytes())

    layer_info = s16(len(layers)) + b"".join(records) + b"".join(channel_data)
    if len(layer_info) % 2:
        layer_info += b"\0"
    layer_mask = u32(len(layer_info)) + layer_info + u32(0)
    # The flattened composite is opaque RGB (3 channels); individual layers retain RGBA.
    header = b"8BPS" + s16(1) + b"\0" * 6 + s16(3) + u32(height) + u32(width) + s16(8) + s16(3)
    merged = composite.convert("RGB").split()
    planar = b"".join(channel.tobytes() for channel in merged)
    with Path(output).open("wb") as f:
        f.write(header + u32(0) + u32(0) + u32(len(layer_mask)) + layer_mask)
        f.write(s16(0) + planar)
    validate_psd(output, width, height, len(layers))


def validate_psd(path, width, height, expected_layers):
    """Check the written PSD section lengths and all layer channel payloads."""
    data = Path(path).read_bytes()
    assert data[:4] == b"8BPS" and struct.unpack_from(">H", data, 4)[0] == 1
    channels, actual_height, actual_width, depth, mode = struct.unpack_from(">HIIHH", data, 12)
    assert (channels, actual_width, actual_height, depth, mode) == (3, width, height, 8, 3)
    pos = 26
    color_len = struct.unpack_from(">I", data, pos)[0]
    pos += 4 + color_len
    resource_len = struct.unpack_from(">I", data, pos)[0]
    pos += 4 + resource_len
    section_len = struct.unpack_from(">I", data, pos)[0]
    section_start = pos + 4
    layer_info_len = struct.unpack_from(">I", data, section_start)[0]
    info_start = section_start + 4
    count = struct.unpack_from(">h", data, info_start)[0]
    assert count == expected_layers
    record_pos = info_start + 2
    channels_total = 0
    for _ in range(count):
        record_pos += 16
        channel_count = struct.unpack_from(">H", data, record_pos)[0]
        record_pos += 2
        lengths = []
        for _ in range(channel_count):
            record_pos += 2
            length = struct.unpack_from(">I", data, record_pos)[0]
            record_pos += 4
            lengths.append(length)
        assert data[record_pos:record_pos + 8] == b"8BIMnorm"
        assert not (data[record_pos + 10] & 2)  # bit 1 set means hidden
        record_pos += 12
        extra_len = struct.unpack_from(">I", data, record_pos)[0]
        extra_start = record_pos + 4
        extra_end = extra_start + extra_len
        p = extra_start
        mask_len = struct.unpack_from(">I", data, p)[0]
        p += 4 + mask_len
        blend_len = struct.unpack_from(">I", data, p)[0]
        p += 4 + blend_len
        name_len = data[p]
        p += 1 + name_len
        p += (4 - ((1 + name_len) % 4)) % 4
        found_unicode_name = False
        while p < extra_end:
            assert data[p:p + 4] == b"8BIM"
            key = data[p + 4:p + 8]
            block_len = struct.unpack_from(">I", data, p + 8)[0]
            payload = p + 12
            if key == b"luni":
                units = struct.unpack_from(">I", data, payload)[0]
                assert data[payload + 4 + units * 2:payload + 6 + units * 2] == b"\0\0"
                found_unicode_name = True
            p = payload + block_len + (block_len % 2)
        assert p == extra_end and found_unicode_name
        record_pos += 4 + extra_len
        assert channel_count == 4 and all(n >= 2 for n in lengths)
        channels_total += sum(lengths)
    channel_start = record_pos
    assert channel_start + channels_total <= info_start + layer_info_len
    assert section_len == 4 + layer_info_len + 4
    merged_pos = section_start + section_len
    assert struct.unpack_from(">H", data, merged_pos)[0] == 0
    merged = data[merged_pos + 2:]
    assert len(merged) == width * height * 3


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manifest", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--preview")
    args = parser.parse_args()
    width, height, layers = load_layers(args.manifest)
    build_psd(width, height, layers, args.output, args.preview)
    print(f"Wrote and validated {args.output}: {width}x{height}, {len(layers)} layers")


if __name__ == "__main__":
    main()
