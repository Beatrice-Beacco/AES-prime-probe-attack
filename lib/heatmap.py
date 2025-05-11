from lib.averages import PlaintextAverages
from lib.constants import FIRST_PLAINTEXT_BITS
import matplotlib.pyplot as plt

y_labels = [
    "0",
    "1",
    "2",
    "3",
    "4",
    "5",
    "6",
    "7",
    "8",
    "9",
    "A",
    "B",
    "C",
    "D",
    "E",
    "F",
]


# Heatmap data: row = 4 plaintext bits, column = line measurement
# Generate a matrix of 16 rows 64 columns with the corrected averages data
def generate_heatmap_from_averages(averages: list[PlaintextAverages], byte_index: int):
    heatmap_output_file_path = f"heatmaps/byte_{byte_index}.png"

    heatmap_data = list(range(len(FIRST_PLAINTEXT_BITS)))
    for plaintext_bit, sample_averages in enumerate(averages):
        heatmap_data[plaintext_bit] = sample_averages
    plt.xlabel("Cache Set")
    plt.ylabel("Plaintext Bits")
    plt.yticks(ticks=range(len(y_labels)), labels=y_labels)
    plt.title("AES Cache Access Heatmap")
    plt.imshow(
        heatmap_data,
        cmap="hot",
    )
    plt.savefig(heatmap_output_file_path)
