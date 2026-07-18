"""
Multilingual pipeline orchestrator for the Sikkim SSO chatbot.

Ties together:
  - LanguageDetector   → detect user's language
  - Transliterator     → Romanized → Devanagari (for Hinglish / Romanized Nepali)
  - Translator         → Devanagari ↔ English via NLLB-200

Provides a simple preprocess/postprocess API for the RAG chain.
Includes an LRU cache to avoid re-translating repeated queries.
"""

import time
import logging
from functools import lru_cache

from multilingual.language_detector import LanguageDetector
from multilingual.transliterator import Transliterator
from multilingual.translator import Translator

logger = logging.getLogger(__name__)


class MultilingualPipeline:
    """
    Complete multilingual pre/post-processing pipeline.

    Usage:
        pipeline = MultilingualPipeline()

        # Before RAG retrieval
        english_query, detected_lang = pipeline.preprocess("ST certificate kaise banaye?")

        # ... RAG retrieval with english_query ...

        # After LLM generates English answer
        localized_answer = pipeline.postprocess(english_answer, detected_lang)
    """

    def __init__(self, translation_model: str = "facebook/nllb-200-distilled-600M",
                 device: str = "cpu", cache_size: int = 1024):
        """
        Initialize all sub-components.

        Args:
            translation_model: HuggingFace model name for NLLB.
            device: Device for translation model ('cpu', 'cuda', 'mps').
            cache_size: Max entries in the translation LRU cache.
        """
        self.detector = LanguageDetector()
        self.transliterator = Transliterator()
        self.translator = Translator(model_name=translation_model, device=device)
        self._cache_size = cache_size

        # Create cached versions of translation functions
        self._cached_to_english = lru_cache(maxsize=cache_size)(self._translate_to_english)
        self._cached_from_english = lru_cache(maxsize=cache_size)(self._translate_from_english)

        logger.info(
            "MultilingualPipeline initialized (model=%s, device=%s, cache=%d)",
            translation_model, device, cache_size,
        )

    def preprocess(self, query: str) -> tuple[str, str]:
        """
        Detect language and translate query to English for retrieval.

        Args:
            query: Raw user query in any supported language.

        Returns:
            Tuple of (english_query, detected_language).
            If already English, returns the original query unchanged.
        """
        t0 = time.perf_counter()

        # ── Step 1: Detect language ──
        detected_lang = self.detector.detect(query)
        t_detect = time.perf_counter() - t0

        if detected_lang == "english":
            logger.info(
                "[Multilingual] Language: english (detection: %.1fms) — no translation needed",
                t_detect * 1000,
            )
            return query, "english"

        # ── Step 2: Transliterate if Romanized ──
        text_for_translation = query
        t_translit = 0.0

        if detected_lang in ("hinglish", "romanized_nepali"):
            t1 = time.perf_counter()
            text_for_translation = self.transliterator.to_devanagari(query)
            t_translit = time.perf_counter() - t1
            logger.debug(
                "[Multilingual] Transliterated: '%s' → '%s'",
                query, text_for_translation,
            )

        # ── Step 3: Translate to English ──
        t2 = time.perf_counter()
        english_query = self._cached_to_english(text_for_translation, detected_lang)
        t_translate = time.perf_counter() - t2

        total = time.perf_counter() - t0
        logger.info(
            "[Multilingual] Preprocess: lang=%s, detect=%.1fms, translit=%.1fms, "
            "translate=%.1fms, total=%.1fms | '%s' → '%s'",
            detected_lang, t_detect * 1000, t_translit * 1000,
            t_translate * 1000, total * 1000,
            query[:50], english_query[:50],
        )

        return english_query, detected_lang

    def postprocess(self, english_answer: str, target_lang: str) -> str:
        """
        Translate English answer back to the user's detected language.

        Args:
            english_answer: The LLM's response in English.
            target_lang: The language to translate into (from preprocess).

        Returns:
            Answer in the target language. If target is English, returns as-is.
        """
        if target_lang == "english":
            return english_answer

        t0 = time.perf_counter()

        # For Romanized languages, translate to Devanagari first.
        # The user typed in Latin script, but we return Devanagari since
        # the NLLB model outputs Devanagari. The Devanagari response is
        # more readable and standard than attempting reverse transliteration.
        base_lang = target_lang
        if target_lang == "hinglish":
            base_lang = "hindi"
        elif target_lang == "romanized_nepali":
            base_lang = "nepali"

        translated = self._cached_from_english(english_answer, base_lang)

        total = time.perf_counter() - t0
        logger.info(
            "[Multilingual] Postprocess: target=%s, time=%.1fms | %d chars → %d chars",
            target_lang, total * 1000,
            len(english_answer), len(translated),
        )

        return translated

    def _translate_to_english(self, text: str, detected_lang: str) -> str:
        """Uncached translation to English (wrapped by lru_cache)."""
        return self.translator.to_english(text, detected_lang)

    def _translate_from_english(self, text: str, target_lang: str) -> str:
        """Uncached translation from English (wrapped by lru_cache)."""
        return self.translator.from_english(text, target_lang)

    @property
    def cache_info(self) -> dict:
        """Return cache statistics for monitoring."""
        to_eng = self._cached_to_english.cache_info()
        from_eng = self._cached_from_english.cache_info()
        return {
            "to_english": {
                "hits": to_eng.hits,
                "misses": to_eng.misses,
                "size": to_eng.currsize,
                "maxsize": to_eng.maxsize,
            },
            "from_english": {
                "hits": from_eng.hits,
                "misses": from_eng.misses,
                "size": from_eng.currsize,
                "maxsize": from_eng.maxsize,
            },
        }
