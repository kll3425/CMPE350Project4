import math

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


