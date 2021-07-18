from bitarray import bitarray
from math import floor, ceil, log2

BITS_PER_BYTE = 8


def encode(data: bitarray):
	
	data_length     = len(data) 
	num_parity_bits = _num_parity_bits_needed(data_length)
	encoded_length  = data_length + num_parity_bits + 1

	encoded = bitarray(encoded_length) 
	
	for parity_bit_index in _powers_of_two(num_parity_bits):
		encoded[parity_bit_index] = _calculate_parity(data, parity_bit_index)
	
	data_index = 0
	for encoded_index in range(3, len(encoded)):
		if not _is_power_of_two(encoded_index):
			encoded[encoded_index] = data[data_index]
			data_index += 1

	encoded[0] = _calculate_parity(encoded[1:], 0)

	return encoded

def decode(encoded: bitarray):
	
	encoded_length  = len(encoded)
	num_parity_bits = floor(log2(encoded_length - 1)) + 1
	index_of_error  = 0 

	decoded = _extract_data(encoded)

	overall_expected = _calculate_parity(encoded[1:], 0)
	overall_actual   = encoded[0]
	overall_correct  = overall_expected == overall_actual

	for parity_bit_index in _powers_of_two(num_parity_bits):
		expected = _calculate_parity(decoded, parity_bit_index)
		actual   = encoded[parity_bit_index]
		if not expected == actual:
			index_of_error += parity_bit_index

	if index_of_error and overall_correct:
		raise ValueError("Ошибки в последовательности.")
	elif index_of_error and not overall_correct:
		encoded[index_of_error] = not encoded[index_of_error]
	decoded = _extract_data(encoded)
	return decoded



def _num_parity_bits_needed(length: int):
	n = _next_power_of_two(length)
	lower_bin = floor(log2(n))
	upper_bin = lower_bin + 1
	data_bit_boundary = n - lower_bin - 1					
	return lower_bin if length <= data_bit_boundary else upper_bin

def _calculate_parity(data: bitarray, parity: int):
	
	retval = 0 
	if parity == 0: 
		for bit in data:
			retval ^= bit
	else:
		for data_index in _data_bits_covered(parity, len(data)):
			retval ^= data[data_index]
	return retval

def _data_bits_covered(parity: int, lim: int):
	
	if not _is_power_of_two(parity):
		raise ValueError("Некорректная последовательность")

	data_index  = 1
	total_index = 3 

	while data_index <= lim:
		curr_bit_is_data = not _is_power_of_two(total_index)
		if curr_bit_is_data and (total_index % (parity << 1)) >= parity:	
			yield data_index - 1 
		data_index += curr_bit_is_data
		total_index += 1
	return None

def _extract_data(encoded: bitarray):
	data = bitarray()
	for i in range(3, len(encoded)):
		if not _is_power_of_two(i):
			data.append(encoded[i])
	return data

def _next_power_of_two(n: int):
	if (not (type(n) == int)) or (n <= 0):
		raise ValueError("Число должно быть положительным")
	elif _is_power_of_two(n):
		return n << 1
	return 2 ** ceil(log2(n))

def _is_power_of_two(n: int):
	return (not (n == 0)) and ((n & (n - 1)) == 0)

def _powers_of_two(n: int):
	power, i = 1, 0
	while i < n:
		yield power
		power <<= 1
		i += 1
	return None

def bytes_to_bits(byte_stream: bytearray):
	out = bitarray()
	for byte in byte_stream:
		data = bin(byte)[2:].zfill(BITS_PER_BYTE)
		for bit in data:
			out.append(0 if bit == '0' else 1)
	return out

def bits_to_bytes(bits: bitarray):
	out = bytearray()
	for i in range(0, len(bits) // BITS_PER_BYTE * BITS_PER_BYTE, BITS_PER_BYTE):
		byte, k = 0, 0
		for bit in bits[i:i + BITS_PER_BYTE][::-1]:
			byte += bit * (1 << k)
			k += 1
		out.append(byte)

	if len(bits) % BITS_PER_BYTE:
		byte, k = 0, 0
		for bit in bits[int(len(bits) // BITS_PER_BYTE * BITS_PER_BYTE):][::-1]:
			byte += bit * (1 << k)
			k += 1
		out.append(byte)

	return out

def finding_error(value):
    data=list(value)
    data.reverse()
    c,ch,j,r,error,h,parity_list,h_copy=0,0,0,0,0,[],[],[]

    for k in range(0,len(data)):
        p=(2**c)
        h.append(int(data[k]))
        h_copy.append(data[k])
        if(p==(k+1)):
            c=c+1
            
    for parity in range(0,(len(h))):
        ph=(2**ch)
        if(ph==(parity+1)):

            startIndex=ph-1
            i=startIndex
            toXor=[]

            while(i<len(h)):
                block=h[i:i+ph]
                toXor.extend(block)
                i+=2*ph

            for z in range(1,len(toXor)):
                h[startIndex]=h[startIndex]^toXor[z]
            parity_list.append(h[parity])
            ch+=1
    parity_list.reverse()
    error=sum(int(parity_list) * (2 ** i) for i, parity_list in enumerate(parity_list[::-1]))
    
    if((error)==0):
        print('Ошибок нет')

    elif((error)>=len(h_copy)):
        print('Нельзя определить ошибки')

    else:
        print('Ошибка: ',error)

        if(h_copy[error-1]=='0'):
            h_copy[error-1]='1'

        elif(h_copy[error-1]=='1'):
            h_copy[error-1]='0'
            print('После коррекции код:- ')
        h_copy.reverse()
        print('После коррекции: ')
        print(int(''.join(map(str, h_copy))))

if __name__ == '__main__':
    print("Введите последовательность бит: ")
    bits = input("Последовательность: ")
    print("Выберите, что вы хотите сделать: ")
    print("1 - Закодировать последовательность бит")
    print("2 - Декодировать последовательность")
    print("3 - Коррекция ошибок: ")
    option = input("Ваш выбор - ")
    if (option == '1'):
        data = encode(bitarray(bits))
        print(data.to01())
    elif (option == '2'):
        data = decode(bitarray(bits))
        print(data.to01())
    elif (option == '3'):
        finding_error(bits)
        