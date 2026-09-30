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
4. Assemble PNG layers into a PSD using `scripts/build_psd.py`. Provide the PSD, a flattened preview, and a short layer inventory. Keep source assets and a manifest next to the output so text or assets can be replaced and the PSD rebuilt.
5. Verify the PSD signature, dimensions, layer count/names, and composite preview. Check that the visible preview matches the brief and that every requested exact text string is legible and spelled correctly.

## Editable text and format limits

When Photoshop is installed, first verify that this task can actually control its running instance. Prefer Photoshop-native type layers using an available Windows COM/UXP automation route; if only desktop interaction is available, use the computer-control tool. Save to a new PSD copy, reopen it, and verify the exact text and layer stack before claiming success. Photoshop 2024 can run a local `.psjs` script from **File > Scripts > Browse**; see [Adobe's scripting guide](https://helpx.adobe.com/photoshop/using/scripting.html) and [UXP scripting guide](https://developer.adobe.com/photoshop/uxp/scripting/).

An installed app is not proof that the current task has an automation connection. If connection fails or the app cannot be controlled, use the bundled writer and disclose the fallback. Each text block then remains its own transparent raster layer; it can be moved, hidden, replaced, or repainted in Photoshop, but its words are not editable with the Type tool. Include exact copy in the manifest so it can be changed and rerendered. Do not claim native text editing when the PSD contains raster text.

The bundled writer supports standard RGB, 8-bit PSD documents with independent raster layers. If the brief requires vector shape layers, live type, smart objects, CMYK, or other unsupported Photoshop-specific structures, use a capable native editor if available; otherwise state the limitation clearly and still deliver the best valid layered PSD possible.

The bundled writer requires Python 3 and Pillow. If Pillow is unavailable, use an already available PSD-capable editor or explain the dependency before attempting another route.

## Bundled writer

Run from this skill directory or pass absolute paths:

```powershell
python psd-layered-design/scripts/build_psd.py --manifest path\to\layers.json --output path\to\design.psd --preview path\to\preview.png
```

Manifest schema: `canvas` is `[width, height]`; `layers` are ordered bottom-to-top. Each item has `name` and either an image `file` plus optional `x`, `y`, or a `text` string plus optional `x`, `y`, `font`, `font_size`, `color`, and `align`. Image assets may be RGBA transparent cutouts or full-canvas RGB/RGBA images. Text defaults to a suitable installed font. Every layer is clipped to the canvas.
