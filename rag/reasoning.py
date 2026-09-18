from typing import Dict, List


def analyze_environment(profile: Dict) -> List[Dict]:

    recommendations = []

    soc = profile.get("soil_organic_carbon")
    moisture = profile.get("soil_moisture")
    rainfall = profile.get("rainfall")
    land_use = profile.get("land_use", "")
    species_richness = profile.get("species_richness")
    habitat_diversity = profile.get("habitat_diversity")
    pollution = profile.get("pollution", "")
    deforestation = profile.get("deforestation", "")

    # =========================================================
    # RECOMMENDATION 1
    # LOW SOC + LOW RAINFALL + LOW SOIL MOISTURE
    # =========================================================

    if (
        soc is not None
        and soc < 1.0
        and rainfall is not None
        and rainfall < 600
        and moisture is not None
        and moisture < 25
    ):

        recommendations.append({

            "recommendation":
                "Increase soil organic matter and maintain year-round "
                "vegetation cover using locally suitable organic amendments "
                "and cover vegetation.",

            "reasoning":
                "The recommendation is based on the interaction between "
                "soil organic carbon, rainfall and soil moisture rather than "
                "any single variable. Improving soil organic matter and "
                "maintaining vegetation cover can address soil condition, "
                "water retention and habitat simultaneously.",

            "impacted_metrics": [
                "soil_organic_carbon",
                "soil_moisture",
                "vegetation_cover",
                "habitat_condition"
            ],

            "time_horizon": "6-24 months",

            "confidence_score": 0.85,

            "confidence": "High",

            "evidence_keywords": [
                "soil organic carbon",
                "soil moisture",
                "vegetation",
                "soil biodiversity",
                "water retention"
            ],

            # Quantitative evidence references
            "quantitative_evidence_ids": [
                "SOC_COVER_CROPS",
                "SOC_ORGANIC_AMENDMENTS"
            ],

            "measurement_plan": {

                "baseline_metrics": [
                    "soil_organic_carbon",
                    "soil_moisture",
                    "vegetation_cover"
                ],

                "monitoring_frequency":
                    "Measure soil moisture seasonally and soil organic carbon periodically.",

                "expected_direction": {
                    "soil_organic_carbon": "increase",
                    "soil_moisture": "increase or become more stable",
                    "vegetation_cover": "increase",
                    "habitat_condition": "improve"
                },

                "biodiversity_indicator":
                    "Track species richness and habitat diversity over time."
            }
        })


    # =========================================================
    # RECOMMENDATION 2
    # MONOCULTURE + LOW HABITAT DIVERSITY + LOW SPECIES RICHNESS
    # =========================================================

    if (
        "monoculture" in land_use.lower()
        and habitat_diversity is not None
        and habitat_diversity < 3
        and species_richness is not None
        and species_richness < 20
    ):

        recommendations.append({

            "recommendation":
                "Increase habitat diversity by introducing suitable "
                "crop diversification, field margins, or locally "
                "appropriate agroforestry elements.",

            "reasoning":
                "A monoculture combined with low habitat diversity and "
                "low species richness indicates reduced vegetation "
                "structure and resource diversity. Increasing habitat "
                "variety can provide additional food, shelter and "
                "vegetation structures for organisms.",

            "impacted_metrics": [
                "habitat_diversity",
                "species_richness",
                "vegetation_diversity",
                "habitat_connectivity"
            ],

            "time_horizon": "1-3 years",

            "confidence_score": 0.80,

            "confidence": "High",

            "evidence_keywords": [
                "monoculture",
                "habitat diversity",
                "species richness",
                "vegetation diversity",
                "habitat fragmentation",
                "agroforestry"
            ],

            # Quantitative evidence reference
            "quantitative_evidence_ids": [
                "BIODIVERSITY_DIVERSIFIED_FARMING"
            ],

            "measurement_plan": {

                "baseline_metrics": [
                    "species_richness",
                    "habitat_diversity",
                    "vegetation_diversity"
                ],

                "monitoring_frequency":
                    "Record biodiversity observations seasonally or annually.",

                "expected_direction": {
                    "species_richness": "increase or stabilize",
                    "habitat_diversity": "increase",
                    "vegetation_diversity": "increase",
                    "habitat_connectivity":
                        "improve where connected vegetation is restored"
                },

                "biodiversity_indicator":
                    "Compare repeated species observations and habitat classes against the baseline."
            }
        })


    # =========================================================
    # RECOMMENDATION 3
    # DEFORESTATION + LOW SPECIES RICHNESS
    # =========================================================

    if (
        "high" in deforestation.lower()
        and species_richness is not None
        and species_richness < 20
    ):

        recommendations.append({

            "recommendation":
                "Prioritize protection and restoration of existing "
                "natural vegetation and improve habitat connectivity "
                "where feasible.",

            "reasoning":
                "High deforestation can reduce and fragment habitat. "
                "When species richness is also low, protecting remaining "
                "vegetation and restoring connected habitat can address "
                "both habitat availability and biodiversity pressure.",

            "impacted_metrics": [
                "species_richness",
                "habitat_connectivity",
                "habitat_diversity",
                "vegetation_cover"
            ],

            "time_horizon": "1-5 years",

            "confidence_score": 0.82,

            "confidence": "High",

            "evidence_keywords": [
                "deforestation",
                "habitat fragmentation",
                "species richness",
                "habitat connectivity",
                "natural vegetation"
            ],

            "measurement_plan": {

                "baseline_metrics": [
                    "species_richness",
                    "habitat_connectivity",
                    "vegetation_cover"
                ],

                "monitoring_frequency":
                    "Review vegetation and biodiversity indicators annually.",

                "expected_direction": {
                    "species_richness": "increase or stabilize",
                    "habitat_connectivity": "improve",
                    "habitat_diversity": "increase",
                    "vegetation_cover": "increase"
                },

                "biodiversity_indicator":
                    "Track repeated species observations and mapped vegetation connectivity."
            }
        })


    # =========================================================
    # RECOMMENDATION 4
    # POLLUTION + LOW SPECIES RICHNESS
    # =========================================================

    if (
        "high" in pollution.lower()
        and species_richness is not None
        and species_richness < 20
    ):

        recommendations.append({

            "recommendation":
                "Identify and reduce the major pollution source and "
                "establish appropriate vegetated buffer areas where suitable.",

            "reasoning":
                "High pollution can place pressure on organisms and "
                "ecosystem processes. Reducing the pollution source "
                "addresses the pressure directly, while suitable "
                "vegetation buffers may help reduce movement of some pollutants.",

            "impacted_metrics": [
                "pollution",
                "species_richness",
                "habitat_condition"
            ],

            "time_horizon": "6-24 months",

            "confidence_score": 0.78,

            "confidence": "Medium-High",

            "evidence_keywords": [
                "pollution",
                "soil biodiversity",
                "species richness",
                "vegetation",
                "ecosystem functions"
            ],

            "measurement_plan": {

                "baseline_metrics": [
                    "pollution level",
                    "species_richness",
                    "habitat condition"
                ],

                "monitoring_frequency":
                    "Monitor the relevant pollution indicator according to the pollutant type and repeat biodiversity observations periodically.",

                "expected_direction": {
                    "pollution": "decrease",
                    "species_richness": "increase or stabilize",
                    "habitat_condition": "improve"
                },

                "biodiversity_indicator":
                    "Track species richness and habitat condition alongside the pollution indicator."
            }
        })


    return recommendations