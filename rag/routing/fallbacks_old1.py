# rag/routing/fallbacks.py

MDES_REDIRECT_MSG = (
    "I only answer questions about the MSc Engineering Design & Innovation (EDI) programme. "
    "For MDes (Master of Design in Integrated Design), please refer to the official programme website."
)

NOT_FOUND_FALLBACK = (
    "I can’t find this in the MSc EDI admissions information I’m currently using. "
    "If you rephrase your question, I may be able to help."
)

REQUIREMENT_FALLBACK_GENERIC = (
    "I can’t find a confirmed EDI-specific requirement statement for this in my current sources. "
    "Admissions are usually assessed holistically (academic background, projects/experience, and motivation)."
)

SUITABILITY_FALLBACK = (
    "Candidates who tend to thrive in MSc Engineering Design & Innovation (EDI) are typically curious about working across disciplines, "
    "comfortable with ambiguity, and motivated to solve real-world problems through design and technology. "
    "The programme suits people who enjoy collaboration and want to broaden beyond a single discipline."
)

PROGRAMME_START_FALLBACK = (
    "The MSc Engineering Design & Innovation (EDI) programme typically has one intake per academic year, "
    "with classes starting in the second half of the year (often around August). "
    "Please refer to your offer/enrolment instructions for the confirmed start date."
)

OFFER_OUTCOME_FALLBACK = (
    "If you do not accept the offer within the acceptance period stated in your offer letter, "
    "the offer will typically lapse and you will not be enrolled in MSc Engineering Design & Innovation (EDI). "
    "For any conditions (including fees), please refer to your offer letter, as details can vary."
)

REAPPLICATION_FALLBACK = (
    "Yes — you can apply again to MSc Engineering Design & Innovation (EDI) in a later application cycle. "
    "Each cycle is assessed independently, and it helps to strengthen your application with updated experience/projects."
)

VISA_FALLBACK = (
    "A student pass/visa is not usually part of the admissions decision, but it may be required for enrolment "
    "if you are an international student. After you accept an offer, NUS typically provides instructions for the student pass/visa process. "
)

VISA_PROCESS_FALLBACK = (
    "Visa application is typically handled after you accept an offer. NUS will usually provide official instructions "
    "for applying for a Student’s Pass through Singapore’s immigration system. The exact steps depend on your nationality."
)
