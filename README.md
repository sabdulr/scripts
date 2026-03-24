OK, after several years I decided to log back into GitHub and try to update existing code and add new repositories.

# Password Generator

A simple Python password generator for personal use.

This version supports both command-line arguments and interactive prompts. If you do not pass an argument, the script will ask for it interactively.

## Features

- Generate random passwords
- Interactive mode for missing arguments
- Optional uppercase letters
- Optional numbers
- Optional special characters
- Optional saving to a file
- Uses `dataclasses` for configuration
- Uses `secrets` instead of `random` for password generation

## What Changed

The script was updated to improve structure, correctness, and security.

### 1. Switched from `random` to `secrets`

Password generation now uses Python’s `secrets` module:

- `random.choice(...)` was replaced with `secrets.choice(...)`

This is better for password generation because `secrets` is intended for sensitive random values.

### 2. Added a `dataclass` for configuration

A `PasswordConfig` dataclass now stores the resolved settings for the script.

This makes the code easier to read and maintain by grouping related settings in one place.

Example fields:

- `length`
- `mixed_case`
- `include_numbers`
- `include_special_chars`
- `save`
- `name`
- `path`

### 3. Kept interactive mode

If you do not provide arguments, the script prompts you for them.

For example:

- password length
- whether to include uppercase letters
- whether to include numbers
- whether to include special characters
- whether to save the password
- file name and path if saving is enabled

### 4. Improved validation

Validation is now cleaner and more explicit.

Examples:

- password length must be greater than 0
- save path must exist and be a directory
- name must be present when saving

### 5. Fixed character-set behavior

The password character pool now starts with lowercase letters and conditionally adds:

- uppercase letters
- digits
- punctuation

This is cleaner than the previous approach.

## Requirements

- Python 3.10+ recommended

This script uses:
- `dataclasses`
- `pathlib`
- modern type hints like `str | None`

## Usage

### Interactive mode

Run with no arguments:

```bash
python3 genPassword.py