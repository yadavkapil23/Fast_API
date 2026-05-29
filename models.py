# models.py - How data looks in DATABASE
from dataclasses import dataclass

@dataclass
class User:
    id: int
    name: str
    email: str
