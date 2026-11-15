import math, random, struct

W, H = 1920, 1080
random.seed(42)

def gen_y(x, y):
    base = 128 + 80 * math.sin(x / 90.0) * math.cos(y / 70.0)
    edge = 60 if (x // 240 + y // 270) % 2 == 0 else -20
    noise = random.gauss(0, 6)
    return min(255, max(0, base + edge + noise))

def gen_c(x, y):
    return min(255, max(0, 128 + 60 * math.sin((x + y) / 120.0) + random.gauss(0, 3)))

with open("bench/test_1080p.y4m", "wb") as f:
    f.write(b"YUV4MPEG2 W%d H%d F30:1 Ip A1:1 C420jpeg\nFRAME\n" % (W, H))
    f.write(bytes(int(gen_y(x, y)) for y in range(H) for x in range(W)))
    f.write(bytes(int(gen_c(x, y)) for y in range(H // 2) for x in range(W // 2)))
    f.write(bytes(int(gen_c(x, y)) for y in range(H // 2) for x in range(W // 2)))
print("done")
