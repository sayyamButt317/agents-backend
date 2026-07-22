

from app.agents.aesthetic.state.aesthic_state import AestheticState


async def CustomersReview(state: AestheticState) -> AestheticState:
    llm = ChatOpenAI(model="gpt-4o-mini")
    return Command(
        update={"reviews": "customer reviews"},
        goto="customer_reviews"
    )
    