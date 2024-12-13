import argparse
import csv
import struct

def execute_program(binary_file, output_file):
    with open(binary_file, 'rb') as infile, open(output_file, 'w', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(["Address", "Value"])  # Заголовки в CSV

        memory = [0] * 1024  # Увеличенный размер памяти
        result_addresses = []  # Адреса, которые нужно записать в CSV

        while True:
            byte = infile.read(1)
            if not byte:
                break  # Конец файла
            command_type = ord(byte)
        
            if command_type == 0:
                continue
            
            print(f"Command type: {command_type}")
            
            if command_type == 169:  # LOAD_CONST
                try:
                    B = struct.unpack('>H', infile.read(2))[0]
                    C = struct.unpack('>H', infile.read(2))[0]
                    print(f"Loaded B={B}, C={C}")

                    # Проверяем корректность B
                    if B >= len(memory):
                        raise ValueError(f"Address B={B} exceeds memory size")

                    memory[B] = C  # Загрузить константу в память
                    result_addresses.append(B)
                except struct.error as e:
                    print(f"Error reading command: {e}")
                    break
            elif command_type == 204:  # READ_MEM
                try:
                    B = struct.unpack('>H', infile.read(2))[0]
                    C = struct.unpack('>H', infile.read(2))[0]
                    D = struct.unpack('>H', infile.read(2))[0]
                    print(f"Read B={B}, C={C}, D={D}")

                    if D >= len(memory):
                        raise ValueError(f"Address D={D} exceeds memory size")
                    if C >= len(memory):
                        raise ValueError(f"Address C={C} exceeds memory size")
                    if memory[D] + B >= len(memory):
                        raise ValueError(f"Calculated address {memory[D] + B} exceeds memory size")

                    memory[C] = memory[memory[D] + B]
                    result_addresses.append(C)
                except struct.error as e:
                    print(f"Error reading command: {e}")
                    break
            elif command_type == 26:  # WRITE_MEM
                try:
                    B = struct.unpack('>H', infile.read(2))[0]
                    C = struct.unpack('>H', infile.read(2))[0]
                    print(f"Write B={B}, C={C}")

                    if C >= len(memory):
                        raise ValueError(f"Address C={C} exceeds memory size")
                    if B >= len(memory):
                        raise ValueError(f"Address B={B} exceeds memory size")

                    memory[C] = memory[B]
                    result_addresses.append(C)
                except struct.error as e:
                    print(f"Error reading command: {e}")
                    break

            elif command_type == 116:  # SHIFT_LEFT
                try:
                    B = struct.unpack('>H', infile.read(2))[0]
                    C = struct.unpack('>H', infile.read(2))[0]
                    D = struct.unpack('>H', infile.read(2))[0]
                    print(f"Shift left B={B}, C={C}, D={D}")

                    if B >= len(memory):
                        raise ValueError(f"Address B={B} exceeds memory size")
                    if C >= len(memory):
                        raise ValueError(f"Address C={C} exceeds memory size")
                    if D >= len(memory):
                        raise ValueError(f"Address D={D} exceeds memory size")

                    memory[B] = memory[C] << memory[D]
                    result_addresses.append(B)
                except struct.error as e:
                    print(f"Error reading command: {e}")
                    break


        for addr in result_addresses:
            csv_writer.writerow([addr, memory[addr]])

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Интерпретатор для УВМ")
    parser.add_argument('--binary', type=str, help="Путь к бинарному файлу")
    parser.add_argument('--result', type=str, help="Путь к файлу для вывода результатов")

    args = parser.parse_args()
    execute_program(args.binary, args.result)
    print(f"Результаты выполнения программы сохранены в {args.result}")
