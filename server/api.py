from functools import lru_cache
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel, field_validator
from transformers import pipeline

from server.auth import get_auth_token
from server.models import SuggestionsRequest, _BLANK_PLACEHOLDER, unmasker, sentiment_analysis

_MAX_SAMPLING = 20
_MAX_SUGGESTIONS = 5

# Setup API
app = FastAPI()

@app.post("/suggestions/")
def get_suggestions(request: SuggestionsRequest, token: str = Depends(get_auth_token)):
    suggestions = cached_suggestions(request.sentence)
    return {"suggestions": ", ".join(suggestions)}

@lru_cache(maxsize=32)
def cached_suggestions(sentence: str):
    # Replace _BLANK_PLACEHOLDER with the fill-mask token and get predictions
    masked_input = sentence.replace(_BLANK_PLACEHOLDER, unmasker.tokenizer.mask_token)
    predictions = unmasker(masked_input, top_k=_MAX_SAMPLING)

    # Run sentiment analysis on the suggestions and filter out non-positive ones
    suggestions = []
    for pred in predictions:
        suggestion = pred["token_str"]
        sentiment = sentiment_analysis(pred["sequence"])
        if len(sentiment) < 1:
            continue
        if sentiment[0]['label'] == 'POSITIVE':
            suggestions.append(suggestion)
            if len(suggestions) == _MAX_SUGGESTIONS:
                break
    return suggestions
