import sys, re

A = "0"
C = "1"
T = "2"
G = "3"

past = ""

memory = []
stack = []

PUSH = ["CCT", "CCC", "CCA", "CCG"] # P
COUT = ["TGT", "TGC"] # C
INPUT = ["ATA", "ATC", "ATT"] # I

ADD = ["GCT", "GCC", "GCA", "GCG"] # A
SUB = ["TCT", "TCC", "TCA", "TCG", "AGT", "AGC"] # S
MULTIPLY = ["ATG"] # M
DIVIDE = ["GAT", "GAC"] # D
MODULUS = ["CAT", "CAC"] # H

COPY = ["GTT", "GTC", "GTA", "GTG"] # V
TURN = ["ACA", "ACC", "ACT", "ACG"] # T

FORGET = ["TTT", "TTC"] # F
REMEMBER = ["CGT", "CGC", "CGA", "CGG", "AGA", "AGG"] # R

LOOP = ["CTT", "CTC", "CTA", "CTG", "TTA", "TTG"] # L
STOP = ["TAA", "TAG", "TGA"] # STOP

source  = open(sys.argv[1], "r").read()
instructions = source.split()
# instructions = re.findall('...', source)

loopdict = {}
loopstack = []
for ip, instruction in enumerate(instructions):
	if len(instruction) != 3:
		continue
	if instruction in LOOP:
		loopstack.append(ip)
	elif instruction in STOP:
		if instructions[ip-1] in PUSH:
			pass
		else:
			b = loopstack.pop()
			loopdict[b] = ip
			loopdict[ip] = b

ip = 0
while ip != len(instructions):
	instruction = instructions[ip]
	if len(instruction) != 3:
		continue
	if instruction in PUSH:
		ip += 1
		if len(instructions[ip]) != 3:
			instructions[ip] = "AAA"
		value1 = int(instructions[ip].replace("A", A).replace("C", C).replace("T", T).replace("G", G), 4)
		stack.append(value1)
	elif instruction in COPY:
		stack.append(stack[len(stack)-1])

	elif instruction in ADD:
		value1 = stack.pop(len(stack)-1)
		value2 = stack.pop(len(stack)-1)
		value3 = value1 + value2
		stack.append(value3)
	elif instruction in SUB:
		value1 = stack.pop(len(stack)-1)
		value2 = stack.pop(len(stack)-1)
		value3 = value1 - value2
		stack.append(value3)
	elif instruction in MULTIPLY:
		value1 = stack.pop(len(stack)-1)
		value2 = stack.pop(len(stack)-1)
		value3 = value1 * value2
		stack.append(value3)
	elif instruction in DIVIDE:
		value1 = stack.pop(len(stack)-1)
		value2 = stack.pop(len(stack)-1)
		value3 = int(value1 / value2)
		stack.append(value3)
	elif instruction in MODULUS:
		value1 = stack.pop(len(stack)-1)
		value2 = stack.pop(len(stack)-1)
		value3 = int(value1 % value2)
		stack.append(value3)

	elif instruction in FORGET:
		value1 = stack.pop(len(stack)-1)
		memory.append(value1)
	elif instruction in REMEMBER:
		value1 = memory.pop()
		stack.append(value1)

	elif instruction in LOOP:
		if stack[len(stack)-1] == 0:
			ip = loopdict[ip]
	elif instruction in STOP:
		if len(stack)!=0 and stack[len(stack)-1] != 0:
			ip = loopdict[ip]

	elif instruction in COUT:
		value1 = stack.pop(len(stack)-1)
		print(chr(value1), end="")
	elif instruction in INPUT:
		value1 = input()
		for val in value1:
			stack.append(ord(val))
	elif instruction in TURN:
		stack.reverse()
	ip+=1