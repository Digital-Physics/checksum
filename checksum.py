# data integrity
# checksum is used in some protocols for error detection that arises in information transmission or storage

# checksum bits are calculated from a bit string message
# the bitstring message here is represented as a list of smaller chunks of bit sequences, sometimes called "words"
def calcChecksum(original_message_bits: list[str]) -> str:
    print()
    total = "0"  # initialize
    word_length = len(original_message_bits[0])

    # add the binary string words
    for word in original_message_bits:
        total = bin(int(total,2) + int(word,2))
    print("intermediate Checksum total before overflow bits wrap around:", total)

    # calc length of unrestricted intermediate bitstring
    total = total[2:]  # take away the 0b binary prefix
    bit_sum_length = len(total)

    # limit the length of the sum to the length of the individual words; wrap around the bits; shift register?
    if bit_sum_length > word_length:
        print("add least significant bits up to the word length to the spillover bits:", total[-word_length:], total[:bit_sum_length-word_length])
        total = bin(int(total[-word_length:], 2) + int(total[:bit_sum_length-word_length], 2))

    total = int(total,2)
    print("the sum total (in decimal, not binary) after constraining the Checksum to the word length:", total)
    total =bin(total)
    print("total as binary", total)

    # flip the bits; 1's complement
    # bitwise NOT ~ doesn't work the way we want
    print("the bitstring if we remove the 0b prefix", total[2:])
    total = "".join(["0" if bit == "1" else "1" for bit in total[2:]])
    print("checksum after the bit flip:", total)
    print()
    return total

def checkForErrors(receivedMessage, Checksum):
    # Calc the binary sum of packets + checksum
    total = bin(int(Checksum,2))
    word_length = len(receivedMessage[0])
    for word in receivedMessage:
        total = bin(int(total, 2) + int(word, 2))

    total = total[2:]
    bit_sum_length = len(total)

    if bit_sum_length > word_length:
        total = bin(int(total[-word_length:], 2) + int(total[:bit_sum_length-word_length], 2))

    total = bin(int(total, 2))
    total = "".join(["0" if bit == "1" else "1" for bit in total[2:]])

    # If sum = 0, No error is detected
    if int(total, 2) == 0:
        print("The data may be ok because the message bits with the checksum bits add to 0.")
    else:
        print("The data must be corrupted because the message bits with the checksum bits don't add to 0.")

SentMessage = ["1111111111111111", "1111111100000000", "1111000011110000", "1100000011000000"]
print("sent message:", SentMessage)
checksum = calcChecksum(SentMessage)
print("Checksum:", checksum)
# assume the message is not corrupted
ReceivedMessage = SentMessage
print("received message:", ReceivedMessage)

print()
print("check #1")
print("run our Checksum data integrity check")
checkForErrors(ReceivedMessage, checksum)

print()
print("check #2")
print("sent message:", SentMessage)
print("Checksum:", checksum)
# assume the message is corrupted
ReceivedMessage = ["1111111111111111", "1111111100000000", "1111000011110000", "1100000011000001"]
print("received message:", ReceivedMessage)

print()
print("run our Checksum data integrity check")
checkForErrors(ReceivedMessage, checksum)


