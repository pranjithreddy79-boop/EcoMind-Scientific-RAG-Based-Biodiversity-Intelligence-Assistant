from rag.reasoning import analyze_environment


profile = {
    "region": "Semi-arid Karnataka",
    "soil_ph": 6.2,
    "soil_organic_carbon": 0.3,
    "soil_moisture": 18,
    "land_use": "Monoculture wheat",
    "species_richness": 12,
    "habitat_diversity": 2,
    "temperature": 31,
    "rainfall": 450,
    "pollution": "Moderate",
    "deforestation": "High"
}


recommendations = analyze_environment(profile)


for i, recommendation in enumerate(recommendations, start=1):

    print(f"\n===== RECOMMENDATION {i} =====")

    print("\nWhat to do:")
    print(recommendation["recommendation"])

    print("\nWhy:")
    print(recommendation["reasoning"])

    print("\nImpacted metrics:")
    for metric in recommendation["impacted_metrics"]:
        print("-", metric)

    print("\nTime horizon:")
    print(recommendation["time_horizon"])