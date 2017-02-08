import random

def reverse (bitstring, index, length):
	reverse_string = bitstring[index:index+length]
	for i in range(int (len(reverse_string)/2)):
		a = reverse_string[i];
		b = reverse_string[len(reverse_string)-1-i]
		reverse_string[i] = b
		reverse_string[len(reverse_string)-1-i] = a
	new_string = bitsting
	new_string[index:index_length] = reverse_string
	return new_string 




#print (reverse('0100011', 1, 3))

def make_01(length):
	o_one_str = ""
	for i in range(length):
		o_one_str += "01"
	return o_one_str

#print (make_01(32))

def make64():
	new_str = ""
	for i in range(64):
		if (random.random() > 0.5):
			new_str +=  "0"
		else:
			new_str += "1"
	return new_str

def reverseBit(bitstring):
	new_str = ""
	for i in range(1, len(bitstring)+1):
		new_str += bitstring[-i]
	return new_str

a = make64()
print (a)
b = reverseBit(a)
print (b)

