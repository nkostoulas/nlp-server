from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, field_validator
from transformers import pipeline

_BLANK_PLACEHOLDER = "<blank>"
_MAX_SUGGESTIONS = 5

app = FastAPI()

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

@app.post("/suggestions/")
def get_suggestions(request: SuggestionsRequest):
    # Replace _BLANK_PLACEHOLDER with the fill-mask token and get predictions
    masked_input = request.sentence.replace(_BLANK_PLACEHOLDER, unmasker.tokenizer.mask_token)
    predictions = unmasker(masked_input, top_k=20)

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

    return {"suggestions": ", ".join(suggestions)}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
