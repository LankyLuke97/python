# 5.3 Flip Bit to Win: You have an integer and you can flip exactly one bit from a 0 to a 1. Write code to find the longest sequence of ones you could create

test_cases = [
    (int("111100111011110101111", 2), 8),
    (int("00011010101010101010111111111100", 2), 12),
    (int("11011101111", 2), 8),
    (int("011111", 2), 5),
    (int("0", 2), 1),
    (int("1", 2), 1),
    (int("10", 2), 2),
]


def longest_consecutive_ones(n: int) -> int:
    prev_block = -1
    longest_consecutive = 1
    while n:
        cur_block = 0
        while n & 1:
            cur_block += 1
            n >>= 1
        n >>= 1
        longest_consecutive = max(longest_consecutive, cur_block + prev_block + 1)
        prev_block = cur_block

    return longest_consecutive


for test_case, expected_answer in test_cases:
    assert longest_consecutive_ones(test_case) == expected_answer
