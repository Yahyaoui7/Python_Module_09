from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, ValidationError


class SpaceStation(BaseModel):

    station_id: str = Field(min_length=3, max_length=10)
    name: str = Field(min_length=1, max_length=50)
    crew_size: int = Field(ge=1, le=20)
    power_level: float = Field(ge=0.0, le=100.0)
    oxygen_level: float = Field(ge=0.0, le=100.0)
    last_maintenance: datetime
    is_operational: bool = True
    notes: Optional[str] = Field(default=None, max_length=200)


def print_station(station: SpaceStation) -> None:
    """Display station information in a clear format."""
    status = "Operational" if station.is_operational else "Not operational"

    print("Valid station created:")
    print(f"ID: {station.station_id}")
    print(f"Name: {station.name}")
    print(f"Crew: {station.crew_size} people")
    print(f"Power: {station.power_level}%")
    print(f"Oxygen: {station.oxygen_level}%")
    print(f"Status: {status}")

    if station.notes:
        print(f"Notes: {station.notes}")


def main() -> None:
    """Run a small demo: one valid station + one invalid station."""
    print("Space Station Data Validation")
    print("=" * 40)

    station_ok = SpaceStation(
        station_id="ISS001",
        name="International Space Station",
        crew_size=6,
        power_level=85.5,
        oxygen_level=92.3,
        last_maintenance="2024-02-01T10:30:00",
        is_operational=True,
        notes="All systems nominal.",
    )
    print_station(station_ok)

    print("\n" + "=" * 40)

    try:
        SpaceStation(
            station_id="BAD01",
            name="Too Many Crew Station",
            crew_size=25,
            power_level=80.0,
            oxygen_level=90.0,
            last_maintenance="2024-02-01T10:30:00",
        )
    except ValidationError as exc:
        print("Expected validation error:")

        for err in exc.errors():
            msg = err.get("msg", "Validation error")
            print(msg)


if __name__ == "__main__":
    main()
