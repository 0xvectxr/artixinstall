"""
artixinstall.installer.network — Hostname and network service configuration.

Handles setting the hostname and selecting/enabling a network manager.
"""

import os

from artixinstall.utils.shell import run, MOUNT_POINT
from artixinstall.utils.log import log_info
from artixinstall.tui.screen import Screen
from artixinstall.tui.menu import run_selection_menu
from artixinstall.tui.prompts import text_input
from artixinstall.utils.validate import is_valid_hostname

# Network manager options and their service/package requirements
NETWORK_OPTIONS = {
    "NetworkManager": {
        "description": "NetworkManager (recommended, GUI-friendly)",
        "packages": ["networkmanager"],
        "services": ["NetworkManager"],
    },
    "dhcpcd": {
        "description": "dhcpcd (simple, wired connections)",
        "packages": ["dhcpcd"],
        "services": ["dhcpcd"],
    },
    "wpa_supplicant+dhcpcd": {
        "description": "wpa_supplicant + dhcpcd (wifi without GUI)",
        "packages": ["wpa_supplicant", "dhcpcd"],
        "services": ["wpa_supplicant", "dhcpcd"],
    },
    "none": {
        "description": "None (manual configuration)",
        "packages": [],
        "services": [],
    },
}


def configure_hostname(screen: Screen) -> str | None:
    """
    Interactive hostname configuration.

    Returns the hostname string, or None if cancelled.
    """
    return text_input(
        screen,
        "Enter hostname for the new system:",
        default="artix",
        validator=is_valid_hostname,
    )


def configure_network(screen: Screen) -> str | None:
    """
    Interactive network manager selection.

    Returns the network manager key, or None if cancelled.
    """
    options = [info["description"] for info in NETWORK_OPTIONS.values()]
    keys = list(NETWORK_OPTIONS.keys())

    selected = run_selection_menu(screen, "Select network manager", options)
    if selected is None:
        return None

    idx = options.index(selected)
    return keys[idx]


def get_network_packages(network_choice: str) -> list[str]:
    """Get the package list for a network manager choice."""
    info = NETWORK_OPTIONS.get(network_choice, {})
    return list(info.get("packages", []))


def get_network_services(network_choice: str) -> list[str]:
    """Get the service names that need to be enabled for a network manager."""
    info = NETWORK_OPTIONS.get(network_choice, {})
    return list(info.get("services", []))


def apply_hostname(hostname: str) -> tuple[bool, str]:
    """
    Apply hostname settings inside the chroot.

    Steps:
    1. Write /etc/hostname
    2. Write /etc/hosts
    """
    hostname_path = os.path.join(MOUNT_POINT, "etc", "hostname")
    hosts_path = os.path.join(MOUNT_POINT, "etc", "hosts")

    try:
        with open(hostname_path, "w") as f:
            f.write(f"{hostname}\n")
    except OSError as e:
        return False, f"Failed to write hostname: {e}"

    try:
        with open(hosts_path, "w") as f:
            f.write("# /etc/hosts: static lookup table for host names\n")
            f.write("#\n")
            f.write("# <ip-address>   <hostname.domain.org>   <hostname>\n")
            f.write(f"127.0.0.1       localhost\n")
            f.write(f"::1             localhost\n")
            f.write(f"127.0.1.1       {hostname}.localdomain   {hostname}\n")
    except OSError as e:
        return False, f"Failed to write hosts file: {e}"

    log_info(f"Hostname set to {hostname}")
    return True, ""
