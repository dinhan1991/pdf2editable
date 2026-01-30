"""Basic unit tests for font mapper."""

import pytest
from app.services.font_mapper import FontMapper


class TestFontMapper:
    """Test font mapping functionality."""
    
    def test_web_safe_font_unchanged(self):
        """Web-safe fonts should remain unchanged."""
        assert FontMapper.map_font("Arial") == "Arial"
        assert FontMapper.map_font("Times New Roman") == "Times New Roman"
    
    def test_vietnamese_font_substitution(self):
        """Vietnamese fonts should be substituted."""
        assert FontMapper.map_font("UTM Avo") == "Arial"
        assert FontMapper.map_font("VNI-Times") == "Times New Roman"
    
    def test_common_font_substitution(self):
        """Common fonts should be mapped correctly."""
        assert FontMapper.map_font("Helvetica") == "Arial"
        assert FontMapper.map_font("Roboto") == "Arial"
    
    def test_unknown_font_fallback(self):
        """Unknown fonts should fallback to Arial."""
        assert FontMapper.map_font("SomeRandomFont123") == "Arial"
    
    def test_font_name_cleaning(self):
        """Font variants should be cleaned."""
        # Note: Current implementation is basic, these might need refinement
        cleaned = FontMapper._clean_font_name("Arial-Bold")
        assert "Bold" not in cleaned
    
    def test_get_font_info(self):
        """Font info should include mapping reason."""
        info = FontMapper.get_font_info("Arial")
        assert info["reason"] == "web-safe"
        
        info = FontMapper.get_font_info("UTM Avo")
        assert info["reason"] == "substituted"
        assert info["mapped"] == "Arial"
        
        info = FontMapper.get_font_info("UnknownFont")
        assert info["reason"] == "fallback"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
