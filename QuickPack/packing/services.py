"""Box recommendation logic. Pure Python (no database) so it is easy to test.

Units: cm, kg, rupees.
"""
from collections import Counter
from dataclasses import dataclass
from itertools import permutations
from typing import Optional

# Fragile items are never packed with items heavier than this.
FRAGILE_HEAVY_LIMIT_KG = 2.0


@dataclass(frozen=True)
class Item:
    name: str
    length: float
    width: float
    height: float
    weight: float
    fragile: bool = False

    @property
    def dims(self):
        return (self.length, self.width, self.height)

    @property
    def volume(self):
        return self.length * self.width * self.height


@dataclass(frozen=True)
class BoxSpec:
    name: str
    length: float
    width: float
    height: float
    max_weight: float
    cost: float
    id: Optional[int] = None

    @property
    def dims(self):
        return (self.length, self.width, self.height)

    @property
    def volume(self):
        return self.length * self.width * self.height


def expand(order_items):
    """[(Item, qty)] -> flat list with one entry per physical unit."""
    return [item for item, qty in order_items for _ in range(qty)]


def fits_alone(item, box):
    """Rotation allowed: compare sorted dimensions."""
    return all(i <= b for i, b in zip(sorted(item.dims), sorted(box.dims)))


def can_pack(units, box):
    """Shelf/layer heuristic. Returns True only if a real placement was found,
    so it never says 'fits' when it does not (it may miss tight packings).

    Box is filled in layers (bottom to top); each layer has rows (along the width);
    each row is filled along the length. Biggest items are placed first and every
    one of the 6 orientations is tried.
    """
    L, W, H = box.dims
    layers = []  # {"h": layer height, "used_w": width used, "rows": [[row_width, used_len]]}
    used_h = 0.0
    for u in sorted(units, key=lambda x: -x.volume):
        orients = sorted(set(permutations(u.dims)))
        placed = False
        for a, b, c in orients:                      # a=length b=width c=height
            for layer in layers:
                if c > layer["h"]:
                    continue
                for row in layer["rows"]:            # 1) existing row
                    if b <= row[0] and row[1] + a <= L:
                        row[1] += a
                        placed = True
                        break
                if not placed and a <= L and layer["used_w"] + b <= W:  # 2) new row
                    layer["rows"].append([b, a])
                    layer["used_w"] += b
                    placed = True
                if placed:
                    break
            if placed:
                break
        if not placed:                               # 3) new layer on top
            for a, b, c in orients:
                if a <= L and b <= W and used_h + c <= H:
                    layers.append({"h": c, "used_w": b, "rows": [[b, a]]})
                    used_h += c
                    placed = True
                    break
        if not placed:
            return False
    return True


def fragile_conflict(units):
    has_fragile = any(u.fragile for u in units)
    has_heavy = any(u.weight > FRAGILE_HEAVY_LIMIT_KG and not u.fragile for u in units)
    return has_fragile and has_heavy


def check_box(units, box):
    """Returns (ok, reason). Reason explains the FIRST thing that fails."""
    total_weight = sum(u.weight for u in units)
    if total_weight > box.max_weight:
        return False, f"total weight {total_weight:.2f} kg is above the {box.max_weight:g} kg limit"
    for u in units:
        if not fits_alone(u, box):
            return False, (f"'{u.name}' ({' x '.join(f'{d:g}' for d in u.dims)} cm) "
                           f"does not fit in any orientation")
    if sum(u.volume for u in units) > box.volume:
        return False, "total item volume is bigger than the box volume"
    if not can_pack(units, box):
        return False, "items fit individually but could not be arranged together"
    return True, "fits"


def cheapest_fit(units, ordered_boxes):
    for box in ordered_boxes:
        if check_box(units, box)[0]:
            return box
    return None


def _compatible(group, unit):
    """Fragile vs heavy rule for split packing."""
    if unit.fragile and any(x.weight > FRAGILE_HEAVY_LIMIT_KG and not x.fragile for x in group):
        return False
    if unit.weight > FRAGILE_HEAVY_LIMIT_KG and not unit.fragile and any(x.fragile for x in group):
        return False
    return True


def split_pack(units, ordered_boxes):
    """Greedy: biggest item first; put it where it adds the least cost
    (an existing box, possibly upgraded to a bigger one, or a new box).
    Returns (bins, None) or (None, unfittable_unit)."""
    bins = []
    for u in sorted(units, key=lambda x: -x.volume):
        new_box = cheapest_fit([u], ordered_boxes)
        if new_box is None:
            return None, u
        best = (new_box.cost, None, new_box)         # (added cost, bin, box)
        for b in bins:
            if not _compatible(b["units"], u):
                continue
            box = cheapest_fit(b["units"] + [u], ordered_boxes)
            if box is not None and box.cost - b["box"].cost <= best[0]:
                best = (box.cost - b["box"].cost, b, box)
        _, target, box = best
        if target is None:
            bins.append({"units": [u], "box": box})
        else:
            target["units"].append(u)
            target["box"] = box
    return bins, None


def _report(box, units):
    fill = round(100 * sum(u.volume for u in units) / box.volume, 1)
    return {
        "box": box.name, "box_id": box.id, "cost": box.cost,
        "items": dict(Counter(u.name for u in units)),
        "weight_kg": round(sum(u.weight for u in units), 3),
        "fill_percent": fill, "wasted_percent": round(100 - fill, 1),
    }


def recommend(order_items, boxes, allow_split=True):
    """order_items: [(Item, qty)], boxes: [BoxSpec].

    status: single_box | multi_box | no_fit | empty
    """
    units = expand(order_items)
    base = {"status": "empty", "message": "Order has no items", "boxes": [],
            "total_cost": 0, "total_weight_kg": 0, "rejected": [], "warnings": [],
            "savings_vs_largest": None}
    if not units:
        return base
    base["total_weight_kg"] = round(sum(u.weight for u in units), 3)
    if not boxes:
        return {**base, "status": "no_fit", "message": "No boxes are configured"}

    ordered = sorted(boxes, key=lambda b: (b.cost, b.volume))   # cheapest first
    largest = max(boxes, key=lambda b: b.volume)

    rejected = []
    if fragile_conflict(units):
        why = (f"fragile items cannot share a box with items heavier than "
               f"{FRAGILE_HEAVY_LIMIT_KG:g} kg")
        rejected = [{"box": b.name, "reason": why} for b in ordered]
    else:
        for box in ordered:
            ok, reason = check_box(units, box)
            if ok:
                return {**base, "status": "single_box",
                        "message": f"Use the {box.name} box: cheapest box that fits everything",
                        "boxes": [_report(box, units)], "total_cost": box.cost,
                        "savings_vs_largest": largest.cost - box.cost, "rejected": rejected}
            rejected.append({"box": box.name, "reason": reason})
    base["rejected"] = rejected

    if allow_split:
        bins, bad = split_pack(units, ordered)
        if bad is not None:
            return {**base, "status": "no_fit",
                    "message": f"'{bad.name}' does not fit in any available box, even alone"}
        reports = [_report(b["box"], b["units"]) for b in bins]
        total = sum(r["cost"] for r in reports)
        if fragile_conflict(units):
            msg = (f"Fragile items cannot share a box with items heavier than "
                   f"{FRAGILE_HEAVY_LIMIT_KG:g} kg, so the order is split into {len(reports)} boxes")
        else:
            msg = f"No single box fits. Split into {len(reports)} boxes"
        return {**base, "status": "multi_box", "boxes": reports, "total_cost": total,
                "message": msg,
                "warnings": ["Order is shipped in multiple parcels"]}

    return {**base, "status": "no_fit", "message": "No single box fits"}
