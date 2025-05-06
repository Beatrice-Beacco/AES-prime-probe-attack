
from dataclasses import dataclass
import statistics

from lib.constants import LINES_NUM, FIRST_PLAINTEXT_BITS
from lib.parser import AESInvocationData


@dataclass
class SampleCryptoData(object):
    plaintext: bytes
    ciphertext: bytes

@dataclass
class PlaintextAverage(object):
    hex_plaintext: str
    samples_crypto_data: list[SampleCryptoData]
    averages: list[float]


def compute_samples_average(samples: list[AESInvocationData]) -> list[float]:
    # Create list of the size of the number of lines (64 elements) and initialize it with empty lists
    grouped_samples_measurements: list[list[int]] = [[] for _ in range(LINES_NUM)] 

    # Group elements in the same line for all samples. Elements of the same line will be added to the same list
    for sample in samples:
        for index, cache_line_measurement in enumerate(sample.line_measurements):
            grouped_samples_measurements[index].append(cache_line_measurement)
    
    # Calculate the average of each grouped line measurements
    samples_averages: list[float] = [statistics.mean(cache_line_measurements) for cache_line_measurements in grouped_samples_measurements]
    return samples_averages

def compute_plaintext_averages_for_byte(plaintext_samples: list[AESInvocationData], byte_index: int) -> list[PlaintextAverage]:
    # Create the hashmap for each of the 16 starting plaintext bits
    grouped_plaintext_samples: dict[str, list[AESInvocationData]] = {}
    for plaintext_bits in FIRST_PLAINTEXT_BITS:
        grouped_plaintext_samples[plaintext_bits] = []
        
    # Group samples by the first 4 bits of the plaintext
    for sample in plaintext_samples:
        bytes_data = bytes.fromhex(sample.plaintext) # Convert hex string to bytes
        shifted_bytes = [b >> 4 for b in bytes_data] # Shift on the right by 4 to discard the last 4 bits of each byte
        most_significant_bits = f"0x{shifted_bytes[byte_index]:X}" # Take the 4 msb of the first byte and convert to hex
        grouped_plaintext_samples[most_significant_bits].append(sample)
    
    # Calculate the average of each plaintext group
    plaintext_averages = list(range(len(FIRST_PLAINTEXT_BITS)))
    for plaintext_bits, plaintext_samples in grouped_plaintext_samples.items():
        samples_crypto_data = [SampleCryptoData(sample.plaintext, sample.ciphertext) for sample in plaintext_samples]
        averages = compute_samples_average(plaintext_samples)
        plaintext_bits_int = int(plaintext_bits, 16)
        plaintext_averages[plaintext_bits_int] = PlaintextAverage(
            hex_plaintext=plaintext_bits,
            samples_crypto_data=samples_crypto_data,
            averages=averages
        )
    
    
    return plaintext_averages

def calculate_corrected_averages(plaintext_samples_averages: list[PlaintextAverage], all_samples_averages: list[float]) -> list[PlaintextAverage]:
    # Deep copy the plaintext samples averages
    plaintext_samples_averages_copy = [PlaintextAverage(sample.hex_plaintext, sample.samples_crypto_data, sample.averages.copy()) for sample in plaintext_samples_averages]

    for sample_averages in plaintext_samples_averages_copy:
        for cache_line_num, cache_line_average in enumerate(sample_averages.averages):
            sample_averages.averages[cache_line_num] = cache_line_average - all_samples_averages[cache_line_num]
            
    return plaintext_samples_averages_copy
