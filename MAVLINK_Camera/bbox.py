import json
from dataclasses import dataclass
from typing import List

@dataclass
class BBox:
    latitude: float
    longitude: float 
    radius: float
    confidence: float

    def __init__(self, latitude: float, longitude: float, radius: float, confidence: float):
        self.latitude = latitude
        self.longitude = longitude 
        self.radius = radius
        self.confidence = confidence
        
    @classmethod
    def from_json(cls, string: str):
        data: dict = json.loads(string)
        return cls(**data)

    def json(self):
        return json.dumps(self, default=lambda o: o.__dict__)

@dataclass
class BBoxes:
    bboxes: List[BBox]