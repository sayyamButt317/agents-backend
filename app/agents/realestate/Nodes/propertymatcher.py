from agents import Agent, Runner
import json


async def LanguageDetectorNode(state):
    print("Entering into Language Detector")
    user_message = state.get("user_message", "")

    result = await Runner.run(
        Agent(
            name="language_detector",
            instructions="""
            Detect language from user input.
            Return ONLY valid JSON:
            {
              "language": "en" | "ar"
            }
            """,
        ),
        input=user_message,
    )
    output = result.final_output
    print(f"detected language:{output}")

    if isinstance(output, str):
        try:
            output = json.loads(output)
        except:
            output = {"language": "en"}
    state["language"] = output.get("language", "en")
    return state
