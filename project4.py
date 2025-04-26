import math
import random
from collections import deque
import subprocess

cache = {}
access_table = []
lru_tracker = {}  # For LRU replacement tracking

nominal = int(input("Please enter the nominal size : "))
words_per_block = int(input("Enter the amount of words per block: "))
bytes_per_block = 4 * words_per_block
blockNum = int(nominal / bytes_per_block)

print("The number of blocks is: ", blockNum)

policy = input("Please enter the mapping policy (DM or set associative): ").upper()
replacement_policy = 'LRU' if policy == 'SET ASSOCIATIVE' else 'FIFO'

if policy == "SET ASSOCIATIVE":
    numSets = int(input("Enter the number of sets: "))
    print("The number of sets is: ", blockNum / numSets)

    offset = int(math.log2(bytes_per_block))
    index = int(math.log2(blockNum / numSets))
    tag = int(32 - (index + offset))

    print("The offset is: ", offset)
    print("The index is: ", index)
    print("The tag is: ", tag)

    real = nominal + blockNum * ((tag + offset)/8)
    print("The real size is: ", real)

elif policy == "DM":
    offset = int(math.log2(bytes_per_block))
    index = int(math.log2(blockNum))
    tag = int(32 - (index + offset))

    print("The offset is: ", offset)
    print("The index is: ", index)
    print("The tag is: ", tag)

    real = nominal + blockNum * ((tag + offset)/8)
    print("The real size is: ", real)

offset_bits = offset
index_bits = index
tag_bits = tag

def get_binary_parts(address, index_bits, offset_bits):
    bin_addr = bin(address)[2:].zfill(32)
    tag = bin_addr[:32 - (index_bits + offset_bits)]
    index = bin_addr[32 - (index_bits + offset_bits):32 - offset_bits]
    offset = bin_addr[32 - offset_bits:]
    return tag, index, offset

def simulate_mode(num_addresses=20):
    """
    Simulation Mode:
    Step 4 requirement:
    - Generate a series of memory accesses
    - Track hits and misses
    - Fill and update the cache according to the policy (DM or Set Associative)
    Extra Credit:
    - Support random, locality, and manual address patterns
    - Write access trace to simtrace.txt for graphical visualization
    - Implement LRU replacement policy for set associative caches
    - Automatically launch cache population visualization
    """

    print(f"\nChoose simulation mode:")
    choice = input("Enter 'random', 'locality', or 'manual': ").lower()

    # Clear previous simulation data
    cache.clear()
    access_table.clear()
    lru_tracker.clear()

    trace_file = open("simtrace.txt", "w")  # Prepare trace log file for visualization

    hits = 0
    misses = 0
    addresses = []

    # Generate addresses depending on mode (random, locality, manual)
    if choice == 'random':
        addresses = [random.randint(0, (blockNum * words_per_block) - 1) for _ in range(num_addresses)]
    elif choice == 'locality':
        base = random.randint(0, (blockNum * words_per_block) - 10)
        addresses = [base + random.randint(0, 10) for _ in range(num_addresses)]
    elif choice == 'manual':
        print(f"Enter up to {num_addresses} addresses manually (type 'done' to finish early):")
        while len(addresses) < num_addresses:
            entry = input(f"Address {len(addresses)+1}: ")
            if entry.lower() == 'done':
                break
            if not entry.isdigit():
                print("Invalid input. Please enter a number.")
                continue
            addresses.append(int(entry))
    else:
        print("Invalid choice. Defaulting to random mode.")
        addresses = [random.randint(0, (blockNum * words_per_block) - 1) for _ in range(num_addresses)]

    # Process each access
    for word_address in addresses:
        byte_address = word_address * 4
        tag_bin, index_bin, offset_bin = get_binary_parts(byte_address, index_bits, offset_bits)

        if policy == "DM":
            # Direct Mapped: only one block per index
            if index_bin in cache and cache[index_bin] == tag_bin:
                hit = "Hit"
                hits += 1
            else:
                hit = "Miss"
                misses += 1
                cache[index_bin] = tag_bin
            access_table.append((word_address, tag_bin, index_bin, hit))
            trace_file.write(f"{int(index_bin, 2)} {tag_bin} {hit}\n")

        elif policy == "SET ASSOCIATIVE":
            # Set Associative: multiple blocks per set, using LRU replacement
            set_index = index_bin
            if set_index not in cache:
                cache[set_index] = []
                lru_tracker[set_index] = deque()

            tags_in_set = cache[set_index]
            tracker = lru_tracker[set_index]

            if tag_bin in tags_in_set:
                # Cache hit: Move tag to most recently used position
                hit = "Hit"
                hits += 1
                tracker.remove(tag_bin)
                tracker.append(tag_bin)
            else:
                # Cache miss: Apply LRU if set is full
                hit = "Miss"
                misses += 1
                if len(tags_in_set) >= blockNum / numSets:
                    lru_tag = tracker.popleft()  # Remove least recently used tag
                    tags_in_set.remove(lru_tag)
                tags_in_set.append(tag_bin)
                tracker.append(tag_bin)

            access_table.append((word_address, tag_bin, set_index, hit))
            trace_file.write(f"{int(set_index, 2)} {tag_bin} {hit}\n")

    trace_file.close()

    # Print simulation summary
    print(f"\nSimulation complete. Total accesses: {len(addresses)}")
    print(f"Hits: {hits}")
    print(f"Misses: {misses}")
    hit_rate = (hits / len(addresses)) * 100
    print(f"Hit Rate: {hit_rate:.2f}%")

    # Extra Credit: Automatically launch live graphical visualization
    print("\nGenerating visualization...")
    subprocess.run(["python3", "visualize.py"])



while True:
    cmd = input("\nEnter a word address to access (or type 'clear', 'table', 'simulate', or 'exit'): ").lower()

    if cmd == 'exit':
        break
    elif cmd == 'clear':
        cache.clear()
        access_table.clear()
        lru_tracker.clear()
        print("Cache cleared.")
        continue
    elif cmd == 'table':
        print("\nAccess Table:")
        print("{:<12} {:<10} {:<10} {:<6}".format("Address", "Tag", "Index", "Hit/Miss"))
        for row in access_table:
            print("{:<12} {:<10} {:<10} {:<6}".format(*row))
        continue
    elif cmd == 'simulate':
        simulate_mode()
        continue
    elif not cmd.isdigit():
        print("Invalid input. Enter a numeric word address.")
        continue

    word_address = int(cmd)
    byte_address = word_address