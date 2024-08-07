
## Simple NLP server

This is a simple Python server that offers an NLP API for text completion that is based on pre-trained models.

### Running the server

#### Locally

Prerequisites:
- python3
- pip

Create a local virtual environment and activate:

```bash
python3 -m venv env
source env/bin/activate
```

Install the required dependencies:
```bash
pip install -r requirements.txt
```

Create an auth token file containing an auth token under `secrets/token`.

Run the application:
```bash
python3 main.py
```

#### Docker

Prerequisites:
- docker

Build the docker image:
```bash
docker build -t nlp-server .
```

Run the image that hosts the server at 8000:
```bash
docker run -d -p 8000:8000 nlp-server
```

#### Kubernetes

Prerequisites:
- docker
- kubernetes

Build the docker image:
```bash
docker build -t nlp-server .
```

Apply kubernetes resources:
```bash
kubernetes apply -f k8s/
```

### Testing

#### cURL

Example requests can be set to the NLP server running locally using the following command:
```bash
curl -X POST "http://127.0.0.1:8000/suggestions/" \
-H "Content-Type: application/json" \
-H "Authorization: Bearer <token>" \
-d '{"sentence": "The weather today is <blank>."}'
```
