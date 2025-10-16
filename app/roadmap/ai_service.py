"""
AI service module to interact with OpenAI API for generating roadmaps.
"""
import os
import openai

from app.logger_config import setup_logger


logger = setup_logger(__name__)


class AIServiceError(Exception):
    """Custom exception for AI service errors."""


model = "gpt-4o-2024-08-06"


def get_openai_client() -> openai.OpenAI:
    """Get OpenAI client with API key."""
    return openai.OpenAI(
        api_key=os.environ.get("OPENAI_API_KEY"),
    )


def generate_roadmap(career_goal: str) -> str:
    """Sends the career goal to OpenAI and generates a roadmap."""
    if not os.environ.get("OPENAI_API_KEY"):
        logger.error("Missing OpenAI API key.")
        raise AIServiceError("Missing OpenAI API key.")

    client = get_openai_client()
    prompt = f"career goal: {career_goal}"

    try:
        response = client.chat.completions.create(
            model=model,
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are an expert career advisor. "
                        "Generate a professional learning roadmap "
                        "for the given career goal. "
                        "Structure it in stages: Essential Learning, "
                        "Industry Essential Learning, and UpSkill Learning. "
                        "For each course, provide the following format:\n\n"
                        "(<duration in hours or minutes>)\n"
                        " <course description>\n"
                        "<course link>\n\n"
                        "Rules for course selection:\n"
                        "1. Select **one focused, high-quality course per "
                        "technology**, with high ratings, many learners, "
                        "and up-to-date content.\n"
                        "2. Prefer courses with valid, working links; if "
                        "possible, include coupon links.\n"
                        "3. Avoid free courses unless they are exceptionally "
                        "high quality and comprehensive.\n"
                    ),
                },
                {"role": "user", "content": prompt},
            ],
        )

        logger.info("Successfully received a result from OpenAI.")
        return response.choices[0].message.content or ""

    except openai.RateLimitError:
        logger.warning("OpenAI API rate limit reached.")
        raise AIServiceError("OpenAI API rate limit reached.")
    except Exception as e:
        logger.exception("Unexpected OpenAI error.")
        raise AIServiceError(
            f"Unexpected OpenAI error: {e}"
        )
