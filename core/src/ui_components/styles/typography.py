"""
Typography System for GHST UI

Apple-inspired font system with proper scaling and hierarchy.
Provides consistent typography across all UI components.
"""

from typing import Dict


class FontFamily:
    """Font family definitions."""
    
    # System font stack (iOS/macOS inspired)
    SYSTEM = "-apple-system, BlinkMacSystemFont, 'Segoe UI', 'SF Pro Display', 'Helvetica Neue', Arial, sans-serif"
    
    # Monospace font stack (code display)
    MONOSPACE = "'SF Mono', 'Monaco', 'Menlo', 'Consolas', 'Courier New', monospace"
    
    # Fallback fonts
    SANS_SERIF = "Arial, Helvetica, sans-serif"
    SERIF = "Georgia, 'Times New Roman', serif"


class FontSize:
    """Font size scale (13px base)."""
    
    # Base sizes
    TINY = "10px"
    SMALL = "11px"
    BASE = "13px"          # Default base size
    MEDIUM = "14px"
    LARGE = "16px"
    XL = "18px"
    XXL = "20px"
    XXXL = "24px"
    TITLE = "32px"
    DISPLAY = "48px"
    
    # Line heights
    LINE_HEIGHT_TIGHT = 1.25
    LINE_HEIGHT_NORMAL = 1.5
    LINE_HEIGHT_RELAXED = 1.75
    LINE_HEIGHT_LOOSE = 2.0


class FontWeight:
    """Font weight scale."""
    
    THIN = 100
    EXTRA_LIGHT = 200
    LIGHT = 300
    NORMAL = 400
    MEDIUM = 500
    SEMIBOLD = 600
    BOLD = 700
    EXTRA_BOLD = 800
    BLACK = 900


class Typography:
    """
    Typography utility class.
    
    Provides pre-configured typography styles for common UI elements.
    """
    
    @staticmethod
    def get_heading_1() -> Dict[str, str]:
        """Get H1 heading style."""
        return {
            'font-family': FontFamily.SYSTEM,
            'font-size': FontSize.TITLE,
            'font-weight': str(FontWeight.BOLD),
            'line-height': str(FontSize.LINE_HEIGHT_TIGHT),
            'letter-spacing': '-0.02em'
        }
    
    @staticmethod
    def get_heading_2() -> Dict[str, str]:
        """Get H2 heading style."""
        return {
            'font-family': FontFamily.SYSTEM,
            'font-size': FontSize.XXL,
            'font-weight': str(FontWeight.SEMIBOLD),
            'line-height': str(FontSize.LINE_HEIGHT_TIGHT),
            'letter-spacing': '-0.01em'
        }
    
    @staticmethod
    def get_heading_3() -> Dict[str, str]:
        """Get H3 heading style."""
        return {
            'font-family': FontFamily.SYSTEM,
            'font-size': FontSize.LARGE,
            'font-weight': str(FontWeight.SEMIBOLD),
            'line-height': str(FontSize.LINE_HEIGHT_NORMAL)
        }
    
    @staticmethod
    def get_body() -> Dict[str, str]:
        """Get body text style."""
        return {
            'font-family': FontFamily.SYSTEM,
            'font-size': FontSize.BASE,
            'font-weight': str(FontWeight.NORMAL),
            'line-height': str(FontSize.LINE_HEIGHT_NORMAL)
        }
    
    @staticmethod
    def get_body_small() -> Dict[str, str]:
        """Get small body text style."""
        return {
            'font-family': FontFamily.SYSTEM,
            'font-size': FontSize.SMALL,
            'font-weight': str(FontWeight.NORMAL),
            'line-height': str(FontSize.LINE_HEIGHT_NORMAL)
        }
    
    @staticmethod
    def get_code() -> Dict[str, str]:
        """Get code text style."""
        return {
            'font-family': FontFamily.MONOSPACE,
            'font-size': FontSize.BASE,
            'font-weight': str(FontWeight.NORMAL),
            'line-height': str(FontSize.LINE_HEIGHT_RELAXED)
        }
    
    @staticmethod
    def get_button() -> Dict[str, str]:
        """Get button text style."""
        return {
            'font-family': FontFamily.SYSTEM,
            'font-size': FontSize.BASE,
            'font-weight': str(FontWeight.SEMIBOLD),
            'line-height': '1'
        }
    
    @staticmethod
    def get_label() -> Dict[str, str]:
        """Get label text style."""
        return {
            'font-family': FontFamily.SYSTEM,
            'font-size': FontSize.SMALL,
            'font-weight': str(FontWeight.MEDIUM),
            'line-height': '1'
        }
    
    @staticmethod
    def format_style_dict(style_dict: Dict[str, str]) -> str:
        """
        Convert style dictionary to CSS string.
        
        Args:
            style_dict: Dictionary of CSS properties
            
        Returns:
            CSS string
        """
        return '; '.join(f"{key}: {value}" for key, value in style_dict.items())
    
    @staticmethod
    def get_css_string(typography_type: str) -> str:
        """
        Get CSS string for a typography type.
        
        Args:
            typography_type: Type of typography ('h1', 'h2', 'h3', 'body', 'code', etc.)
            
        Returns:
            CSS string
        """
        type_map = {
            'h1': Typography.get_heading_1(),
            'h2': Typography.get_heading_2(),
            'h3': Typography.get_heading_3(),
            'body': Typography.get_body(),
            'body-small': Typography.get_body_small(),
            'code': Typography.get_code(),
            'button': Typography.get_button(),
            'label': Typography.get_label()
        }
        
        style_dict = type_map.get(typography_type, Typography.get_body())
        return Typography.format_style_dict(style_dict)


# Convenience constants for quick access
HEADING_1_CSS = Typography.get_css_string('h1')
HEADING_2_CSS = Typography.get_css_string('h2')
HEADING_3_CSS = Typography.get_css_string('h3')
BODY_CSS = Typography.get_css_string('body')
CODE_CSS = Typography.get_css_string('code')
BUTTON_CSS = Typography.get_css_string('button')
LABEL_CSS = Typography.get_css_string('label')
