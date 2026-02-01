
from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field, ValidationError, model_validator


class ContactType(Enum):
    """Allowed alien contact types."""
    radio = "radio"
    visual = "visual"
    physical = "physical"
    telepathic = "telepathic"


class AlienContact(BaseModel):

    contact_id: str = Field(..., min_length=5, max_length=15)
    timestamp: datetime
    location: str = Field(..., min_length=3, max_length=100)
    contact_type: ContactType
    signal_strength: float = Field(..., ge=0.0, le=10.0)
    duration_minutes: int = Field(..., ge=1, le=1440)
    witness_count: int = Field(..., ge=1, le=100)
    message_received: Optional[str] = Field(None, max_length=500)
    is_verified: bool = False

    @model_validator(mode="after")
    def validate_business_rules(self) -> "AlienContact":
        if not self.contact_id.startswith("AC"):
            raise ValueError("Contact ID must start with 'AC' (Alien Contact)")

        if self.contact_type == ContactType.physical and not self.is_verified:
            raise ValueError("Physical contact reports must be verified")

        if self.contact_type == ContactType.telepathic and self.witness_count < 3:
            raise ValueError("Telepathic contact requires at least 3 witnesses")

        if self.signal_strength > 7.0 and not self.message_received:
            raise ValueError(
                "Strong signals (> 7.0) should include a received message"
            )

        return self


def print_contact(c: AlienContact) -> None:
    msg = c.message_received if c.message_received else "(no message)"
    print(f"ID: {c.contact_id}")
    print(f"Type: {c.contact_type.value}")
    print(f"Location: {c.location}")
    print(f"Signal: {c.signal_strength}/10")
    print(f"Duration: {c.duration_minutes} minutes")
    print(f"Witnesses: {c.witness_count}")
    print(f"Message: {msg}")
    print(f"Verified: {c.is_verified}")


def main() -> None:
    print("Alien Contact Log Validation")
    print("======================================")

    # ✅ Valid example
    try:
        valid_contact = AlienContact(
            contact_id="AC_2024_001",
            timestamp="2024-06-01T14:30:00",
            location="Area 51, Nevada",
            contact_type=ContactType.radio,
            signal_strength=8.5,
            duration_minutes=45,
            witness_count=5,
            message_received="Greetings from Zeta Reticuli",
            is_verified=False,
        )
        print("Valid contact report:")
        print_contact(valid_contact)
    except ValidationError as exc:
        print("Unexpected validation error for valid contact:")
        print(exc)

    print("\n======================================")

    try:
        invalid_contact = AlienContact(
            contact_id="AC_2024_002",
            timestamp=datetime.now(),
            location="Desert Outpost",
            contact_type=ContactType.telepathic,
            signal_strength=6.0,
            duration_minutes=10,
            witness_count=1,
            message_received=None,
            is_verified=False,
        )
        print("This should not print (invalid contact created):")
        print_contact(invalid_contact)
    except ValidationError as exc:
        print("Expected validation error:")
        print(exc)


if __name__ == "__main__":
    main()
