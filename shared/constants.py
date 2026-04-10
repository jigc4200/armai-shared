"""Shared constants — single source of truth for agent tool identifiers.

All layers (worker-langchain, api-gateway, dashboard) MUST use these
exact strings when referring to agent tools.  Adding a new tool?  Add
it here first, then wire it in tools.py and Settings.tsx.
"""


class AgentTool:
    SEARCH_KNOWLEDGE_BASE = "search_knowledge_base"
    ESCALATE_TO_HUMAN = "escalate_to_human"
    GET_CURRENT_DATETIME = "get_current_datetime"
    SEND_EMAIL = "send_email"
    MAKE_CALL = "make_call"


ALL_AGENT_TOOLS = [
    AgentTool.SEARCH_KNOWLEDGE_BASE,
    AgentTool.ESCALATE_TO_HUMAN,
    AgentTool.GET_CURRENT_DATETIME,
    AgentTool.SEND_EMAIL,
    AgentTool.MAKE_CALL,
]
