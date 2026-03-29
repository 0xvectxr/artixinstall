"""
artixinstall.utils.validate — Input validation helpers.

Provides validation functions for usernames, hostnames, passwords, and
other user-supplied inputs to guard against injection and invalid data.
"""

import re


def is_valid_username(name: str) -> tuple[bool, str]:
    """
    Validate a Linux username.

    Rules: 1-32 chars, lowercase letters/digits/underscore, must start
    with a letter or underscore.

    Returns (True, "") on success, (False, reason) on failure.
    """
    if not name:
        return False, "Username cannot be empty."
    if len(name) > 32:
        return False, "Username must be 32 characters or fewer."
    if not re.match(r'^[a-z_][a-z0-9_]*$', name):
        return False, "Username must be lowercase alphanumeric or underscore, starting with a letter or underscore."
    # Reject names that could clash with system accounts
    reserved = {"root", "daemon", "bin", "sys", "sync", "games", "man",
                "lp", "mail", "news", "uucp", "proxy", "www-data",
                "nobody", "systemd-network", "sshd"}
    if name in reserved:
        return False, f"'{name}' is a reserved system username."
    return True, ""


def is_valid_hostname(name: str) -> tuple[bool, str]:
    """
    Validate a hostname per RFC 1123.

    Returns (True, "") on success, (False, reason) on failure.
    """
    if not name:
        return False, "Hostname cannot be empty."
    if len(name) > 63:
        return False, "Hostname must be 63 characters or fewer."
    if not re.match(r'^[a-zA-Z0-9]([a-zA-Z0-9\-]*[a-zA-Z0-9])?$', name):
        return False, "Hostname must be alphanumeric (hyphens allowed, not at start/end)."
    return True, ""


def is_valid_password(password: str) -> tuple[bool, str]:
    """
    Validate a password (minimal rules — we don't enforce complexity,
    just non-empty and no control characters).

    Returns (True, "") on success, (False, reason) on failure.
    """
    if not password:
        return False, "Password cannot be empty."
    if len(password) < 1:
        return False, "Password cannot be empty."
    # Reject control characters (except common ones)
    if any(ord(c) < 32 and c not in ('\t',) for c in password):
        return False, "Password contains invalid control characters."
    return True, ""


def sanitize_shell_arg(value: str) -> str:
    """
    Sanitize a string for safe inclusion in a shell command.

    This is a defense-in-depth measure — callers should also use
    parameterized commands where possible.
    """
    # Remove any characters that could break out of a shell string
    # Allow only printable ASCII minus dangerous shell metacharacters
    allowed = set(
        'abcdefghijklmnopqrstuvwxyz'
        'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        '0123456789'
        ' ._-+=/:@,'
    )
    return ''.join(c for c in value if c in allowed)


def is_valid_locale(locale: str) -> tuple[bool, str]:
    """
    Basic validation that a locale string looks correct.

    Expected format: xx_XX.UTF-8 (or similar).
    """
    if not locale:
        return False, "Locale cannot be empty."
    if not re.match(r'^[a-z]{2,3}_[A-Z]{2}(\.\S+)?$', locale):
        return False, "Locale must be in format xx_XX or xx_XX.UTF-8."
    return True, ""
