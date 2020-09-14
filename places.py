import argparse
import logging
import string
from pathlib import Path
from random import choice
from typing import Literal, Set


def general_action(path: Path, action: Literal["list", "pick", "drop"], places: Set[str]) -> int:
    """Handle user choice and data.

    :param path: Path to store data in.
    :param action: Action user requested.
    :param places: All data in :ref:`path`.
    :return: Exit code.
    """
    if action == "list":
        if places:
            print(f"Stored places ({len(places)}):")
            print("\n".join(sorted(places)))
        else:
            logging.warning("No places stored")
        return 0

    if action == "pick":
        if not places:
            logging.error("No places stored!")
            return 2

        while True:
            chosen = choice(tuple(places))
            print(f"'{chosen}' was picked")

            answer = input("Satisfied? (Yes/No/Quit): ")[:1].lower()

            if answer == "y":
                print(f"You chose '{chosen}'. Enjoy!")
                return place_action(path, "remove", places, chosen)
            elif answer == "q":
                return 0

    if action == "drop":
        if not path.exists():
            logging.warning("No places stored")
        else:
            path.unlink(missing_ok=True)
            logging.info('Places in "%s" were dropped', path)
        return 0


def place_action(path: Path, action: Literal["add", "remove"], places: Set[str], place: str) -> int:
    """Handle user choice and data.

    :param path: Path to store data in.
    :param action: Action user requested.
    :param places: All data in :ref:`path`.
    :param place: Data user entered.
    :return: Exit code.
    """
    place = normalize(place)

    if action == "add":
        if place in places:
            logging.warning("Place '%s' is already stored", place)
            return 0

        places.add(place)
    elif action == "remove":
        if place not in places:
            logging.warning("Place '%s' was not stored", place)
            return 0

        places.discard(place)

    if places:
        path.write_text("\n".join(places), encoding="utf-8")
    else:
        path.unlink(missing_ok=True)

    logging.info("Place %s successfully %sed", place, action)

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

    def log_level(arg: str) -> str:
        arg = arg.upper()

        if arg not in logging._nameToLevel:
            raise argparse.ArgumentTypeError(f"Invalid choice '{arg}', pick from {tuple(logging._nameToLevel)}")

        return arg

    parser = argparse.ArgumentParser(prog="PlaceReminder", allow_abbrev=False)

    parser.add_argument("file", type=Path, help="File to read/store the places in")

    parser.add_argument("action", choices=("add", "remove", "drop", "list", "pick"), help="Action to take")

    parser.add_argument("places", nargs="*", help="Places to add/remove")

    parser.add_argument(
        "--log-level",
        type=log_level,
        default=logging._levelToName[logging.INFO],
        help="Sets the logging level",
    )

    return parser.parse_args()


def main() -> int:
    """Program entrypoint.

    :return: Exit code.
    """
    args = parse_cli()

    logging.basicConfig(level=args.log_level, format="[%(levelname)s] %(message)s")

    places = load_places(args.file)

    if args.action in ("drop", "list", "pick"):
        if args.places:
            logging.warning("Action '%s' does not accept any places", args.action)

        return general_action(args.file, args.action, places)

    if not args.places:
        logging.error("Place required for '%s' action", args.action)
        return 1

    for place in args.places:
        if ret := place_action(args.file, args.action, places, place):
            return ret

    return 0


if __name__ == "__main__":
    exit(main())
