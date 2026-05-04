"""Shared constants — single source of truth for agent tool and module identifiers.

All layers (worker-langchain, api-gateway, dashboard) MUST use these
exact strings when referring to agent tools or modules.  Adding a new
tool or module?  Add it here first, then wire it in the corresponding
layer.
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


class AgentModule:
    """Canonical module names for the modular agent suite.

    These map 1:1 to specialised LangGraph agents and their tool sets.
    .. code-block:: python

        from shared.constants import AgentModule
        active_modules = ["core", "sales"]
    """
    CORE = "core"
    GENERAL = "general"
    SALES = "sales"
    SUPPORT = "support"
    AGENDA = "agenda"
    PAYMENTS = "payments"


ALL_AGENT_MODULES = [
    AgentModule.CORE,
    AgentModule.GENERAL,
    AgentModule.SALES,
    AgentModule.SUPPORT,
    AgentModule.AGENDA,
    AgentModule.PAYMENTS,
]


# ── Legacy tool → module mapping (for migration script) ───────────────────
#
# When a tenant had ``agent_tools`` configured, this mapping determines
# which modules should be enabled after the migration to ``tenant_modules``.
TOOL_TO_MODULE: dict[str, str] = {
    AgentTool.SEARCH_KNOWLEDGE_BASE: AgentModule.CORE,
    AgentTool.ESCALATE_TO_HUMAN: AgentModule.CORE,
    AgentTool.GET_CURRENT_DATETIME: AgentModule.CORE,
    AgentTool.SEND_EMAIL: AgentModule.CORE,
    AgentTool.MAKE_CALL: AgentModule.CORE,
}
