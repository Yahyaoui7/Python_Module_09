from datetime import datetime
from enum import Enum
from typing import List

from pydantic import BaseModel, Field, model_validator


class Rank(Enum):
    cadet = "cadet"
    officer = "officer"
    lieutenant = "lieutenant"
    captain = "captain"
    commander = "commander"


class CrewMember(BaseModel):
    member_id: str = Field(min_length=3, max_length=10)
    name: str = Field(min_length=2, max_length=50)
    rank: Rank
    age: int = Field(ge=18, le=80)
    specialization: str = Field(min_length=3, max_length=30)
    years_experience: int = Field(ge=0, le=50)
    is_active: bool = True


class SpaceMission(BaseModel):
    mission_id: str = Field(min_length=5, max_length=15)
    mission_name: str = Field(min_length=3, max_length=100)
    destination: str = Field(min_length=3, max_length=50)
    launch_date: datetime
    duration_days: int = Field(ge=1, le=3650)

    crew: List[CrewMember] = Field(min_length=1, max_length=12)

    mission_status: str = "planned"
    budget_millions: float = Field(ge=1.0, le=10000.0)

    @model_validator(mode="after")
    def validate_mission_id(self) -> "SpaceMission":
        if not self.mission_id.startswith("M"):
            raise ValueError("Mission ID must start with 'M'")

        has_leader = any(
            member.rank in (Rank.captain, Rank.commander)
            for member in self.crew
        )
        if not has_leader:
            raise ValueError(
                "Mission must have at least one Captain or Commander"
                )
        experienced_count = 0
        if self.duration_days > 365:
            experienced_count = sum(
                1 for member in self.crew if member.years_experience >= 5
            )
            if experienced_count < len(self.crew) / 2:
                msg = "Long missions require at "
                msg1 = "least 50% experienced crew (5+ years)"
                raise ValueError(msg+msg1)

        if any(not member.is_active for member in self.crew):
            raise ValueError("All crew members must be active")

        return self


""" Valid mission (with leader)"""


crew_with_leader = [
    CrewMember(
        member_id="C03",
        name="Sarah Connor",
        rank=Rank.commander,
        age=45,
        specialization="mission command",
        years_experience=20,
        is_active=True,
    ),
    CrewMember(
        member_id="C04",
        name="John Smith",
        rank=Rank.officer,
        age=29,
        specialization="engineering",
        years_experience=29,
        is_active=True,
    ),
]


"""Invalid mission (no leader) """

crew_no_leader = [
    CrewMember(
        member_id="C01",
        name="Alice",
        rank=Rank.officer,
        age=30,
        specialization="engineering",
        years_experience=6,
        is_active=True,
    ),
    CrewMember(
        member_id="C02",
        name="Bob",
        rank=Rank.lieutenant,
        age=35,
        specialization="navigation",
        years_experience=10,
        is_active=True,
    ),
]


def print_contact(m: SpaceMission):
    print(f"Mission: {m.mission_name}")
    print(f"ID: {m.mission_id}")
    print(f"Destination: {m.destination}")
    print(f"Duration: {m.duration_days} days")
    print(f"Budget: ${m.budget_millions}M")
    print(f"Crew size: {len(m.crew)}")
    print("Crew members:")
    for member in m.crew:
        print(
            f"- {member.name} "
            f"({member.rank.value}) "
            f"- {member.specialization}"
        )


def main():
    print("Space Mission Crew Validation")
    print("=" * 40)
    print("Valid mission created:")

    try:
        mission = SpaceMission(
            mission_id="M2026_OK",
            mission_name="Mars Exploration Mission",
            destination="Mars",
            launch_date=datetime.now(),
            duration_days=900,
            crew=crew_with_leader,
            budget_millions=2500.0,
        )
        print_contact(mission)
    except ValueError as e:
        print("Expected validation error:")
        print(e.errors()[0]["msg"])

    print("\n" + ("=" * 40))
    try:
        SpaceMission(
            mission_id="M2026_ERR",
            mission_name="Test Mission Without Leader",
            destination="Mars",
            launch_date=datetime.now(),
            duration_days=120,
            crew=crew_no_leader,
            budget_millions=800.0,
        )
    except ValueError as e:
        print("Expected validation error:")
        print(e.errors()[0]["msg"])


if __name__ == "__main__":
    main()
