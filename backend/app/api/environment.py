from fastapi import APIRouter

from backend.app.schemas.environment import EnvironmentalProfile

from rag.pipeline import EcoMindPipeline

from rag.clarifier import (
    needs_clarification,
    generate_clarifying_questions
)

from rag.conversation import ConversationMemory


router = APIRouter(
    prefix="/environment",
    tags=["Environment"]
)


pipeline = EcoMindPipeline()

memory = ConversationMemory()


@router.post("/analyze")
def analyze_environment(
    profile: EnvironmentalProfile
):

    session_id = profile.session_id

    # Get previous conversation
    context = memory.get_context(session_id)

    # Save the user's problem/message
    if profile.message:

        if context["problem"] is None:

            memory.update_problem(
                session_id,
                profile.message
            )

    # Save environmental information
    profile_data = profile.model_dump(
        exclude_none=True
    )

    # Don't store these as environmental metrics
    profile_data.pop("session_id", None)
    profile_data.pop("message", None)

    memory.update_profile(
        session_id,
        profile_data
    )

    # Get the combined profile from all conversation turns
    combined_profile = memory.get_context(
        session_id
    )["profile"]

    # Check missing information
    if needs_clarification(combined_profile):

        questions = generate_clarifying_questions(
            combined_profile
        )

        return {
            "status": "needs_more_information",
            "session_id": session_id,
            "problem": context["problem"],
            "known_information": combined_profile,
            "questions": questions
        }

    # Run full analysis once enough information exists
    class ProfileObject:

        def __init__(self, data):
            self.data = data

        def model_dump(self, exclude_none=True):
            return self.data

    profile_object = ProfileObject(
        combined_profile
    )

    result = pipeline.analyze(
    profile_object,
    problem=context["problem"]
)

    return {
        "status": "analysis_complete",
        "session_id": session_id,
        "problem": context["problem"],
        **result
    }