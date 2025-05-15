from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional

@dataclass
class Persona:
    id: Optional[int] = None
    name: str = ""
    role: str = ""
    age: Optional[int] = None
    gender: str = ""
    location: str = ""
    education: str = ""
    income_level: str = ""
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

@dataclass
class Goal:
    id: Optional[int] = None
    persona_id: Optional[int] = None
    description: str = ""
    priority: int = 1

@dataclass
class PainPoint:
    id: Optional[int] = None
    persona_id: Optional[int] = None
    description: str = ""
    severity: int = 1

@dataclass
class Behavior:
    id: Optional[int] = None
    persona_id: Optional[int] = None
    description: str = ""
    frequency: str = ""

@dataclass
class Quote:
    id: Optional[int] = None
    persona_id: Optional[int] = None
    quote_text: str = ""
    context: str = ""

@dataclass
class Scenario:
    id: Optional[int] = None
    persona_id: Optional[int] = None
    title: str = ""
    description: str = ""
    steps: str = ""

    