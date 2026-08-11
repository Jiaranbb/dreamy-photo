# Prompt Recipes

## Contents

- Prompt visibility contract
- Process card
- Required prompt order
- Chinese template
- English generation template
- Negative prompt
- Preservation add-ons
- Strategy modules
- Worked examples
- Optional poster module

## Prompt Visibility Contract

Always build an internal image-to-image prompt before generation.

- Show the compact process card before generation, including summarized Keep / Fade / Remove decisions and the selected visual mechanisms.
- Do not show the full prompt, negative prompt, preflight scorecard, or hidden rendering constraints by default.
- If the user asks to see the prompt, generate the image and include only the requested prompt material.
- If the user explicitly asks for prompts only or says not to generate, return the prompt package and do not call an image-generation route.
- Use the English template as the built-in generation brief unless the current tool or user explicitly requires another language.

## Process Card

For a Chinese request, show this structure immediately before calling the active image-generation route:

```text
**照片诊断**
主体：【一句话】
必须保留：【只列主体语义不变量】
可利用的光线/动态/前景：【真实存在的素材】
风险：【身份、肢体、文字、Logo、结构等】

**构图提炼**
Keep：【主体、关键关系或物体、原生强调色、最多两个线索】
Fade：【转化为动态氛围的次要层】
Remove：【不影响故事的细节】
肤色身份锁定：【有可见皮肤时填写：源图肤色明度、冷暖底色、年龄感和柔和度】
主体曝光基线：【人物填写源图中必须继续可读的肤色基底、浅色衣物和暗色衣物层次；非人物填写一个必须继续可读的中间调或材质面；仅在源图或用户要求时允许剪影】
主体清晰岛：【必须保持可读的连续区域、轮廓与一种材质细节】
动态边界：【拖影、光晕和扩散允许出现的位置；不得跨越主体清晰岛】
动态覆盖：【目标比例】
安静留白：【目标比例】
前景掠影：【源图支持时填写】
中景拖影：【源图支持时填写】
背景光色流：【源图支持时填写】
光斑形状约束：【保持自然、不对称、不规则、无定形、无可识别语义；生成提示中不枚举禁用符号名称】
主体占比与位置：【目标视觉权重和位置】

**视觉方案**
主机制：【机制及其来源】
辅助机制：【可选机制；不需要时写无】
强度：【克制高级／梦幻朦胧／实验记忆】
选择理由：【一句物理可信的理由】
三层运动景深：
- 前景掠影：【来源、方向、尺度、遮挡或透明度】
- 中景拖影：【来源、方向、尺度、透明度】
- 背景光色流：【来源、方向、融合程度】
光线：【主光源、光晕、光泄漏和暗部处理】
色彩：【重构后的环境底色、发光色、身份色及大致占比】
光学质感：【慢门、颗粒、微对比度、色散、暗角】
整体情绪：【一句情绪方向】
保真优先级：【从高到低排列；只把前 2–4 项当硬约束】
建议参数：比例【比例】；重绘强度【强度】
比例理由：【主体的水平／垂直／均衡空间方向，以及为何该画幅不会削弱主体】
输出：【比例、摄影写实和禁止新增内容】

质量检查通过，开始生成：
```

Keep the card observational and concise. It is not the prompt and must not expose negative-prompt dumps or internal score calculations.

## Required Prompt Order

Write the internal prompt in this order:

1. ranked source invariants;
2. skin identity lock when people are visible and a hero exposure floor for every hero type;
3. hero sharpness island, motion boundary, and non-symbolic light-shape constraint;
4. Keep / Fade / Remove and a requirement that Fade lose readability;
5. visible transformation mandate;
6. composition strategy and output ratio;
7. three-layer motion-depth design;
8. one primary mechanism and at most one support mechanism;
9. lighting treatment;
10. visible palette reconstruction;
11. analog texture;
12. emotional tone;
13. rendering constraints.

Begin with what must remain unchanged, not with adjectives such as `beautiful`, `dreamy`, or `cinematic`.

Only protect hero-critical invariants. Do not preserve background geometry, landmarks, the source crop, or the source aspect ratio unless the background is itself the hero or the user explicitly requests fidelity. Do not invent objects merely to satisfy a style module.

## Chinese Image-to-Image Template

```text
按以下优先级保留原照片：【第 1 优先级】＞【第 2 优先级】＞【第 3 优先级】＞【可牺牲的第 4 优先级】。只把前 2–4 项视为硬约束，不把整张照片的结构和细节等量锁定。保持【身份／姿态／人数／关键关系／核心结构路径】不变，不替换主体，不新增无关人物或物体。

若有可见皮肤，锁定源图中可观察到的【肤色明度、冷暖底色、年龄感和柔和度】。综合色调主要重构环境；皮肤只接受克制的环境边缘反光，不得整体变黑、晒黑、发红、发灰、改变人种观感或增加年龄感。主体清晰表示轮廓和动作清楚，不表示强化毛孔、皱纹、血管、褶皱、斑点和干燥纹理。

锁定主体曝光基线。人物需让【源图中可读的肤色基底、浅色衣物和暗色衣物层次】继续可辨；物体、花卉、建筑或风景需保留【一个源图可读的中间调或材质面】。除非源图本身就是剪影或用户明确要求，不得把主体压成无细节黑影，不得用主体欠曝来换取逆光氛围。

建立主体清晰岛：【连续区域】。其中【定义性轮廓】和【一种身份／材质细节】必须可读，清晰度明显高于周围动态氛围。拖影、扩散、反射和光晕只能位于【允许区域】，可以框住主体、从主体后方经过或从边缘发出，但不得横穿或洗掉主体清晰岛。动态覆盖比例表示画面视觉权重，不表示可以模糊同等比例的主体。

先进行语义提炼：Keep【唯一主体或结构路径、关键动作／物体／重复节奏、最多一个身份色】；Fade【可转化为氛围的次要人物、建筑、家具、车辆、树叶、纹理或灯光】；Remove【无关小物件、重复人物、高对比杂乱元素和多余颜色】。Fade 中的窗格、建筑轮廓、枝叶、标牌和表面纹理必须失去可盘点的清晰度，只保留方向、体量和色彩，并归并为 2–4 个大面积动态色块。

必须形成清晰可见的编辑重构，不能只是原图加暖色、降对比、全局柔焦或普通胶片滤镜。

构图：【source-led-asymmetry／geometry-preserving-frame／low-angle-color-field】，主体空间方向为【水平／垂直／均衡】，输出【画幅比例】。允许重新裁切、放大核心、简化背景；只有用户明确要求时才保持原比例，但不得仅因源图较宽或主体较小就强制竖裁。视觉分配为【主体 x%／动态氛围 y%／安静留白 z%】。

三层运动景深：前景【来源、方向、尺度、遮挡及与清晰岛的边界】；中景【来源、方向、尺度、透明度及与清晰岛的边界】；背景【来源、方向、融合程度】。只让原照片中存在的次要形体、建筑边缘、色块或灯光形成统一方向的慢门氛围，不让整张照片均匀模糊。空栈道、走廊、站台或桥梁可利用透视和重复灯光暗示人流经过，但中央路径、内侧栏杆边界、灯具发光核心和一条连续灯序列必须保持可读，不得新增人物。

主机制：【一个主机制】，负责画面绝大多数可见变化。辅助机制：【无或一个辅助机制】，只加强空间或运动，不与主机制争夺视觉主导。两者必须由原图的真实光源、透视、材质或运动线索支持。

光线：从【真实光源】出发形成【光晕、光泄漏、局部光束】，但保留小而清晰的发光核心和光源身份；暗部保留【有颜色的层次】，不制造全局白雾。路径灯、地灯和边缘灯可以直接作为 Backlit Halation 的发光源。

光斑、光泄漏和负空间必须保持自然、不对称、不规则、无定形、无可识别语义，像真实镜头中的连续光学能量而不是装饰图标。生成提示中不要枚举禁用符号名称，以免形成词语诱导；具体符号只在成图质检阶段识别和拒绝。

色彩重构：先选择【源色提炼／盛夏风感／金色回忆／蓝调时刻／夜间疏离／用户指定方向】。让【主环境色场】占约【60–75%】，让【发光或对比色族】占约【15–30%】，其余为中性支撑；只保留【一个身份色】。色温关系可以是冷暖、冷冷或暖中性，不能把逆光自动翻译成蜂蜜金、黄昏或怀旧。结果必须明显偏离原图白平衡和杂色分布，但可见皮肤属于受保护身份色，不跟随环境整体换色或降明度。

质感：使用真实慢门拖影、镜头扩散、浅景深或可解释反射；加入细到中等胶片颗粒、较低数码微对比度、轻微色散、克制暗角和扫描胶片质感。

情绪：【朦胧记忆／青春残影／诗意疏离／安静孤独】。梦幻但不奇幻，像偶然捕捉到的一帧旧电影。若强度为梦幻朦胧，主动态必须明显，不能用大量“轻微、柔和、克制”把它削弱成保守调色。

输出：【画幅比例】，摄影写实，主体可辨认，肢体结构正确，文字与标志准确；不得新增人物、花朵、首饰、服装、道具或文字。
```

## English Generation Template

```text
Preserve the source in this descending order: [priority 1] > [priority 2] > [priority 3] > [sacrificable priority 4]. Treat only the first two to four items as hard constraints; do not lock all visible structures and detail equally. Keep [identity, pose, person count, essential relationship, or core structural path] unchanged. Do not replace the hero or invent unrelated people or objects.

When human skin is visible, lock its observed source-relative complexion lightness, undertone, apparent age, and softness. Rebuild the environment palette around it. Skin may receive restrained blue or amber edge reflections, but must not become globally darker, tanned, redder, grayer, older, or ethnically different in appearance. Subject clarity means readable anatomy and gesture, not added pores, wrinkles, veins, creases, spots, dryness, or gritty micro-contrast.

Lock the hero exposure floor. For people, preserve the source-readable skin base tone, light garment identity, and dimensional separation in dark clothing. For objects, flowers, structures, and landscapes, preserve one source-readable midtone or material plane. Unless the source is already a silhouette or the user explicitly requests one, do not turn a readable hero into a featureless or near-black cutout and do not underexpose it to manufacture backlit mood.

Define the hero sharpness island as [one contiguous protected region]. Keep [defining contour] and [one identity or material texture] readable and decisively sharper than the surrounding motion field. Motion, diffusion, reflection, and halation may frame, pass behind, or originate beside this island but must not sweep across or wash it out. Kinetic percentage describes compositional visual weight, not permission to blur the same percentage of the hero.

Compress the scene into Keep / Fade / Remove. Keep [the single hero or structural path, essential action/object/repeated rhythm, and at most one identity color]. Fade [source-supported secondary people, architecture, furniture, vehicles, foliage, texture, or light]. Fade elements must lose inventory-level readability: dissolve window grids, building contours, individual branches or leaves, signs, and surface texture into two to four broad directional motion or color masses. Remove [unrelated small objects, duplicates, high-contrast clutter, and excess color accents].

Create a clearly visible editorial re-composition, not the original scene with only warmer color, reduced contrast, global softness, or a generic film filter.

Composition axis: [source-led-asymmetry / geometry-preserving-frame / low-angle-color-field]. The hero's dominant spatial axis is [horizontal / vertical / balanced]. Permit a changed aspect ratio, edge crop, larger hero scale, and background reconstruction unless the user explicitly requests the source ratio, but never force portrait solely because the source is wide or the hero is small. Output at [aspect ratio]. Use an approximate visual allocation of [hero x% / kinetic atmosphere y% / quiet space z%]. Preserve hero semantics and hero-critical geometry, not every background edge.

Three-layer motion depth: foreground [source, direction, scale, occlusion, and boundary from hero island]; midground [source, direction, scale, opacity, and boundary from hero island]; background [source, direction, degree of fusion]. Apply directional motion only to existing secondary figures, forms, architectural edges, color, or light. An empty walkway, corridor, platform, or bridge may imply Crowd Drift through its perspective and repeated lights, but do not add people. Keep the central path, inner railing boundaries, luminous lamp cores, and one continuous lamp rhythm readable. Never blur the whole frame uniformly.

Primary mechanism: [one mechanism], responsible for most of the visible change. Support mechanism: [none or one mechanism], used only to deepen movement or space. Tie both to observed light, perspective, material, or movement.

Lighting: build from [observed source], create [halation, leakage, or local beams] around a small readable luminous core, retain chromatic shadow detail, and avoid global white fog. Visible path, edge, or ground fixtures may directly drive Backlit Halation, but the fixture identity must not dissolve completely.

Keep bokeh, light leaks, lens flare, and illuminated negative space natural, asymmetrical, irregular, amorphous, continuous, and non-semantic, like optical energy rather than designed decoration. Do not enumerate forbidden symbol names in the generation brief; reserve specific symbol recognition for result QA.

Palette reconstruction: choose [source-led / summer-breeze / golden-memory / blue-hour / night-solitude / user-specified direction]. Use [dominant environmental field] for roughly [60–75%], [luminous or contrasting family] for [15–30%], and neutral support for the remainder. The temperature relationship may be cool-warm, cool-cool, or warm-neutral; backlight does not automatically mean amber nostalgia. Preserve at most one native identity color in addition to protected human skin. The environment must visibly depart from the source white balance, but skin must preserve source-relative brightness, undertone, apparent age, and soft tonal transitions.

Texture: physically believable slow-shutter drag, lens diffusion, shallow depth, or explainable reflection; fine-to-medium film grain, reduced digital micro-contrast, mild chromatic aberration, restrained vignette, and subtle scanned-film texture.

Emotional tone: [fragmented memory / youthful transience / poetic distance / quiet loneliness]. Premium and dreamlike but not fantasy; an accidentally captured frame from an old film rather than a generic social-media filter. In dream-haze mode, keep the main motion unmistakable and do not dilute it with repeated subtle, gentle, mild, or restrained wording.

Output: [aspect ratio], photographic realism, recognizable hero, correct anatomy and geometry, accurate text and logos, no invented people, flowers, jewelry, clothing, props, or text.
```

## Negative Prompt

Use only the exclusions relevant to the source:

```text
identity drift, different person, face replacement, altered age, altered ethnicity, changed complexion lightness, darkened skin, tanned skin, reddened skin, gray skin, muddy skin, age progression, coarse skin, gritty hand texture, exaggerated wrinkles, exaggerated veins, enlarged pores, deepened creases, added age spots, crushed hero exposure, near-black person, featureless silhouette without request, lost light garment identity, lost dark-clothing tonal separation, crushed non-human hero midtones, unreadable hero material plane, duplicated subject, changed person count, extra limbs, extra fingers, fused hands, broken anatomy, warped product geometry, unreadable label, warped hero perspective, blur crossing the hero sharpness island, softened defining hero contour, smeared hero surface, radial zoom blur through the subject, dissolved lamp cores, broken continuous lamp rhythm, equal protection of every structure, readable Fade elements, crisp window grids, distinct secondary building contours, individually readable leaves and branches, literal full-scene reconstruction, unchanged tiny hero, forced portrait crop against horizontal subject direction, source-crop lock without request, source-like white balance, source-like palette, weak palette hierarchy, unrequested nostalgic amber cast, unrequested magenta or purple cast, weak transformation, mere warm color grade, generic soft-focus filter, busy equal-detail background, static empty background, uniform Gaussian blur, hero fully out of focus, unexplained duplicates, excessive fog, global white haze, fantasy sparkles, recognizable icon-like bokeh, semantic light glyphs, figurative negative-space shapes, isolated magenta decorative marks, random flowers, random petals, invented people, invented jewelry, invented clothing, invented props, invented text, plastic skin, waxy beauty retouching, HDR halos, crunchy clarity, extreme teal-orange grade, cyberpunk neon, cheap wedding photography, cosplay, stock-photo smile, heavy grunge, giant fake light leak, watermark, logo mutation
```

## Preservation Add-Ons

### Portrait

```text
Preserve exact facial proportions, eye spacing, nose and mouth shape, hairstyle, age, skin tone, expression, pose, and clothing. Keep one face plane readable and place motion in secondary layers.
```

### Visible Skin or Hand

```text
Preserve the source-relative complexion brightness, undertone, apparent age, and skin softness. Keep anatomy, gesture, nail shapes, and jewelry placement readable without increasing pores, wrinkles, veins, creases, dryness, spots, or micro-contrast. Apply the new palette to the environment; allow only restrained colored edge reflections on skin.
```

### Couple or Group

```text
Preserve the number of people, each identity, relative height, spacing, gaze, and interaction. Do not merge bodies or duplicate faces. Keep one shared gesture or central relationship as the anchor.
```

### Product or Object

```text
Preserve silhouette, proportions, materials, label placement, typography, logo geometry, and functional details. Place motion and bloom outside critical edges and text.
```

### Architecture

```text
Rank structural fidelity. Preserve only the hero path, vanishing perspective, defining silhouette, or repeated rhythm required for recognition; treat secondary buildings, openings, window grids, materials, and vegetation as Fade unless the user requests documentary fidelity. Apply motion to light and noncritical layers rather than bending the top-priority structure.
```

### Flower or Plant

```text
Preserve species cues, petal-count impression, stem direction, and native color. Keep one blossom center or petal edge readable while existing foreground blooms dissolve optically.
```

## Strategy Modules

### Composition

- **source-led-asymmetry:** Reframe from the source viewpoint, place the hero off-center, crop noncritical edges, and create one directional path into quiet space.
- **geometry-preserving-frame:** Keep critical silhouette, perspective, labels, and recognition edges stable; simplify or move atmosphere outside them.
- **low-angle-color-field:** Use an existing open sky or wall as a broad photographic color field without inventing a new viewpoint the source cannot support.

### Motion

- **crowd-drift:** Keep the hero path stable while existing passersby, traffic, or the implied flow of an empty public corridor, walkway, platform, bridge, railing, and repeated light sequence forms directional slow-shutter trails. Never add people to an empty source.
- **passing-gesture:** Use one real nearby hand, fabric edge, hair strand, paper, foliage, water, or light edge as a local directional veil.
- **source-layer-drift:** Stretch existing background edges, architecture, color, foliage, reflections, or light into directional atmosphere without adding new objects.

### Optical

- **floral-diffusion:** Use only existing flowers or foliage as near-lens color veils; preserve one readable blossom, face plane, or gesture.
- **glass-memory:** Use one real reflective surface to create a controlled overlap; preserve perspective, face count, and limb structure.
- **none:** Keep the optical layer absent and rely on motion, depth, light, and texture.

### Lighting

- **source-light-bloom:** Preserve the observed direction and soften only real highlights.
- **backlit-halation:** Bloom existing rim light, window light, hard sun, a credible bright opening, or visible path, edge, and ground fixtures.
- **night-color-glow:** Stretch real night lights into restrained colored trails while keeping shadows chromatic.

## Worked Examples

### Flat Indoor Selfie

- Composition: source-led-asymmetry.
- Motion: passing-gesture using an existing hair, fabric, paper, plant, or light edge.
- Optical: none unless a visible mirror or window reflection exists.
- Lighting: source-light-bloom or backlit-halation only when a real window supports it.
- Strength: dream-haze, reduced to restrained-premium when facial recognition is fragile.

### Backlit Street Portrait

- Composition: source-led-asymmetry.
- Motion: crowd-drift when passersby or traffic exist; otherwise source-layer-drift.
- Optical: none unless visible glass or foliage supports a layer.
- Lighting: backlit-halation.
- Keep the face plane and body count stable.

### Couple on a Bench in a Wide Landscape

- Keep: the same two people, their relative seated positions, affectionate leaning gesture, recognizable clothing or hat, and the bench as the essential shared object.
- Fade: mountains, tree lines, sky, field texture, foreground grass, overhanging foliage, and trunk into a few broad directional depth layers.
- Remove: tiny distant structures, signs, and location-specific clutter that do not affect the relationship.
- Composition: source-led-asymmetry; when the couple is small, prefer a 4:5 or 3:4 editorial crop with the couple around 30% of the visual weight, low and off-center.
- Motion: source-layer-drift using real overhanging foliage, field texture, clouds, and distant color boundaries as large directional motion masses.
- Optical: none, or floral-diffusion only when existing near-lens foliage can form a credible veil.
- Lighting: backlit-halation when a bright sky opening filters through the canopy; amplify that opening into honey-gold bloom while keeping cooler shadow depth.
- Strength: dream-haze with about 45% kinetic atmosphere and 25% quiet space. The result must read as a poetic re-composition, not a preserved landscape with a warm filter.

Expected process card for this pattern:

```text
**照片诊断**
主体：一对情侣背坐长椅，女生戴草帽倚向男生
必须保留：两人背影轮廓、坐姿关系、草帽、长椅、倚靠手势
可利用的光线/动态/前景：树冠透光、草帽边缘、前景草地、远处丘陵
风险：无正面时背影身份风险较低；检查人数、肢体和长椅结构；无文字或 Logo 时无需文字保护

**构图提炼**
Keep：情侣背影轮廓、长椅、草帽、倚靠姿态、金棕色草地色
Fade：远处树木、丘陵、天空云、前景草丛、树干树枝
Remove：山顶小建筑、杂乱细节
动态覆盖：约 45%，可在梦幻朦胧模式下扩展到 35–55%
安静留白：15–30%
前景掠影：树冠枝叶形成大面积方向性虚影
中景拖影：草地纹理拉伸为半透明色带
背景光色流：远山和天空融为柔和光带
主体占比与位置：约 30%，偏画面中下偏右

**视觉方案**
主机制：Backlit Halation（树冠透光形成逆光晕染）
辅助机制：Passing Gesture（风吹草帽边缘和树叶形成方向性虚影）
强度：梦幻朦胧
选择理由：原图已有树冠滤光的自然逆光条件，草帽和树叶对风敏感，两个机制物理上可信

质量检查通过，开始生成：
```

### Night Reflection Portrait

- Composition: source-led-asymmetry or geometry-preserving-frame for identity lock.
- Motion: source-layer-drift or crowd-drift when movement exists.
- Optical: glass-memory.
- Lighting: night-color-glow.
- Allow only one explainable reflection overlap.

### Night Illuminated Walkway

- Preservation priority: vanishing perspective > repeated ground-lamp rhythm > cool/warm contrast > distant building outline. The building outline is expendable.
- Keep: the single central walkway path, converging railings, lamp sequence, and warm-white lamp identity.
- Hero sharpness island: the central walking surface from the lower frame to the vanishing point, the inner railing boundaries, readable lamp cores, and one continuous bilateral lamp rhythm. Preserve a restrained amount of pavement texture inside this island.
- Motion boundary: keep long trails outside the central path corridor and behind the inner railing boundaries. Outer-frame atmosphere may be strong; the protected corridor must remain clearly sharper.
- Fade: buildings, window grids, trees, leaves, and only the noncritical outer pavement texture into two to four broad deep-blue, ink-cyan, and amber motion masses; none should remain crisply inventory-readable.
- Remove: isolated signs, blue specks, tiny windows, and incidental clutter.
- Composition: a 4:5 vertical geometry-preserving crop, but preserve only the walkway's vanishing structure rather than the whole city scene.
- Primary mechanism: Backlit Halation, driven by the visible ground lamps. Expand their honey-gold and warm-amber glow into local leakage without white fog.
- Support mechanism: Crowd Drift, driven by the implied movement of the receding public passage and repeated fixtures. Do not add people.
- Three-layer motion depth: near outer-edge lamp bloom and peripheral railing reflections form warm directional veils without covering the central path or dissolving the fixture cores; two or three secondary midground light residuals stretch semi-transparently outside the inner railing boundaries; distant buildings and foliage merge into cold blue-black and ink-cyan light bands.
- Color: approximately 65% deep blue or ink cyan, 25% honey gold or warm amber, and 10% neutral dark. The palette must visibly differ from the source while retaining the lamps' warm-white identity.
- Texture: real handheld slow-shutter drag, fine-to-medium grain, lower digital micro-contrast, mild aberration, restrained vignette.
- Mood: hazy memory, poetic distance, night solitude, like an accidentally captured old-film frame.

Expected process card for this pattern:

```text
**照片诊断**
主体：一条由两侧地灯引向消失点的夜间栈道
必须保留：单一消失点、栈道连续路径、两侧地灯序列、暖光冷空对比
可利用的光线/动态/前景：地灯现成光源、栏杆透视、重复灯光节奏、两侧树木和建筑边缘
风险：透视和灯序列易漂移；不得新增人物、文字或道具

**构图提炼**
Keep：栈道透视路径、地灯序列节奏、暖白身份色
Fade：建筑、窗格、树木、枝叶、主体清晰岛之外的路面纹理
Remove：零碎蓝色亮点、孤立窗灯和小杂物
主体清晰岛：中央栈道路面、两侧内栏杆边界、地灯发光核心和一条连续灯序列；保留少量路面质感
动态边界：长拖影只进入外侧栏杆区域和背景，不横穿中央栈道路径
动态覆盖：约 45%
安静留白：约 25%
前景掠影：外侧近处灯晕和栏杆反光形成暖色方向性虚影，只遮挡画面边缘，保留灯芯与中央路径
中景拖影：2–3 个次要灯光残影沿透视方向拉成半透明光带，位于内栏杆之外
背景光色流：城市和树木融合为深蓝、墨青色块拖影
主体占比与位置：栈道路径约 30%，居中下方通向画面中心

**视觉方案**
主机制：Backlit Halation（地灯作为可见光源，强化蜂蜜金光晕和光泄漏）
辅助机制：Crowd Drift（空栈道的公共通行属性、透视和重复灯光暗示慢门流动，不新增人物）
强度：梦幻朦胧
选择理由：地灯提供可信晕染源，栈道纵深和灯序列提供统一的拖影方向
三层运动景深：
- 前景掠影：外侧近处灯晕和栏杆反光沿消失点方向形成暖色虚影，只遮挡画面边缘，不进入主体清晰岛
- 中景拖影：2–3 个次要灯光残影沿透视方向形成半透明暖色光带，保持中央路径、内栏杆和主灯序列清晰
- 背景光色流：建筑和树木融为低可读性的冷蓝、墨青色块
光线：蜂蜜金和暖琥珀局部晕染，暗部保留深蓝冷色，不制造白雾
色彩：深蓝和墨青约 65%，蜂蜜金和暖琥珀约 25%，中性暗部约 10%
光学质感：真实慢门、细到中等胶片颗粒、降低数码微对比度、轻微色散、克制暗角
整体情绪：朦胧记忆、诗意疏离、夜间独行，像偶然捕捉到的一帧旧电影
保真优先级：透视线条 > 地灯序列 > 暖冷对比 > 建筑轮廓
建议参数：比例 4:5；重绘强度 dream-haze
输出：4:5 竖幅，摄影写实，不新增人物、花朵、文字或道具

质量检查通过，开始生成：
```

### Product Photo

- Composition: geometry-preserving-frame.
- Motion: source-layer-drift.
- Optical: none unless real glass or flora exists.
- Lighting: source-light-bloom or source-supported backlit-halation.
- Preserve exact geometry, label, typography, and material edges.

## Optional Poster Module

Only when the user explicitly requests poster treatment within the dreamification task:

- title: one to six words;
- optional subtitle: one short line;
- placement: existing quiet space;
- type direction: restrained serif, neo-grotesk, or narrow sans;
- typography: under 12% of the frame.

Do not ask the image generator to render long exact text. Recommend adding final typography in a design tool when spelling matters.
