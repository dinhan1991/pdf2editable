"""Font mapping and substitution system."""

from typing import Dict, Optional


class FontMapper:
    """Handles font detection and substitution."""
    
    # Font substitution mapping
    FONT_SUBSTITUTION: Dict[str, str] = {
        # Vietnamese fonts
        "UTM Avo": "Arial",
        "UTM Times": "Times New Roman",
        "VNI-Times": "Times New Roman",
        "VNI-Helve": "Arial",
        ".VnTime": "Times New Roman",
        ".VnArial": "Arial",
        
        # Common fonts
        "Helvetica": "Arial",
        "Helvetica Neue": "Arial",
        "SF Pro": "Segoe UI",
        "SF Pro Display": "Segoe UI",
        "Roboto": "Arial",
        "Open Sans": "Arial",
        "Lato": "Arial",
        
        # Serif fonts
        "Georgia": "Times New Roman",
        "Palatino": "Times New Roman",
        "Cambria": "Times New Roman",
        
        # Monospace
        "Courier": "Courier New",
        "Monaco": "Courier New",
        "Consolas": "Courier New",
    }
    
    # Web-safe fallback fonts
    WEB_SAFE_FONTS = {
        "Arial",
        "Times New Roman",
        "Courier New",
        "Verdana",
        "Georgia",
        "Comic Sans MS",
        "Trebuchet MS",
        "Arial Black",
        "Impact",
    }
    
    @classmethod
    def map_font(cls, pdf_font_name: str) -> str:
        """
        Map PDF font to Word-compatible font.
        
        Args:
            pdf_font_name: Font name from PDF
            
        Returns:
            Mapped font name (Word-compatible)
        """
        # Clean font name (remove variants like -Bold, -Italic)
        clean_name = cls._clean_font_name(pdf_font_name)
        
        # Check if it's already web-safe
        if clean_name in cls.WEB_SAFE_FONTS:
            return clean_name
        
        # Try substitution mapping
        if clean_name in cls.FONT_SUBSTITUTION:
            return cls.FONT_SUBSTITUTION[clean_name]
        
        # Fallback to Arial
        return "Arial"
    
    @staticmethod
    def _clean_font_name(font_name: str) -> str:
        """
        Clean font name by removing variants.
        
        Examples:
            "Arial-Bold" -> "Arial"
            "TimesNewRoman-Italic" -> "Times New Roman"
        """
        # Remove common suffixes
        for suffix in ["-Bold", "-Italic", "-BoldItalic", "-Regular", "MT"]:
            font_name = font_name.replace(suffix, "")
        
        # Handle CamelCase (e.g., "TimesNewRoman" -> "Times New Roman")
        # Simple heuristic: add space before uppercase letters
        result = []
        for i, char in enumerate(font_name):
            if i > 0 and char.isupper() and font_name[i-1].islower():
                result.append(" ")
            result.append(char)
        
        return "".join(result).strip()
    
    @classmethod
    def get_font_info(cls, pdf_font_name: str) -> Dict[str, str]:
        """
        Get detailed font mapping information.
        
        Returns:
            Dict with original, mapped, and reason
        """
        mapped = cls.map_font(pdf_font_name)
        clean_original = cls._clean_font_name(pdf_font_name)
        
        if clean_original == mapped:
            reason = "web-safe"
        elif clean_original in cls.FONT_SUBSTITUTION:
            reason = "substituted"
        else:
            reason = "fallback"
        
        return {
            "original": pdf_font_name,
            "cleaned": clean_original,
            "mapped": mapped,
            "reason": reason,
        }
