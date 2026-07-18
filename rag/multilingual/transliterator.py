"""
Rule-based Latin → Devanagari transliterator.

Converts Romanized Hindi and Nepali text to Devanagari script so that
NLLB-200 (which expects Devanagari input) can translate accurately.

Key features:
  - Handles standard ITRANS-like mappings (sh→श, chh→छ, kh→ख, etc.)
  - Preserves English terms (ST Certificate, OBC, SSO) by skipping them.
  - Fast: pure Python, no model loading, < 2ms per query.

Limitations:
  - ~85% accuracy on informal Romanized text (ambiguous vowels, missing halants).
  - Does not handle every colloquial spelling variant.
"""

import re
import logging

logger = logging.getLogger(__name__)

# Government and English terms that should NOT be transliterated.
# These are kept as-is in the output.
PRESERVE_TERMS = {
    "st", "obc", "sc", "ews", "sso", "certificate", "aadhaar", "aadhar",
    "employment", "card", "income", "caste", "tribe", "department",
    "apply", "application", "document", "pdf", "portal", "online",
    "login", "register", "registration", "form", "fee", "status",
    "download", "upload", "verification", "sikkim", "email", "mobile",
    "phone", "number", "otp", "password", "website", "url", "link",
    "noc", "bpl", "apl", "pan", "gst",
}

# ── Consonant mappings (longest match first) ──
# Order matters: longer sequences must be checked before shorter ones.
_CONSONANT_MAP = [
    # Four-letter combinations
    ("shri", "श्री"),
    # Three-letter combinations
    ("chh", "छ"),
    ("cch", "च्छ"),
    ("ksh", "क्ष"),
    ("tra", "त्र"),
    ("gya", "ज्ञ"),
    ("jny", "ज्ञ"),
    ("shr", "श्र"),
    ("thr", "थ्र"),
    # Two-letter combinations (aspirated consonants)
    ("kh", "ख"),
    ("gh", "घ"),
    ("ch", "च"),
    ("jh", "झ"),
    ("th", "थ"),
    ("dh", "ध"),
    ("ph", "फ"),
    ("bh", "भ"),
    ("sh", "श"),
    ("ng", "ङ"),
    ("ny", "ञ"),
    ("nn", "ण"),
    ("tt", "ट्ट"),
    ("dd", "ड्ड"),
    # Single consonants
    ("k", "क"),
    ("g", "ग"),
    ("c", "च"),
    ("j", "ज"),
    ("t", "त"),
    ("d", "द"),
    ("n", "न"),
    ("p", "प"),
    ("b", "ब"),
    ("m", "म"),
    ("y", "य"),
    ("r", "र"),
    ("l", "ल"),
    ("v", "व"),
    ("w", "व"),
    ("s", "स"),
    ("h", "ह"),
    ("f", "फ"),
    ("z", "ज़"),
    ("q", "क"),
    ("x", "क्स"),
]

# ── Vowel mappings ──
# Independent vowel forms (used at the start of a word or after another vowel)
_VOWEL_INDEPENDENT = [
    ("aa", "आ"),
    ("ai", "ऐ"),
    ("au", "औ"),
    ("ee", "ई"),
    ("oo", "ऊ"),
    ("ou", "औ"),
    ("oi", "ऐ"),
    ("a", "अ"),
    ("i", "इ"),
    ("u", "उ"),
    ("e", "ए"),
    ("o", "ओ"),
]

# Dependent vowel forms (mātrā, used after a consonant)
_VOWEL_DEPENDENT = [
    ("aa", "ा"),
    ("ai", "ै"),
    ("au", "ौ"),
    ("ee", "ी"),
    ("oo", "ू"),
    ("ou", "ौ"),
    ("oi", "ै"),
    ("a", ""),      # Inherent 'a' — no mātrā needed
    ("i", "ि"),
    ("u", "ु"),
    ("e", "े"),
    ("o", "ो"),
]

# Halant (virāma) — suppresses the inherent 'a'
_HALANT = "्"

# Pattern to identify words that are likely English
_ENGLISH_WORD_RE = re.compile(r"^[A-Z]{2,}$|^\d+$")


class Transliterator:
    """
    Converts Romanized Hindi/Nepali text to Devanagari script.

    English terms (government terminology, proper nouns) are preserved as-is.
    """

    def __init__(self, extra_preserve_terms: set[str] | None = None):
        """
        Args:
            extra_preserve_terms: Additional terms to preserve (not transliterate).
        """
        self.preserve_terms = PRESERVE_TERMS.copy()
        if extra_preserve_terms:
            self.preserve_terms |= {t.lower() for t in extra_preserve_terms}

    def to_devanagari(self, text: str) -> str:
        """
        Transliterate Romanized Hindi/Nepali text to Devanagari.

        Args:
            text: Input text in Latin script (may contain mixed English).

        Returns:
            Text with Romanized portions converted to Devanagari,
            English terms preserved.
        """
        if not text or not text.strip():
            return text

        tokens = text.split()
        result = []

        for token in tokens:
            # Separate leading/trailing punctuation
            prefix, word, suffix = self._strip_punctuation(token)

            if self._should_preserve(word):
                result.append(token)  # Keep original with punctuation
            else:
                converted = self._transliterate_word(word.lower())
                result.append(f"{prefix}{converted}{suffix}")

        return " ".join(result)

    def _should_preserve(self, word: str) -> bool:
        """Check if a word should be kept as-is (English term, number, abbreviation)."""
        if not word:
            return True
        # Check against preserve list
        if word.lower() in self.preserve_terms:
            return True
        # ALL-CAPS abbreviations (ST, OBC, etc.)
        if _ENGLISH_WORD_RE.match(word):
            return True
        # Pure numbers
        if word.isdigit():
            return True
        return False

    def _strip_punctuation(self, token: str) -> tuple[str, str, str]:
        """Strip leading and trailing punctuation from a token."""
        prefix = ""
        suffix = ""
        word = token

        while word and not word[0].isalnum():
            prefix += word[0]
            word = word[1:]
        while word and not word[-1].isalnum():
            suffix = word[-1] + suffix
            word = word[:-1]

        return prefix, word, suffix

    def _transliterate_word(self, word: str) -> str:
        """Transliterate a single Romanized word to Devanagari."""
        result = []
        i = 0
        after_consonant = False

        while i < len(word):
            matched = False

            # Try consonant mappings (longest first)
            for roman, devanagari in _CONSONANT_MAP:
                if word[i:i + len(roman)] == roman:
                    if after_consonant:
                        # Previous consonant had no explicit vowel — add halant
                        result.append(_HALANT)
                    result.append(devanagari)
                    i += len(roman)
                    after_consonant = True
                    matched = True
                    break

            if matched:
                # Check if the next character(s) form a vowel mātrā
                vowel_matched = False
                vowel_map = _VOWEL_DEPENDENT if after_consonant else _VOWEL_INDEPENDENT
                for roman_v, dev_v in vowel_map:
                    if word[i:i + len(roman_v)] == roman_v:
                        result.append(dev_v)
                        i += len(roman_v)
                        after_consonant = False
                        vowel_matched = True
                        break

                if not vowel_matched:
                    # Consonant is followed by another consonant or end of word
                    # The inherent 'a' handling is deferred
                    pass
                continue

            # Try independent vowel mappings
            vowel_map = _VOWEL_DEPENDENT if after_consonant else _VOWEL_INDEPENDENT
            for roman_v, dev_v in vowel_map:
                if word[i:i + len(roman_v)] == roman_v:
                    if after_consonant:
                        result.append(dev_v)
                    else:
                        # Use independent form
                        for r, d in _VOWEL_INDEPENDENT:
                            if word[i:i + len(r)] == r:
                                result.append(d)
                                break
                    i += len(roman_v)
                    after_consonant = False
                    matched = True
                    break

            if not matched:
                # Unknown character — pass through
                if after_consonant:
                    after_consonant = False
                result.append(word[i])
                i += 1

        return "".join(result)
