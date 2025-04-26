import matplotlib.pyplot as plt
import time

SIM_FILE = "simtrace.txt"
num_blocks = 8  # Adjust based on your simulation settings
cache_state = [0] * num_blocks
bar_colors = ['red'] * num_blocks

plt.ion()
fig, ax = plt.subplots()
bars = ax.bar(range(num_blocks), cache_state, color=bar_colors)

ax.set_ylim(0, 1.5)
ax.set_xlabel('Cache Block Index')
ax.set_ylabel('Occupied (1 = yes)')
ax.set_title('Cache Visualization')


def update_plot(current_hit_rate):
    ax.set_title(f'Cache Visualization (Hit Rate: {current_hit_rate:.2f}%)')
    for i in range(num_blocks):
        bars[i].set_height(cache_state[i])
        if cache_state[i] == 1:
            bars[i].set_color('green')
        else:
            bars[i].set_color('red')
    fig.canvas.draw()
    fig.canvas.flush_events()


def run_from_trace():
    hits = 0
    misses = 0
    total = 0

    try:
        with open(SIM_FILE, 'r') as f:
            lines = f.readlines()
    except FileNotFoundError:
        print(f"Error: {SIM_FILE} not found. Make sure your simulation wrote to it.")
        return

    for line in lines:
        if line.startswith("#") or not line.strip():
            continue

        parts = line.strip().split()
        if len(parts) != 3:
            continue

        index = int(parts[0])
        tag = parts[1]
        hit = parts[2] == 'Hit'

        if cache_state[index] == 1 and not hit:
            # Flash evicted block red if miss after being filled
            bars[index].set_color('red')
            fig.canvas.draw()
            fig.canvas.flush_events()
            time.sleep(0.3)

        cache_state[index] = 1
        total += 1
        if hit:
            hits += 1

        current_hit_rate = (hits / total) * 100
        update_plot(current_hit_rate)
        time.sleep(0.5)

    plt.ioff()
    plt.show()


run_from_trace()
