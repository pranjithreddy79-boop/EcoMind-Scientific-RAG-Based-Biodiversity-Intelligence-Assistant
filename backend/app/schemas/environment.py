from typing import Optional

from pydantic import BaseModel, Field


class EnvironmentalProfile(BaseModel):

    session_id: str = "default"

    message: Optional[str] = None

    region: Optional[str] = None

    latitude: Optional[float] = None

    longitude: Optional[float] = None

    soil_ph: Optional[float] = Field(
        default=None,
        ge=0,
        le=14
    )

    soil_organic_carbon: Optional[float] = Field(
        default=None,
        ge=0
    )

    soil_moisture: Optional[float] = Field(
        default=None,
        ge=0,
        le=100
    )

    land_use: Optional[str] = None

    species_richness: Optional[float] = Field(
        default=None,
        ge=0
    )

    habitat_diversity: Optional[float] = Field(
        default=None,
        ge=0
    )

    temperature: Optional[float] = None

    rainfall: Optional[float] = Field(
        default=None,
        ge=0
    )

    pollution: Optional[str] = None

    deforestation: Optional[str] = None