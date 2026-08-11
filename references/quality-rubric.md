# Prompt and Result Quality

## Contents

- Prompt preflight
- Generated-image result gates
- Hard failures
- Targeted revision rule
- Delivery contract

## Prompt Preflight

Score each dimension from 0 to 2 before generation. Require at least 20/22 and no zero on ranked invariants, skin identity when applicable, semantic compression, Fade destruction, primary-route fit, physical motivation, palette reconstruction, transformation visibility, or invention control.

### 1. Ranked Source Invariants

- **2:** Ranks two to four hero-critical items and makes lower priorities explicitly expendable.
- **1:** Preserves the hero but lists invariants without a clear priority or protects one unnecessary background feature.
- **0:** Allows subject replacement, semantic rewriting, or hero-geometry drift; or locks the full background, source crop, and source aspect ratio without a user request.

Repair: move the hero invariants to the first sentence, remove location-only details from that list, and repeat only hero-critical constraints in rendering rules.

### 2. Human Skin Identity

- **2:** When skin is visible, locks source-relative complexion lightness, undertone, apparent age, and softness while isolating it from the environment grade; otherwise marks this dimension not applicable and awards 2.
- **1:** Preserves generic skin tone but does not explicitly control lightness, age impression, or microtexture.
- **0:** Allows darker, tanned, redder, grayer, older, coarser, or ethnically different-looking skin; or equates subject clarity with enhanced pores, wrinkles, veins, and creases.

Repair: state the observed source skin baseline, grade the environment around it, and preserve soft skin tonal transitions with only restrained colored edge reflections.

### 3. Semantic Compression

- **2:** Uses clear Keep / Fade / Remove decisions and keeps no more than two readable context cues by default.
- **1:** Simplifies the scene but leaves competing detail.
- **0:** Preserves every source object equally or removes all context.

Repair: keep one hero and one essential cue, fade selected secondary forms, and remove only clutter.

### 4. Fade Destruction

- **2:** Named Fade elements are required to lose small-detail readability and collapse into two to four broad directional masses.
- **1:** Fade is named but the degree of simplification is ambiguous.
- **0:** Window grids, secondary building outlines, individual branches or leaves, signs, or surface texture are allowed to remain readable.

Repair: name which readable contours must disappear and what broad direction, mass, or color they become.

### 5. Primary Route Fit

- **2:** Declares exactly one primary mechanism and at most one source-supported mechanism; the primary clearly owns most visible change.
- **1:** Mechanisms are plausible but their visual hierarchy is vague.
- **0:** Treats all diagnostic axes as equal effects, stacks incompatible mechanisms, or selects a conservative fallback that contradicts stronger source evidence.

Repair: diagnose the axes, then choose one dominant mechanism and no more than one support.

### 6. Physical Motivation

- **2:** Motion, haze, reflection, diffusion, and bloom come from visible people, objects, material, depth, or light.
- **1:** Names a plausible effect but does not tie it clearly to the source.
- **0:** Uses magical haze, random petals, invented glass, unexplained duplicates, or global white fog.

Repair: replace abstract dream language with a source-supported camera, material, movement, or light cause.

### 7. Hero Sharpness Island and Three-Layer Motion

- **2:** Defines one contiguous hero sharpness island with a readable contour, material cue, and source-relative exposure floor for the actual hero type; states the motion boundary; and assigns foreground, midground, and background motion outside it with source, direction, scale, and opacity or occlusion whenever supported.
- **1:** Names a stable anchor but leaves its protected area, material cue, exposure floor, or motion boundary ambiguous.
- **0:** Applies equal blur everywhere, lets trails cross the protected hero, preserves only rough geometry while erasing the hero's defining contour and texture, or crushes a source-readable person into a featureless silhouette without explicit reason.

Repair: name the protected continuous region and one texture; preserve skin/light-clothing/dark-clothing planes for people or one readable midtone/material plane for non-human heroes; then move long trails to peripheral, secondary, or background layers.

### 8. Lighting and Palette Reconstruction

- **2:** Uses a credible source light, selects a mood-appropriate dominant field and luminous or contrasting family, retains at most one non-skin identity color, isolates visible skin from the environment grade, requires a visible environmental departure from source white balance, and keeps bokeh, flare, and negative space optically irregular and non-symbolic.
- **1:** Gives a palette but does not require a clear visual change from the source.
- **0:** Keeps nearly the same source palette, creates inconsistent shadows or global overexposure, uses an arbitrary extreme teal-orange grade, or invents heart, star, wing, halo, butterfly, letter, logo, or other semantic light shapes.

Repair: identify the real source light, choose the mood independently, and assign approximate shares such as 60–75% dominant field and 15–30% luminous or contrasting family with neutral support. Do not force amber nostalgia from backlight alone.

### 9. Analog Restraint

- **2:** Uses grain, lower micro-contrast, mild aberration, local halation, and scan texture in moderation.
- **1:** Mentions film texture without controlling intensity.
- **0:** Uses heavy scratches, grunge, giant light leaks, plastic skin, or oversharpened film presets.

Repair: keep texture fine-to-medium and subordinate to the photograph.

### 10. Invention Control

- **2:** Explicitly rejects unrelated people, props, flowers, clothing, jewelry, text, anatomy errors, and logo mutation.
- **1:** Includes generic negatives but misses a source-specific risk.
- **0:** Invites decorative invention or omits identity and geometry constraints.

Repair: add only the negative controls relevant to the observed source.

### 11. Transformation Visibility

- **2:** Requires a clearly visible editorial re-composition through crop, hero scale, directional atmosphere, depth separation, or light flow appropriate to the selected strength.
- **1:** Requests a plausible dreamy treatment but leaves the amount of visual change ambiguous.
- **0:** Allows the original full-scene composition to remain nearly unchanged with only warmer color, reduced contrast, global softness, or tiny decorative streaks.

Repair: name the changed crop or hero scale, assign the selected strength's visual allocation, and state that the result must not read as a light filter pass.

## Generated-Image Result Gates

Inspect the actual generated image, not only the prompt.

### Source Preservation

Pass when the chosen hero remains the same person, relationship, object, flower, structure, or landscape anchor with stable identity, count, pose, anatomy, hero-critical geometry, labels, and native color. Do not require location-only scenery or the source crop to remain exact when people carry the meaning.

### Skin Identity and Age

When skin is visible, pass only when its complexion remains source-relative in lightness and undertone, its apparent age remains stable, and its texture is no coarser than the source. Night color may appear as soft rim or reflected light, but must not globally darken, tan, redden, gray, age, or sharpen the skin.

### Editorial Hierarchy

Pass when one hero dominates, no more than two context cues remain readable, and secondary detail supports rather than competes with the hero.

### Directional Atmosphere

Pass when motion has a coherent direction and depth. When the source supports foreground, midground, and background, all three layers should read at first glance. The result may use fewer layers only when the source lacks material; it must not rely on tiny decorative streaks or uniform blur.

### Hero Sharpness Island

Pass when the hero's defining contour, relationship, repeated rhythm, or structural path is clearly sharper than the surrounding motion field and retains one readable material cue. Motion may frame or pass behind the hero, but must not wash across it. For a walkway, the central surface, inner railing boundaries, luminous fixture cores, and one continuous lamp rhythm must remain legible from foreground toward the vanishing point.

### Hero Exposure Floor

For a source-readable person, pass only when the visible skin base tone, light-garment identity, and at least one dimensional plane in dark clothing remain tonally readable. A backlit rim cannot replace subject exposure. A near-black or featureless silhouette passes only when the source already supports it or the user explicitly requested it.

For a non-human hero, pass only when one defining source-relative midtone or material plane remains readable inside the hero sharpness island. A crisp silhouette without material or tonal separation fails unless the source or user explicitly calls for silhouette treatment.

### Fade Readability

Pass when Fade elements can no longer be inventoried as crisp window grids, secondary building contours, individual branches or leaves, signs, or detailed surface texture. They may remain as broad directional masses, color fields, or partial silhouettes.

### Transformation Visibility

Pass when the result visibly reflects the selected strength. In default `dream-haze`, the hero hierarchy, crop or scale, directional atmosphere, and light flow must be apparent at first glance. A near-literal source reconstruction with a warm grade or generic softness fails even when anatomy and color are technically clean.

### Optical and Lighting Plausibility

Pass when floral diffusion, reflection, halation, or night glow has a visible source and does not conceal the anchor. Bokeh, flare, and illuminated negative space must remain natural, irregular, and non-symbolic; reject invented hearts, stars, wings, halos, butterflies, letters, logos, and similar decorative shapes.

### Color and Texture

Pass when the environment palette is controlled and visibly re-authored relative to the source, protected skin retains its source complexion and age impression, hero materials remain believable, grain and bloom are restrained, and the result does not look like a generic filter. In `dream-haze`, a nearly unchanged environment white balance fails; protected skin is exempt from aggressive palette replacement.

### Invention and Anatomy

Pass when the result contains no unexplained people, flowers, props, clothing, jewelry, text, duplicated faces, extra limbs, fused hands, or warped critical geometry.

## Hard Failures

A generated image fails when any of these appear:

- identity replacement, changed person count, broken anatomy, or lost relationship;
- changed source-relative skin lightness or undertone; darker, tanned, redder, grayer, muddier, older, coarser, or ethnically different-looking skin;
- added or exaggerated pores, wrinkles, veins, creases, dryness, spots, or high-definition skin microcontrast;
- a source-readable person becomes a near-black or featureless silhouette; visible skin base tone, light clothing, or dark-clothing dimensional separation is lost without an explicit silhouette request;
- a source-readable object, flower, structure, or landform becomes a dark cutout with no defining midtone or material plane;
- warped product, label, architecture, perspective, or defining silhouette;
- uniform blur that removes the anchor;
- directional or radial blur, diffusion, reflection, or halation crossing the hero sharpness island;
- a structural hero retaining only a vague silhouette while its central surface, defining edges, luminous cores, or repeated rhythm are smeared away;
- random people, flowers, petals, jewelry, clothing, props, or text;
- heart-shaped bokeh, star shapes, wings, halos, butterflies, letters, logos, or any other invented semantic light or negative-space symbol;
- unexplained face or body duplication;
- global white fog, fantasy particles, plastic skin, or generic beauty retouching;
- static empty background with no directional atmosphere;
- every source object preserved with equal visual weight;
- Fade elements remain readable as crisp window grids, distinct secondary buildings, individual branches or leaves, signs, or surface texture;
- the preservation constraints are flat and force secondary structures to compete with the hero path, relationship, or rhythm;
- default `dream-haze` retains the full source crop and a tiny hero when an editorial reframe is clearly supported;
- the output forces a portrait crop that weakens or clips a clearly horizontal hero, or forces landscape against a clearly vertical hero, without a user request;
- the result is merely warmer, softer, lower-contrast, or more film-like than the source without visible recomposition or directional motion;
- default `dream-haze` retains essentially the same dominant palette or white balance as the source;
- the result introduces an unrequested sunset, nostalgic amber, magenta, or purple cast that conflicts with the selected mood;
- dense typography covering the hero or critical geometry.

## Targeted Revision Rule

If the first result has a hard failure:

1. name the single highest-impact failure internally;
2. repeat all source invariants;
3. issue one targeted revision through the active image-generation route that changes only the failing dimension;
4. inspect the revised image again.

Do not stack multiple new effects during revision. If a hard failure remains after one targeted revision, return the best available result and briefly state the unresolved limitation instead of claiming full success.

## Delivery Contract

### Default

- Before generation, show the process card with `照片诊断`, `构图提炼`, `视觉方案`, and `质量检查通过，开始生成：` in that order for a Chinese request.
- Include Keep / Fade / Remove, skin identity lock when applicable, hero exposure baseline, hero sharpness island, motion boundary, non-symbolic light-shape constraint, motion and quiet-space targets, source-supported depth treatments, hero share and position, primary and support mechanisms, light, color, optical texture, mood, ranked fidelity priority, ratio with a spatial-axis reason, strength, and a physical reason.
- Keep each field to one compact line, omit inapplicable optional fields, and do not expose the full prompt, negative prompt, or scorecard.
- Return the final generated image.
- Add one short sentence naming the composition, motion, optical or lighting direction, and strength.
- Do not show prompts, negative prompts, or scorecards.

### Prompt Requested

- Still generate and return the image unless the user explicitly says not to.
- Show only the requested prompt material.

### Prompts Only

- Do not call an image-generation route.
- Return the Chinese prompt, English prompt, negative prompt, preservation constraints, and aspect-ratio or strength guidance requested by the user.
- Do not attach a placeholder image.
