#!/usr/bin/env python3
"""Benchmark: libaom vs SVT-AV1 AVIF encoding through libheif.

Usage:  python3 bench/sweep.py [y4m-input]
Requires heif-enc / heif-dec built in ./build (set BUILD_DIR to override).
Prints a rate/distortion/time table and writes bench/results.json.
"""
import subprocess, os, time, sys, json

BUILD = os.environ.get("BUILD_DIR", "build")
P = os.getcwd()
env = dict(os.environ)
env["LD_LIBRARY_PATH"] = f"{P}/{BUILD}/libheif:" + env.get("LD_LIBRARY_PATH", "")
env["LIBHEIF_PLUGIN_PATH"] = f"{P}/{BUILD}/libheif/plugins"
ENC = f"./{BUILD}/examples/heif-enc"
DEC = f"./{BUILD}/examples/heif-dec"
SRC = sys.argv[1] if len(sys.argv) > 1 else "bench/test_1080p.y4m"
OUT = "bench/out"
RUNS = 3
os.makedirs(OUT, exist_ok=True)

def run(cmd):
    r = subprocess.run(cmd, env=env, capture_output=True)
    assert r.returncode == 0, r.stderr.decode()

def bench(name, Q, args):
    out = f"{OUT}/{name}.avif"
    best = 1e9
    for _ in range(RUNS):
        t0 = time.perf_counter()
        run([ENC, "-q", str(Q), "-A", "-o", out, SRC] + args)
        best = min(best, time.perf_counter() - t0)
    run([DEC, "-o", f"{OUT}/{name}.y4m", out])
    p = subprocess.run(["python3", "bench/psnr.py", SRC, f"{OUT}/{name}.y4m"],
                       capture_output=True, text=True).stdout
    psnr = float(p.split("Y=")[1].split("dB")[0])
    sz = os.path.getsize(out)
    print(f"{name:<12} q{Q:<3} time={best:6.2f}s size={sz/1024:8.1f}KB PSNR-Y={psnr:.2f}dB",
          flush=True)
    return (name, Q, round(best, 2), sz, round(psnr, 2))

CONFIGS = [
    ("aom_s2", ["-e", "aom", "-p", "speed=2",  "-p", "threads=16"]),
    ("aom_s4", ["-e", "aom", "-p", "speed=4",  "-p", "threads=16"]),
    ("aom_s6", ["-e", "aom", "-p", "speed=6",  "-p", "threads=16"]),
    ("svt_s4", ["-e", "svt", "-p", "speed=4",  "-p", "threads=16"]),
    ("svt_s6", ["-e", "svt", "-p", "speed=6",  "-p", "threads=16"]),
    ("svt_s8", ["-e", "svt", "-p", "speed=8",  "-p", "threads=16"]),
    ("svt_s12", ["-e", "svt", "-p", "speed=12", "-p", "threads=16"]),
]

results = []
for Q in [50, 70]:
    for name, args in CONFIGS:
        results.append(bench(f"{name}_q{Q}", Q, args))
json.dump(results, open("bench/results.json", "w"), indent=1)
