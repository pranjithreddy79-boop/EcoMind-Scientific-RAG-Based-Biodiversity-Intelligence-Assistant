from rag.clarifier import (
    needs_clarification,
    generate_clarifying_questions
)


profile = {
    "region": "Semi-arid Karnataka",
    "land_use": "Monoculture wheat"
}


if needs_clarification(profile):

    print("\nAdditional information required:\n")

    questions = generate_clarifying_questions(profile)

    for number, question in enumerate(questions, start=1):
        print(f"{number}. {question}")

else:

    print("Enough environmental information is available.")