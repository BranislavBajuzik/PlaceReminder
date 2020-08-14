import argparse
import string
from pathlib import Path
from random import choice
from typing import Literal, Set


def take_action(
    file: Path, action: Literal["add", "remove", "list", "pick"], places: Set[str], place: str = None
) -> int:
    if action == "list":
        if places:
            print(f"Stored places ({len(places)}):")
            print("\n".join(sorted(places)))
        else:
            print("No places sorted")
        return 0

    if action == "pick":
        chosen = choice(tuple(places))
        print(f"'{chosen}' was chosen")

        if input("Satisfied? ")[:1].lower() == "y":
            return take_action(file, "remove", places, chosen)
        else:
            return take_action(file, "pick", places)

    if place is None:
        print(f"Place required for action {action}")
        return 1

    place = normalize(place)

    if action == "add":
        if place in places:
            print(f"[warning] Place '{place}' already stored")
            return 0

        places.add(place)
    elif action == "remove":
        if place not in places:
            print(f"[warning] Place '{place}' was not stored")
            return 0

        places.discard(place)

    file.write_text("\n".join(places), encoding="utf-8")

    return 0


def normalize(text: str) -> str:
    return string.capwords(text.strip().casefold())


def load_places(file: Path) -> Set[str]:
    if not file.is_file():
        return set()

    with file.open(encoding="utf-8") as f:
        return {stripped for line in f if (stripped := normalize(line))}


def parse_cli() -> argparse.Namespace:
    parser = argparse.ArgumentParser(prog="PlaceReminder", allow_abbrev=False)

    parser.add_argument("file", type=Path, help="File to read/store the places in")

    parser.add_argument("action", choices=("add", "remove", "list", "pick"), help="File to read/store the places in")

    parser.add_argument("places", nargs="*", help="Places to add/remove")

    return parser.parse_args()


def main() -> int:
    args = parse_cli()

    places = load_places(args.file)

    if not args.places:
        return take_action(args.file, args.action, places)

    for place in args.places:
        if ret := take_action(args.file, args.action, places, place):
            return ret

    return 0


if __name__ == "__main__":
    exit(main())
