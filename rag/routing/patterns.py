# rag/routing/patterns.py
import re

GREETING_PATTERN = re.compile(r"^(hi|hello|hey|good morning|good afternoon|good evening|how are you)\W*$", re.IGNORECASE)
THANKS_PATTERN   = re.compile(r"^(thanks|thank you|thx|bye|goodbye)\W*$", re.IGNORECASE)
PRAISE_PATTERN   = re.compile(r"^(nice response|good answer|that helps|great)\W*$", re.IGNORECASE)

MDES_PATTERN = re.compile(r"\b(mdes|master\s+of\s+design|integrated\s+design)\b", re.IGNORECASE)
OVERVIEW_PATTERN = re.compile(r"\b(tell me more|tell me about|what is|describe|overview)\b", re.IGNORECASE)

# Requirement intent (keep it conservative)
REQUIREMENT_PATTERN = re.compile(
    r"\b(required|required for admission|admission requirement|is .* mandatory|requirement)\b",
    re.IGNORECASE,
)
WH_PREFIX_PATTERN = re.compile(r"^\s*(when|where|how|what|which)\b", re.IGNORECASE)

# Suitability / profile
SUITABILITY_PATTERN = re.compile(r"\b(good fit|fit for|suitable|eligible|my background|background)\b", re.IGNORECASE)
SUITABILITY_PROFILE_PATTERN = re.compile(
    r"\b(kind of candidate|who thrives|who tends to thrive|who is suited|who should apply|profile of students)\b",
    re.IGNORECASE,
)

# Intake / dates
INTAKE_PATTERN = re.compile(
    r"\b(intake|matriculat\w*|cohort)\b",
    re.IGNORECASE
)

PROGRAMME_START_PATTERN = re.compile(
    r"\b(programme\s+start|program\s+start|start\s+date|classes\s+begin|when\s+does\s+edi\s+start)\b",
    re.IGNORECASE
)

APPLICATION_PERIOD_PATTERN = re.compile(
    r"\b(application\s+period|application\s+window|applications?\s+open|applications?\s+close|apply\s+by|deadline)\b",
    re.IGNORECASE
)


# Policy/process
REAPPLICATION_PATTERN = re.compile(r"\b(reapply|re-apply|apply again|second attempt|try again)\b", re.IGNORECASE)
OFFER_OUTCOME_PATTERN = re.compile(
    r"\b(not accept|do not accept|dont accept|decline|reject|lapse|expire|miss the acceptance deadline|what happens if.*accept)\b",
    re.IGNORECASE,
)

# Logistics
ARRIVAL_PATTERN = re.compile(r"\b(arrive|arrival|reach|come to nus|on campus|move to singapore)\b", re.IGNORECASE)
VISA_PATTERN    = re.compile(r"\b(visa|student pass|student visa|immigration|ipa|entry permit)\b", re.IGNORECASE)
VISA_PROCESS_PATTERN = re.compile(
    r"\b(how do i apply|how to apply|application process|apply for a visa|visa application)\b",
    re.IGNORECASE,
)

LOGISTICS_PATTERN = re.compile(
    r"\b(visa|student pass|immigration|ipa|entry permit|arrive|arrival|on campus|move to singapore)\b",
    re.IGNORECASE,
)

# Visa keywords (do I need a visa?)
VISA_PATTERN = re.compile(
    r"\bvisa\b|\bstudent\s*pass\b|\bimmigration\b",
    re.I
)

# Visa process / application (must mention visa explicitly)
VISA_PROCESS_PATTERN = re.compile(
    r"(visa|student\s*pass|immigration).*(apply|application|process|procedure|how)"
    r"|"
    r"(apply|application|process|procedure|how).*(visa|student\s*pass|immigration)",
    re.I
)


