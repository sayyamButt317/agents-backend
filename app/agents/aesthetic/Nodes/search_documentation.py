from app.agents.aesthetic.state.aesthic_state import AestheticState


async def SearchDocumentation(state: AestheticState) -> AestheticState:
    llm = ChatOpenAI(model="gpt-4o-mini")
    return Command(
        update={"documentation": "documentation searched successfully"},
        goto="search_documentation"
    )