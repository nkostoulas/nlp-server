
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

Create an auth token file containing an auth token under `secrets/token`.

Build the docker image:
```bash
docker build -t nlp-server .
```

Run the image that hosts the server at 8001:
```bash
docker run -d -p 8001:8001 nlp-server
```

#### Kubernetes

Prerequisites:
- kubernetes

The kubernetes resources under `k8s/` used a pre-built image (as above) pushed to Docker Hub.

Create kubernetes namespace:
```bash
kubectl create namespace mlops
```

Apply kubernetes resources:
```bash
kubernetes apply -f k8s/
```

### Testing

#### cURL

Example requests can be sent to the NLP server running locally using the following command:
```bash
curl -X POST "http://127.0.0.1:8001/suggestions/" \
-H "Content-Type: application/json" \
-H "Authorization: Bearer <token>" \
-d '{"sentence": "The weather today is <blank>."}'
```

If testing the kubernetes setup with minikube you can get the minikube ip address with:
```bash
minikube ip
```

and send the same curl command as follows:
```bash
curl -X POST "http://<minikube-ip>:31000/suggestions/" \
-H "Content-Type: application/json" \
-H "Authorization: Bearer <token>" \
-d '{"sentence": "The weather today is <blank>."}'
```

### Documentation

Docs for the API are available directly from the server at the `/docs` path.

Locally or with docker these can be found at `127.0.0.1:8001/docs`.

For minikube these docs are accessible at `<minikube-ip>:31000/docs`.
