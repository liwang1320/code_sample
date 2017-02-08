

import random

def makeTest(shiftString, offset, shiftLength, shiftAmountRight):
    #given shiftString (string 0f 0 or 1)
    #offset (where we begin shifting)
    #shiftLength (how much we shift by)
    #shiftAmountRight (shift right by this many vals)
    #print original string and ans

    print (shiftString)
    if shiftLength==0 or shiftAmountRight==0:
    	new = shiftString 
    else:
    	shiftAmountRight = shiftAmountRight%shiftLength
    	if shiftAmountRight < 0:
    		shiftAmountRight += shiftLength
    	b = shiftString[(offset+shiftLength-shiftAmountRight):(offset+shiftLength)]
    	a = shiftString[offset:(offset+shiftLength-shiftAmountRight)]

    	before = shiftString[:offset]
    	after = shiftString[(offset+shiftLength):]

    	new = before + b + a + after
    print ("\n")
    print (new) 


def makeString(length, prop):
	#created random string of 0's and 1's of length length and 
	# a 0 to 1 prop ratio 
    newStr = ""
    for i in range(length):
    	if random.random() < prop:
    		newStr+="0"
    	else:
    		newStr+="1"
    return newStr

#makeTest(makeString(16, 0.5), 4, 7, 14)
# makeTest(makeString(16, 0.4), 0, 13, 32)

#insert in vim is shift+ins

def makeAlt(length):
	#make alternating string of 0 and 1 of length length
	newStr = ""
	for i in range(length):
		if i%2==0:
			newStr+="0"
		else:
			newStr+="1"
	return newStr




a = makeString(136, 0.4)
b = makeTest(a, 3, 131, -37)

# v = makeString(257, 0.5)
# m = makeTest(v, 0, 256, 129)