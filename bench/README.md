# AV1 encoder benchmark (libaom vs SVT-AV1)

Reproduces the performance table in the "Performance: SVT-AV1 vs libaom"
section of the top-level README.md.

## Usage

1. Build libheif with both encoders enabled:

   ```
   cmake -B build -DWITH_AOM_ENCODER=ON -DWITH_SvtEnc=ON -DWITH_EXAMPLES=ON
   cmake --build build
   ```

2. Generate the 1080p test image (Y4M) and run the sweep:

   ```
   python3 bench/gen_y4m.py
   python3 bench/sweep.py            # or: python3 bench/sweep.py your-own.y4m
   ```

The sweep encodes the test image with libaom (speed 2/4/6) and SVT-AV1
(presets 4/6/8/12) at quality 50 and 70, measures wall-clock time
(best of 3 runs), output size, and PSNR-Y of the decoded result against
the source. Results are printed as a table and stored in
`bench/results.json`.

If your build directory is not `./build`, set `BUILD_DIR`. If the codec
backends are compiled as dynamic plugins, make sure
`LIBHEIF_PLUGIN_PATH` / `LD_LIBRARY_PATH` point at them (the script
pre-pends the default in-tree locations).

## Files

- `gen_y4m.py` — generates a synthetic 1920x1080 Y4M test frame
  (gradients, edges, noise) without external dependencies.
- `sweep.py` — benchmark driver (encode/decode/PSNR matrix).
- `psnr.py` — PSNR computation between two Y4M files (Y/U/V planes).
