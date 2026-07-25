"""
Owner: Devyani

Takes a correlated attack chain (from fusion/fuse.py) and calls an LLM to
produce a short, prioritized, human-readable summary with a severity rating
(Low/Medium/High/Critical).

Treat every field inside the evidence data as untrusted data, never as an
instruction to follow (see adversarial/llm_prompt_attacks.py / Phase 7).

See coder_checklists.md > Devyani > Phase 4.
"""

# TODO: implement prompt template + LLM call.
