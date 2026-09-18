from pathlib import Path
import json


EXTRACTED_DIR = Path("knowledge/extracted")
SOURCES_FILE = Path("data/sources.json")


def load_sources():

    if not SOURCES_FILE.exists():
        return {}

    with open(
        SOURCES_FILE,
        "r",
        encoding="utf-8"
    ) as file:

        sources = json.load(file)

    return {
        source["source_id"]: source
        for source in sources
    }


def identify_source(file_path, sources):

    filename = file_path.name.lower()

    if "fao_soil_biodiversity" in filename:

        return sources.get(
            "FAO_SOIL_BIODIVERSITY"
        )

    if "ipcc_ar6_chapter_2" in filename:

        return sources.get(
            "IPCC_AR6_WGII_CH2"
        )

    if "ipcc_ar6_chapter_4" in filename:

        return sources.get(
            "IPCC_AR6_WGII_CH4"
        )

    return None


def load_documents():

    documents = []

    sources = load_sources()

    if not EXTRACTED_DIR.exists():

        print(
            "ERROR: knowledge/extracted folder not found."
        )

        return documents

    for file_path in EXTRACTED_DIR.glob("*.txt"):

        text = file_path.read_text(
            encoding="utf-8"
        )

        source_info = identify_source(
            file_path,
            sources
        )

        if source_info is None:

            print(
                f"Warning: No source metadata for "
                f"{file_path.name}"
            )

        documents.append({

            "source": str(file_path),

            "text": text,

            "source_info": source_info,

            "source_type": "scientific_report"

        })

    return documents


if __name__ == "__main__":

    documents = load_documents()

    print(
        f"\nLoaded {len(documents)} scientific reports."
    )

    for document in documents:

        print(
            "\nFile:",
            document["source"]
        )

        source = document.get(
            "source_info"
        )

        if source:

            print(
                "Scientific source:",
                source["title"]
            )

            print(
                "Organization:",
                source["organization"]
            )