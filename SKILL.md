---
name: psd-layered-design
description: Turn a visual brief into a layered, editable PSD by generating separate image assets and keeping exact text on independent layers. Use when the requested deliverable is a PSD users can rearrange or revise.
---

# Layered PSD Design

Create a finished, layered PSD from the user's image brief. Treat the generated image assets as movable design layers; never ask an image model to render exact names, slogans, dates, logos, or other text that must be correct.

## Workflow

1. Extract the canvas size, intended use, style, palette, focal subject, required wording, and likely independent objects from the brief. Ask only if a missing choice materially blocks the design; otherwise use a sensible canvas for the stated use.
2. Plan the composition and layer stack. Keep the background, focal art, secondary objects, decorative accents, and each text block as separately named layers. Generate distinct visual assets with one image-generation call per asset. For cutouts, request transparency; otherwise use full-canvas assets with clear negative space. Inspect generated assets and regenerate only assets with visible defects.
3. Render exact copy locally with an installed font, one text block per transparent PNG layer. Preserve spelling, punctuation, and requested line breaks. Never substitute model-generated lettering for exact copy. For logos or seals, use a user-provided asset or a verified official source; if unavailable, leave a clearly named placeholder layer instead of inventing a distorted mark.
4. Assemble the image and rendered-copy PNGs into a PSD using `scripts/build_psd.py`. Provide the PSD, a flattened preview, and a short layer inventory. Keep source assets and a manifest next to the output so assets can be replaced and raster copy can be rerendered.
5. Verify the PSD signature, dimensions, layer count/names and visibility flags, and composite preview. Check that the visible preview matches the brief and that every requested exact text string is legible and spelled correctly.
6. If Photoshop is installed and desktop control is available, verify the actual target window, open the exact output PSD, inspect the visible artwork and layer visibility in its stack, and save/reopen it if you changed it in Photoshop. Do not treat an installed executable, splash screen, or a successful binary check as proof that Photoshop opened the deliverable.

## Editable text and format limits

The bundled builder renders manifest `text` entries into independent transparent pixel layers. These layers can be moved, hidden, replaced, or rerendered, but the words cannot be edited with Photoshop's Type tool. Describe them as raster text layers, not editable text.

If the user needs to change wording directly in Photoshop, create one native Type layer per exact text block using an available Photoshop UXP script or desktop-control route. Photoshop 24.2 and later expose `Document.createTextLayer`; UXP scripts use the `.psjs` extension and can run from **File > Scripts > Browse**. See [Adobe's UXP scripting guide](https://developer.adobe.com/photoshop/uxp/scripting/) and [text layer creation options](https://developer.adobe.com/photoshop/uxp/ps_reference/objects/createoptions/textlayercreateoptions/). Preserve exact copy, assign descriptive layer names, and adjust the text positions and styles to match the approved composition. Hide or remove the matching rasterized copy layer to prevent duplicate text. The font installed on the machine and Photoshop's text metrics may differ from the Pillow preview, so inspect the Photoshop rendering rather than assuming pixel-identical placement.

Before claiming native text editing, verify that each requested text block is a Type layer in Photoshop, that the visible copy is exact, and that the saved PSD reopens with those layers intact. If Photoshop cannot be controlled in this session, use the bundled writer and state clearly that text is rasterized; include the exact copy in the manifest so it can be changed and rerendered.

The bundled writer supports standard RGB, 8-bit PSD documents with independent raster layers. If the brief requires vector shape layers, live type, smart objects, CMYK, or other unsupported Photoshop-specific structures, use a capable native editor if available; otherwise state the limitation clearly and still deliver the best valid layered PSD possible.

The bundled writer requires Python 3 and Pillow. If Pillow is unavailable, use an already available PSD-capable editor or explain the dependency before attempting another route.

## Bundled writer

Run from this skill directory or pass absolute paths:

```powershell
python psd-layered-design/scripts/build_psd.py --manifest path\to\layers.json --output path\to\design.psd --preview path\to\preview.png
```

Manifest schema: `canvas` is `[width, height]`; `layers` are ordered bottom-to-top. Each item has `name` and either an image `file` plus optional `x`, `y`, or a `text` string plus optional `x`, `y`, `font`, `font_size`, `color`, and `align`. Image assets may be RGBA transparent cutouts or full-canvas RGB/RGBA images. Text defaults to a suitable installed font. Every layer is clipped to the canvas.
