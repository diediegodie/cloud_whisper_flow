"""
CloudWhisper Flow UI Styles
Centralized palette, spacing, and typography for Flet UI (no inline styles)
"""

import flet as ft

# Color Palette
WIDGET_BG = "#18191D"
OVERLAY_BG = "#232429E6"  # 90% opacity
PRIMARY_ACCENT = "#FFCC40"
TEXT_PRIMARY = "#FFFFFF"
TEXT_MUTED = "#9A9CA6"
SUCCESS = "#4CAF50"
ERROR = "#FF5252"
CHARCOAL_DARK = "#1E1F25"
CHARCOAL_MID = "#2B2D33"

# Spacing (8pt grid)
MARGIN = 16
GUTTER = 8
COMPONENT_RADIUS = 8
TITLE_SIZE = 20
BODY_SIZE = 14
SMALL_SIZE = 12

# Typography
FONT_FAMILY = "Inter, Roboto, SF Pro Display, sans-serif"
FONT_WEIGHT_REGULAR = ft.FontWeight.W_400
FONT_WEIGHT_MEDIUM = ft.FontWeight.W_500
FONT_WEIGHT_SEMIBOLD = ft.FontWeight.W_600

# Widget dimensions
WIDGET_WIDTH = 300
WIDGET_HEIGHT = 80
WIDGET_HEIGHT_EXPANDED = 140
