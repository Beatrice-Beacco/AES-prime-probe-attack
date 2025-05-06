
from typing import List
from lib.averages import calculate_corrected_averages, compute_plaintext_averages_for_byte, compute_samples_average
from lib.constants import PLAINTEXT_BYTE_NUM
from lib.heatmap import generate_heatmap_from_averages
from lib.key_recovery import extract_cache_misses_lines, recover_msb_key_from_cache_misses_lines
from lib.parser import AESInvocationData, parse_aes_input_file

aes_output_file_path = "output.txt"

if __name__ == '__main__':
    
    # Open the file and parse the data in a readable format
    aes_data: List[AESInvocationData] = parse_aes_input_file(aes_output_file_path)

    # Calculate the average of all samples
    all_samples_averages = compute_samples_average(aes_data)

    recovered_key: list[str] = []
    for byte_index in range(PLAINTEXT_BYTE_NUM):
        # Average of each of the 16 possible 4 starting bits samples of the current byte
        plaintext_samples_averages = compute_plaintext_averages_for_byte(aes_data, byte_index) 
        # Calculate corrected averages for the current byte
        corrected_plaintext_samples_averages = calculate_corrected_averages(plaintext_samples_averages, all_samples_averages) 
        # Generate heat map .png on the corrected averages
        generate_heatmap_from_averages(corrected_plaintext_samples_averages, byte_index)
        # Get cache misses
        cache_misses_lines = extract_cache_misses_lines(corrected_plaintext_samples_averages)
        print(f"Cache misses lines: {cache_misses_lines}")
        # TODO: Calculate the partial key
        partial_key = recover_msb_key_from_cache_misses_lines(cache_misses_lines, byte_index)
        print(f"Partial key: {partial_key}")
        recovered_key.append(partial_key)
    
    print(f"Recovered key: {recovered_key}")
    # TODO: output heatmaps data + key to a file heatmaps.txt