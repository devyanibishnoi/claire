"""
Owner: Devyani

Embeds a hidden prompt-injection instruction inside a fused evidence record's
text field (e.g. a fake log message telling the LLM to downplay severity),
runs it through explanation/llm_explain.py, and records whether the model
gets fooled — before/after adding the "treat evidence as untrusted data" rule.

See coder_checklists.md > Devyani > Phase 6-7.
"""

# TODO: implement prompt-injection test + before/after evaluation.
