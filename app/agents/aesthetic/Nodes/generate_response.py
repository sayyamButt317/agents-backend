

async def GenerateResponse(state: AestheticState) -> Command:
    return Command(
        update={"response": "Response generated successfully"},
        goto="end",
    )