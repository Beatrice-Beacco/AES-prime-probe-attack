
from typing import List
from lib.averages import compute_plaintext_averages, compute_samples_average
from lib.constants import FIRST_PLAINTEXT_BITS
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
    for sample_averages in plaintext_samples_averages.values():
        for plaintext_bit_int, average in enumerate(sample_averages.averages):
            sample_averages.averages[plaintext_bit_int] = average - all_samples_averages[plaintext_bit_int]
    print(f"Corrected averages \n {[f"Plaintext: {key}, Averages: {sample_averages}" for key, sample_averages in plaintext_samples_averages.items()]}")
            
    # Generate heat maps on corrected averages
    # Heatmap data: row = 4 plaintext bits, column = cycle measurement
    # Generate a matrix of 16 rows 64 columns with the corrected averages data
    heatmap_data = [ [] for _ in range(len(FIRST_PLAINTEXT_BITS))]
    for plaintext, sample_averages in plaintext_samples_averages.items():
        plaintext_bit_int = int(plaintext, 16)
        heatmap_data[plaintext_bit_int] = sample_averages.averages
    
    plt.xlabel('Cache Set')
    plt.ylabel('Plaintext Byte')
    plt.title('AES Cache Access Heatmap') 
    plt.imshow(heatmap_data, cmap='hot', interpolation='nearest')
    plt.savefig(heatmap_output_file_path)

    
    # TODO: Get cache misses and obtain partial key
    # TODO: calculate the key (somehow idk)
    # TODO: output heatmaps data + key to a file heatmaps.txt