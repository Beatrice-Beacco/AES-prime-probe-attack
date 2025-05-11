from lib.averages import PlaintextAverages
from lib.constants import (
    CACHE_OFFSET,
    FIRST_PLAINTEXT_BITS,
    PLAINTEXT_BYTE_NUM,
    SETS_NUM,
)
from collections import Counter


# For each corrected average, find the line where the measurement exceeds the threshold
# Index of the list = plaintext bit integer value, value at that index = cache miss line
def extract_cache_misses_lines(
    corrected_averages: list[PlaintextAverages],
) -> list[int]:
    cache_misses_lines = list(range(len(FIRST_PLAINTEXT_BITS)))
    for plaintex_bit, corrected_average in enumerate(corrected_averages):
        max_measurement_line_index = corrected_average.index(max(corrected_average))
        cache_misses_lines[plaintex_bit] = max_measurement_line_index
    return cache_misses_lines


def recover_msb_key_from_cache_misses_lines(
    cache_misses_lines: list[int], byte_index: int
) -> str:
    # Determine the base cache set for the T-table used by this byte. Each table has 16 cache sets, we have 4 tables.
    # Take into account that the first table starts at table index 16*2 + 2. We have both a table number offset of 2 and a initial table set offset of 2.
    base_table_set = (
        ((byte_index % 4) + CACHE_OFFSET) % 4 * 16
    ) + CACHE_OFFSET  # T0:34-49, T1:50-01, T2:02-17, T3:18-33
    candidates = []

    # Iterate over all 16 possible plaintext bits
    for plaintext_int in range(PLAINTEXT_BYTE_NUM):
        cache_miss_set = cache_misses_lines[plaintext_int]
        # Handle wrap around
        table_set_index = 0
        if cache_miss_set < base_table_set:
            table_set_index = SETS_NUM - (base_table_set - cache_miss_set)
        else:
            table_set_index = cache_miss_set - base_table_set

        print(
            f"P_hi=0x{plaintext_int:X}: Base Table Set={base_table_set} Cache Miss set={cache_miss_set}, Set index inside the table={table_set_index}"
        )
        candidate = table_set_index ^ plaintext_int
        candidates.append(candidate)

    # Find the most common valid candidate (mode)
    if not candidates:
        raise ValueError("No valid candidates found for the key recovery.")

    counts = Counter(candidates)
    key_hi = counts.most_common(1)[0][0]  # Get most frequent candidate

    # Return as a single hex character (0x0-F)
    return f"0x{key_hi:X}"
