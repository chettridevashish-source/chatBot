"""
NLLB-200 translation wrapper for the Sikkim SSO chatbot.

Uses facebook/nllb-200-distilled-600M for bidirectional translation:
  - Hindi (Devanagari) ↔ English
  - Nepali (Devanagari) ↔ English

Key features:
  - Single model for all language pairs
  - Government terminology preservation via placeholder tokens
  - Model loaded once at startup, reused across requests
"""

import re
import logging
from typing import Optional

logger = logging.getLogger(__name__)

# Government terms that must NEVER be translated.
# These are replaced with placeholders before translation and restored after.
PRESERVE_TERMS = {
    # Certificate types
    "ST Certificate", "ST certificate", "st certificate",
    "OBC Certificate", "OBC certificate", "obc certificate",
    "SC Certificate", "SC certificate", "sc certificate",
    "EWS Certificate", "EWS certificate", "ews certificate",
    "Income Certificate", "Income certificate", "income certificate",
    "Caste Certificate", "Caste certificate", "caste certificate",
    "Domicile Certificate", "Domicile certificate", "domicile certificate",
    "Birth Certificate", "Birth certificate", "birth certificate",
    "Death Certificate", "Death certificate", "death certificate",
    "Marriage Certificate", "Marriage certificate", "marriage certificate",
    "Employment Card", "Employment card", "employment card",
    "Ration Card", "Ration card", "ration card",
    "NOC",

    # Abbreviations and proper nouns
    "ST", "OBC", "SC", "EWS", "BPL", "APL",
    "SSO", "Aadhaar", "aadhaar", "AADHAAR",
    "PAN", "GST", "OTP", "COI",

    # Government entities
    "Sikkim SSO", "SSO Portal", "SSO portal",

    # Specific department/scheme names
    "Panchayat", "panchayat",
    "Block Administrative Centre", "BAC",
    "District Collector", "District Administrative Centre",
    "Sub-Divisional Magistrate", "SDM",
}

# NLLB language codes
LANG_CODES = {
    "english": "eng_Latn",
    "hindi": "hin_Deva",
    "nepali": "npi_Deva",
    # Romanized variants are transliterated to Devanagari first,
    # then use the same codes as their Devanagari counterparts.
    "hinglish": "hin_Deva",
    "romanized_nepali": "npi_Deva",
}

# Placeholder pattern for term preservation
_PLACEHOLDER_TEMPLATE = "__TERM_{idx}__"
_PLACEHOLDER_RE = re.compile(r"__TERM_(\d+)__")


class Translator:
    """
    Bidirectional translator using NLLB-200-distilled-600M.

    Loads the model once and reuses it for all translation requests.
    Preserves government terminology by replacing terms with placeholders
    before translation and restoring them after.
    """

    def __init__(self, model_name: str = "facebook/nllb-200-distilled-600M",
                 device: str = "cpu"):
        """
        Initialize the translator.

        Args:
            model_name: HuggingFace model identifier for NLLB.
            device: Device to run inference on ('cpu', 'cuda', 'mps').
        """
        self.model_name = model_name
        self.device = device
        self._model = None
        self._tokenizer = None
        self._loaded = False

    def _load_model(self):
        """Lazy-load the translation model on first use."""
        if self._loaded:
            return

        logger.info("Loading translation model: %s on %s ...", self.model_name, self.device)

        from transformers import AutoModelForSeq2SeqLM, AutoTokenizer

        self._tokenizer = AutoTokenizer.from_pretrained(self.model_name)
        self._model = AutoModelForSeq2SeqLM.from_pretrained(self.model_name)
        self._model.to(self.device)
        self._model.eval()

        self._loaded = True
        logger.info("✅ Translation model loaded successfully.")

    def translate(self, text: str, src_lang: str, tgt_lang: str,
                  max_length: int = 512) -> str:
        """
        Translate text from source to target language.

        Args:
            text: Input text to translate.
            src_lang: Source NLLB language code (e.g., 'hin_Deva').
            tgt_lang: Target NLLB language code (e.g., 'eng_Latn').
            max_length: Maximum output token length.

        Returns:
            Translated text with government terms preserved.
        """
        if not text or not text.strip():
            return text

        self._load_model()

        # ── Step 1: Extract and replace preservable terms with placeholders ──
        protected_text, term_map = self._protect_terms(text)

        # ── Step 2: Translate ──
        self._tokenizer.src_lang = src_lang

        inputs = self._tokenizer(
            protected_text,
            return_tensors="pt",
            padding=True,
            truncation=True,
            max_length=max_length,
        ).to(self.device)

        # Get the target language token ID
        tgt_lang_id = self._tokenizer.convert_tokens_to_ids(tgt_lang)

        import torch
        with torch.no_grad():
            generated = self._model.generate(
                **inputs,
                forced_bos_token_id=tgt_lang_id,
                max_new_tokens=max_length,
            )

        translated = self._tokenizer.batch_decode(
            generated, skip_special_tokens=True
        )[0]

        # ── Step 3: Restore preserved terms ──
        result = self._restore_terms(translated, term_map)

        return result

    def to_english(self, text: str, detected_lang: str) -> str:
        """
        Translate from any supported language to English.

        Args:
            text: Input text (in Devanagari or with preserved English terms).
            detected_lang: Language identifier from LanguageDetector.

        Returns:
            English translation.
        """
        src_code = LANG_CODES.get(detected_lang)
        if not src_code:
            logger.warning("Unknown source language '%s', returning text as-is.", detected_lang)
            return text

        return self.translate(text, src_lang=src_code, tgt_lang="eng_Latn")

    def from_english(self, text: str, target_lang: str) -> str:
        """
        Translate from English to a target language.

        Args:
            text: Input text in English.
            target_lang: Target language identifier.

        Returns:
            Translated text.
        """
        tgt_code = LANG_CODES.get(target_lang)
        if not tgt_code:
            logger.warning("Unknown target language '%s', returning text as-is.", target_lang)
            return text

        return self.translate(text, src_lang="eng_Latn", tgt_lang=tgt_code)

    def _protect_terms(self, text: str) -> tuple[str, dict[str, str]]:
        """
        Replace government terms with placeholder tokens.

        Returns:
            Tuple of (modified text, mapping of placeholder → original term).
        """
        term_map = {}
        protected = text

        # Sort terms by length (longest first) to avoid partial replacements
        sorted_terms = sorted(PRESERVE_TERMS, key=len, reverse=True)

        idx = 0
        for term in sorted_terms:
            if term in protected:
                placeholder = _PLACEHOLDER_TEMPLATE.format(idx=idx)
                protected = protected.replace(term, placeholder)
                term_map[placeholder] = term
                idx += 1

        return protected, term_map

    def _restore_terms(self, text: str, term_map: dict[str, str]) -> str:
        """Restore placeholder tokens with original terms."""
        result = text
        for placeholder, original in term_map.items():
            result = result.replace(placeholder, original)
        return result
