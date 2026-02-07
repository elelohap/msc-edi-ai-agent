# rag/routing/policy.py
# keep this ordering 

from typing import Any, Optional, Tuple

from . import patterns as P
from . import fallbacks as F
from .helpers import chunks_to_text, has_any_signal, extract_requirement_thing, POSITIONING_SIGNALS, HARD_REQUIREMENT_SIGNALS

def answer_requirement(q: str, context_chunks: Any) -> str:
    thing = extract_requirement_thing(q) or "that"
    ctx = chunks_to_text(context_chunks)
    if ctx and has_any_signal(ctx, HARD_REQUIREMENT_SIGNALS):
        return f"Yes — {thing} is required for admission to MSc Engineering Design & Innovation (EDI)."
    if ctx and has_any_signal(ctx, POSITIONING_SIGNALS):
        return (
            f"No — {thing} is not a formal requirement for admission to MSc Engineering Design & Innovation (EDI). "
            "The programme is intended for applicants from varied backgrounds, and admissions are usually assessed holistically."
        )
    return F.REQUIREMENT_FALLBACK_GENERIC

def route_early(q: str) -> Optional[str]:
    # smalltalk
    if P.GREETING_PATTERN.match(q):
        return "Hello! I can help with MSc EDI admissions questions. What would you like to know?"
    if P.THANKS_PATTERN.match(q):
        return "You’re welcome!"
    if P.PRAISE_PATTERN.match(q):
        return "Glad it helped!"
    # programme guard
    if P.MDES_PATTERN.search(q):
        return F.MDES_REDIRECT_MSG
    return None

def route_intake(q: str) -> Optional[str]:
    if P.INTAKE_PATTERN.search(q):
        if P.PROGRAMME_START_PATTERN.search(q):
            return F.PROGRAMME_START_FALLBACK
        if P.APPLICATION_PERIOD_PATTERN.search(q):
            return None  # allow normal RAG / policy flow
        return (
            "When you say “intake”, do you mean the **programme start date** (when classes begin) or the **application period**?\n\n"
            "• **Programme start date (intake):** when the cohort begins classes\n"
            "• **Application period:** when you submit your application (often an Oct–Feb window)\n\n"
            "Tell me which one you mean and I’ll answer for MSc EDI."
        )
    return None

def route_policy_logistics(q: str, context_chunks: Any) -> Optional[str]:
    # Policy/process first
    if P.OFFER_OUTCOME_PATTERN.search(q):
        return F.OFFER_OUTCOME_FALLBACK
    if P.REAPPLICATION_PATTERN.search(q):
        return F.REAPPLICATION_FALLBACK

    # Visa process should not depend on RAG
    if P.VISA_PROCESS_PATTERN.search(q):
        return F.VISA_PROCESS_FALLBACK

    # Visa “need” questions
    if P.VISA_PATTERN.search(q):
        return F.VISA_FALLBACK

    # Arrival: if you have docs, let RAG handle it; else not-found
    if P.ARRIVAL_PATTERN.search(q):
        return None if context_chunks else F.NOT_FOUND_FALLBACK

    return None

def route_requirement_or_suitability(q: str, context_chunks: Any) -> Optional[Tuple[str, str]]:
    # Returns ("direct", answer) or ("rag", fallback)
    # Requirement (exclude WH + logistics)
    if P.REQUIREMENT_PATTERN.search(q) and not P.WH_PREFIX_PATTERN.search(q) and not P.LOGISTICS_PATTERN.search(q):
        return ("direct", answer_requirement(q, context_chunks))

    # Suitability: first-person OR third-person profile
    #if P.SUITABILITY_PATTERN.search(q) or P.SUITABILITY_PROFILE_PATTERN.search(q):
    #    return ("direct", F.SUITABILITY_FALLBACK)
    if P.SUITABILITY_PATTERN.search(q) or P.SUITABILITY_PROFILE_PATTERN.search(q):
        return ("suitability", "")

    return None

def pick_rag_fallback(q: str) -> str:
    if P.REQUIREMENT_PATTERN.search(q) and not P.WH_PREFIX_PATTERN.search(q) and not P.LOGISTICS_PATTERN.search(q):
        return F.REQUIREMENT_FALLBACK_GENERIC
    if P.SUITABILITY_PATTERN.search(q) or P.SUITABILITY_PROFILE_PATTERN.search(q):
        return F.SUITABILITY_FALLBACK
    return F.NOT_FOUND_FALLBACK
