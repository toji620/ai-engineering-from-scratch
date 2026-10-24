# Lesson 0.3 results: GPU Setup & Cloud

Machine: Apple M5 Pro (16-core GPU), 24 GB unified memory, PyTorch 2.14.1

## Lesson's gpu_check.py
`CUDA available: False`. There's no NVIDIA GPU, and `nvidia-smi` isn't installed (expected on a Mac).

## Exercise 1: CPU vs MPS benchmark (5000x5000 matmul, `benchmark.py`)
| Run | CPU | MPS | Speedup |
|-----|-----|-----|---------|
| 1 (includes warm-up) | 0.177 s | 0.216 s | 0.8x |
| 2 | 0.153 s | 0.055 s | 2.8x |

The CPU reached about 1.6 TFLOP/s and the GPU about 4.5 TFLOP/s (2 × 5000³ ≈ 2.5e11 FLOPs per matmul).

## Exercise 2: Google Colab T4
`nvidia-smi`: Tesla T4, 15360 MiB VRAM, CUDA 13.0, driver 580.82.07. PyTorch reports 15.6 GB.

| Run | Colab CPU | T4 GPU | Speedup |
|-----|-----------|--------|---------|
| 1 (includes warm-up) | 2.147 s | 0.190 s | 11x |
| 2 | 2.034 s | 0.088 s | 23x |

The big speedup is mostly down to Colab's weak free-tier CPU, which was 13x slower than the M5 Pro CPU.
In fp32 the M5 Pro GPU (0.055 s) beat the T4 (0.088 s). The T4's Tensor Cores only help in fp16.
T4 fit estimate: 15.6 GB / 2 ≈ 7.8B params in fp16 with no margin, so about 5-6B in practice.

## Exercise 3: largest model that fits
- `torch.mps.recommended_max_memory()` = 19.1 GB usable by the GPU
- fp16 at 2 bytes/param: 19.1 GB / 2 ≈ 9.5B params with no margin, so about 7B in practice after a ~25% margin
- fp32 at 4 bytes/param: about 4.8B params with no margin
