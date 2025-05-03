
from dataclasses import dataclass


@dataclass
class AESInvocationData(object):
    plaintext: str
    ciphertext: str
    cycle_measurements: list[int]


def parse_aes_input_file(file_path: str) -> list[AESInvocationData]:
    data = []
    with open(file_path, 'r') as file:
        for line in file:
                line_elements = line.split()
                cycles = [int(x) for x in line_elements[2:]]
                line = AESInvocationData(
                    plaintext = line_elements[0],
                    ciphertext = line_elements[1],
                    cycle_measurements = cycles
                )
                data.append(line)
    return data