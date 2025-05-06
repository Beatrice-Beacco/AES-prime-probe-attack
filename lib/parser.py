
from dataclasses import dataclass


@dataclass
class AESInvocationData(object):
    plaintext: str
    ciphertext: str
    line_measurements: list[int]


def parse_aes_input_file(file_path: str) -> list[AESInvocationData]:
    data = []
    with open(file_path, 'r') as file:
        for line in file:
                line_elements = line.split()
                lines = [int(x) for x in line_elements[2:]]
                line = AESInvocationData(
                    plaintext = line_elements[0],
                    ciphertext = line_elements[1],
                    line_measurements = lines
                )
                data.append(line)
    return data