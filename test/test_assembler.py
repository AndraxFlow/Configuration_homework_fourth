import os 
import struct

import sys

import pytest
sys.path.append('/work/config4/src')


from assembler import assemble_line, assemble_program


def test_assemble_line_load_const():
    line = "LOAD_CONST A=3 B=26113 C=45"
    expected = struct.pack('>H', 3) + struct.pack('>H', 26113) + struct.pack('>H', 45)
    assert assemble_line(line) == expected
    
def test_assemble_big_line_load_const():
    line = "LOAD_CONST A=3 B=2611300 C=45"  # Ошибочная строка с большим B
    with pytest.raises(struct.error, match="'H' format requires 0 <= number <= 65535"):
        assemble_line(line)

def test_assemble_line_read_mem():
    line = "READ_MEM A=4 B=500 C=600 D=700"
    expected = struct.pack('>H', 4) + struct.pack('>H', 500) + struct.pack('>H', 600) + struct.pack('>H', 700)
    assert assemble_line(line) == expected

def test_assemble_line_write_mem():
    line = "WRITE_MEM A=5 B=30 C=40"
    expected = struct.pack('>H', 5) + struct.pack('>H', 30) + struct.pack('>H', 40)
    assert assemble_line(line) == expected

def test_assemble_line_shift_left():
    line = "SHIFT_LEFT A=6 B=50 C=60 D=70"
    expected = struct.pack('>H', 6) + struct.pack('>H', 50) + struct.pack('>H', 60) + struct.pack('>H', 70)
    assert assemble_line(line) == expected

def test_assemble_program(tmp_path):
    input_file = tmp_path / "test_program.txt"
    output_file = tmp_path / "program.bin"
    
    with open(input_file, 'w') as f:
        f.write("LOAD_CONST A=3 B=26113 C=45\n")
        f.write("READ_MEM A=4 B=500 C=600 D=700\n")
        f.write("WRITE_MEM A=5 B=30 C=40\n")
        f.write("SHIFT_LEFT A=6 B=50 C=60 D=70\n")
    
    assemble_program(str(input_file), str(output_file))
    
    with open(output_file, 'rb') as f:
        binary_data = f.read()
    
    expected = (
        struct.pack('>H', 3) + struct.pack('>H', 26113) + struct.pack('>H', 45) +
        struct.pack('>H', 4) + struct.pack('>H', 500) + struct.pack('>H', 600) + struct.pack('>H', 700) +
        struct.pack('>H', 5) + struct.pack('>H', 30) + struct.pack('>H', 40) +
        struct.pack('>H', 6) + struct.pack('>H', 50) + struct.pack('>H', 60) + struct.pack('>H', 70)
    )
    assert binary_data == expected