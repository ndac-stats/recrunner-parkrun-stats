from dataclasses import dataclass
from datetime import date
from typing import Any


type ParkrunID = str
type ParkrunnerResultHistory = list[ParkrunResult]

@dataclass
class Parkrunner:
    parkrun_id: ParkrunID
    first_name: str
    last_name: str
    display_name: str
    parkrun_join_date: date
    active: bool

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Parkrunner":
        """Create a Parkrunner instance from a dictionary."""

        data = data.copy()

        # Convert ISO date string to date object
        if isinstance(data["parkrun_join_date"], str):
            data["parkrun_join_date"] = date.fromisoformat(
                data["parkrun_join_date"]
            )

        return cls(**data)

    def to_dict(self) -> dict:
        return {
            "parkrun_id": self.parkrun_id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "display_name": self.display_name,
            "parkrun_join_date": self.parkrun_join_date.isoformat(),
            "active": self.active
        }


@dataclass
class ParkrunResult:
    parkrun_id: ParkrunID
    event: str
    run_date: date
    run_number: int
    position: int
    time_seconds: int
    age_grade: float
    pb: bool

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "ParkrunResult":
        """Create a ParkrunResult from a dictionary."""

        data = data.copy()

        # Convert date string
        if isinstance(data["run_date"], str):
            data["run_date"] = date.fromisoformat(data["run_date"])

        # Convert time string HH:MM:SS to seconds
        if isinstance(data["time_seconds"], str):
            parts = data["time_seconds"].split(":")
            data["time_seconds"] = (
                int(parts[0]) * 3600
                + int(parts[1]) * 60
                + int(parts[2])
            )

        return cls(**data)

    def to_dict(self) -> dict:
        """Convert result to a JSON-compatible dictionary."""

        return {
            "parkrun_id": self.parkrun_id,
            "event": self.event,
            "run_date": self.run_date.isoformat(),
            "run_number": self.run_number,
            "position": self.position,
            "time_seconds": self.time_seconds,
            "age_grade": self.age_grade,
            "pb": self.pb
        }

    @property
    def formatted_time(self) -> str:
        """Return finish time as HH:MM:SS."""

        hours, remainder = divmod(self.time_seconds, 3600)
        minutes, seconds = divmod(remainder, 60)

        return f"{hours:02}:{minutes:02}:{seconds:02}"
