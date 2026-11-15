import sys, math

def read_y4m(path):
    data = open(path, "rb").read()
    hdr_end = data.index(b"\n") + 1
    hdr = data[:hdr_end].decode()
    w = int(hdr.split("W")[1].split()[0]); h = int(hdr.split("H")[1].split()[0])
    frame_start = data.index(b"FRAME\n", hdr_end) + 6
    raw = data[frame_start:]
    ysz = w * h; csz = (w // 2) * (h // 2)
    return w, h, raw[:ysz], raw[ysz:ysz+csz], raw[ysz+csz:ysz+2*csz]

def psnr(a, b):
    n = len(a)
    mse = sum((a[i] - b[i]) ** 2 for i in range(0, n, 7)) / (n // 7 + 1)  # sampled for speed
    return 99.0 if mse == 0 else 10 * math.log10(255.0 * 255.0 / mse)

w, h, y1, u1, v1 = read_y4m(sys.argv[1])
_, _, y2, u2, v2 = read_y4m(sys.argv[2])
print(f"PSNR Y={psnr(y1,y2):.2f}dB U={psnr(u1,u2):.2f}dB V={psnr(v1,v2):.2f}dB")
