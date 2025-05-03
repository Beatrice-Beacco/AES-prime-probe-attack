
from dataclasses import dataclass
import statistics
from typing import Dict

from lib.constants import CYCLES_NUM, FIRST_PLAINTEXT_BITS
from lib.parser import AESInvocationData

type PlaintextAveragesDict = Dict[str, PlaintextAverage]

@dataclass
class SampleCryptoData(object):
    plaintext: bytes
    ciphertext: bytes

@dataclass
class PlaintextAverage(object):
    samples_crypto_data: list[SampleCryptoData]
    averages: list[float]


def compute_samples_average(samples: list[AESInvocationData]) -> list[float]:
    # Create list of the size of the number of cycles (64 elements) and initialize it with empty lists
    grouped_samples_measurements: list[list[int]] = [[] for _ in range(CYCLES_NUM)] 

    # Group elements in the same cycle for all samples. Elements of the same cycle will be added to the same list
    for sample in samples:
        for index, cycle_measurement in enumerate(sample.cycle_measurements):
            grouped_samples_measurements[index].append(cycle_measurement)
    
    # Calculate the average of each grouped cycle measurements
    samples_averages: list[float] = [statistics.mean(cycle_measurements) for cycle_measurements in grouped_samples_measurements]
    return samples_averages

def compute_plaintext_averages(plaintext_samples: list[AESInvocationData]) -> PlaintextAveragesDict:
    # Create the hashmap for each of the 16 starting plaintext bits
    grouped_plaintext_samples: dict[str, list[AESInvocationData]] = {}
    for plaintext_bits in FIRST_PLAINTEXT_BITS:
        grouped_plaintext_samples[plaintext_bits] = []
        
    # Group samples by the first 4 bits of the plaintext
    for sample in plaintext_samples:
        bytes_data = bytes.fromhex(sample.plaintext) # Convert hex string to bytes
        shifted_bytes = [b >> 4 for b in bytes_data] # Shift on the right by 4 to discard the last 4 bits of each byte
        most_significant_bits = f"0x{shifted_bytes[0]:X}" # Take the 4 msb of the first byte and convert to hex
        grouped_plaintext_samples[most_significant_bits].append(sample)
    
    # Calculate the average of each plaintext group
    plaintext_averages: PlaintextAveragesDict = {}
    for plaintext_bits, plaintext_samples in grouped_plaintext_samples.items():
        samples_crypto_data = [SampleCryptoData(sample.plaintext, sample.ciphertext) for sample in plaintext_samples]
        averages = compute_samples_average(plaintext_samples)
        plaintext_averages[plaintext_bits] = PlaintextAverage(samples_crypto_data, averages)
    
    
    return plaintext_averages