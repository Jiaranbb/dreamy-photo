#!/usr/bin/env python3
"""Convert human-observed photo traits into a validated dreamy-photo strategy."""

from __future__ import annotations

import argparse
import json


SUBJECT_CHOICES = (
    "portrait",
    "group",
    "product",
    "object",
    "flower",
    "architecture",
    "landscape",
)
LIGHT_CHOICES = ("flat", "window", "hard-sun", "backlit", "mixed", "night")
MOTION_CHOICES = ("still", "walking", "crowd", "traffic", "turning", "reaching", "wind")
DEPTH_CHOICES = ("shallow", "layered", "deep")
BACKGROUND_CHOICES = (
    "indoor",
    "studio",
    "street",
    "corridor",
    "walkway",
    "bridge",
    "platform",
    "sky",
    "open",
    "wall",
    "nature",
    "city",
)
STRENGTH_CHOICES = ("restrained-premium", "dream-haze", "experimental-memory")
FIDELITY_CHOICES = ("semantic-core", "identity-lock", "experimental-abstraction")
MOOD_CHOICES = (
    "auto",
    "source-led",
    "summer-breeze",
    "golden-memory",
    "blue-hour",
    "night-solitude",
)
SUBJECT_AXIS_CHOICES = ("auto", "horizontal", "vertical", "balanced")
STRUCTURE_ROLE_CHOICES = ("auto", "passage", "standalone", "background")
VALID_RISKS = {"face", "faces", "hands", "geometry", "text"}


class PhotoObservations:
    def __init__(
        self,
        subject="portrait",
        light="flat",
        motion="still",
        depth="shallow",
        reflection=False,
        flora=False,
        practical_lights=False,
        implied_movement=False,
        background="indoor",
        risks=None,
        strength="dream-haze",
        fidelity="semantic-core",
        mood="auto",
        subject_axis="auto",
        structure_role="auto",
    ):
        self.subject = subject
        self.light = light
        self.motion = motion
        self.depth = depth
        self.reflection = bool(reflection)
        self.flora = bool(flora)
        self.practical_lights = bool(practical_lights)
        self.implied_movement = bool(implied_movement)
        self.background = background
        self.risks = None if risks is None else list(risks)
        self.strength = strength
        self.fidelity = fidelity
        self.mood = mood
        self.subject_axis = subject_axis
        self.structure_role = structure_role


def inferred_risks(subject):
    return {
        "portrait": ["face"],
        "group": ["faces"],
        "product": ["geometry", "text"],
        "object": ["geometry"],
        "flower": [],
        "architecture": ["geometry"],
        "landscape": [],
    }[subject]


def resolved_risks(observations):
    if observations.risks is None or observations.risks == ["auto"]:
        return inferred_risks(observations.subject)
    return observations.risks


def preservation_constraints(observations):
    constraints = []
    risks = set(resolved_risks(observations))

    if "face" in risks:
        constraints.append("protect face identity")
    if "faces" in risks or observations.subject == "group":
        constraints.append("protect all recognizable faces")
    if "hands" in risks:
        constraints.append("protect hand anatomy and finger count")
    if {"face", "faces", "hands"} & risks or observations.subject in {"portrait", "group"}:
        constraints.append("protect source-relative skin lightness, undertone, age impression, and softness")
    if observations.subject in {"product", "object"}:
        constraints.append("protect object geometry and any readable labels")
    elif observations.subject != "architecture" and {"geometry", "text"} & risks:
        constraints.append("protect critical source geometry and readable text")
    if observations.subject == "architecture":
        if resolved_structure_role(observations) == "passage":
            constraints.append("protect the ranked hero path and vanishing perspective, not every secondary structure")
        else:
            constraints.append("protect the standalone hero structure, defining silhouette, and one material cue")
    if not constraints:
        constraints.append("preserve the source subject and composition anchor")

    constraints.append("apply blur mainly to secondary layers")
    if observations.subject in {"product", "object"}:
        constraints.append("protect source-relative material brightness, midtone separation, and surface character")
    elif observations.subject == "flower":
        constraints.append("protect hero blossom brightness, petal separation, and one natural surface cue")
    elif observations.subject == "architecture":
        constraints.append("protect readable structural midtones and one source-relative material plane")
    elif observations.subject == "landscape":
        constraints.append("protect readable landform or horizon separation and one natural tonal plane")
    constraints.append("do not invent unrelated people, props, flowers, clothing, or text")
    return constraints


def resolved_structure_role(observations):
    if observations.structure_role != "auto":
        return observations.structure_role
    if observations.subject == "architecture" and (
        observations.implied_movement
        or observations.background in {"corridor", "walkway", "bridge", "platform"}
    ):
        return "passage"
    if observations.subject == "architecture":
        return "standalone"
    return "background"


def palette_direction(observations):
    if observations.mood == "summer-breeze":
        return "airy summer blue, fresh leaf green, and pale sunlit cream with clean luminous highlights and no nostalgic amber cast"
    if observations.mood == "golden-memory":
        return "soft honey gold, faded grass, warm cream, and restrained cool shadow depth"
    if observations.mood == "blue-hour":
        return "clean cobalt and dusk blue with restrained silver-blue light and no magenta contamination"
    if observations.mood == "night-solitude":
        return "ink blue and deep cyan shadows with restrained amber or coral warmth"
    if observations.mood == "source-led":
        return "re-author the observed source colors into one dominant field, one luminous family, and neutral support without forcing a preset warm-cool grade"
    if observations.light == "night":
        return "ink blue and deep cyan shadows with restrained amber or coral warmth"
    if observations.flora or observations.subject == "flower":
        return "fresh botanical green, airy cyan, and one source-derived floral accent with natural luminous highlights"
    if observations.light == "hard-sun" and observations.background in {"sky", "open", "nature"}:
        return "airy summer blue, clean leaf green, and pale sunlit cream with restrained warmth"
    if observations.light in {"backlit", "window"}:
        return "choose clean daylight bloom or restrained warm halation from the observed source; do not default to amber"
    if observations.background in {"indoor", "studio"}:
        return "muted charcoal, dusty cyan, and warm cream highlights"
    return "one source-supported dominant field, one distinct luminous family, and neutral support with a visible but mood-appropriate palette departure"


def aspect_ratio_guidance(observations):
    if observations.subject_axis == "horizontal":
        return "preserve or choose a landscape ratio such as 3:2 or 16:9 so the hero's horizontal spread remains readable"
    if observations.subject_axis == "vertical":
        return "choose a portrait ratio such as 4:5 or 3:4 when it strengthens the hero's vertical direction"
    if observations.subject_axis == "balanced":
        return "use the source ratio or a restrained 4:5, 3:4, or 1:1 crop according to surrounding quiet space"
    if observations.subject == "landscape":
        return "prefer a landscape ratio unless the observed hero itself is clearly vertical"
    if resolved_structure_role(observations) == "passage":
        return "choose portrait or landscape from the passage direction; protect the complete vanishing path rather than forcing 4:5"
    return "infer portrait, landscape, or balanced output from the hero's dominant spatial axis; never force a portrait crop merely because the source is wide"


def visual_allocation(observations):
    if observations.fidelity == "identity-lock":
        return {"hero_percent": 45, "kinetic_percent": 25, "quiet_percent": 30}
    if observations.strength == "restrained-premium":
        return {"hero_percent": 40, "kinetic_percent": 30, "quiet_percent": 30}
    if observations.strength == "experimental-memory":
        return {"hero_percent": 20, "kinetic_percent": 65, "quiet_percent": 15}
    return {"hero_percent": 30, "kinetic_percent": 45, "quiet_percent": 25}


def select_composition(observations):
    if observations.fidelity == "identity-lock" or observations.subject in {
        "product",
        "object",
        "architecture",
    }:
        return (
            "geometry-preserving-frame",
            "recognition-sensitive geometry should remain stable while secondary detail is simplified",
        )
    if observations.background in {"sky", "open", "wall"} and observations.subject in {
        "portrait",
        "flower",
        "landscape",
    }:
        return (
            "low-angle-color-field",
            "the existing open field can support graphic negative space without inventing a new setting",
        )
    return (
        "source-led-asymmetry",
        "an asymmetric crop can simplify the source while keeping its viewpoint believable",
    )


def select_motion(observations):
    scores = {
        "crowd-drift": 0,
        "passing-gesture": 0,
        "source-layer-drift": 2,
    }
    reasons = {
        "crowd-drift": [],
        "passing-gesture": [],
        "source-layer-drift": ["existing background edges, light, and color provide a safe motion source"],
    }

    if observations.subject == "group":
        scores["crowd-drift"] += 7
        reasons["crowd-drift"].append("multiple people support selective motion separation")
    if observations.motion in {"walking", "crowd", "traffic"}:
        scores["crowd-drift"] += 5
        reasons["crowd-drift"].append("existing movement supports slow-shutter drag")
        if observations.background == "street":
            scores["crowd-drift"] += 2
            reasons["crowd-drift"].append("street perspective supports directional flow")
    passage_backgrounds = {"corridor", "walkway", "bridge", "platform"}
    if observations.implied_movement or observations.background in passage_backgrounds:
        scores["crowd-drift"] += 12
        reasons["crowd-drift"].append(
            "the receding public passage and repeated structure imply slow-shutter movement without adding people"
        )
    if observations.subject in {"product", "object", "flower", "architecture", "landscape"} and not (
        observations.implied_movement or observations.background in passage_backgrounds
    ):
        scores["crowd-drift"] -= 8

    if observations.motion in {"turning", "reaching", "wind"}:
        scores["passing-gesture"] += 4
        reasons["passing-gesture"].append("an existing gesture can carry local movement")
    if observations.motion == "still":
        scores["passing-gesture"] += 2
        reasons["passing-gesture"].append("a nearby source element can add restrained motion")
    if observations.background in {"indoor", "studio"}:
        scores["passing-gesture"] += 2
        reasons["passing-gesture"].append("fabric, hair, paper, foliage, or light can add controlled depth")
    if observations.subject in {"portrait", "product", "object", "flower"}:
        scores["passing-gesture"] += 1

    if observations.subject in {"product", "object", "flower", "architecture", "landscape"}:
        scores["source-layer-drift"] += 4
        reasons["source-layer-drift"].append("the subject benefits from motion kept outside its critical geometry")
    if observations.motion == "still":
        scores["source-layer-drift"] += 2
    if observations.depth in {"layered", "deep"}:
        scores["source-layer-drift"] += 1

    ordered = ("crowd-drift", "passing-gesture", "source-layer-drift")
    selected = sorted(ordered, key=lambda name: (-scores[name], ordered.index(name)))[0]
    reason = "; ".join(reasons[selected][:2])
    return selected, reason, scores


def select_optical(observations):
    if observations.flora or observations.subject == "flower":
        return (
            "floral-diffusion",
            "existing flora can become a physically plausible near-lens color veil",
        )
    if observations.reflection:
        return (
            "glass-memory",
            "an observed reflective surface supports one controlled optical overlap",
        )
    return ("none", "the source does not require an added optical layer")


def select_lighting(observations):
    if observations.practical_lights:
        return (
            "backlit-halation",
            "visible path, edge, or ground fixtures can directly drive local halation and light leakage",
        )
    if observations.light == "night":
        return (
            "night-color-glow",
            "existing night lights can form restrained colored trails and local bloom",
        )
    if observations.light in {"backlit", "hard-sun", "window"}:
        return (
            "backlit-halation",
            "the existing directional light supports localized halation",
        )
    return (
        "source-light-bloom",
        "preserve the observed light direction and soften only credible highlights",
    )


def composition_guidance(observations):
    allocation = visual_allocation(observations)
    if observations.fidelity == "identity-lock":
        max_context_cues = 3
        retain_secondary_motion_forms = "1-2 large blurred forms"
    elif observations.strength == "experimental-memory":
        max_context_cues = 1
        retain_secondary_motion_forms = "3-5 large blurred forms"
    elif observations.strength == "restrained-premium":
        max_context_cues = 2
        retain_secondary_motion_forms = "1-2 large blurred forms"
    else:
        max_context_cues = 2
        retain_secondary_motion_forms = "2-4 large blurred forms"

    if observations.subject in {"product", "object"}:
        keep = ["hero object geometry", "one material or label cue", "one native accent color"]
    elif observations.subject == "group":
        keep = ["one hero relationship or gesture", "recognizable key faces", "one contextual color cue"]
    elif observations.subject == "flower":
        keep = ["one hero blossom or botanical silhouette", "one petal or stem cue", "one native accent color"]
    elif observations.subject == "architecture" and resolved_structure_role(observations) == "passage":
        keep = ["hero path and vanishing perspective", "repeated light or railing rhythm", "one luminous identity color"]
        hero_sharpness_island = (
            "central walking surface, inner railing boundaries, luminous fixture cores, and one continuous repeated rhythm"
        )
        motion_boundary = "keep long trails outside the central path corridor and behind its inner structural boundaries"
    elif observations.subject == "architecture":
        keep = ["hero structure and perspective", "one defining edge or material cue", "one native accent color"]
        hero_sharpness_island = "defining structure, perspective edges, and one readable material surface"
        motion_boundary = "keep motion outside critical structural geometry"
    elif observations.subject == "landscape":
        keep = ["hero landform or horizon", "one depth cue", "one native accent color"]
        hero_sharpness_island = "hero landform or horizon plus one readable depth or surface cue"
        motion_boundary = "keep long motion in peripheral or noncritical depth layers"
    else:
        keep = ["hero identity and gesture", "one clothing or object cue", "one native accent color"]
        hero_sharpness_island = "hero identity plus the full gesture or relationship silhouette"
        motion_boundary = "let motion frame or pass behind the hero without crossing the protected silhouette"

    if observations.subject in {"product", "object"}:
        hero_sharpness_island = "hero body, defining contour, functional edges, and readable label or material cue"
        motion_boundary = "keep motion outside the product body and all readable text"
    elif observations.subject == "group":
        hero_sharpness_island = "all recognizable faces plus the full shared gesture or relationship silhouette"
        motion_boundary = "keep motion behind or beside the group without crossing faces or the shared gesture"
    elif observations.subject == "flower":
        hero_sharpness_island = "hero blossom center or botanical silhouette plus one petal or stem texture"
        motion_boundary = "keep diffusion outside the hero center and defining botanical contour"

    return {
        "preservation_mode": observations.fidelity,
        "visual_allocation": allocation,
        "max_context_cues": max_context_cues,
        "retain_secondary_motion_forms": retain_secondary_motion_forms,
        "dynamic_layers": [
            "near-lens directional veil when supported by the source",
            "midground secondary-form drag",
            "background light, color, or architectural trails",
        ],
        "keep": keep,
        "hero_sharpness_island": hero_sharpness_island,
        "motion_boundary": motion_boundary,
        "preservation_priority": keep + ["secondary contextual detail is expendable"],
        "aspect_ratio_guidance": aspect_ratio_guidance(observations),
        "fade": [
            "background signage, window grids, and small readable detail",
            "secondary architecture, furniture, foliage, vehicles, and texture into 2-4 broad directional masses",
            "nonessential people or repeated forms",
        ],
        "remove": [
            "unrelated secondary objects",
            "duplicate people or repeated props",
            "small high-contrast clutter outside the hero zone",
        ],
    }


def analyze_observations(observations):
    composition, composition_reason = select_composition(observations)
    motion, motion_reason, motion_scores = select_motion(observations)
    optical, optical_reason = select_optical(observations)
    lighting, lighting_reason = select_lighting(observations)
    if lighting == "backlit-halation":
        primary_mechanism = lighting
        support_mechanism = motion if motion != "source-layer-drift" or observations.depth != "shallow" else "none"
    else:
        primary_mechanism = motion
        support_mechanism = lighting if lighting != "source-light-bloom" else "none"

    return {
        "strategy": {
            "fidelity": observations.fidelity,
            "composition": composition,
            "motion": motion,
            "optical": optical,
            "lighting": lighting,
            "primary_mechanism": primary_mechanism,
            "support_mechanism": support_mechanism,
            "strength": observations.strength,
        },
        "rationale": {
            "composition": composition_reason,
            "motion": motion_reason,
            "optical": optical_reason,
            "lighting": lighting_reason,
        },
        "palette": palette_direction(observations),
        "mood": observations.mood,
        "aspect_ratio": aspect_ratio_guidance(observations),
        "structure_role": resolved_structure_role(observations),
        "constraints": preservation_constraints(observations),
        "composition": composition_guidance(observations),
        "motion_scores": motion_scores,
    }


def parse_risks(value):
    normalized = value.strip().lower()
    if normalized == "auto":
        return None
    if normalized in {"", "none"}:
        return []
    risks = [part.strip() for part in normalized.split(",") if part.strip()]
    invalid = sorted(set(risks) - VALID_RISKS)
    if invalid:
        raise argparse.ArgumentTypeError(
            "unknown risks: " + ", ".join(invalid) + "; choose from face,faces,hands,geometry,text"
        )
    return risks


def parse_args(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--subject", choices=SUBJECT_CHOICES, default="portrait")
    parser.add_argument("--light", choices=LIGHT_CHOICES, default="flat")
    parser.add_argument("--motion", choices=MOTION_CHOICES, default="still")
    parser.add_argument("--depth", choices=DEPTH_CHOICES, default="shallow")
    parser.add_argument("--background", choices=BACKGROUND_CHOICES, default="indoor")
    parser.add_argument("--reflection", action="store_true")
    parser.add_argument("--flora", action="store_true")
    parser.add_argument(
        "--practical-lights",
        action="store_true",
        help="visible path, edge, ground, or other practical fixtures can drive halation",
    )
    parser.add_argument(
        "--implied-movement",
        action="store_true",
        help="perspective or repeated structures imply public passage even without visible people",
    )
    parser.add_argument(
        "--risks",
        type=parse_risks,
        default=None,
        help="auto, none, or comma-separated: face,faces,hands,geometry,text",
    )
    parser.add_argument("--strength", choices=STRENGTH_CHOICES, default="dream-haze")
    parser.add_argument("--fidelity", choices=FIDELITY_CHOICES, default="semantic-core")
    parser.add_argument("--mood", choices=MOOD_CHOICES, default="auto")
    parser.add_argument("--subject-axis", choices=SUBJECT_AXIS_CHOICES, default="auto")
    parser.add_argument("--structure-role", choices=STRUCTURE_ROLE_CHOICES, default="auto")
    parser.add_argument("--json", action="store_true")
    return parser.parse_args(argv)


def main(argv=None):
    args = parse_args(argv)
    result = analyze_observations(
        PhotoObservations(
            subject=args.subject,
            light=args.light,
            motion=args.motion,
            depth=args.depth,
            reflection=args.reflection,
            flora=args.flora,
            practical_lights=args.practical_lights,
            implied_movement=args.implied_movement,
            background=args.background,
            risks=args.risks,
            strength=args.strength,
            fidelity=args.fidelity,
            mood=args.mood,
            subject_axis=args.subject_axis,
            structure_role=args.structure_role,
        )
    )
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        strategy = result["strategy"]
        print(f"composition: {strategy['composition']}")
        print(f"motion: {strategy['motion']}")
        print(f"optical: {strategy['optical']}")
        print(f"lighting: {strategy['lighting']}")
        print(f"strength: {strategy['strength']}")
        print(f"palette: {result['palette']}")
        print(f"aspect-ratio: {result['aspect_ratio']}")
        allocation = result["composition"]["visual_allocation"]
        print(
            "visual-allocation: "
            f"hero {allocation['hero_percent']}%, "
            f"kinetic {allocation['kinetic_percent']}%, "
            f"quiet {allocation['quiet_percent']}%"
        )
        print("constraints:")
        for constraint in result["constraints"]:
            print(f"  - {constraint}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
