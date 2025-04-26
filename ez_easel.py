import argparse
import typing


STANDARD_EASEL_SLOTS = [(5, 7), (8, 10), (11, 14), (16, 20), (20, 24)]


class Point(typing.NamedTuple):
    x: float
    y: float


class Box(typing.NamedTuple):
    height: float
    width: float


class EaselBlades(typing.NamedTuple):
    left: float
    right: float
    top: float
    bottom: float


ASPECT_RATIOS = {
    "135F": 24 / 36,
    "135H": 18 / 24,
    "135FP": 24 / 65,
    "6x4.5": 4.5 / 6,
    "6x6": 6 / 6,
    "6x7": 6 / 7,
    "6x8": 6 / 8,
    "6x9": 6 / 9,
    "4x5": 4 / 5,
}
FLIPPED_RATIOS = {f"-{k}": 1 / v for k, v in ASPECT_RATIOS.items()}
ASPECT_RATIOS.update(FLIPPED_RATIOS)


def easel_slot(paper_width: float) -> Box:
    for easel_height, easel_width in STANDARD_EASEL_SLOTS:
        if paper_width <= easel_width:
            return Box(easel_height, easel_width)
    raise ValueError(f"paper width {paper_width} too wide to fit")


def image_dimensions(
    paper_height, paper_width, aspect_ratio: str, border: float
) -> Box:
    ratio = ASPECT_RATIOS[aspect_ratio]
    max_height = paper_height - border * 2
    max_width = paper_width - border * 2

    option_1 = Box(max_height, max_height / ratio)
    option_2 = Box(max_width * ratio, max_width)

    if option_1.width > max_width:
        return option_2
    return option_1


def ez_easel(
    paper_height: float, paper_width: float, image_height: float, image_width: float
) -> EaselBlades:
    slot = easel_slot(paper_width)

    easel_center = Point(slot.width / 2, slot.height / 2)

    top_left_corner = Point(
        (paper_width - image_width) / 2, (paper_height - image_height) / 2
    )
    bottom_right_corner = Point(
        paper_width - top_left_corner.x, paper_height - top_left_corner.y
    )

    left_blade = (easel_center.x - top_left_corner.x) * 2
    right_blade = (bottom_right_corner.x - easel_center.x) * 2
    top_blade = (easel_center.y - top_left_corner.y) * 2
    bottom_blade = (bottom_right_corner.y - easel_center.y) * 2

    return EaselBlades(left_blade, right_blade, top_blade, bottom_blade)


def ez_ez_easel(
    paper_height: float, paper_width: float, aspect_ratio: str, border: float
) -> EaselBlades:
    image_dims = image_dimensions(paper_height, paper_width, aspect_ratio, border)
    return ez_easel(paper_height, paper_width, image_dims.height, image_dims.width)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("paper_height", type=float)
    parser.add_argument("paper_width", type=float)
    parser.add_argument("aspect_ratio", type=str)
    parser.add_argument("border", type=float)
    # parser.add_argument("image_height", type=float)
    # parser.add_argument("image_width", type=float)

    args = parser.parse_args()
    # easel_blades = ez_easel(args.paper_height, args.paper_width, args.image_height, args.image_width)
    easel_blades = ez_ez_easel(
        args.paper_height, args.paper_width, args.aspect_ratio, args.border
    )
    image_size = image_dimensions(
        args.paper_height, args.paper_width, args.aspect_ratio, args.border
    )
    easel_slot = easel_slot(args.paper_width)
    print(f"use the easel's slot for {easel_slot.height} x {easel_slot.width}")
    print(f"image size: {image_size.height:.02f} x {image_size.width:.02f}")
    print("set the easel's blades to:")
    print(
        "  "
        f"left: {easel_blades.left:.02f} right: {easel_blades.right:.02f}, "
        f"top: {easel_blades.top:.02f}, bottom: {easel_blades.bottom:.02f}"
    )
