"""Main file."""

import argparse
import string
from pathlib import Path
from random import choice
from typing import Literal, Set


def take_action(
    path: Path, action: Literal["add", "remove", "list", "pick"], places: Set[str], place: str = None
) -> int:
    """Handle user choice and data.

    :param path: Path to store data in.
    :param action: Action user requested.
    :param places: All data in :ref:`path`.
    :param place: Data user entered.
    :return: Exit code.
    """
    if action == "list":
        if places:
            print(f"Stored places ({len(places)}):")
            print("\n".join(sorted(places)))
        else:
            print("No places sorted")
        return 0

    if action == "pick":
        if not places:
            print("No places stored")
            return 2

        chosen = choice(tuple(places))
        print(f"'{chosen}' was chosen")

        if (satisfaction := input("Satisfied? (y/n/q): ")[:1].lower()) == "y":
            return take_action(path, "remove", places, chosen)
        elif satisfaction == "q":
            return 0
        else:
            return take_action(path, "pick", places)

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

    if places:
        path.write_text("\n".join(places), encoding="utf-8")
    else:
        path.unlink(missing_ok=True)

    return 0


def normalize(text: str) -> str:
    """Normalize :ref:`text` for string operations.

    :param text: String to normalize.
    :return: Normalized string.
    """
    return string.capwords(text.strip().casefold())


def load_places(path: Path) -> Set[str]:
    """Deserialize data.

    :param path: Path to load from.
    :return: Deserialized data.
    """
    if not path.is_file():
        return set()

    with path.open(encoding="utf-8") as f:
        return {stripped for line in f if (stripped := normalize(line))}


def parse_cli() -> argparse.Namespace:
    """Parse the command line arguments.

    :return: Object with arguments bound as attributes.
    """
    parser = argparse.ArgumentParser(prog="PlaceReminder", allow_abbrev=False)

    parser.add_argument("file", type=Path, help="File to read/store the places in")

    parser.add_argument("action", choices=("add", "remove", "list", "pick"), help="Action to take")

    parser.add_argument("places", nargs="*", help="Places to add/remove")

    return parser.parse_args()


def main() -> int:
    """Program entrypoint.

    :return: Exit code.
    """
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
