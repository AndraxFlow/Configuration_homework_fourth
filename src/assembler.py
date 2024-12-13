import struct

def assemble_line(line):
    if line.startswith("LOAD_CONST"):
        _, A, B, C = line.split()
        A = int(A.split('=')[1])
        B = int(B.split('=')[1])
        C = int(C.split('=')[1])
        return struct.pack('>H', A) + struct.pack('>H', B) + struct.pack('>H', C)
    
    elif line.startswith("READ_MEM"):
        _, A, B, C, D = line.split()
        A = int(A.split('=')[1])
        B = int(B.split('=')[1])
        C = int(C.split('=')[1])
        D = int(D.split('=')[1])
        return struct.pack('>H', A) + struct.pack('>H', B) + struct.pack('>H', C) + struct.pack('>H', D)
    elif line.startswith("WRITE_MEM"):
        _, A, B, C = line.split()
        A = int(A.split('=')[1])
        B = int(B.split('=')[1])
        C = int(C.split('=')[1])
        return struct.pack('>H', A) + struct.pack('>H', B) + struct.pack('>H', C)

    elif line.startswith("SHIFT_LEFT"):
        _, A, B, C, D = line.split()
        A = int(A.split('=')[1])
        B = int(B.split('=')[1])
        C = int(C.split('=')[1])
        D = int(D.split('=')[1])
        return struct.pack('>H', A) + struct.pack('>H', B) + struct.pack('>H', C) + struct.pack('>H', D)
    
    return b''

def assemble_program(input_file, output_file):
    with open(input_file, 'r') as infile, open(output_file, 'wb') as outfile:
        for line in infile:
            binary_command = assemble_line(line.strip())
            if binary_command:
                outfile.write(binary_command)


if __name__ == '__main__':
    # Тестовый вызов
    input_program = 'test_program.txt'  # Исходная программа
    output_binary = 'program.bin'       # Выходной бинарный файл

    assemble_program(input_program, output_binary)
    print(f"Программа ассемблирована в {output_binary}")
