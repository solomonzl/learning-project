import numpy as np

B, PW50, L = 10.0, 20.0, 10          # nm, nm, taps each side
bits = np.array([1, 0, 1, 1, 0, 0, 1, 0, 1, 1])   # example bit sequence
def signed_transitions(bits):
    d = np.zeros(len(bits))
    k = 0
    for j, b in enumerate(bits):
        if b:
            d[j] = (-1)**k
            k += 1
    return d

n = np.arange(-L, L+1)
h = 1 / (1 + (2*n*B/PW50)**2)        # [.0099 ... .1 .2 .5 1 .5 .2 .1 ... .0099]

d = signed_transitions(bits)
V = np.convolve(d, h, mode='same')   # one sample per bit, 2 GSa/s

import matplotlib.pyplot as plt

INK = "#0b0b0b"
MUTED = "#898781"
GRID = "#e1e0d9"
BLUE = "#2a78d6"    # readback voltage V
GREEN = "#008300"   # signed transitions d

fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(9, 8), facecolor="#fcfcfb")

ax1.plot(n, h, color=BLUE, linewidth=2)
ax1.set_title("Lorentzian pulse response", color=INK, loc="left")
ax1.set_xlabel("n (taps)", color=MUTED)
ax1.set_ylabel("h(n)", color=MUTED)

bit_idx = np.arange(len(bits))
ax2.axhline(0, color=GRID, linewidth=1, zorder=0)
markerline, stemlines, baseline = ax2.stem(bit_idx, d, linefmt=GREEN, markerfmt="o", basefmt=" ")
plt.setp(markerline, color=GREEN, markersize=6)
plt.setp(stemlines, color=GREEN, linewidth=2)
ax2.set_title("Signed transitions (d)", color=INK, loc="left")
ax2.set_xlabel("bit index", color=MUTED)
ax2.set_ylabel("amplitude", color=MUTED)

# NB: len(V) != len(bits) whenever h is longer than d (mode='same' pads to the
# longer input), so V gets its own sample-index axis rather than bit_idx.
v_idx = np.arange(len(V))
ax3.axhline(0, color=GRID, linewidth=1, zorder=0)
ax3.plot(v_idx, V, color=BLUE, linewidth=2, marker="o", markersize=4)
ax3.set_title("Readback voltage (V)", color=INK, loc="left")
ax3.set_xlabel("sample index", color=MUTED)
ax3.set_ylabel("amplitude", color=MUTED)

for ax in (ax1, ax2, ax3):
    ax.set_facecolor("#fcfcfb")
    ax.grid(True, color=GRID, linewidth=1)
    ax.tick_params(colors=MUTED)
    for spine in ax.spines.values():
        spine.set_color(GRID)

fig.tight_layout()
plt.show()