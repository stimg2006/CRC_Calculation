# -*- coding: utf-8 -*-
class CRC:

    def __init__(self, crc_type, polynomial_value, initial_value, final_xor_value):
        self.crc_type = crc_type
        self.polynomial_value = polynomial_value
        self.initial_value = initial_value
        self.final_xor_value = final_xor_value
        
        self.Look_up_table = []
    
    def calculate_crc_look_up_table(self, verbose=False):
        self.Look_up_table = []
        if self.crc_type == 'CRC8':
            for i in range(256):
                current_byte = i
                for _ in range(8):
                    if (current_byte & 0x80) != 0:
                        current_byte <<= 1
                        current_byte ^= self.polynomial_value
                    else:
                        current_byte <<= 1
                current_byte &= 0xFF
                self.Look_up_table.append(current_byte)
                if verbose:
                    print(f'0x{format(current_byte, "02X")}')

        elif self.crc_type == 'CRC16':
            for i in range(256):
                current_byte = i << 8
                for _ in range(8):
                    if (current_byte & 0x8000) != 0:
                        current_byte <<= 1
                        current_byte ^= self.polynomial_value
                    else:
                        current_byte <<= 1
                current_byte &= 0xFFFF
                self.Look_up_table.append(current_byte)
                if verbose:
                    print(f'0x{format(current_byte, "02X")}')

        else:
            if verbose:
                print('Non-Supported CRC Type!!!')

        return self.Look_up_table

    def main_crc_calculation(self, data, verbose=False):
        if self.crc_type == 'CRC8':
            xor_target_value = self.initial_value
            for byte in data:
                xor_target_value = self.Look_up_table[xor_target_value ^ byte]
            xor_target_value ^= self.final_xor_value
            crc_value = xor_target_value & 0xFF
            if verbose:
                print('Data:')
                for byte in data:
                    print(f'   0x{format(byte, "02X")}')
                print(
                    f'Polynomial=0x{format(self.polynomial_value, "02X")}, '
                    f'Initial XOR=0x{format(self.initial_value, "02X")}, '
                    f'final XOR=0x{format(self.final_xor_value, "02X")}'
                )
                print(f'Checksum:0x{format(crc_value, "02X")}')

        elif self.crc_type == 'CRC16':
            xor_target_value = self.initial_value
            for byte in data:
                pos = ((xor_target_value ^ (byte << 8)) >> 8) & 0xFF
                xor_target_value = (xor_target_value << 8) ^ self.Look_up_table[pos]
            xor_target_value ^= self.final_xor_value
            crc_value = xor_target_value & 0xFFFF
            if verbose:
                print('Data:')
                for byte in data:
                    print(f'   0x{format(byte, "02X")}')
                print(
                    f'Polynomial=0x{format(self.polynomial_value, "02X")}, '
                    f'Initial XOR=0x{format(self.initial_value, "02X")}, '
                    f'final XOR=0x{format(self.final_xor_value, "02X")}'
                )
                print(f'Checksum:0x{format(crc_value, "02X")}')

        else:
            crc_value = 'invalid'

        return crc_value

    def format_lookup_table(self):
        return '\n'.join(f'0x{format(item, "02X")},' for item in self.Look_up_table)

if __name__ == '__main__':
    # polynomial_value = 0x1D
    # calculate_crc_look_up_table(polynomial_value)
    # data = []
    # main_crc_calculation(data)
    print('This file is sub-module of CRC calculation tool')

