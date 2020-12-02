import wave
import struct

# all data in 50us increaments

# preamble - 770Hz for 4 seconds (1300us period first low 650us then high 650us) 13 samples low and 13 samples high
# sync bit - 2500Hz half cycle low and 2000Hz half cycle high (450us period first low 200us then high 250us) 4 samples low and 5 samples high

# data 0 = 2000Hz (500us period first low 250us then high 250us) 5 samples low and 5 samples high
# data 1 = 1000Hz (1000us period first low 500us then high 500us) 10 samples low and 10 samples high

# length   - two bytes, LSByte first, this is actually the length - 1

# 10 PRINT "A"
# 10 8 10 0 186 34 65 34 0 0 0

sample_rate = 20000.0 # hertz

low = -32767
high = 32767
preamble_freq = 770 # Hz
preamble_time = 4 # sec
zero = [low] * 5 + [high] * 5
one = [low] * 10 + [high] * 10
preamble_half_period = int(sample_rate / 2 / preamble_freq + 0.5)
preamble_cycle = [low] * preamble_half_period + [high] * preamble_half_period 
preamble = preamble_cycle * (preamble_time * preamble_freq)

sync = [low] * 4 + [high] * 5

start_byte = 0x55 # 0xD5 to auto run

program_data = [10, 8, 10, 0, 186, 34, 65, 34, 0, 0, 0]

def byte_2_data(byte_in):
    data_out = []
    for i in range(8):
        if byte_in & 0x80:
            data_out = data_out + one
        else:
            data_out = data_out + zero
        byte_in = byte_in << 1
    return data_out

program_checksum = 0xFF
data_length = len(program_data)
for i in range(data_length):
    program_checksum ^= program_data[i]
checksum_end = byte_2_data(program_checksum)

length_low_byte = (len(program_data) - 1) & 0xFF
length_high_byte = ((len(program_data) - 1) & 0xFF00) >> 8
length = byte_2_data(length_low_byte)
length += byte_2_data(length_high_byte)

start = byte_2_data(start_byte)

checksum_data = 0xFF
checksum_data ^= length_low_byte
checksum_data ^= length_high_byte
checksum_data ^= start_byte
checksum_start = byte_2_data(checksum_data)

program =[]
data_length = len(program_data)
for i in range(data_length):
    program += byte_2_data(program_data[i])

tape = preamble + sync + length + start + checksum_start + preamble + sync + program + checksum_end

obj = wave.open('program.wav','w')
obj.setnchannels(1) # mono
obj.setsampwidth(2) # one byte
obj.setframerate(sample_rate)

data_length = len(tape)
for i in range(data_length):
    value = tape[i]
    data = struct.pack('h', value)
    obj.writeframesraw(data) 

obj.close()

print(program_data)
print("start_byte = 0x{0:02X}".format(start_byte))
print("length bytes =",length_low_byte, length_high_byte)
print("checksum_data = 0x{0:02X}".format(checksum_data))
print("program_checksum = 0x{0:02X}".format(program_checksum))