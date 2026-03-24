#!/usr/bin/env python3

import argparse
import secrets
import string
from dataclasses import dataclass
from pathlib import Path


YES_VALUES = {"y", "yes"}
NO_VALUES = {"n", "no"}


@dataclass
class PasswordConfig:
    length: int
    mixed_case: bool
    include_numbers: bool
    include_special_chars: bool
    save: bool
    name: str | None = None
    path: Path | None = None

    def __post_init__(self) -> None:
        if self.length <= 0:
            raise ValueError("Password length must be greater than 0.")

        if self.save:
            if not self.name or not self.name.strip():
                raise ValueError("Name is required when save=True.")
            if self.path is None:
                raise ValueError("Path is required when save=True.")
            if not self.path.exists() or not self.path.is_dir():
                raise ValueError(f"Path does not exist or is not a directory: {self.path}")


def generate_password(
    length: int,
    mixed_case: bool = True,
    include_numbers: bool = True,
    include_special_chars: bool = True,
) -> str:
    char_string = string.ascii_lowercase

    if mixed_case:
        char_string += string.ascii_uppercase
    if include_numbers:
        char_string += string.digits
    if include_special_chars:
        char_string += string.punctuation

    return "".join(secrets.choice(char_string) for _ in range(length))


def prompt_yes_no(prompt: str) -> bool:
    while True:
        answer = input(prompt).strip().lower()
        if answer in YES_VALUES:
            return True
        if answer in NO_VALUES:
            return False
        print("--ERROR-- Expected answers are [y|yes|n|no]. Try again.")


def parse_yes_no(value: str | None, prompt: str) -> bool:
    if value is None:
        return prompt_yes_no(prompt)

    value = value.strip().lower()
    if value in YES_VALUES:
        return True
    if value in NO_VALUES:
        return False

    raise ValueError("--ERROR-- Expected answers are [y|yes|n|no]")


def get_length(value: int | None) -> int:
    if value is not None:
        if value <= 0:
            raise ValueError("--ERROR-- Password length must be greater than 0.")
        return value

    while True:
        raw = input("Length of password: ").strip()
        try:
            length = int(raw)
            if length <= 0:
                print("--ERROR-- Password length must be greater than 0.")
                continue
            return length
        except ValueError:
            print("--ERROR-- Please enter a valid integer.")


def get_name(value: str | None) -> str:
    if value is not None:
        value = value.strip()
        if not value:
            raise ValueError("--ERROR-- Name cannot be empty.")
        return value

    while True:
        name = input("Enter name of password: ").strip()
        if name:
            return name
        print("--ERROR-- Name cannot be empty.")


def get_path(value: str | None) -> Path:
    if value is not None:
        path = Path(value).expanduser()
        if not path.exists() or not path.is_dir():
            raise ValueError(f"--ERROR-- Please make sure {path} exists.")
        return path

    while True:
        raw = input("Enter path to save password file: ").strip()
        path = Path(raw).expanduser()
        if path.exists() and path.is_dir():
            return path
        print(f"--ERROR-- Please make sure {path} exists.")


def get_args() -> PasswordConfig:
    parser = argparse.ArgumentParser(description="Generate a random password.")
    parser.add_argument("-l", "--length", type=int, help="Length of password")
    parser.add_argument("-mc", "--mixed_case", type=str, help="Use mixed case? [y|yes|n|no]")
    parser.add_argument("-in", "--include_numbers", type=str, help="Include numbers? [y|yes|n|no]")
    parser.add_argument(
        "-is",
        "--include_special_chars",
        type=str,
        help="Include special characters? [y|yes|n|no]",
    )
    parser.add_argument("-s", "--save", type=str, help="Save password to file? [y|yes|n|no]")
    parser.add_argument("-n", "--name", type=str, help="Name of password")
    parser.add_argument("-p", "--path", type=str, help="Path to save password file")

    args = parser.parse_args()

    length = get_length(args.length)
    mixed_case = parse_yes_no(args.mixed_case, "Use mixed case? [y|yes|n|no]: ")
    include_numbers = parse_yes_no(args.include_numbers, "Include numbers? [y|yes|n|no]: ")
    include_special_chars = parse_yes_no(
        args.include_special_chars,
        "Include special characters? [y|yes|n|no]: ",
    )
    save = parse_yes_no(args.save, "Save password to file? [y|yes|n|no]: ")

    name = None
    path = None

    if save:
        name = get_name(args.name)
        path = get_path(args.path)

    return PasswordConfig(
        length=length,
        mixed_case=mixed_case,
        include_numbers=include_numbers,
        include_special_chars=include_special_chars,
        save=save,
        name=name,
        path=path,
    )


def main() -> None:
    config = get_args()

    password = generate_password(
        length=config.length,
        mixed_case=config.mixed_case,
        include_numbers=config.include_numbers,
        include_special_chars=config.include_special_chars,
    )

    if config.save:
        filename = config.path / f"{config.name}.pwd"
        filename.write_text(password + "\n", encoding="utf-8")
        print(f"Password saved to {filename}")
    else:
        print(password)


if __name__ == "__main__":
    main()