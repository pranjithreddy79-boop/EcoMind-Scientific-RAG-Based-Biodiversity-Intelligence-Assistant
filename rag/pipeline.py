from pathlib import Path
import json

from rag.retriever import Retriever
from rag.reasoning import analyze_environment


def load_quantitative_evidence():

    evidence_file = Path(
        "data/quantitative_evidence.json"
    )

    if not evidence_file.exists():
        print("Warning: quantitative_evidence.json not found.")
        return {}

    with open(
        evidence_file,
        "r",
        encoding="utf-8"
    ) as file:

        return json.load(file)


class EcoMindPipeline:

    def __init__(self):

        print("Initializing EcoMind AI pipeline...")

        self.retriever = Retriever()

        self.quantitative_evidence = (
            load_quantitative_evidence()
        )

        print(
            f"Loaded {len(self.quantitative_evidence)} "
            "quantitative evidence records."
        )

        print("EcoMind AI pipeline ready.")

    def analyze(self, profile, problem=None):

        profile_data = profile.model_dump(
            exclude_none=True
        )

        # =========================================
        # BUILD RAG QUERY
        # =========================================

        query_parts = []

        if problem:

            query_parts.append(
                f"Environmental problem: {problem}"
            )

        for key, value in profile_data.items():

            query_parts.append(
                f"{key}: {value}"
            )

        query = (
            "Environmental biodiversity assessment: "
            + ", ".join(query_parts)
        )

        # =========================================
        # RETRIEVE SCIENTIFIC EVIDENCE
        # =========================================

        evidence = self.retriever.retrieve(
            query,
            top_k=8
        )

        # =========================================
        # GENERATE RECOMMENDATIONS
        # =========================================

        recommendations = analyze_environment(
            profile_data
        )

        # =========================================
        # ATTACH EVIDENCE TO EACH RECOMMENDATION
        # =========================================

        for recommendation in recommendations:

            # -------------------------------------
            # Quantitative evidence
            # -------------------------------------

            evidence_ids = recommendation.get(
                "quantitative_evidence_ids",
                []
            )

            recommendation[
                "quantitative_evidence"
            ] = []

            for evidence_id in evidence_ids:

                evidence_item = (
                    self.quantitative_evidence.get(
                        evidence_id
                    )
                )

                if evidence_item:

                    recommendation[
                        "quantitative_evidence"
                    ].append(
                        evidence_item
                    )

            # -------------------------------------
            # Scientific RAG evidence
            # -------------------------------------

            keywords = [
                keyword.lower()
                for keyword in recommendation.get(
                    "evidence_keywords",
                    []
                )
            ]

            matched_evidence = []

            for item in evidence:

                text = item.get(
                    "text",
                    ""
                ).lower()

                keyword_matches = sum(
                    1
                    for keyword in keywords
                    if keyword in text
                )

                if keyword_matches > 0:

                    matched_evidence.append(
                        (
                            keyword_matches,
                            item
                        )
                    )

            # -------------------------------------
            # Sort evidence
            # -------------------------------------

            matched_evidence.sort(
                key=lambda x: (
                    x[0],
                    x[1].get(
                        "score",
                        0
                    )
                ),
                reverse=True
            )

            # -------------------------------------
            # Select top 3 evidence chunks
            # -------------------------------------

            selected_evidence = [
                item
                for _, item
                in matched_evidence[:3]
            ]

            # Fallback
            if not selected_evidence:

                selected_evidence = evidence[:3]

            recommendation[
                "evidence"
            ] = []

            for item in selected_evidence:

                source_info = item.get(
                    "source_info"
                )

                scientific_source = None

                if source_info:

                    scientific_source = {

                        "title":
                            source_info.get(
                                "title"
                            ),

                        "organization":
                            source_info.get(
                                "organization"
                            ),

                        "type":
                            source_info.get(
                                "type"
                            ),

                        "url":
                            source_info.get(
                                "url"
                            )
                    }

                recommendation[
                    "evidence"
                ].append({

                    "source":
                        item.get(
                            "source"
                        ),

                    "relevance_score":
                        round(
                            item.get(
                                "score",
                                0
                            ),
                            4
                        ),

                    "supporting_text":
                        item.get(
                            "text"
                        ),

                    "scientific_source":
                        scientific_source
                })

        # =========================================
        # FINAL RESPONSE
        # =========================================

        return {

            "query":
                query,

            "environmental_profile":
                profile_data,

            "recommendations":
                recommendations,

            "retrieved_evidence":
                evidence
        }