import json

DOCKERFILE = open("Dockerfile").read()
MANIFEST = json.load(open("deployment.json"))


def review(dockerfile_text, manifest):
    return []


print(review(DOCKERFILE, MANIFEST))
