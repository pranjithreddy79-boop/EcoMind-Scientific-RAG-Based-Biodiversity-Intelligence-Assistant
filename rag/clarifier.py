from typing import Dict, List


# These are the environmental variables we consider important
# before making a biodiversity recommendation.
REQUIRED_VARIABLES = {
    "soil_organic_carbon": "soil organic carbon (%)",
    "soil_moisture": "soil moisture (%)",
    "rainfall": "annual rainfall (mm)",
    "land_use": "land-use type",
    "species_richness": "species richness",
    "habitat_diversity": "habitat diversity"
}


def find_missing_variables(profile: Dict) -> List[str]:

    missing = []

    for key, description in REQUIRED_VARIABLES.items():

        value = profile.get(key)

        if value is None or value == "":
            missing.append(description)

    return missing


def generate_clarifying_questions(profile: Dict) -> List[str]:

    missing = find_missing_variables(profile)

    questions = []

    for variable in missing:

        questions.append(
            f"What is the {variable}?"
        )

    return questions


def needs_clarification(profile: Dict) -> bool:

    missing = find_missing_variables(profile)

    return len(missing) > 0