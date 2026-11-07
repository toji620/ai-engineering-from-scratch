"""Lesson 0.7, Exercise 3: a tiny API served from inside the ai-dev container."""
import platform

import torch
from flask import Flask, jsonify

app = Flask(__name__)


@app.get("/")
def info():
    return jsonify(
        message="Hello from inside a Docker container",
        torch=torch.__version__,
        cuda_available=torch.cuda.is_available(),
        machine=platform.machine(),
    )


if __name__ == "__main__":
    # 0.0.0.0 = listen on every interface, so -p 5000:5000 can reach it.
    # 127.0.0.1 would only accept connections from inside this container.
    app.run(host="0.0.0.0", port=5000)
