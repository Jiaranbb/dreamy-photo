import contextlib
import importlib.util
import io
import unittest
from pathlib import Path

SCRIPT = Path(__file__).parents[1] / "scripts" / "analyze_photo.py"
spec = importlib.util.spec_from_file_location("analyze_photo", SCRIPT)
analyzer = importlib.util.module_from_spec(spec)
spec.loader.exec_module(analyzer)


class AnalyzePhotoTests(unittest.TestCase):
    def route(self, **overrides):
        data = {
            "subject": "portrait",
            "light": "flat",
            "motion": "still",
            "depth": "shallow",
            "reflection": False,
            "flora": False,
            "background": "indoor",
            "risks": None,
            "strength": "dream-haze",
            "fidelity": "semantic-core",
        }
        data.update(overrides)
        return analyzer.analyze_observations(analyzer.PhotoObservations(**data))

    def test_backlit_walking_portrait_separates_motion_and_lighting(self):
        result = self.route(light="backlit", motion="walking", depth="layered", background="street")
        self.assertEqual(result["strategy"]["motion"], "crowd-drift")
        self.assertEqual(result["strategy"]["lighting"], "backlit-halation")
        self.assertIn("protect face identity", result["constraints"])

    def test_flat_indoor_selfie_uses_passing_gesture(self):
        result = self.route(background="indoor", motion="still", depth="shallow")
        self.assertEqual(result["strategy"]["motion"], "passing-gesture")
        self.assertEqual(result["strategy"]["optical"], "none")

    def test_flower_closeup_uses_flora_as_optical_layer(self):
        result = self.route(subject="flower", flora=True, depth="layered")
        self.assertEqual(result["strategy"]["optical"], "floral-diffusion")
        self.assertNotEqual(result["strategy"]["motion"], "crowd-drift")

    def test_group_with_motion_uses_crowd_drift(self):
        result = self.route(subject="group", motion="walking", background="street")
        self.assertEqual(result["strategy"]["motion"], "crowd-drift")
        self.assertIn("protect all recognizable faces", result["constraints"])

    def test_product_auto_risks_do_not_add_face_constraint(self):
        result = self.route(subject="product", background="studio")
        self.assertEqual(result["strategy"]["composition"], "geometry-preserving-frame")
        self.assertEqual(result["strategy"]["motion"], "source-layer-drift")
        self.assertIn("protect object geometry and any readable labels", result["constraints"])
        self.assertNotIn("protect face identity", result["constraints"])

    def test_night_reflection_uses_independent_optical_and_light_axes(self):
        result = self.route(light="night", background="street", reflection=True, depth="layered")
        self.assertEqual(result["strategy"]["optical"], "glass-memory")
        self.assertEqual(result["strategy"]["lighting"], "night-color-glow")

    def test_safe_fallback_never_defaults_to_crowd_without_evidence(self):
        result = self.route(
            subject="architecture",
            light="mixed",
            motion="still",
            depth="deep",
            background="city",
        )
        self.assertEqual(result["strategy"]["motion"], "source-layer-drift")
        self.assertEqual(result["motion_scores"]["crowd-drift"], -8)
        self.assertIn(
            "protect the standalone hero structure, defining silhouette, and one material cue",
            result["constraints"],
        )
        self.assertEqual(result["structure_role"], "standalone")
        self.assertNotIn("protect object geometry and any readable labels", result["constraints"])

    def test_empty_lit_walkway_uses_bold_source_supported_route(self):
        result = self.route(
            subject="architecture",
            light="night",
            motion="still",
            depth="deep",
            background="walkway",
            practical_lights=True,
            implied_movement=True,
        )
        self.assertEqual(result["strategy"]["motion"], "crowd-drift")
        self.assertEqual(result["strategy"]["lighting"], "backlit-halation")
        self.assertEqual(result["strategy"]["primary_mechanism"], "backlit-halation")
        self.assertEqual(result["strategy"]["support_mechanism"], "crowd-drift")
        self.assertEqual(
            result["composition"]["preservation_priority"][0],
            "hero path and vanishing perspective",
        )
        self.assertIn("central walking surface", result["composition"]["hero_sharpness_island"])
        self.assertIn("outside the central path corridor", result["composition"]["motion_boundary"])
        self.assertIn("do not invent unrelated people", " ".join(result["constraints"]))
        self.assertEqual(result["structure_role"], "passage")

    def test_axes_can_combine_without_competing(self):
        result = self.route(
            subject="portrait",
            light="backlit",
            motion="walking",
            depth="layered",
            reflection=True,
            background="sky",
        )
        self.assertEqual(result["strategy"]["composition"], "low-angle-color-field")
        self.assertEqual(result["strategy"]["motion"], "crowd-drift")
        self.assertEqual(result["strategy"]["optical"], "glass-memory")
        self.assertEqual(result["strategy"]["lighting"], "backlit-halation")

    def test_visual_allocation_is_non_overlapping(self):
        result = self.route(strength="dream-haze")
        allocation = result["composition"]["visual_allocation"]
        self.assertEqual(allocation["hero_percent"], 30)
        self.assertEqual(sum(allocation.values()), 100)

    def test_identity_lock_overrides_strength_allocation(self):
        result = self.route(fidelity="identity-lock", strength="experimental-memory")
        allocation = result["composition"]["visual_allocation"]
        self.assertEqual(result["strategy"]["composition"], "geometry-preserving-frame")
        self.assertEqual(allocation, {"hero_percent": 45, "kinetic_percent": 25, "quiet_percent": 30})

    def test_composition_outputs_keep_fade_remove(self):
        result = self.route(subject="architecture", background="city")
        composition = result["composition"]
        self.assertTrue(composition["keep"])
        self.assertTrue(composition["fade"])
        self.assertTrue(composition["remove"])

    def test_explicit_no_anatomy_risks_still_preserves_visible_skin_identity(self):
        result = self.route(subject="portrait", risks=[])
        self.assertNotIn("protect face identity", result["constraints"])
        self.assertIn(
            "protect source-relative skin lightness, undertone, age impression, and softness",
            result["constraints"],
        )

    def test_visible_hands_lock_skin_identity_without_extra_texture(self):
        result = self.route(subject="object", risks=["hands"])
        self.assertIn("protect hand anatomy and finger count", result["constraints"])
        self.assertIn(
            "protect source-relative skin lightness, undertone, age impression, and softness",
            result["constraints"],
        )

    def test_horizontal_landscape_does_not_default_to_portrait_crop(self):
        result = self.route(
            subject="landscape",
            light="hard-sun",
            background="nature",
            subject_axis="horizontal",
        )
        self.assertIn("landscape ratio", result["aspect_ratio"])
        self.assertNotIn("4:5", result["aspect_ratio"])

    def test_auto_daylight_palette_is_not_forced_to_honey_gold(self):
        result = self.route(
            subject="landscape",
            light="hard-sun",
            background="nature",
        )
        self.assertIn("summer blue", result["palette"])
        self.assertNotIn("honey-gold", result["palette"])

    def test_explicit_blue_hour_rejects_magenta_contamination(self):
        result = self.route(mood="blue-hour")
        self.assertIn("no magenta contamination", result["palette"])

    def test_nonhuman_hero_gets_material_exposure_floor(self):
        result = self.route(subject="architecture", structure_role="standalone")
        self.assertIn(
            "protect readable structural midtones and one source-relative material plane",
            result["constraints"],
        )

    def test_invalid_subject_is_rejected(self):
        with contextlib.redirect_stderr(io.StringIO()):
            with self.assertRaises(SystemExit):
                analyzer.parse_args(["--subject", "unknown"])

    def test_invalid_risk_is_rejected(self):
        with self.assertRaises(analyzer.argparse.ArgumentTypeError):
            analyzer.parse_risks("face,unknown")


if __name__ == "__main__":
    unittest.main()
