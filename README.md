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
4. 用随附脚本构建 RGB、8-bit PSD 和扁平预览图，并检查尺寸、图层数、可见性标志、通道结构和 PSD 合并图。
5. 若本次 Codex 会话能控制 Photoshop，则在 Photoshop 中实际打开交付 PSD，检查画面、图层眼睛状态和图层内容，并在 Photoshop 修改后保存、重开确认。只检测到已安装程序或通过文件结构检查，不算 Photoshop 打开验证。

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
    {"name": "Headline", "text": "Sample headline", "x": 190, "y": 130,
     "font_size": 48,
     "color": "#163A70", "align": "center"}
  ]
}
```

### 文字编辑与格式边界

脚本把清单中的 `text` 渲染成透明像素图层。它们可以在 Photoshop 中移动、隐藏、删除或替换，但不能用文字工具修改原有文字；应称为“文字像素层”，不能笼统声称文案可编辑。

如果需求要求在 Photoshop 里直接改字，skill 会在可用的 Photoshop 会话中，为每段准确文案创建独立的原生文字图层，并检查文字、图层及重开结果。Photoshop 24.2 及以上支持 `Document.createTextLayer`；UXP 脚本使用 `.psjs` 文件，可通过 Photoshop 的“文件 > 脚本 > 浏览”运行。详见 [Adobe UXP 脚本指南](https://developer.adobe.com/photoshop/uxp/scripting/) 和 [原生文字图层选项](https://developer.adobe.com/photoshop/uxp/ps_reference/objects/createoptions/textlayercreateoptions/)。机器上的字体和 Photoshop 文字度量可能与预览图不同，须检查 Photoshop 中的实际排版。

如果当前会话无法控制 Photoshop，就交付有独立文字像素层的 PSD 和准确文案清单，并明确告知文字不能用文字工具直接改。写出器不创建矢量形状、智能对象、图层蒙版或 CMYK 文档。

### 许可与安全

仓库中的代码、文档和示例背景图采用 MIT License；此许可不自动覆盖用户素材、第三方素材或单次生成的设计输出。安全问题与数据处理方式见 [SECURITY.md](SECURITY.md)。

## English

### Overview

`psd-layered-design` is a reusable Codex skill that turns a visual brief into a layer plan, generates separate visual assets, typesets exact copy, and assembles an editable Photoshop document. It is intended for posters, certificates, covers, social graphics, and similar single-page designs.

### Workflow

1. Identify canvas, style, palette, focal elements, and exact copy from the brief.
2. Plan background, subject, decorations, logo placeholders, and copy as independent layers. Generate and review each distinct visual asset separately.
3. Never ask an image model to render text that must be exact (names, slogans, dates, or official marks). Typeset copy locally. Use only user-provided or verified official logo assets; otherwise keep a clearly named placeholder.
4. Build a standard RGB, 8-bit layered PSD and flattened preview with the bundled script. Check dimensions, layer count, visibility flags, channel structure, and the merged PSD image.
5. When Photoshop can be controlled in the current session, open the exact deliverable there and inspect the visible artwork and layer visibility in the stack. Reopen the saved document after Photoshop-side edits. An installed application or a binary structure check alone does not verify Photoshop compatibility.

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

### Text editing and format limits

The bundled writer renders manifest `text` entries into independent transparent pixel layers. In Photoshop those layers can be moved, hidden, deleted, or replaced, but their words cannot be changed with the Type tool. Call them raster text layers.

When the user needs direct text editing in Photoshop, create a separate native Type layer for each exact text block in a controllable Photoshop session, then check the displayed copy, layer types, and saved/reopened PSD. Hide or remove the matching raster copy layer to prevent duplicate text. Photoshop 24.2 and later provide `Document.createTextLayer`; UXP scripts use the `.psjs` extension and can run through **File > Scripts > Browse**. See [Adobe's UXP scripting guide](https://developer.adobe.com/photoshop/uxp/scripting/) and [text layer creation options](https://developer.adobe.com/photoshop/uxp/ps_reference/objects/createoptions/textlayercreateoptions/). Fonts and text metrics may change placement from the Pillow preview, so inspect Photoshop's rendering. If Photoshop cannot be controlled in the current session, disclose that text is rasterized and provide the exact copy in the manifest for rerendering. The minimal writer does not create vector shape layers, Smart Objects, layer masks, or CMYK documents.

### License and security

Repository code, documentation, and the bundled example background are licensed under the MIT License. This does not automatically license user-provided assets, third-party assets, or one-off generated designs. See [SECURITY.md](SECURITY.md) for security guidance and vulnerability reporting.
