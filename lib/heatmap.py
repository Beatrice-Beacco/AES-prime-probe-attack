from lib.averages import PlaintextAverages
import matplotlib.pyplot as plt


# Heatmap data: row = 4 plaintext bits, column = line measurement
def generate_heatmap_from_averages(averages: list[PlaintextAverages], byte_index: int):
    heatmap_output_file_path = f"heatmaps/byte_{byte_index}.png"

    plt.xlabel("Cache Set")
    plt.ylabel("Plaintext Bits")
    plt.title("AES Cache Access Heatmap")
    plt.imshow(
        averages,
        cmap="hot",
    )
    plt.savefig(heatmap_output_file_path)
