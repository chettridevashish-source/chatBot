"""
Hybrid language detector for the Sikkim SSO chatbot.

Detects five language types:
  - english
  - hindi           (Devanagari script)
  - nepali          (Devanagari script)
  - hinglish        (Romanized Hindi mixed with English)
  - romanized_nepali (Romanized Nepali mixed with English)

Strategy:
  1. Unicode script analysis  → Devanagari ratio
  2. Devanagari sub-detection → Hindi vs Nepali via vocabulary markers
  3. Romanized detection      → keyword/morpheme matching
  4. Fallback                 → English
"""

import re
import logging

logger = logging.getLogger(__name__)

# ── Devanagari Unicode range: U+0900 – U+097F ──
_DEVANAGARI_RE = re.compile(r"[\u0900-\u097F]")

# ── Marker words for Devanagari sub-classification ──
# Nepali-specific markers (words/particles rarely used in Hindi)
_NEPALI_DEVANAGARI_MARKERS = {
    "कसरी", "गर्नु", "गर्ने", "हुन्छ", "छ", "छैन", "भयो", "गरिन्छ",
    "पाइन्छ", "चाहिन्छ", "बनाउने", "लागि", "मलाई", "तपाईं", "तपाईंले",
    "कहाँ", "किन", "कस्तो", "भन्नुहोस्", "गर्नुहोस्", "दिनुहोस्",
    "खोज्ने", "निवेदन", "प्रमाणपत्र", "आवश्यक", "कागजात",
}

# Hindi-specific markers (words/particles rarely used in Nepali)
_HINDI_DEVANAGARI_MARKERS = {
    "कैसे", "क्या", "है", "हैं", "कहाँ", "कौन", "कब", "क्यों",
    "करना", "बनाएं", "करें", "होता", "होती", "मिलता", "चाहिए",
    "बनवाना", "कराना", "लगता", "आवेदन", "प्रमाणपत्र", "जरूरी",
    "दस्तावेज", "कृपया", "बताइए", "बताएं", "मुझे", "आपको",
}

# ── Romanized language markers ──
# Hinglish markers (Romanized Hindi particles and verb forms)
_HINGLISH_MARKERS = {
    "kaise", "kya", "hai", "hain", "karna", "banaye", "banao",
    "kaise", "hota", "hoti", "milta", "chahiye", "karein",
    "banwana", "karana", "lagta", "kahan", "kaun", "kab",
    "kyun", "kyon", "mujhe", "aapko", "zaruri", "jaruri",
    "bataiye", "bataye", "bataein", "karo", "dijiye", "boliye",
    "mein", "ke", "ka", "ki", "se", "ko", "par", "liye",
    "wala", "nahi", "nahin", "aur", "ya", "lekin", "abhi",
    "yahan", "wahan", "iska", "uska", "apna",
}

# Romanized Nepali markers (verb forms and particles distinct from Hindi)
_ROMANIZED_NEPALI_MARKERS = {
    "kasari", "garnu", "garne", "huncha", "chha", "chhaina",
    "bhayo", "garincha", "paincha", "chahincha", "banawnu",
    "lagi", "malai", "tapain", "tapaile", "kaha", "kina",
    "kasto", "bhannuhos", "garnuhos", "dinuhos", "khojne",
    "niwedan", "pramanpatra", "aawashyak", "kagajat", "ma",
    "ko", "le", "lai", "bata", "sanga", "haru", "haruko",
    "pani", "nai", "bhane", "garda", "garera", "gardai",
    "hunna", "thyo", "thiyo", "hola", "parcha",
}

# Government/English terms to ignore during language detection.
# These appear in all languages and should not bias detection.
_ENGLISH_TERMS_TO_IGNORE = {
    "st", "obc", "sc", "ews", "sso", "certificate", "aadhaar",
    "aadhar", "employment", "card", "income", "caste", "tribe",
    "department", "apply", "application", "document", "pdf",
    "portal", "online", "login", "register", "registration",
    "form", "fee", "status", "download", "upload", "verification",
    "sikkim",
}


class LanguageDetector:
    """
    Detects language of user queries for the Sikkim SSO chatbot.

    Returns one of: 'english', 'hindi', 'nepali', 'hinglish', 'romanized_nepali'.
    """

    def detect(self, text: str) -> str:
        """
        Detect the language/script of the input text.

        Args:
            text: The raw user query.

        Returns:
            Language identifier string.
        """
        if not text or not text.strip():
            return "english"

        text = text.strip()

        # ── Step 1: Check Devanagari content ──
        devanagari_chars = _DEVANAGARI_RE.findall(text)
        total_alpha = sum(1 for c in text if c.isalpha())

        if total_alpha == 0:
            return "english"

        devanagari_ratio = len(devanagari_chars) / total_alpha

        if devanagari_ratio > 0.3:
            # Text has significant Devanagari content
            lang = self._classify_devanagari(text)
            logger.debug("Devanagari detected (ratio=%.2f) → %s", devanagari_ratio, lang)
            return lang

        # ── Step 2: Latin script — check for Romanized markers ──
        lang = self._classify_romanized(text)
        logger.debug("Romanized classification → %s", lang)
        return lang

    def _classify_devanagari(self, text: str) -> str:
        """Distinguish Hindi from Nepali in Devanagari text."""
        words = set(text.split())

        nepali_score = len(words & _NEPALI_DEVANAGARI_MARKERS)
        hindi_score = len(words & _HINDI_DEVANAGARI_MARKERS)

        if nepali_score > hindi_score:
            return "nepali"
        if hindi_score > nepali_score:
            return "hindi"

        # Tie-breaking: check for Nepali-specific Unicode characters
        # Nepali uses some characters less common in Hindi
        # e.g., ज्ञ is more common in Nepali, but this is unreliable.
        # Default to Hindi as it's more widely used.
        # The translation quality is similar for both via NLLB.
        return "hindi"

    def _classify_romanized(self, text: str) -> str:
        """Classify Latin-script text as English, Hinglish, or Romanized Nepali."""
        # Tokenize and lowercase, filtering out English government terms
        words = set(text.lower().split())
        # Remove punctuation from tokens
        words = {re.sub(r"[^\w]", "", w) for w in words}
        # Remove known English/government terms
        words = words - _ENGLISH_TERMS_TO_IGNORE
        # Remove empty strings
        words.discard("")

        if not words:
            # Only English terms remain
            return "english"

        hinglish_hits = words & _HINGLISH_MARKERS
        nepali_hits = words & _ROMANIZED_NEPALI_MARKERS

        hinglish_score = len(hinglish_hits)
        nepali_score = len(nepali_hits)

        # Require at least one marker word to classify as non-English
        if nepali_score > hinglish_score and nepali_score >= 1:
            return "romanized_nepali"
        if hinglish_score > nepali_score and hinglish_score >= 1:
            return "hinglish"
        if hinglish_score >= 1 and nepali_score >= 1:
            # Tie: prefer Hinglish as it's more common
            return "hinglish"
        if hinglish_score >= 1:
            return "hinglish"
        if nepali_score >= 1:
            return "romanized_nepali"

        return "english"
