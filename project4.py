import math

# dictionary to represent the cache. Keys are index/set values and values are tags
cache = {}
# stores history of accesses (display the access table)
access_table = []

nominal = int(input("Please enter the nominal size : "))

words_per_block = int(input("Enter the amount of words per block: "))

bytes_per_block = 4 * (words_per_block)

blockNum = nominal / bytes_per_block

print("The number of blocks is: ", blockNum)

policy = (input("Please enter the mapping policy (DM or set associative): ")).upper()

if (policy == "SET ASSOCIATIVE"):
    numSets = int(input("Enter the number of sets: "))
    print("The number of sets is: ", (blockNum / numSets))

    offset = math.log2(bytes_per_block)
    print("The offset is: ", offset)

    index = math.log2(blockNum/numSets)
    print("The index is: ", index)

    tag = 32 - (index + offset)
    print("The tag is: ", tag)

    real = nominal + (blockNum * ((tag + offset)/8))
    print("The real size is: ", real)

elif (policy == "DM"):
    offset = math.log2(bytes_per_block)
    print("The offset is: ", offset)

    index = math.log2(blockNum)
    print("The index is: ", index)

    tag = 32 - (index + offset)
    print("The tag is: ", tag)

    real = nominal + blockNum * ((tag + offset)/8)
    print("The real size is: ", real)

# extract tag, index, and offset
def get_binary_parts(address, index_bits, offset_bits):
    bin_addr = bin(address)[2:].zfill(32)
    tag = bin_addr[:32 - (index_bits + offset_bits)]
    index = bin_addr[32 - (index_bits + offset_bits):32 - offset_bits]
    offset = bin_addr[32 - offset_bits:]
    return tag, index, offset

while True:
    cmd = input("\nEnter a word address to access (or type 'clear', 'table', or 'exit'): ").lower()

    # option to exit the simulation
    if cmd == 'exit':
        break

    # option to clear cache and access history
    elif cmd == 'clear':
        cache.clear()
        access_table.clear()
        print("Cache cleared.")
        continue

    # option to display table of all word accesses
    elif cmd == 'table':
        print("\nAccess Table:")
        print("{:<12} {:<10} {:<10} {:<6}".format("Address", "Tag", "Index", "Hit/Miss"))
        
        for row in access_table:
            print("{:<12} {:<10} {:<10} {:<6}".format(*row))
        continue

    # ensure the address is a number
    if not cmd.isdigit():
        print("Invalid input. Enter a numeric word address.")
        continue

    # convert word address to byte address
    word_address = int(cmd)
    byte_address = word_address * 4

    # convert offset, index, and tag values to integers for bit handling
    offset_bits = int(offset)
    index_bits = int(index)
    tag_bits = int(tag)

    # extract binary parts from address
    tag_bin, index_bin, offset_bin = get_binary_parts(byte_address, index_bits, offset_bits)

    if policy == "DM":

        # check if index exists and tag matches for hit
        if index_bin in cache and cache[index_bin] == tag_bin:
            hit = "Hit"

        else:
            hit = "Miss"
            cache[index_bin] = tag_bin

        # add entry to access history table
        access_table.append((word_address, tag_bin, index_bin, hit))

        print(f"Address {word_address} maps to Index {int(index_bin, 2)} with Tag {tag_bin}: {hit}")
    
    elif policy == "SET ASSOCIATIVE":
        # use index as set identifier
        set_index = index_bin

        # initialize the set if not in cache yet
        if set_index not in cache:
            cache[set_index] = []

        # et current tags in this set
        tags_in_set = cache[set_index]

        # check if tag matches in set for hit
        if tag_bin in tags_in_set:
            hit = "Hit"

        else:
            hit = "Miss"

            # replace oldest block if set is full (FIFO)
            if len(tags_in_set) >= blockNum / numSets:
                tags_in_set.pop(0)
            
            # add new tag to set
            tags_in_set.append(tag_bin)

        # add entry to access history table
        access_table.append((word_address, tag_bin, set_index, hit))

        print(f"Address {word_address} maps to Set {int(set_index, 2)} with Tag {tag_bin}: {hit}")
