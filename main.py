#!/usr/bin/env python3
"""Write one unsent micro-confession to /output/entry.txt.

The entry is exactly two parts: a To: line naming who the message was
meant for, and the unsent message itself, one line written as it was
typed, with no explanation after it.
"""

import os

TO_LINE = "To: Rosa, my aunt"

MESSAGE = (
    "I never told you I heard you crying the night uncle left. "
    "I was twelve and I stood outside your door for an hour "
    "holding a glass of water."
)

MAX_ENTRY_CHARS = 260
MAX_MESSAGE_CHARS = 200


def output_directory():
    """The directory the entry is written to, /output unless overridden."""
    return os.environ.get("OUTPUT_DIR", "/output")


def parts():
    """The two parts of the confession: addressee line and message line."""
    to_line = TO_LINE.strip()
    message = MESSAGE.strip()
    assert to_line.startswith("To: "), "entry must open with a To: line"
    assert "\n" not in message, "message must be one line"
    assert len(message) <= MAX_MESSAGE_CHARS, "message must be at most 200 characters"
    return to_line, message


def build_entry():
    """Assemble the two-part confession as one text."""
    to_line, message = parts()
    text = to_line + "\n" + message
    assert 1 <= len(text) <= MAX_ENTRY_CHARS, "entry must be 1 to 260 characters"
    return text


def main():
    out_dir = output_directory()
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    text = build_entry()
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(text + "\n")
    try:
        os.chmod(path, 0o644)
    except OSError:
        pass
    verify(path, text)


def verify(path, expected):
    """Read the file back and confirm it holds exactly the entry text."""
    with open(path, encoding="utf-8", newline="\n") as f:
        written = f.read()
    assert written == expected + "\n", "entry.txt does not match the confession"
    print(path)
    print(expected)


if __name__ == "__main__":
    os.umask(0o022)
    main()
