# Psd-codex-image

**Codex skill for generating AI-assisted, layered, editable Photoshop documents (PSD).**

**面向 Codex 的 AI 分层 PSD 生成技能：**根据图片需求生成可移动的独立素材层，将准确文案单独排版，并导出带预览的 Photoshop PSD。

## 中文

### 项目简介

`psd-layered-design` 是一个可复用的 Codex skill，用于把自然语言视觉需求整理为图层计划、生成独立视觉素材、准确排版文案，并组装为可继续编辑的 PSD。它适用于海报、证书、封面、社交媒体图片及类似的单页视觉设计。

### 能力与工作流

1. 从需求中确定画布、风格、配色、焦点元素和准确文案。
2. 将背景、主体、装饰、标识占位和文案规划为独立图层；每个独立视觉素材分别生成并审核。
3. 不让图像模型生成必须准确的名称、标语、日期或校徽。文案使用本机字体排版；校徽等标识只使用用户提供或经核验的官方素材，没有素材时保留占位层。
4. 用随附脚本构建 RGB、8-bit PSD 和扁平预览图，并检查尺寸、图层数、通道结构和 PSD 合并图。

### 安装

将本仓库内容复制到 Codex skills 目录下的 `psd-layered-design` 文件夹：

```powershell
$target = "$env:USERPROFILE\.codex\skills\psd-layered-design"
New-Item -ItemType Directory -Force -Path $target | Out-Null
Copy-Item .\SKILL.md, .\scripts -Destination $target -Recurse -Force
```

如需使用手动生成 PSD 的脚本，请安装 Python 3 和 Pillow：

```powershell
python -m pip install Pillow
```

### 使用

安装后，在 Codex 中描述你要设计的图片并提出 PSD 交付要求。skill 会规划图层、调用当前运行环境可用的图像生成能力、排版准确文案、构建 PSD 并检查预览。

也可以直接调用脚本。清单中 `layers` 按**从底到顶**排列。图像层使用 `file`，文案层使用 `text`；图层位置以左上角像素坐标计。相对资源路径以清单文件所在目录为基准。

```powershell
python .\scripts\build_psd.py `
  --manifest .\examples\layers.example.json `
  --output .\design.psd `
  --preview .\design-preview.png
```

清单字段示例：

```json
{
  "canvas": [640, 360],
  "layers": [
    {"name": "Background", "file": "assets/background.png", "x": 0, "y": 0},
    {"name": "Headline", "text": "Editable headline", "x": 190, "y": 130,
     "font_size": 48,
     "color": "#163A70", "align": "center"}
  ]
}
```

### 格式边界

脚本输出标准 RGB、8-bit、带独立像素图层的 PSD。文本层默认是透明像素图层：在 Photoshop 中可移动、隐藏、删除或替换，但不能用文字工具直接编辑原有字形。若当前环境能够控制 Photoshop，skill 会优先尝试原生文字层；无法连接时会明确说明这一限制。该简易写出器不创建矢量形状、智能对象、图层蒙版或 CMYK 文档。

### 许可与安全

仓库中的代码、文档和示例背景图采用 MIT License；此许可不自动覆盖用户素材、第三方素材或单次生成的设计输出。安全问题与数据处理方式见 [SECURITY.md](SECURITY.md)。

## English

### Overview

`psd-layered-design` is a reusable Codex skill that turns a visual brief into a layer plan, generates separate visual assets, typesets exact copy, and assembles an editable Photoshop document. It is intended for posters, certificates, covers, social graphics, and similar single-page designs.

### Workflow

1. Identify canvas, style, palette, focal elements, and exact copy from the brief.
2. Plan background, subject, decorations, logo placeholders, and copy as independent layers. Generate and review each distinct visual asset separately.
3. Never ask an image model to render text that must be exact (names, slogans, dates, or official marks). Typeset copy locally. Use only user-provided or verified official logo assets; otherwise keep a clearly named placeholder.
4. Build a standard RGB, 8-bit layered PSD and flattened preview with the bundled script. Check dimensions, layer count, channel structure, and the merged PSD image.

### Installation

Copy the repository contents into a `psd-layered-design` directory under your Codex skills folder (usually `%USERPROFILE%\.codex\skills` on Windows or `$CODEX_HOME/skills` when configured). Install Python 3 and Pillow to run the bundled PSD builder:

```sh
python -m pip install Pillow
```

### Use

After installation, describe the visual you want in Codex and request a PSD deliverable. The skill plans the layers, uses the image-generation capability available in the current runtime, typesets exact copy, builds the PSD, and checks the preview.

The builder can also be run directly:

```sh
python scripts/build_psd.py --manifest examples/layers.example.json \
  --output design.psd --preview design-preview.png
```

Manifest layers are ordered bottom-to-top. Image layers use `file`; copy layers use `text`. Coordinates are top-left pixel coordinates. Relative asset paths are resolved from the manifest directory. See the Chinese example above and `examples/layers.example.json` for the complete schema.

### Format limits

The bundled writer creates standard RGB, 8-bit PSDs with independent raster layers. Text is rendered to transparent pixel layers by default. In Photoshop those layers can be moved, hidden, deleted, or replaced, but their glyphs are not editable with the Type tool. If Photoshop automation is available, the skill prefers native type layers; if not, it discloses the raster-text fallback. The minimal writer does not create vector shape layers, Smart Objects, layer masks, or CMYK documents.

### License and security

Repository code, documentation, and the bundled example background are licensed under the MIT License. This does not automatically license user-provided assets, third-party assets, or one-off generated designs. See [SECURITY.md](SECURITY.md) for security guidance and vulnerability reporting.
