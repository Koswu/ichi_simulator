import click
import struct

memory = None

PREFIX_MAP = {
    0x0000: 'loadn',
    0x0001: 'loadp',
    0x0002: 'storep',
    0x0003: 'mov',
    0x0010: 'add',
    0x0011: 'or',
    0x0012: 'and',
    0x0013: 'not',
    0x0014: 'xor',
    0x0015: 'lshift',
    0x0016: 'rshift',
    0x0017: 'le',
    0x0018: 'gt',
    0x0019: 'eq',
    0x0020: 'jmp',
    0x0021: 'nop',
    0x0022: 'halt',
}
REG_INDEX_MAP = {
    0x00: 'ax',
    0x01: 'bx',
    0x02: 'cx',
    0x03: 'dx',
    0x10: 'pc',
    0x11: 'sp',
    0x12: 'bp',
    0x13: 'flag',
}
REVERSE_REG_INDEX_MAP = {
    v: k for k, v in REG_INDEX_MAP.items()
}
reg_values = {
    k: 0 for k in REVERSE_REG_INDEX_MAP
}


@click.command()
@click.argument('mem_file', type=click.File('rb'))
def main(mem_file):
    global memory, reg_values
    reg_values['pc'] = 0x0200
    memory = bytearray(mem_file.read())
    while True:
        pc = reg_values['pc']
        command = struct.unpack('<I', bytes(memory[pc:pc + 4]))[0]
        prefix, postfix = command >> 16, command & 0xFFFF
        try:
            operator = PREFIX_MAP[prefix]
        except IndexError:
            operator = 'err'
        print(operator)
        print(pc)
        if operator == 'loadn':
            reg_values['ax'] = postfix
        elif operator == 'loadp':
            reg_values['ax'] = struct.unpack('<H', memory[reg_values['dx']:reg_values['dx'] + 2])[0]
        elif operator == 'storep':
            dx = reg_values['dx']
            memory[dx:dx + 2] = struct.pack('<H', reg_values['ax'])
        elif operator == 'mov':
            dst, src = (postfix & 0xFF00) >> 8, postfix & 0xFF
            print("DST")
            print(dst, src)
            reg_values[REG_INDEX_MAP[dst]] = reg_values[REG_INDEX_MAP[src]]
        elif operator == 'add':
            reg_values['ax'] += reg_values['bx']
            reg_values['ax'] &= 0xFFFF
        elif operator == 'or':
            reg_values['ax'] |= reg_values['bx']
        elif operator == 'and':
            reg_values['ax'] &= reg_values['bx']
        elif operator == 'not':
            reg_values['ax'] = reg_values['ax'] ^ 0xFFFF
        elif operator == 'xor':
            reg_values['ax'] ^= reg_values['bx']
        elif operator == 'lshift':
            reg_values['ax'] <<= reg_values['bx']
            reg_values['ax'] &= 0xFFFF
        elif operator == 'rshift':
            reg_values['ax'] >>= reg_values['bx']
        elif operator == 'le':
            reg_values['flag'] = int(reg_values['ax'] < reg_values['bx'])
        elif operator == 'gt':
            reg_values['flag'] = int(reg_values['ax'] > reg_values['bx'])
        elif operator == 'eq':
            reg_values['flag'] = int(reg_values['ax'] == reg_values['bx'])
        elif operator == 'jmp' and reg_values['flag']:
            reg_values['pc'] = reg_values['dx']
            continue
        elif operator == 'nop':
            continue
        elif operator == 'halt':
            break
        else:
            reg_values['dx'] = reg_values['pc'] + 4
            reg_values['pc'] = 0x100
            print("invalid val")
            continue
        reg_values['pc'] += 4

    with open('mem_dump.bin', 'wb') as mem_dump_file:
        mem_dump_file.write(memory)


if __name__ == '__main__':
    main()
