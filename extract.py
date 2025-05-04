
from typing import List
from lib.averages import compute_plaintext_averages, compute_samples_average
from lib.constants import CACHE_MISS_TRESHOLD, FIRST_PLAINTEXT_BITS
from lib.parser import AESInvocationData, parse_aes_input_file
import matplotlib.pyplot as plt

aes_output_file_path = "output.txt"
heatmap_output_file_path = "heatmap.png"

if __name__ == '__main__':
    
    # Open the file and parse the data in a readable format
    aes_data: List[AESInvocationData] = parse_aes_input_file(aes_output_file_path)

    # Calculate the average of all samples
    all_samples_averages = compute_samples_average(aes_data)
    #print(f"All samples averages: {all_samples_averages}")

    # Average of each of the 16 possible 4 starting bits samples
    plaintext_samples_averages = compute_plaintext_averages(aes_data)
    #print(f"Plaintext samples averages: {plaintext_samples_averages}")

    # Calculate corrected averages
    for sample_averages in plaintext_samples_averages:
        for cycle_num, cycle_average in enumerate(sample_averages.averages):
            sample_averages.averages[cycle_num] = cycle_average - all_samples_averages[cycle_num]
    #print(f"Corrected averages \n {[f"Plaintext: {key}, Averages: {sample_averages}" for key, sample_averages in plaintext_samples_averages.items()]}")
            
    # Generate heat maps on corrected averages
    # Heatmap data: row = 4 plaintext bits, column = cycle measurement
    # Generate a matrix of 16 rows 64 columns with the corrected averages data
    heatmap_data = list(range(len(FIRST_PLAINTEXT_BITS)))
    for plaintext_bit, sample_averages in enumerate(plaintext_samples_averages):
        heatmap_data[plaintext_bit] = sample_averages.averages
    print(f"Heatmap data: {heatmap_data}")
    
    plt.xlabel('Cache Set')
    plt.ylabel('Plaintext Byte')
    plt.title('AES Cache Access Heatmap') 
    plt.imshow(heatmap_data, cmap='hot', interpolation='nearest')
    plt.savefig(heatmap_output_file_path)

    # Get cache misses and obtain partial key
    # For each corrected average, find the cycle where the measurement exceeds the threshold
    # Index of the list = plaintext bit integer value, value at that index = cache miss cycle
    cache_misses_cycles = list(range(len(FIRST_PLAINTEXT_BITS)))
    for plaintex_bit, corrected_average in enumerate(plaintext_samples_averages):
        cache_miss_cycle = [cycle_index for cycle_index, average in enumerate(corrected_average.averages) if average > CACHE_MISS_TRESHOLD]
        cache_misses_cycles[plaintex_bit] = cache_miss_cycle[0] if cache_miss_cycle else None
    print(f"Cache misses cycles: {cache_misses_cycles}")
    
    # TODO: calculate the key (somehow idk)
    # TODO: output heatmaps data + key to a file heatmaps.txt