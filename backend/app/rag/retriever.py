"""
Retrieval layer for the RAG pipeline.

Design decision (documented in full in docs/rag-design.md): rather than
sentence-transformers + FAISS, this uses scikit-learn's TF-IDF vectorizer
with cosine similarity. For a knowledge base of this size (a few dozen
short documents describing one person's projects, skills and experience),
a neural embedding model adds ~2GB of dependencies and multi-second cold
starts for no measurable retrieval-quality benefit — the vocabulary is
small, technical, and mostly proper nouns (project names, technologies),
which is exactly where sparse lexical retrieval is strong. The retriever
is isolated behind a small interface so swapping in embeddings later
(e.g. for a much larger knowledge base) only means changing this file.
"""
from __future__ import annotations

import re
from dataclasses import dataclass
from typing import List

from sklearn.feature_extraction.text import ENGLISH_STOP_WORDS, TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from app.services.knowledge_base import Document, knowledge_base

_URL_PATTERN = re.compile(r"https?://\S+")


def _strip_urls(text: str) -> str:
    """Remove URLs before vectorizing — a URL like linkedin.com/in/yash-kushwaha99
    would otherwise leak the subject's own name as a 'matching' token for any
    query that mentions them, regardless of actual topical relevance."""
    return _URL_PATTERN.sub(" ", text)


def _build_stop_words(extra: List[str]) -> List[str]:
    """English stop words plus the knowledge base subject's own name.

    The person's name appears in nearly every document (titles, bios,
    URLs), so on its own it carries no discriminating signal for
    retrieval — including it as a "match" is what let an unrelated
    question like "What is Yash's salary?" retrieve the profile/links
    documents purely because they contain the word "Yash". Excluding
    name tokens forces a real topical overlap before anything is
    considered grounded.
    """
    return list(ENGLISH_STOP_WORDS | {w.lower() for w in extra if len(w) > 1})


@dataclass
class RetrievedChunk:
    document: Document
    score: float


class TfidfRetriever:
    def __init__(self, documents: List[Document], name_stop_words: List[str] | None = None):
        self.documents = documents
        self._corpus = [_strip_urls(f"{d.title}. {d.text}") for d in documents]
        stop_words = _build_stop_words(name_stop_words or [])
        self._vectorizer = TfidfVectorizer(
            stop_words=stop_words,
            ngram_range=(1, 2),
            min_df=1,
        )
        self._matrix = (
            self._vectorizer.fit_transform(self._corpus)
            if self._corpus
            else None
        )

    def search(self, query: str, top_k: int = 4, min_score: float = 0.12) -> List[RetrievedChunk]:
        if not self._corpus or self._matrix is None or not query.strip():
            return []
        query_vec = self._vectorizer.transform([_strip_urls(query)])
        scores = cosine_similarity(query_vec, self._matrix)[0]
        ranked = sorted(
            zip(self.documents, scores), key=lambda pair: pair[1], reverse=True
        )
        results = [
            RetrievedChunk(document=doc, score=float(score))
            for doc, score in ranked
            if score >= min_score
        ][:top_k]
        return results

    def search_within_section(
        self, query: str, section: str, top_k: int = 4, min_score: float = 0.0
    ) -> List[RetrievedChunk]:
        section_docs = [d for d in self.documents if d.section == section]
        if not section_docs:
            return []
        sub_retriever = TfidfRetriever(section_docs)
        return sub_retriever.search(query, top_k=top_k, min_score=min_score)


def _name_tokens() -> List[str]:
    name = knowledge_base.profile.get("name", "")
    return re.findall(r"[A-Za-z]+", name)


# Built once at process start from the knowledge base singleton.
retriever = TfidfRetriever(knowledge_base.documents, name_stop_words=_name_tokens())
