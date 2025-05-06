
from lib.averages import PlaintextAverage
from lib.constants import FIRST_PLAINTEXT_BITS
import matplotlib.pyplot as plt


# Heatmap data: row = 4 plaintext bits, column = line measurement
# Generate a matrix of 16 rows 64 columns with the corrected averages data
def generate_heatmap_from_averages(averages: list[PlaintextAverage], byte_index: int):
    heatmap_output_file_path = f"heatmaps/byte_{byte_index}.png"

    heatmap_data = list(range(len(FIRST_PLAINTEXT_BITS)))
    for plaintext_bit, sample_averages in enumerate(averages):
        heatmap_data[plaintext_bit] = sample_averages.averages
    #print(f"Heatmap data: {heatmap_data}")
    
    plt.xlabel('Cache Set')
    plt.ylabel('Plaintext Byte')
    plt.title('AES Cache Access Heatmap') 
    plt.imshow(heatmap_data, cmap='hot', interpolation='nearest')
    plt.savefig(heatmap_output_file_path)