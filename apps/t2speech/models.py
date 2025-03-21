from dataclasses import dataclass
from typing import Optional, List, Set

@dataclass(frozen=True)
class FilterModelAI:
    name: Optional[str] = None
    category: Optional[str] = None
    language: Optional[str] = None
    isStandard: Optional[bool] = None
    gender: Optional[str] = None
    dialect: Optional[str] = None
    Type: Optional[str] = None

@dataclass(frozen=True)
class ModelAiCreate:
    name: str
    AbsolutePath:str
    category: Optional[str] = None
    language: Optional[str] = None
    isStandard: Optional[bool] = None
    gender: Optional[str] = None
    dialect: Optional[str] = None
    Type: Optional[str] = None
