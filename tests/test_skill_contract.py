import unittest
from pathlib import Path

ROOT = Path(__file__).parents[1]


class SkillContractTests(unittest.TestCase):
    def read(self, relative):
        return (ROOT / relative).read_text(encoding="utf-8")

    def test_description_is_narrowed_to_photo_dreamification(self):
        skill = self.read("SKILL.md")
        self.assertIn("图片梦幻化", skill)
        self.assertIn("照片梦幻化", skill)
        self.assertIn("Do not use for general image generation", skill)
        self.assertNotIn("帖子视觉、封面图、艺术摄影", skill)

    def test_default_contract_generates_and_returns_image(self):
        skill = self.read("SKILL.md")
        self.assertIn("Default to `generate-and-return`", skill)
        self.assertIn("return the finished image", skill)
        self.assertIn("Do not show the internal prompt", skill)

    def test_prompt_visibility_requires_explicit_request(self):
        skill = self.read("SKILL.md")
        recipes = self.read("references/prompt-recipes.md")
        self.assertIn("If the user explicitly asks to see the prompt", skill)
        self.assertIn("Do not show the full prompt", recipes)
        self.assertIn("prompts only or says not to generate", recipes)

    def test_default_process_card_is_visible_before_generation(self):
        skill = self.read("SKILL.md")
        recipes = self.read("references/prompt-recipes.md")
        rubric = self.read("references/quality-rubric.md")
        for label in ("照片诊断", "构图提炼", "视觉方案", "质量检查通过，开始生成："):
            self.assertIn(label, skill)
            self.assertIn(label, recipes)
            self.assertIn(label, rubric)

    def test_prompt_only_mode_skips_generation(self):
        skill = self.read("SKILL.md")
        rubric = self.read("references/quality-rubric.md")
        self.assertIn("return the prompt package and do not call any image-generation route", skill)
        self.assertIn("Do not call an image-generation route", rubric)

    def test_strategy_axes_are_independent(self):
        skill = self.read("SKILL.md")
        style = self.read("references/style-system.md")
        for axis in ("Composition", "Motion", "Optical layer", "Lighting"):
            self.assertIn(f"**{axis}**", skill)
        self.assertIn(
            "Treat composition, motion, optical layering, and lighting as independent diagnostic axes",
            style,
        )

    def test_primary_route_outranks_diagnostic_axes(self):
        skill = self.read("SKILL.md")
        style = self.read("references/style-system.md")
        recipes = self.read("references/prompt-recipes.md")
        self.assertIn("exactly one **primary mechanism**", skill)
        self.assertIn("## Primary and Support Route", style)
        self.assertIn("主机制：【一个主机制】", recipes)

    def test_safe_motion_fallback_is_documented(self):
        skill = self.read("SKILL.md")
        style = self.read("references/style-system.md")
        self.assertIn("`source-layer-drift` as the safe motion fallback", skill)
        self.assertIn("### Source-Layer Drift", style)

    def test_visual_allocations_are_non_overlapping(self):
        skill = self.read("SKILL.md")
        self.assertIn("hero 30%, kinetic atmosphere 45%, quiet space 25%", skill)
        self.assertNotIn("35–55% kinetic motion atmosphere", skill)

    def test_people_semantics_outrank_background_fidelity(self):
        skill = self.read("SKILL.md")
        style = self.read("references/style-system.md")
        recipes = self.read("references/prompt-recipes.md")
        self.assertIn("Do not promote scenery, landmarks, background architecture, or the source crop", skill)
        self.assertIn("their identity, relationship, gesture, and essential shared object outrank the location", style)
        self.assertIn("### Couple on a Bench in a Wide Landscape", recipes)

    def test_source_ratio_is_flexible_by_default(self):
        skill = self.read("SKILL.md")
        style = self.read("references/style-system.md")
        recipes = self.read("references/prompt-recipes.md")
        self.assertIn("Choose the ratio from the hero's dominant spatial axis", skill)
        self.assertIn("Permit a changed aspect ratio", recipes)
        self.assertIn("horizontal / vertical / balanced", recipes)
        self.assertIn("never force portrait solely", recipes)
        self.assertIn("Never force portrait", style)

    def test_palette_is_mood_driven_not_fixed_to_amber(self):
        skill = self.read("SKILL.md")
        style = self.read("references/style-system.md")
        recipes = self.read("references/prompt-recipes.md")
        rubric = self.read("references/quality-rubric.md")
        self.assertIn("backlight does not automatically mean honey-gold", skill)
        self.assertIn("summer-breeze", style)
        self.assertIn("blue-hour", recipes)
        self.assertIn("Do not force amber nostalgia", rubric)

    def test_nonhuman_hero_has_exposure_floor(self):
        skill = self.read("SKILL.md")
        recipes = self.read("references/prompt-recipes.md")
        rubric = self.read("references/quality-rubric.md")
        self.assertIn("for every hero type", skill)
        self.assertIn("For objects, flowers, structures, and landscapes", recipes)
        self.assertIn("For a non-human hero", rubric)

    def test_architecture_role_is_classified_before_path_rules(self):
        skill = self.read("SKILL.md")
        self.assertIn("passage, standalone structure, or background context", skill)
        self.assertIn("only passage architecture inherits a path", skill)

    def test_dream_haze_rejects_light_filter_pass(self):
        skill = self.read("SKILL.md")
        style = self.read("references/style-system.md")
        rubric = self.read("references/quality-rubric.md")
        self.assertIn("stronger than a warm color grade", skill)
        self.assertIn("warm grade plus global softness", style)
        self.assertIn("### Transformation Visibility", rubric)
        self.assertIn("merely warmer, softer, lower-contrast", rubric)

    def test_dream_haze_rebuilds_palette_and_destroys_fade_readability(self):
        skill = self.read("SKILL.md")
        style = self.read("references/style-system.md")
        recipes = self.read("references/prompt-recipes.md")
        rubric = self.read("references/quality-rubric.md")
        self.assertIn("dominant palette must be visibly re-authored", skill)
        self.assertIn("If a viewer can still inventory the Fade list", style)
        self.assertIn("色彩重构", recipes)
        self.assertIn("### Fade Readability", rubric)

    def test_night_walkway_gold_standard_is_documented(self):
        recipes = self.read("references/prompt-recipes.md")
        self.assertIn("### Night Illuminated Walkway", recipes)
        self.assertIn("Backlit Halation（地灯作为可见光源", recipes)
        self.assertIn("Crowd Drift（空栈道的公共通行属性", recipes)
        self.assertIn("透视线条 > 地灯序列 > 暖冷对比 > 建筑轮廓", recipes)

    def test_hero_sharpness_island_blocks_motion_through_subject(self):
        skill = self.read("SKILL.md")
        style = self.read("references/style-system.md")
        recipes = self.read("references/prompt-recipes.md")
        rubric = self.read("references/quality-rubric.md")
        self.assertIn("hero sharpness island", skill)
        self.assertIn("## Hero Sharpness Island", style)
        self.assertIn("主体清晰岛", recipes)
        self.assertIn("### Hero Sharpness Island", rubric)
        self.assertIn("中央栈道路面", recipes)
        self.assertIn("不横穿中央栈道路径", recipes)

    def test_visible_skin_is_identity_locked_and_not_over_sharpened(self):
        skill = self.read("SKILL.md")
        style = self.read("references/style-system.md")
        recipes = self.read("references/prompt-recipes.md")
        rubric = self.read("references/quality-rubric.md")
        self.assertIn("source-relative complexion lightness", skill)
        self.assertIn("## Human Skin Identity", style)
        self.assertIn("肤色身份锁定", recipes)
        self.assertIn("### Visible Skin or Hand", recipes)
        self.assertIn("### Skin Identity and Age", rubric)
        self.assertIn("exaggerated wrinkles", recipes)

    def test_people_keep_exposure_and_light_shapes_stay_non_symbolic(self):
        skill = self.read("SKILL.md")
        style = self.read("references/style-system.md")
        recipes = self.read("references/prompt-recipes.md")
        rubric = self.read("references/quality-rubric.md")
        self.assertIn("hero exposure floor", skill)
        self.assertIn("Hero exposure baseline", style)
        self.assertIn("主体曝光基线", recipes)
        self.assertIn("光斑形状约束", recipes)
        self.assertIn("不枚举禁用符号名称", recipes)
        self.assertIn("recognizable icon-like bokeh", recipes)
        self.assertNotIn("heart-shaped bokeh", recipes)
        self.assertIn("lexical priming", skill)
        self.assertIn("### Hero Exposure Floor", rubric)
        self.assertIn("invented hearts", rubric)

    def test_prompt_recipe_rejects_unsupported_invention(self):
        recipes = self.read("references/prompt-recipes.md")
        self.assertIn("Do not invent objects merely to satisfy a style module", recipes)
        self.assertIn("invented people", recipes)
        self.assertIn("source-layer-drift", recipes)

    def test_quality_rubric_checks_generated_image(self):
        rubric = self.read("references/quality-rubric.md")
        self.assertIn("Inspect the actual generated image, not only the prompt", rubric)
        self.assertIn("## Generated-Image Result Gates", rubric)
        self.assertIn("## Targeted Revision Rule", rubric)

    def test_skill_routes_codex_and_openclaw_image_generation(self):
        skill = self.read("SKILL.md")
        self.assertIn("`image_gen`", skill)
        self.assertIn("`referenced_image_paths`", skill)
        self.assertIn("`num_last_images_to_include`", skill)
        self.assertIn("`image_generate`", skill)
        self.assertIn("reference-image `image` parameter", skill)
        self.assertIn("No compatible image route", skill)


if __name__ == "__main__":
    unittest.main()
