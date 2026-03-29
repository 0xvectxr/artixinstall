"""
artixinstall.installer.desktop — Desktop environment and window manager installation.

Comprehensive selection covering full DEs (GNOME, KDE, XFCE, etc.) and
tiling/stacking WMs (Hyprland, Sway, i3, bspwm, etc.) — matching and
exceeding archinstall's desktop offering.
"""

from artixinstall.utils.log import log_info
from artixinstall.tui.screen import Screen
from artixinstall.tui.menu import run_selection_menu

# ── Shared package groups ──

_PIPEWIRE = [
    "pipewire", "pipewire-pulse", "pipewire-alsa", "wireplumber",
    "pipewire-jack",
]

_XORG = ["xorg-server", "xorg-xinit", "xorg-xrandr", "xorg-xsetroot"]

_WAYLAND_BASE = ["xorg-xwayland", "xdg-desktop-portal"]

_COMMON_UTILS = [
    "xdg-utils", "xdg-user-dirs",
]

# ── Desktop environment definitions ──
# Each entry includes:
#   label:            display name in the menu
#   category:         "de" (desktop environment) or "wm" (window manager) or "none"
#   packages:         list of packages to install
#   display_manager:  DM to use (or None for TTY-launched WMs)
#   services:         services to enable (looked up in services.json)
#   extra_services:   additional services that don't need init-specific mapping (just names)

DESKTOP_ENVIRONMENTS = {
    # ── No desktop ──
    "none": {
        "label": "None (command-line only)",
        "category": "none",
        "packages": [],
        "display_manager": None,
        "services": [],
    },

    # ══════════════════════════════════════
    # ── Full Desktop Environments ──
    # ══════════════════════════════════════

    "gnome": {
        "label": "GNOME",
        "category": "de",
        "packages": [
            "gnome", "gnome-extra",
            "gdm",
            "xdg-desktop-portal-gnome",
            *_WAYLAND_BASE, *_PIPEWIRE, *_COMMON_UTILS,
        ],
        "display_manager": "gdm",
        "services": ["gdm"],
    },

    "kde": {
        "label": "KDE Plasma",
        "category": "de",
        "packages": [
            "plasma", "kde-applications",
            "sddm",
            "xdg-desktop-portal-kde",
            "phonon-qt6-vlc",
            *_XORG, *_WAYLAND_BASE, *_PIPEWIRE, *_COMMON_UTILS,
        ],
        "display_manager": "sddm",
        "services": ["sddm"],
    },

    "xfce": {
        "label": "XFCE",
        "category": "de",
        "packages": [
            "xfce4", "xfce4-goodies",
            "lightdm", "lightdm-gtk-greeter", "lightdm-gtk-greeter-settings",
            "gvfs", "thunar-archive-plugin", "file-roller",
            "pavucontrol", "network-manager-applet",
            *_XORG, *_PIPEWIRE, *_COMMON_UTILS,
        ],
        "display_manager": "lightdm",
        "services": ["lightdm"],
    },

    "cinnamon": {
        "label": "Cinnamon",
        "category": "de",
        "packages": [
            "cinnamon", "nemo-fileroller", "gnome-terminal",
            "lightdm", "lightdm-gtk-greeter",
            "gnome-screenshot", "gnome-keyring",
            "blueberry",
            *_XORG, *_PIPEWIRE, *_COMMON_UTILS,
        ],
        "display_manager": "lightdm",
        "services": ["lightdm"],
    },

    "mate": {
        "label": "MATE",
        "category": "de",
        "packages": [
            "mate", "mate-extra",
            "lightdm", "lightdm-gtk-greeter",
            "network-manager-applet",
            *_XORG, *_PIPEWIRE, *_COMMON_UTILS,
        ],
        "display_manager": "lightdm",
        "services": ["lightdm"],
    },

    "budgie": {
        "label": "Budgie",
        "category": "de",
        "packages": [
            "budgie", "budgie-extras",
            "gnome-terminal", "nemo",
            "lightdm", "lightdm-gtk-greeter",
            "gnome-keyring",
            *_XORG, *_PIPEWIRE, *_COMMON_UTILS,
        ],
        "display_manager": "lightdm",
        "services": ["lightdm"],
    },

    "lxqt": {
        "label": "LXQt",
        "category": "de",
        "packages": [
            "lxqt", "breeze-icons", "oxygen-icons",
            "sddm",
            "xscreensaver",
            "network-manager-applet",
            *_XORG, *_PIPEWIRE, *_COMMON_UTILS,
        ],
        "display_manager": "sddm",
        "services": ["sddm"],
    },

    "deepin": {
        "label": "Deepin",
        "category": "de",
        "packages": [
            "deepin", "deepin-extra",
            "lightdm", "lightdm-gtk-greeter",
            *_XORG, *_PIPEWIRE, *_COMMON_UTILS,
        ],
        "display_manager": "lightdm",
        "services": ["lightdm"],
    },

    "enlightenment": {
        "label": "Enlightenment",
        "category": "de",
        "packages": [
            "enlightenment", "terminology", "econnman",
            "lightdm", "lightdm-gtk-greeter",
            *_XORG, *_PIPEWIRE, *_COMMON_UTILS,
        ],
        "display_manager": "lightdm",
        "services": ["lightdm"],
    },

    # ══════════════════════════════════════
    # ── Tiling / Stacking Window Managers ──
    # ══════════════════════════════════════

    "hyprland": {
        "label": "Hyprland (Wayland compositor)",
        "category": "wm",
        "packages": [
            "hyprland", "hyprpaper", "hypridle", "hyprlock",
            "waybar", "wofi", "dunst",
            "foot", "thunar", "grim", "slurp", "wl-clipboard",
            "polkit-gnome", "xdg-desktop-portal-hyprland",
            "qt5-wayland", "qt6-wayland", "brightnessctl",
            *_WAYLAND_BASE, *_PIPEWIRE, *_COMMON_UTILS,
        ],
        "display_manager": None,  # Started from TTY
        "services": [],
    },

    "sway": {
        "label": "Sway (Wayland tiling – i3 compatible)",
        "category": "wm",
        "packages": [
            "sway", "swayidle", "swaylock", "swaybg",
            "waybar", "wofi", "dunst",
            "foot", "thunar", "grim", "slurp", "wl-clipboard",
            "polkit-gnome", "xdg-desktop-portal-wlr",
            "brightnessctl",
            *_WAYLAND_BASE, *_PIPEWIRE, *_COMMON_UTILS,
        ],
        "display_manager": None,
        "services": [],
    },

    "i3": {
        "label": "i3-wm (X11 tiling)",
        "category": "wm",
        "packages": [
            "i3-wm", "i3status", "i3lock", "i3blocks",
            "dmenu", "rofi", "dunst",
            "alacritty", "thunar", "feh", "picom",
            "lxappearance", "arandr", "nitrogen",
            "network-manager-applet", "pavucontrol",
            *_XORG, *_PIPEWIRE, *_COMMON_UTILS,
        ],
        "display_manager": None,
        "services": [],
    },

    "bspwm": {
        "label": "bspwm (X11 tiling)",
        "category": "wm",
        "packages": [
            "bspwm", "sxhkd",
            "polybar", "rofi", "dunst",
            "alacritty", "thunar", "feh", "picom",
            "nitrogen", "lxappearance",
            *_XORG, *_PIPEWIRE, *_COMMON_UTILS,
        ],
        "display_manager": None,
        "services": [],
    },

    "dwm": {
        "label": "dwm (X11 dynamic – suckless)",
        "category": "wm",
        "packages": [
            "dwm", "dmenu", "st",
            "dunst", "feh", "picom",
            *_XORG, *_PIPEWIRE, *_COMMON_UTILS,
        ],
        "display_manager": None,
        "services": [],
    },

    "qtile": {
        "label": "Qtile (X11/Wayland tiling – Python)",
        "category": "wm",
        "packages": [
            "qtile", "python-psutil", "python-iwlib",
            "rofi", "dunst",
            "alacritty", "thunar", "feh", "picom",
            *_XORG, *_WAYLAND_BASE, *_PIPEWIRE, *_COMMON_UTILS,
        ],
        "display_manager": None,
        "services": [],
    },

    "openbox": {
        "label": "Openbox (X11 stacking)",
        "category": "wm",
        "packages": [
            "openbox", "obconf", "obmenu-generator",
            "tint2", "rofi", "dunst",
            "alacritty", "thunar", "feh", "picom",
            "lxappearance", "nitrogen",
            "network-manager-applet", "volumeicon",
            *_XORG, *_PIPEWIRE, *_COMMON_UTILS,
        ],
        "display_manager": None,
        "services": [],
    },

    "awesome": {
        "label": "awesome (X11 dynamic tiling)",
        "category": "wm",
        "packages": [
            "awesome", "vicious",
            "rofi", "dunst",
            "alacritty", "thunar", "feh", "picom",
            "lxappearance", "network-manager-applet",
            *_XORG, *_PIPEWIRE, *_COMMON_UTILS,
        ],
        "display_manager": None,
        "services": [],
    },

    "river": {
        "label": "River (Wayland dynamic tiling)",
        "category": "wm",
        "packages": [
            "river",
            "waybar", "wofi", "dunst",
            "foot", "thunar", "grim", "slurp", "wl-clipboard",
            "polkit-gnome", "xdg-desktop-portal-wlr",
            *_WAYLAND_BASE, *_PIPEWIRE, *_COMMON_UTILS,
        ],
        "display_manager": None,
        "services": [],
    },
}


def configure_desktop(screen: Screen) -> str | None:
    """
    Interactive desktop environment selection.

    Groups DEs and WMs separately for clarity.
    Returns the DE key (e.g. "hyprland"), or None if cancelled.
    """
    # Build categorized display
    de_options = []
    wm_options = []
    none_options = []

    for key, info in DESKTOP_ENVIRONMENTS.items():
        entry = (key, info["label"])
        if info["category"] == "none":
            none_options.append(entry)
        elif info["category"] == "de":
            de_options.append(entry)
        elif info["category"] == "wm":
            wm_options.append(entry)

    # Build flat display list with section headers
    display_labels = []
    key_map = []

    for key, label in none_options:
        display_labels.append(label)
        key_map.append(key)

    display_labels.append("── Desktop Environments ──")
    key_map.append(None)

    for key, label in de_options:
        display_labels.append(f"  {label}")
        key_map.append(key)

    display_labels.append("── Window Managers ──")
    key_map.append(None)

    for key, label in wm_options:
        display_labels.append(f"  {label}")
        key_map.append(key)

    from artixinstall.tui.menu import run_menu, MenuItem
    items = []
    for i, label in enumerate(display_labels):
        k = key_map[i]
        if k is None:
            items.append(MenuItem(label, is_separator=True))
        else:
            items.append(MenuItem(label, key=k))

    result = run_menu(screen, "Select desktop environment / window manager", items,
                      footer="↑↓ Navigate  Enter Select  ESC Back")
    if result is None:
        return None
    return result.key


def get_desktop_packages(desktop: str) -> list[str]:
    """Get the package list for a desktop environment."""
    info = DESKTOP_ENVIRONMENTS.get(desktop, {})
    return list(info.get("packages", []))


def get_desktop_services(desktop: str) -> list[str]:
    """Get the services that need to be enabled for the DE."""
    info = DESKTOP_ENVIRONMENTS.get(desktop, {})
    return list(info.get("services", []))


def get_desktop_label(desktop: str) -> str:
    """Get the display label for a desktop environment."""
    info = DESKTOP_ENVIRONMENTS.get(desktop, {})
    return info.get("label", desktop)


def get_desktop_category(desktop: str) -> str:
    """Get the category (de/wm/none) for a desktop."""
    info = DESKTOP_ENVIRONMENTS.get(desktop, {})
    return info.get("category", "none")
