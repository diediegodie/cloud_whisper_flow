"""
CloudWhisper Flow UI Skeleton

This module defines the main UI for the CloudWhisper Flow application. It creates a frameless,
always-on-top floating window using the Flet framework. The UI includes a status label, a
progress spinner, and a settings button.

Features:
- Frameless, transparent window that stays on top of other applications.
- Centered status label and progress spinner.
- Settings button with a placeholder panel.

Usage:
Run this script directly to launch the UI.

"""

import flet as ft
import os, sys

# Ensure project root is on sys.path so absolute imports (from app.ui.styles) work
_repo_root = os.path.dirname(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
)
if _repo_root not in sys.path:
    sys.path.insert(0, _repo_root)
from app.ui.styles import *


def main(page: ft.Page):
    """
    Initializes the Flet page and sets up the UI elements.

    Args:
        page (ft.Page): The Flet page object.
    """
    # Window configuration: normal Flet window (OS chrome, resizable, default size)
    page.title = "CloudWhisper"
    page.bgcolor = WIDGET_BG
    page.padding = 0
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.CENTER

    # Status label and spinner
    status_label = ft.Text(
        "Ready",
        size=TITLE_SIZE,
        color=SUCCESS,
        weight=FONT_WEIGHT_SEMIBOLD,
        font_family=FONT_FAMILY,
        text_align=ft.TextAlign.CENTER,
        selectable=False,
    )

    progress_ring = ft.ProgressRing(width=24, height=24, visible=False)

    status_column = ft.Column(
        controls=[status_label, ft.Container(height=8), progress_ring],
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        tight=True,
    )
    # Settings panel state
    settings_open = False

    # Placeholder settings panel (hidden by default)
    settings_panel = ft.Container(
        content=ft.Text(
            "Settings (not yet implemented)",
            size=SMALL_SIZE,
            color=TEXT_MUTED,
            text_align=ft.TextAlign.CENTER,
        ),
        width=WIDGET_WIDTH - (MARGIN * 2),
        bgcolor=CHARCOAL_MID,
        border_radius=ft.border_radius.all(COMPONENT_RADIUS),
        padding=GUTTER,
        visible=False,
        margin=ft.margin.only(top=8, left=MARGIN, right=MARGIN),
    )

    def toggle_settings(e):
        """
        Toggles the visibility of the settings panel.

        Args:
            e: The event object (not used).
        """
        nonlocal settings_open
        settings_open = not settings_open
        settings_panel.visible = settings_open
        widget.height = WIDGET_HEIGHT_EXPANDED if settings_open else WIDGET_HEIGHT
        settings_panel.update()
        widget.update()

    # Plain settings button (no hover handlers to maintain compatibility)
    settings_btn = ft.IconButton(
        icon=ft.icons.Icons.SETTINGS,
        icon_size=18,
        icon_color=TEXT_MUTED,
        tooltip="Settings",
        on_click=toggle_settings,
    )

    # Header row: keep the status centered. The settings button will be
    # positioned in an overlay stack so it doesn't affect the centered layout.
    header_row = ft.Row(
        controls=[
            ft.Container(
                content=status_column, expand=True, alignment=ft.Alignment.CENTER
            ),
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        vertical_alignment=ft.CrossAxisAlignment.START,
    )

    content_column = ft.Column(
        controls=[header_row, settings_panel],
        tight=True,
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
    )

    widget = ft.Container(
        content=content_column,
        width=WIDGET_WIDTH,
        height=WIDGET_HEIGHT,
        bgcolor=WIDGET_BG,
        border_radius=ft.border_radius.all(COMPONENT_RADIUS),
        alignment=ft.Alignment.CENTER,
        padding=0,
        margin=0,
    )

    def set_state(state: str):
        """
        Updates the UI to reflect the current application state.

        Args:
            state (str): The new state of the application. Can be "ready", "recording", or "processing".
        """
        if state == "ready":
            status_label.value = "Ready"
            status_label.color = SUCCESS
            progress_ring.visible = False
        elif state == "recording":
            status_label.value = "Recording"
            status_label.color = ERROR
            progress_ring.visible = False
        elif state == "processing":
            status_label.value = "Processing"
            status_label.color = PRIMARY_ACCENT
            progress_ring.visible = True
        status_label.update()
        progress_ring.update()

    # Use page.overlay for true absolute positioning at the window's top-left corner
    settings_btn.left = GUTTER
    settings_btn.top = GUTTER

    # Add widget normally (page centering keeps it in the middle)
    page.add(widget)

    # Add the settings button to the page overlay for true absolute positioning
    page.overlay.append(settings_btn)
    page.update()

    set_state("ready")


# Entry point for the application
if __name__ == "__main__":
    ft.app(target=main)
