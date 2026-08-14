# dreamy-photo · Dreamify a photo with one short request

![AI Skill](https://img.shields.io/badge/AI-Skill-111111?style=flat-square)
![Photo Editing](https://img.shields.io/badge/Photo-Dreamy%20Editing-2563EB?style=flat-square)
![Codex](https://img.shields.io/badge/Codex-Supported-222222?style=flat-square)
![OpenClaw](https://img.shields.io/badge/OpenClaw-Supported-0F766E?style=flat-square)
![Image Generation](https://img.shields.io/badge/Image%20Generation-Built--in-7C3AED?style=flat-square)
![License](https://img.shields.io/badge/License-MIT--0-D97706?style=flat-square)
![GitHub](https://img.shields.io/badge/GitHub-Jiaranbb-181717?style=flat-square&logo=github&logoColor=white)

[中文 README](README.md) · [30-second start](#30-second-start) · [Examples](#examples) · [FAQ](#faq) · [Contact](SUPPORT.md)

**Author / publisher**: [Jiaranbb](https://github.com/Jiaranbb) · **Support and feedback**: [SUPPORT.md](SUPPORT.md)

`dreamy-photo` is an AI Skill that quickly turns an existing photo into a dreamy, cinematic, or long-exposure-style edit. After the user supplies a photo, the AI identifies its subject, applies directional motion, optical bloom, color reconstruction, and film texture, preserves authentic subject details from the source, and returns the finished image.

> Send a photo and say “Make it dreamy”; the AI edits it and returns the image.

It is for Codex, OpenClaw, and other image-capable Agent users who want stronger atmosphere in travel, portrait, night-city, landscape, architecture, or still-life photographs without sacrificing identity, skin tone, key structures, or important relationships from the source.

## Examples

![Harbour bridge before and after](assets/examples/harbour-bridge-before-after.jpg)

![Lakeside pavilion before and after](assets/examples/lakeside-pavilion-before-after.jpg)

![Summer tree before and after](assets/examples/summer-tree-before-after.jpg)

The example images were provided by Jiaranbb and authorized for public display in this project. They were generated with ChatGPT Image. Image generation is stochastic, so results vary with the source, model capability, and generation pass.

You can also ask the Skill to show its prompt, then manually submit that prompt to Midjourney or another third-party image platform. Third-party results depend on the platform’s model and reference-image support.

## 30-second start

Send this instruction directly to Codex, OpenClaw, Claude Code, WorkBuddy, or another Agent that supports Skills:

```text
Install the dreamy-photo Skill from GitHub: https://github.com/Jiaranbb/dreamy-photo. When installation is complete, remind me to restart or refresh the Agent as required so the new Skill becomes active.
```

If your environment supports the `skills` CLI, you can also run:

```bash
npx skills add https://github.com/Jiaranbb/dreamy-photo --skill dreamy-photo
```

Codex users can install it manually:

```bash
python3 ~/.codex/skills/.system/skill-installer/scripts/install-skill-from-github.py \
  --repo Jiaranbb/dreamy-photo \
  --path . \
  --name dreamy-photo
```

After installation, restart or refresh the Agent as required so the new Skill becomes active.

## Highlights

- **Automatic subject recognition** identifies the people, actions, objects, structures, and relationships that must remain unchanged and gives them the highest fidelity priority.
- **Automatic composition and color direction** selects framing and palette from the subject axis, source light, and native colors to build atmosphere instead of forcing one fixed grade.
- **Layered motion depth** separates foreground sweeps, midground trails, and background light-color flow while preserving a clear subject island, so the entire image is not blurred uniformly.
- **Portrait-specific protection** locks source-relative skin brightness, undertone, apparent age, and softness for faces, hands, and visible skin, preventing darker, rougher, or older-looking skin after the edit.

## Six built-in visual mechanisms

The Skill selects one primary mechanism and no more than one supporting mechanism from materials that actually exist in the source, such as people, flowers, glass, practical lights, viewpoint, or motion-sensitive objects. It does not invent missing elements merely to force a preset look.

| Mechanism | Name | Best source conditions |
|---|---|---|
| `crowd-drift` | Crowd Drift | People, public passages, walkways, traffic, or repeated lights that support long-exposure depth |
| `floral-diffusion` | Floral Diffusion | Existing flowers, foliage, or plants that can become a soft foreground diffusion layer |
| `glass-memory` | Glass Memory | Existing glass, windows, mirrors, or credible reflections that support layered memory-like echoes |
| `backlit-halation` | Backlit Halation | Backlight, light through foliage, bright sky openings, or practical fixtures that support bloom and light leakage |
| `low-angle-color-field` | Low-Angle Color Field | A low viewpoint with a large sky, wall, or color plane that can form a poster-like spatial field |
| `passing-gesture` | Passing Gesture | Hair, fabric, hands, paper, or foliage that can create a directional passing sweep |

## Use it like this

After installation, attach a photo and say:

```text
Make it dreamy.
```

By default, the Skill shows a concise diagnosis and visual plan, invokes the current platform’s available image-generation route, and returns the image. It does not expose the full prompt unless requested.

For prompt-only output, say:

```text
Give me only the dreamy-edit prompt for this photo. Do not generate an image.
```

## Suitable / not suitable

**✅ Suitable**

- Dreamy, cinematic, or long-exposure-style edits of an existing photograph.
- Stronger color and atmosphere while preserving the subject and structural anchors.
- Travel, portrait, city-night, landscape, still-life, and architecture photographs.
- Workflows where the Agent should generate and return the image by default.

**❌ Not suitable**

- General image generation without a source image.
- Routine retouching, blemish removal, cutouts, or simple white-balance correction.
- Prompt writing unrelated to dreamy photo editing.
- Pixel-exact reproduction, forensic preservation, or deterministic output.

## Common scenarios

| Task | Suggested request |
|---|---|
| Landscape | `Keep the landscape orientation and give this photo a bright summer-breeze treatment.` |
| City at night | `Strengthen the cool-blue environment and warm-gold lights; turn secondary buildings into directional light flow.` |
| Portrait | `Preserve identity, skin tone, and pose; apply dreamy motion only to the background.` |
| Still life | `Keep the subject material readable and use nearby reflections to build soft color flow.` |
| Analysis only | `Analyze a dreamy-edit direction and show the prompt, but do not generate an image.` |

## Platform support

| Platform | Status | Notes |
|---|---|---|
| Codex | Supported | Recommended; uses built-in `image_gen` to inspect, edit, and return images |
| OpenClaw | Supported | Uses built-in `image_generate`; requires a configured image-generation model |
| Claude Code | Adaptable | Its built-in image output is often weaker; adapt it to call Codex CLI for generation |
| WorkBuddy | Conditional | Select a model with image generation and reference-image editing; text-only models such as DeepSeek cannot complete the edit, and quality depends on the chosen image model |

## Workflow

1. Diagnose the subject, fidelity priorities, risks, lighting, spatial direction, and usable motion material.
2. Establish Keep / Fade / Remove, a subject clarity island, an exposure baseline, and motion boundaries.
3. Choose one primary mechanism and no more than one supporting mechanism.
4. Select aspect ratio from the subject axis and composition instead of forcing a portrait crop.
5. Choose color direction separately from the lighting mechanism.
6. Generate, then inspect identity, skin tone, exposure, structure, color cast, blur extent, and accidental symbols.
7. If a hard failure remains, make one targeted revision for the highest-impact issue.

## Optional strategy helper

`scripts/analyze_photo.py` does not inspect pixels. It converts human observations into a structured recommendation:

```bash
python3 scripts/analyze_photo.py \
  --subject landscape \
  --light hard-sun \
  --background nature \
  --subject-axis horizontal \
  --mood summer-breeze \
  --strength dream-haze \
  --json
```

List all options:

```bash
python3 scripts/analyze_photo.py --help
```

## Privacy and external requests

| Data or action | Processing location | Notes |
|---|---|---|
| Observation parameters passed to `analyze_photo.py` | Local machine | The script does not access photo pixels or the network |
| User-provided photo | The current Agent and selected image-generation service | The source must be processed to perform the edit |
| Generated image | Agent task or a user-selected location | Retention depends on platform and user choices |
| API keys, cookies, account credentials | Not required | The Skill does not read them |

Follow the terms of the Agent and image-generation services when processing faces, private scenes, or other sensitive images. Never add private test photos, task attachments, or generated results to a public repository.

## Limitations and quality notes

- Image generation is stochastic; the same source and plan can produce different compositions or details.
- Faces, hands, text, logos, repeated structures, and strong perspective can still drift.
- Negative instructions cannot guarantee that decorative symbols will never appear, so inspect the actual output.
- The Skill can constrain art direction but cannot make model versions behave identically.
- For important portraits, explicitly inspect identity, skin tone, apparent age, hands, and subject exposure.

## FAQ

**Why does it generate an image instead of only showing a prompt?**

The Skill is designed to complete the edit. It diagnoses the source, selects a visual plan, invokes the current platform’s available image-generation route, and returns the result. The full prompt is shown only when requested.

**Why not blur the entire photograph?**

Dreaminess depends on contrast between a readable subject and a more fluid environment. The Skill keeps a subject clarity island and places motion mainly in secondary backgrounds, frame edges, and physically credible light sources.

**Can it preserve landscape or portrait orientation?**

Yes. It infers a suitable aspect ratio from the subject axis and composition. State “keep landscape,” “keep portrait,” or a specific ratio when framing is critical.

**Can a person’s skin tone, apparent age, or identity change?**

The Skill treats those as high-priority fidelity constraints, but model drift remains possible. Every portrait result must be inspected and, if necessary, revised specifically for identity and skin tone.

**Why do hearts or other decorations sometimes appear?**

Models can interpret “dreamy” or “romantic” as graphic decoration. The Skill explicitly rejects hearts, stars, stickers, text, and symbols and checks the output, but negative constraints are not absolute guarantees.

**Why do repeated runs differ?**

Image generation is stochastic. Fidelity priorities, mechanisms, color direction, and motion range constrain the result but do not lock every pixel.

**How do I update the Skill?**

If you installed from a Git clone, pull the latest version, reinstall or resync it using the current Agent’s Skill workflow, and then restart or refresh the Agent.

## Validation

```bash
python3 -m py_compile scripts/analyze_photo.py
python3 -m unittest discover -s tests -v
python3 scripts/analyze_photo.py --help
```

Structural validation uses the validator bundled with Codex’s `skill-creator` Skill.

## Related projects

- [ecommerce-helper](https://github.com/Jiaranbb/ecommerce-helper) — a complete e-commerce asset-pack Skill from new-product research and RMB pricing to PDP and social content;
- [report-helper](https://github.com/Jiaranbb/report-helper) — long-form, source-linked research reports and polished PDFs from one request;
- [content-reader](https://github.com/Jiaranbb/content-reader) — agent skills for saving Xiaohongshu, Twitter/X, YouTube, and Bilibili content;
- [xhs-reader](https://github.com/Jiaranbb/xhs-reader) — save Xiaohongshu posts locally without logging in;
- [pdf-reader](https://github.com/Jiaranbb/pdf-reader) — convert PDFs into Markdown with page markers and quality metrics;
- [autoskin-codex](https://github.com/Jiaranbb/autoskin-codex) — preview-first, reversible themes for the Codex desktop app;
- [jiucai-helper](https://github.com/Jiaranbb/jiucai-helper) — a testable personal investment-decision Skill combining method and discipline.

See more original projects on [Jiaranbb's GitHub profile](https://github.com/Jiaranbb?tab=repositories).

## About the author

**Jiaran (Jiaranbb)** — independent developer / AI Builder

I turn workflows I genuinely need into reusable AI tools and Skills.

- Website: [c.aoao.ai](https://c.aoao.ai)
- GitHub: [github.com/Jiaranbb](https://github.com/Jiaranbb)
- X/Twitter: [@_jiaran](https://x.com/_jiaran)
- WeChat: `evadebot`
- WeChat official account: **嘉然学习笔记**
- Support: [SUPPORT.md](SUPPORT.md)
- Project issues: [GitHub Issues](https://github.com/Jiaranbb/dreamy-photo/issues)

## License

MIT-0 License. See [LICENSE](LICENSE).

Copyright 2026 [Jiaranbb](https://github.com/Jiaranbb).
