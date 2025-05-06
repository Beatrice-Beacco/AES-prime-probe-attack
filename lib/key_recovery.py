
from lib.averages import PlaintextAverage
from lib.constants import FIRST_PLAINTEXT_BITS, PLAINTEXT_BYTE_NUM
from collections import Counter


# For each corrected average, find the line where the measurement exceeds the threshold
# Index of the list = plaintext bit integer value, value at that index = cache miss line
def extract_cache_misses_lines(corrected_averages: list[PlaintextAverage]) -> list[int]:
    cache_misses_lines = list(range(len(FIRST_PLAINTEXT_BITS)))
    for plaintex_bit, corrected_average in enumerate(corrected_averages):
        max_measurement_line_index = corrected_average.averages.index(max(corrected_average.averages))
        cache_misses_lines[plaintex_bit] = max_measurement_line_index
    return cache_misses_lines

# TODO:
def recover_msb_key_from_cache_misses_lines(cache_misses_lines: list[int], byte_index: int) -> str:
    # Determine the base cache set for the T-table used by this byte. Each table has 16 cache sets, we have 4 tables.
    base_table_set = ((byte_index % 4) + 2) % 4 * 16
    candidates = []
    
    # Iterate over all 16 possible plaintext bits
    for plaintext_int in range(PLAINTEXT_BYTE_NUM):
        cache_set = cache_misses_lines[plaintext_int]
        valid = base_table_set <= cache_set < base_table_set + 16
        print(f"P_hi=0x{plaintext_int:X}: BaseSet={base_table_set} Cache set={cache_set}, Valid={valid}")
        if valid:
            candidate = (cache_set - base_table_set) ^ plaintext_int
            candidates.append(candidate)
    
    # Find the most common valid candidate (mode)
    if not candidates:
        raise ValueError("No valid candidates found for the key recovery.")
    
    counts = Counter(candidates)
    key_hi = counts.most_common(1)[0][0]  # Get most frequent candidate
    
    # Return as a single hex character (0x0-F)
    return f"0x{key_hi:X}"