# Lesson 0.7 results: Docker for AI

Host: Apple M5 Pro (arm64). Docker Desktop 29.6.1 runs a Linux VM (aarch64, 15 CPUs, 8.3 GB RAM).
The course image pins `--platform=linux/amd64`, so it runs under x86_64 emulation with no GPU. Step 2, the NVIDIA Container Toolkit, was skipped because it is Linux and NVIDIA only.

## Exercise 1: build and check PyTorch
`docker build -t ai-dev` took 5 min 50 s. The build context was 2 B, because the Dockerfile has no COPY.
Layer times: base 64 s, apt 46 s, torch 101 s, libraries 32 s, export 100 s. Image size: 21.5 GB.
Output: `PyTorch 2.6.0+cu124 | CUDA build 12.4 | CUDA available: False | machine x86_64 | Python 3.12.16`

## Exercise 3: add flask, rebuild, serve an API
- The first try failed: `Cannot uninstall blinker 1.4`, a distutils package that apt installed in layer 2.
  The fix was `pip install --ignore-installed blinker flask`, an apt/pip clash much like mixing pip into conda.
- The rebuild took 2.7 s with 6 layers CACHED. Only the flask layer ran.
- Port 5000 on the Mac is taken by macOS AirPlay Receiver (ControlCenter), so I used `-p 5050:5000` (host:container).
- `curl localhost:5050` returned `{"cuda_available":false,"machine":"x86_64","message":"Hello from inside a Docker container","torch":"2.6.0+cu124"}`

## Exercise 2: Compose with Qdrant
`docker-compose.yml` here is the course file with the NVIDIA deploy block removed, for the Mac.
From inside ai-dev, `curl http://qdrant:6333/collections` returned `{"result":{"collections":[]},"status":"ok"}`.
The service name `qdrant` resolved to 172.18.0.3 on the Compose network.
`docker compose down` kept the `qdrant_data` volume. `docker compose down -v` deleted it.

## Exercise 4: devel vs runtime base
| Image | Base | Size | nvcc |
|---|---|---|---|
| ai-dev | devel | 21.5 GB | yes |
| ai-dev-runtime | runtime | 14.3 GB | no |

The runtime base is 7.2 GB smaller and still runs PyTorch 2.6.0+cu124. Changing FROM rebuilt every layer (0 cached, 5 min 9 s).
All three images use 33 GB on disk in total, because they share layers.
