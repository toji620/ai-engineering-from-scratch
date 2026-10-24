"""CPU vs GPU matrix-multiply benchmark (Lesson 0.3, adapted for CUDA, MPS or CPU)."""
import time

import torch

if torch.cuda.is_available():
    device = "cuda"
elif torch.backends.mps.is_available():
    device = "mps"
else:
    device = "cpu"


def sync():
    """Wait until the GPU has really finished, so the timer measures the work."""
    if device == "cuda":
        torch.cuda.synchronize()
    elif device == "mps":
        torch.mps.synchronize()


size = 5000
print(f"Device: {device} | matrices: {size}x{size}\n")

a_cpu = torch.randn(size, size)
b_cpu = torch.randn(size, size)
a_gpu = a_cpu.to(device)
b_gpu = b_cpu.to(device)

for run in (1, 2):
    start = time.time()
    _ = a_cpu @ b_cpu
    cpu_time = time.time() - start

    sync()
    start = time.time()
    _ = a_gpu @ b_gpu
    sync()
    gpu_time = time.time() - start

    print(f"Run {run}: CPU {cpu_time:.3f}s | {device.upper()} {gpu_time:.3f}s | speedup {cpu_time / gpu_time:.1f}x")
