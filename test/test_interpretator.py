import os
import struct
import csv
from interpretator import execute_program

def test_execute_program_load_const(tmp_path):
    binary_file = tmp_path / "program.bin"
    output_file = tmp_path / "result.csv"
    
    # Создаем бинарный файл с командой LOAD_CONST
    with open(binary_file, 'wb') as f:
        f.write(struct.pack('>H', 169))  # A = 169
        f.write(struct.pack('>H', 1023))  # B = 1023
        f.write(struct.pack('>H', 45))  # C = 45
    
    execute_program(str(binary_file), str(output_file))
    
    with open(output_file, 'r') as f:
        reader = csv.reader(f)
        rows = list(reader)
    
    assert rows[0] == ["Address", "Value"]
    print(rows[0])
    try:
        assert rows[1] == ["1023", "45"]
    except:
        raise IndexError('list index out of range, второй строки не существует')

def test_execute_program_write_mem(tmp_path):
    binary_file = tmp_path / "program.bin"
    output_file = tmp_path / "result.csv"
    
    # Создаем бинарный файл с командами WRITE_MEM
    with open(binary_file, 'wb') as f:
        f.write(struct.pack('>H', 26))  # A = 26
        f.write(struct.pack('>H', 1023))  # B = 1023
        f.write(struct.pack('>H', 1022))  # C = 1022
    
    execute_program(str(binary_file), str(output_file))
    
    with open(output_file, 'r') as f:
        reader = csv.reader(f)
        rows = list(reader)
    
    assert rows[0] == ["Address", "Value"]
    assert rows[1] == ["1022", "0"]

def test_execute_program_shift_left(tmp_path):
    binary_file = tmp_path / "program.bin"
    output_file = tmp_path / "result.csv"
    
    # Создаем бинарный файл с командой SHIFT_LEFT
    with open(binary_file, 'wb') as f:
        f.write(struct.pack('>H', 116))  # A = 116
        f.write(struct.pack('>H', 1023))  # B = 1023
        f.write(struct.pack('>H', 1022))  # C = 1022
        f.write(struct.pack('>H', 1))  # D = 1 (Shift by 1)
    
    execute_program(str(binary_file), str(output_file))
    
    with open(output_file, 'r') as f:
        reader = csv.reader(f)
        rows = list(reader)
    
    assert rows[0] == ["Address", "Value"]
    assert rows[1] == ["1023", "0"]  # Assuming initial values of memory are 0
