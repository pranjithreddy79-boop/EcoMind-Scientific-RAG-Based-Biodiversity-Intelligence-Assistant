1. Project Overview

EcoMind is an AI-powered biodiversity intelligence system designed to analyze environmental conditions and provide scientifically grounded, actionable biodiversity recommendations.

It combines structured environmental data, conversational interaction, clarifying questions, scientific document retrieval, Sentence Transformer embeddings, FAISS vector search, multi-variable environmental reasoning, quantitative research evidence, and monitoring plans.

The system is designed to avoid generic LLM-only recommendations by retrieving scientific evidence and combining it with the environmental profile before producing recommendations.

2. Problem Being Solved

Biodiversity is affected by interacting environmental factors such as:

Soil Organic Carbon

Soil Moisture

Soil pH

Rainfall

Temperature

Land Use

Species Richness

Habitat Diversity

Pollution

Deforestation

EcoMind is designed to:

Understand the environmental problem.

Ask for missing information.

Combine multiple environmental variables.

Retrieve relevant scientific evidence.

Generate an actionable recommendation.

Explain why it is relevant.

Identify impacted metrics.

Provide a time horizon.

Provide a measurement/monitoring plan.

Show the scientific evidence used.

3. Main Features

3.1 Structured Environmental Input

The application accepts structured environmental information through JSON/API requests.

Supported fields:

session_id, message, region, latitude, longitude, soil_ph, soil_organic_carbon, soil_moisture, land_use, species_richness, habitat_diversity, temperature, rainfall, pollution, deforestation.

Example:

{
  "session_id": "demo-001",
  "message": "Biodiversity is declining on my farm",
  "region": "Ballari, Karnataka",
  "soil_ph": 6.8,
  "soil_organic_carbon": 0.8,
  "soil_moisture": 20,
  "temperature": 30,
  "rainfall": 500,
  "species_richness": 12,
  "habitat_diversity": 2,
  "land_use": "monoculture",
  "pollution": "low",
  "deforestation": "medium"
}

3.2 Conversational Intelligence

EcoMind stores the environmental problem and environmental variables within a session.

Example:

User: Biodiversity is declining on my land.
EcoMind: asks for missing environmental information.

User: My soil organic carbon is 0.8%.
User: Soil moisture is 20%.
User: Annual rainfall is 500 mm.

The values are combined when analysis is performed.

Current implementation:

rag/conversation.py

Limitation: memory is currently in application memory and is not a persistent production database.

3.3 Clarifying Questions

Implementation:

rag/clarifier.py

The current required variables are:

soil organic carbon

soil moisture

annual rainfall

land-use type

species richness

habitat diversity

If information is missing, the API returns needs_more_information and a list of questions instead of immediately generating a recommendation.

4. Scientific Knowledge Base

Current scientific reports:

FAO

The State of Knowledge of Soil Biodiversity

knowledge/sources/FAO_Soil_Biodiversity.pdf

Topics include soil biodiversity, soil organisms, soil health, and nutrient cycling.

IPCC AR6 WGII Chapter 2

Climate Change 2022: Impacts, Adaptation and Vulnerability — Chapter 2

knowledge/sources/IPCC_AR6_Chapter_2.pdf

Topics include terrestrial ecosystems, biodiversity, climate change, habitat, and species.

IPCC AR6 WGII Chapter 4

Climate Change 2022: Impacts, Adaptation and Vulnerability — Chapter 4

knowledge/sources/IPCC_AR6_Chapter_4.pdf

Topics include water, water availability, climate, and ecosystems.

Scientific source metadata:

data/sources.json

5. RAG Architecture

Scientific PDF
      |
      v
PDF Text Extraction
      |
      v
Text Chunking
      |
      v
Sentence Transformer Embeddings
      |
      v
FAISS Vector Index
      |
      v
Query Embedding
      |
      v
Similarity Search
      |
      v
Relevant Scientific Evidence
      |
      v
Environmental Reasoning
      |
      v
Recommendation + Evidence

6. PDF Processing

Implementation:

rag/pdf_loader.py

Uses pypdf to:

Find PDFs in knowledge/sources/

Extract page text

Add page markers

Save extracted text in knowledge/extracted/

Generated files include:

knowledge/extracted/FAO_Soil_Biodiversity.txt
knowledge/extracted/IPCC_AR6_Chapter_2.txt
knowledge/extracted/IPCC_AR6_Chapter_4.txt

7. Document Loading

Implementation:

rag/document_loader.py

The document loader reads extracted reports, identifies their scientific source metadata, and creates document objects for indexing.

8. Text Chunking

Implementation:

rag/chunker.py

Current configuration:

Chunk size: 120 words

Overlap: 30 words

Conceptually:

Document
  |
  +-- Chunk 1: words 1–120
  |
  +-- Chunk 2: words 91–210
  |
  +-- Chunk 3: words 181–300

9. Embeddings

Implementation:

rag/embedder.py

Model:

all-MiniLM-L6-v2

The model converts text into numerical embeddings. Embeddings are normalized before similarity search.

10. Vector Store

Implementation:

rag/vector_store.py

Technology:

FAISS

Index:

IndexFlatIP

Stored files:

data/environment.index
data/environment_metadata.json

11. Retriever

Implementation:

rag/retriever.py

The retriever:

Receives an environmental query.

Creates an embedding.

Searches FAISS.

Returns relevant scientific chunks with similarity scores.

The analysis pipeline currently retrieves up to 8 results.

12. Environmental Reasoning Engine

Implementation:

rag/reasoning.py

The prototype uses multi-variable rule-based reasoning.

Rule 1 — Soil Condition + Water Stress

Condition:

SOC < 1%
AND Rainfall < 600 mm
AND Soil moisture < 25%

Recommendation:

Increase soil organic matter and maintain year-round vegetation cover using locally suitable organic amendments and cover vegetation.

Impacted metrics:

soil organic carbon

soil moisture

vegetation cover

habitat condition

Time horizon:

6–24 months

Rule 2 — Monoculture + Low Habitat Diversity + Low Species Richness

Condition:

Land use contains "monoculture"
AND Habitat diversity < 3
AND Species richness < 20

Recommendation:

Increase habitat diversity by introducing suitable crop diversification, field margins, or locally appropriate agroforestry elements.

Impacted metrics:

habitat diversity

species richness

vegetation diversity

habitat connectivity

Time horizon:

1–3 years

Rule 3 — Deforestation + Low Species Richness

Condition:

Deforestation contains "high"
AND Species richness < 20

Recommendation:

Prioritize protection and restoration of existing natural vegetation and improve habitat connectivity where feasible.

Impacted metrics:

species richness

habitat connectivity

habitat diversity

vegetation cover

Time horizon:

1–5 years

Rule 4 — Pollution + Low Species Richness

Condition:

Pollution contains "high"
AND Species richness < 20

Recommendation:

Identify and reduce the major pollution source and establish appropriate vegetated buffer areas where suitable.

Impacted metrics:

pollution

species richness

habitat condition

Time horizon:

6–24 months

Reasoning limitation

The thresholds above are prototype decision thresholds, not universal scientific thresholds. Confidence values are heuristic indicators rather than calibrated probabilities.

13. Quantitative Evidence

Implementation:

data/quantitative_evidence.json

Current research evidence includes:

Practice

Metric

Reported Evidence

Cover crops

Soil Organic Carbon

5.2% average increase

Organic amendments

Soil Organic Carbon

29% average increase in croplands

Farm diversification

Species richness

26% higher species richness

These are research-level averages/comparisons, not guaranteed site-specific predictions. Actual effects depend on conditions such as soil, climate, landscape, crop type, and management.

14. Complete AI Pipeline

Implementation:

rag/pipeline.py

User Profile
     |
     v
Create Environmental Query
     |
     v
RAG Retrieval
     |
     v
Scientific Evidence
     |
     v
Multi-Variable Reasoning
     |
     v
Match Quantitative Evidence
     |
     v
Attach Scientific Sources
     |
     v
Final Analysis

The pipeline combines the environmental problem and structured variables into a retrieval query.

15. Backend

Main file:

backend/app/main.py

Framework:

FastAPI

Endpoints:

GET  /
GET  /health
POST /environment/analyze

Health check:

GET /health

Expected:

{
  "status": "healthy"
}

API documentation:

http://127.0.0.1:8000/docs

16. API Processing Flow

backend/app/api/environment.py performs:

Receive EnvironmentalProfile.

Get the session.

Store the environmental problem.

Store supplied variables.

Check missing variables.

Return clarification questions if required.

Combine the session profile.

Run the EcoMind pipeline.

Retrieve scientific evidence.

Run environmental reasoning.

Attach quantitative evidence.

Return the final analysis.

17. Frontend

Files:

frontend/index.html
frontend/style.css
frontend/app.js

Technology:

HTML

CSS

JavaScript

The UI accepts:

Environmental problem

Region

Latitude

Longitude

Soil pH

Soil organic carbon

Soil moisture

Temperature

Rainfall

Species richness

Habitat diversity

Land use

Pollution

Deforestation

The frontend sends the data to:

http://127.0.0.1:8000/environment/analyze

and displays:

Clarifying questions

Recommendation

Reasoning

Impacted metrics

Time horizon

Confidence

Measurement plan

Quantitative evidence

Retrieved scientific evidence

Scientific source information

18. Project Structure

EcoMind/
|
+-- backend/
|   +-- app/
|       +-- api/
|       |   +-- environment.py
|       +-- core/
|       +-- models/
|       +-- schemas/
|       |   +-- environment.py
|       +-- services/
|       +-- main.py
|
+-- knowledge/
|   +-- sources/
|   |   +-- FAO_Soil_Biodiversity.pdf
|   |   +-- IPCC_AR6_Chapter_2.pdf
|   |   +-- IPCC_AR6_Chapter_4.pdf
|   |
|   +-- extracted/
|
+-- rag/
|   +-- embedder.py
|   +-- vector_store.py
|   +-- retriever.py
|   +-- chunker.py
|   +-- pdf_loader.py
|   +-- document_loader.py
|   +-- reasoning.py
|   +-- pipeline.py
|   +-- clarifier.py
|   +-- conversation.py
|
+-- data/
|   +-- environment.index
|   +-- environment_metadata.json
|   +-- quantitative_evidence.json
|   +-- sources.json
|
+-- frontend/
|   +-- index.html
|   +-- style.css
|   +-- app.js
|
+-- tests/
|
+-- requirements.txt
+-- .gitignore
+-- README.md

19. Technology Stack

Backend

Python

FastAPI

Pydantic

Uvicorn

AI / RAG

Sentence Transformers

all-MiniLM-L6-v2

FAISS

NumPy

Scientific Processing

pypdf

JSON

Custom text chunking

Frontend

HTML

CSS

JavaScript

Development

VS Code

Git

GitHub

20. COMPLETE LOCAL STARTUP GUIDE — WINDOWS

This is the normal way to start EcoMind.

Step 1 — Open the project

Open:

D:\EcoMind

in VS Code.

Open:

Terminal -> New Terminal

Expected:

PS D:\EcoMind>

Step 2 — Activate the virtual environment

venv\Scriptsctivate

Expected:

(venv) PS D:\EcoMind>

Step 3 — Install dependencies

For the first setup:

pip install -r requirements.txt

If everything is already installed, this can be skipped.

Step 4 — Start the backend

uvicorn backend.app.main:app --reload

Expected:

Uvicorn running on http://127.0.0.1:8000

Keep this terminal open.

Step 5 — Check the backend

Open:

http://127.0.0.1:8000/health

Expected:

{
  "status": "healthy"
}

Step 6 — Open API documentation

Open:

http://127.0.0.1:8000/docs

You can test /environment/analyze from Swagger.

Step 7 — Start the frontend

Keep the backend terminal running.

Open:

frontend/index.html

using VS Code Live Server.

The browser application will communicate with the FastAPI backend.

21. Quick Start — Copy/Paste

If the project is already configured:

cd D:\EcoMind
venv\Scriptsctivate
uvicorn backend.app.main:app --reload

Then open:

http://127.0.0.1:8000/health

Then:

http://127.0.0.1:8000/docs

Then open:

frontend/index.html

with Live Server.

22. API Test Example

Request:

POST /environment/analyze

Example:

{
  "session_id": "demo-001",
  "message": "Biodiversity is declining on my farm",
  "region": "Ballari, Karnataka",
  "soil_ph": 6.8,
  "soil_organic_carbon": 0.8,
  "soil_moisture": 20,
  "temperature": 30,
  "rainfall": 500,
  "species_richness": 12,
  "habitat_diversity": 2,
  "land_use": "monoculture",
  "pollution": "low",
  "deforestation": "medium"
}

Expected completed response contains:

analysis status

session ID

environmental problem

environmental profile

recommendations

reasoning

impacted metrics

time horizon

confidence

measurement plan

quantitative evidence

retrieved scientific evidence

23. Recommended Demo Test

Use a profile such as:

Soil Organic Carbon: 0.8%
Soil Moisture: 20%
Rainfall: 500 mm
Land Use: monoculture
Species Richness: 12
Habitat Diversity: 2
Temperature: 30°C
Soil pH: 6.8
Pollution: low
Deforestation: medium

This demonstrates multi-variable reasoning.

The system should retrieve scientific evidence and show the relationship between environmental variables and recommendations.

24. Conversational Demo

For the hackathon video:

Message 1

Biodiversity is declining on my land.

The system asks for missing information.

Message 2

My soil organic carbon is 0.8%.

Message 3

My soil moisture is 20%.

Message 4

Annual rainfall is 500 mm.

Message 5

It is a monoculture farm.

Message 6

Species richness is 12 and habitat diversity is 2.

The system combines the information and performs the analysis.

25. What to Show in the Demo Video

Recommended sequence:

1. Open EcoMind
2. Enter environmental problem
3. Show structured environmental inputs
4. Submit
5. Show clarification questions
6. Provide missing values
7. Generate analysis
8. Show recommendation
9. Show multi-variable reasoning
10. Show impacted metrics
11. Show time horizon
12. Show quantitative evidence
13. Show retrieved scientific evidence
14. Show scientific source
15. Show measurement plan
16. Briefly explain the RAG architecture

26. Scientific Grounding

A central feature of EcoMind is that recommendations are connected to retrieved scientific evidence.

The intended flow is:

Recommendation
      |
      v
Reasoning
      |
      v
Impacted Metrics
      |
      v
Quantitative Evidence
      |
      v
Scientific Source
      |
      v
Retrieved Evidence

This allows a judge/user to inspect why a recommendation was produced.

27. Deployment

The project can be deployed as:

GitHub
   |
   +------------------+
   |                  |
   v                  v
Frontend             Backend
Static Host          Render
   |                  |
   +--------+---------+
            |
            v
        EcoMind API
            |
            v
       RAG + FAISS
            |
            v
    Scientific Knowledge

Backend start command on a platform providing $PORT:

uvicorn backend.app.main:app --host 0.0.0.0 --port $PORT

If deployed, the API URL in:

frontend/app.js

must be changed from the local URL to the deployed backend URL.

28. GitHub Repository

Repository:

https://github.com/MYTHILI05896/EcoMind-Scientific-RAG-Based-Biodiversity-Intelligence-Assistant.git

29. Hackathon Requirement Alignment

Requirement

EcoMind Implementation

Scientific knowledge system

FAO + IPCC reports

RAG

Sentence Transformers + FAISS

Environmental understanding

Soil, climate, biodiversity, land and human-impact variables

Clarifying questions

rag/clarifier.py

Multi-turn interaction

rag/conversation.py

Multi-metric reasoning

rag/reasoning.py

Scientific grounding

Retrieved scientific document chunks

Quantitative evidence

data/quantitative_evidence.json

Structured JSON input

Pydantic environmental profile

Actionable recommendations

Environmental reasoning engine

Measurement plan

Recommendation monitoring plan

API

FastAPI

Frontend

HTML/CSS/JavaScript

30. Known Limitations

This is a hackathon prototype.

Known limitations:

Conversation memory is currently in-memory.

Rule thresholds are prototype decision thresholds.

Confidence scores are heuristic indicators, not calibrated probabilities.

Quantitative research values are not site-specific predictions.

Latitude/longitude are accepted by the schema but advanced GIS analysis is not currently implemented.

The scientific knowledge base can be expanded.

Recommendations should be interpreted according to local environmental conditions.

31. Future Improvements

Potential improvements:

Persistent conversation database

GIS integration

Satellite imagery

Region-specific biodiversity datasets

Real-time climate/weather data

Larger scientific knowledge base

Automated citation verification

More biodiversity indicators

Knowledge graphs

Advanced probabilistic reasoning

Region-specific ecological models

Production authentication

Automated CI/CD

Cloud deployment

32. Troubleshooting

uvicorn not recognized

Activate the virtual environment:

venv\Scriptsctivate

Then:

pip install -r requirements.txt

Port 8000 already in use

Run:

uvicorn backend.app.main:app --reload --port 8001

Then change the API URL in frontend/app.js to port 8001.

Missing Python package

Run:

pip install -r requirements.txt

If a specific package is missing, install it and update requirements.txt.

Frontend cannot connect to backend

Check that:

http://127.0.0.1:8000/health

works first.

Then verify the API URL in:

frontend/app.js

33. Project Summary

EcoMind is a scientific RAG-based biodiversity intelligence assistant that combines:

Environmental Data
       +
Conversational Context
       +
Scientific Knowledge Retrieval
       +
FAISS Vector Search
       +
Multi-Variable Reasoning
       +
Quantitative Evidence
       +
Measurement Planning
       =
Biodiversity Intelligence

The system is designed to move from raw environmental information to evidence-grounded biodiversity recommendations.

34. One-Line Description

EcoMind is a scientific RAG-based biodiversity intelligence assistant that combines structured environmental data, conversational context, scientific evidence retrieval, and multi-variable reasoning to generate actionable biodiversity recommendations.
