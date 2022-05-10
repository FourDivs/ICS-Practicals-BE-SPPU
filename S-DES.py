# S-DES Algorithm
# Author: kothariji
# Inputs: plaintext, key

# Sample Inputs
# Enter the 8-bit Plain Text: 1 0 0 1 0 1 1 1
# Enter the 10-bit key: 1 0 1 0 0 0 0 0 1 0

s_box_1 = [
    [1, 0, 3, 2],
    [3, 2, 1, 0],
    [0, 2, 1, 3],
    [3, 1, 3, 2]
]

s_box_2 = [
    [0, 1, 2, 3],
    [2, 0, 1, 3],
    [3, 0, 1, 0],
    [2, 1, 0, 3]
]


def split_bits_into_two_parts(bits_list):
    n = len(bits_list)
    first_half = bits_list[:n//2]
    second_half = bits_list[n//2:]
    return first_half, second_half


def left_shift_bits_list(bits_list, shift_amount=1):
    n = len(bits_list)
    shifted_bits_list = bits_list[shift_amount:] + bits_list[:shift_amount]
    return shifted_bits_list


def xor_bits(bits_list_1, bits_list_2):
    n = len(bits_list_1)
    xor_bits_list = [bits_list_1[i] ^ bits_list_2[i] for i in range(n)]
    return xor_bits_list


def key_generation(ten_bit_key):

    # step -1: P-10 (Permutation)
    # Permutation Order - 3 5 2 7 4 10 1 9 8 6
    b1, b2, b3, b4, b5, b6, b7, b8, b9, b10 = ten_bit_key
    updated_ten_bit_key = [b3, b5, b2, b7, b4, b10, b1, b9, b8, b6]

    # Step -2: Split the key into two halves
    left_half, right_half = split_bits_into_two_parts(updated_ten_bit_key)

    # Step -3: Left Shift the two keys
    left_half_shifted = left_shift_bits_list(left_half)
    right_half_shifted = left_shift_bits_list(right_half)

    # Step -4: Concatenate the two halves
    concatenated_key = left_half_shifted + right_half_shifted

    # Step -5: P-8 (Permutation)
    # Permutation Order - 6 3 7 4 8 5 10 9
    b1, b2, b3, b4, b5, b6, b7, b8, b9, b10 = concatenated_key
    key_1 = [b6, b3, b7, b4, b8, b5, b10, b9]

    # Step -6: Left Shift the key
    # Left shift the Step-2 keys twice
    left_helf_twice_shifted = left_shift_bits_list(left_half_shifted, 2)
    right_half_twice_shifted = left_shift_bits_list(right_half_shifted, 2)

    # Step -7: Concatenate the two halves
    concatenated_key_2 = left_helf_twice_shifted + right_half_twice_shifted

    # Step -8: P-8 (Permutation)
    # Permutation Order - 6 3 7 4 8 5 10 9
    b1, b2, b3, b4, b5, b6, b7, b8, b9, b10 = concatenated_key_2
    key_2 = [b6, b3, b7, b4, b8, b5, b10, b9]

    return key_1, key_2


def initial_permutation(plain_text):
    # Permutation Order - 2 6 3 1 4 8 5 7
    b1, b2, b3, b4, b5, b6, b7, b8 = plain_text
    initial_permutation_plain_text = [b2, b6, b3, b1, b4, b8, b5, b7]
    return initial_permutation_plain_text


def reverse_initial_permutation(initial_permutation_list):
    # Permutation Order - 4 1 3 5 7 2 8 6
    b1, b2, b3, b4, b5, b6, b7, b8 = initial_permutation_list
    initial_permutation_list_reversed = [b4, b1, b3, b5, b7, b2, b8, b6]
    return initial_permutation_list_reversed


def s_des_encryption(plain_text, key_bits):

    # Step -2: Split the plain text into two halves
    plain_text_left_half, plain_text_right_half = split_bits_into_two_parts(
        plain_text)

    # Step -3: Expand the right hand side of the plain text (4 bits to 8 bits)
    # Expansion Order - 4 1 2 3 2 3 4 1
    b1, b2, b3, b4 = plain_text_right_half
    expanded_plain_text_right_half = [b4, b1, b2, b3, b2, b3, b4, b1]

    # Step -4: XOR the expanded plain text with the key
    xor_plain_text_with_key = xor_bits(
        expanded_plain_text_right_half, key_bits)

    # Step -5: Divide the xor_plain_text_with_key into two halves
    xor_plain_text_with_key_left_half, xor_plain_text_with_key_right_half = split_bits_into_two_parts(
        xor_plain_text_with_key)

    # Step -6: get s-box values
    b1, b2, b3, b4 = xor_plain_text_with_key_left_half
    row = int(str(b1) + str(b4), 2)
    col = int(str(b2) + str(b3), 2)
    s_box_1_value = format(s_box_1[row][col], 'b').zfill(2)

    b1, b2, b3, b4 = xor_plain_text_with_key_right_half
    row = int(str(b1) + str(b4), 2)
    col = int(str(b2) + str(b3), 2)
    s_box_2_value = format(s_box_2[row][col], 'b').zfill(2)

    # Step -7: Combine the s-box values
    combined_s_box_values = s_box_1_value + s_box_2_value

    # Step -8: P-4 (Permutation)
    # Permutation Order - 2 4 3 1
    b1, b2, b3, b4 = [int(i) for i in combined_s_box_values]
    permuted_s_box_values = [b2, b4, b3, b1]

    # Step -9: XOR the permuted s-box values with the left half of the plain text

    xor_permuted_s_box_values_with_left_half = xor_bits(
        permuted_s_box_values, plain_text_left_half)

    # Step -10: Concatenate xor_permuted_s_box_values_with_left_half and right half of the plain text
    resultant_plain_text = xor_permuted_s_box_values_with_left_half + plain_text_right_half

    return resultant_plain_text


plain_text = [1, 0, 0, 1, 0, 1, 1, 1]
ten_bit_key = [1, 0, 1, 0, 0, 0, 0, 0, 1, 0]
# plain_text = list(map(int, input("Enter the 8-bit Plain Text: ").split()))
# ten_bit_key = list(map(int, input("Enter the 10-bit key: ").split()))
key_1, key_2 = key_generation(ten_bit_key)

plain_text = initial_permutation(plain_text)
resultant_plain_text = s_des_encryption(plain_text, key_1)


# swap the left and right halves
left_half, right_half = split_bits_into_two_parts(resultant_plain_text)
resultant_plain_text = right_half + left_half

resultant_plain_text = s_des_encryption(resultant_plain_text, key_2)

cipher_text = reverse_initial_permutation(resultant_plain_text)

print("Key 1: ", key_1)
print("Key 2: ", key_2)
print("Cipher Text: ", cipher_text)
