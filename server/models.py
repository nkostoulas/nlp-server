from pydantic import BaseModel, field_validator
from transformers import pipeline

_BLANK_PLACEHOLDER = "<blank>"

# Load pre-trained fill-mask model for sentence preditions
unmasker = pipeline("fill-mask", model="bert-large-uncased")

# Load pre-trained sentiment-analysis model for analyzing sentences
sentiment_analysis = pipeline("sentiment-analysis")

class SuggestionsRequest(BaseModel):
    sentence: str

    @field_validator('sentence')
    @classmethod
    def sentence_must_contain_placeholder(cls, v: str) -> str:
        if _BLANK_PLACEHOLDER not in v:
            raise ValueError('must contain the %s placeholder' % _BLANK_PLACEHOLDER)
        return v
