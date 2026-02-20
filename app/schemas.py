from pydantic import BaseModel, Field
from typing import List, Dict, Optional

class PredictRequest(BaseModel):
    text: Optional[str] = Field(default=None, description="Single input text")
    texts: Optional[List[str]] = Field(default=None, description="Batch input texts (preferred)")
    return_all_scores: bool = Field(default=True, description="Return all label probabilities")

    def normalized_texts(self) -> List[str]:
        if self.texts is not None:
            return self.texts
        if self.text is not None:
            return [self.text]
        return []

class Prediction(BaseModel):
    text: str
    top_label: str
    top_score: float
    scores: Dict[str, float]

class PredictResponse(BaseModel):
    model_id: str
    model_version: str
    predictions: List[Prediction]

class VersionResponse(BaseModel):
    service: str
    service_version: str
    model_id: str
    model_version: str
    environment: str
