
from lib.averages import PlaintextAverage
from lib.constants import CACHE_MISS_TRESHOLD, FIRST_PLAINTEXT_BITS


# For each corrected average, find the line where the measurement exceeds the threshold
# Index of the list = plaintext bit integer value, value at that index = cache miss line
def extract_cache_misses_lines(corrected_averages: list[PlaintextAverage]) -> list[int]:
    cache_misses_lines = list(range(len(FIRST_PLAINTEXT_BITS)))
    for plaintex_bit, corrected_average in enumerate(corrected_averages):
        cache_miss_line = [line_index for line_index, average in enumerate(corrected_average.averages) if average > CACHE_MISS_TRESHOLD]
        cache_misses_lines[plaintex_bit] = cache_miss_line[0] if cache_miss_line else None
    return cache_misses_lines

# TODO:
def recover_key_from_cache_misses_lines(averages: list[PlaintextAverage], cache_misses_lines: list[int]) -> str:
    return ""