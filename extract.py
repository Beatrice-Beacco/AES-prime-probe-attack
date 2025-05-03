
from typing import List
from lib.averages import compute_plaintext_averages, compute_samples_average
from lib.parser import AESInvocationData, parse_aes_input_file


if __name__ == '__main__':
    
    # Open the file and parse the data in a readable format
    aes_output_file_path = "output.txt"
    aes_data: List[AESInvocationData] = parse_aes_input_file(aes_output_file_path)

    # Calculate the average of all samples
    all_samples_averages = compute_samples_average(aes_data)
    #print(f"All samples averages: {all_samples_averages}")

    # Average of each of the 16 possible 4 starting bits samples
    plaintext_samples_averages = compute_plaintext_averages(aes_data)
    #print(f"Plaintext samples averages: {plaintext_samples_averages}")

    # Calculate corrected averages
    for sample_averages in plaintext_samples_averages.values():
        for index, average in enumerate(sample_averages.averages):
            sample_averages.averages[index] = average - all_samples_averages[index]
    print(f"Corrected averages \n {[f"Plaintext: {key}, Averages: {sample_averages}" for key, sample_averages in plaintext_samples_averages.items()]}")
            
    # TODO: Generate heat maps on corrected averages
    # TODO: Get cache misses and obtain partial key
    # TODO: calculate the key (somehow idk)
    # TODO: output heatmaps data + key to a file heatmaps.txt