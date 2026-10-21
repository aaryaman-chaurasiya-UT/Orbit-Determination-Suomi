import numpy as np
import odlib_chaurasiya as ref
#Import numpy and my ODLib file

#Read and save every line of the text file into a list
f = open("LSPRtestinput2.txt", "r")
lines = f.readlines()

N = len(lines)
sumXi = 0.0
sumYi = 0.0
sumXiSquared = 0.0
sumYiSquared = 0.0
sumXiYi = 0.0
sumAi = 0.0
sumAiXi = 0.0
sumAiYi = 0.0
DiSign = False
sumDi = 0.0
sumDiXi = 0.0
sumDiYi = 0.0

for i in range(len(lines)):
    split = lines[i].split()
    sumXi += float(split[0])
    sumYi += float(split[1])
    sumXiSquared += float((split[0])) ** 2
    sumYiSquared += (float(split[1])) ** 2
    sumXiYi += float(split[0]) * float(split[1])

    #use convert to decimal from odlib
    Ai = ref.parse_ra_string(split[2])
    sumAi += ref.convert_hms_to_deg(Ai[0], Ai[1], Ai[2])
    sumAiXi += ref.convert_hms_to_deg(Ai[0], Ai[1], Ai[2]) * float(split[0])
    sumAiYi += ref.convert_hms_to_deg(Ai[0], Ai[1], Ai[2]) * float(split[1])

    Di = ref.parse_dec_string(split[3])

    sumDi += ref.convert_dms_to_deg(Di[0], Di[1], Di[2], Di[3])
    sumDiXi += ref.convert_dms_to_deg(Di[0], Di[1], Di[2], Di[3]) * float(split[0])
    sumDiYi += ref.convert_dms_to_deg(Di[0], Di[1], Di[2], Di[3]) * float(split[1])

matrixA = np.array([[N, sumXi, sumYi],
                   [sumXi, sumXiSquared, sumXiYi],
                   [sumYi, sumXiYi, sumYiSquared]])

matrixAInverse = np.linalg.inv(matrixA)

matrixCalcAlpha = np.array([sumAi, sumAiXi, sumAiYi])
matrixCalcDelta = np.array([sumDi, sumDiXi, sumDiYi])

matrixOutput1 = np.array(matrixAInverse @ matrixCalcAlpha)
matrixOutput2 = np.array(matrixAInverse @ matrixCalcDelta)

devAlphaSum = 0.0
devDeltaSum = 0.0

for i in range(len(lines)):
    split = lines[i].split()
    if(split[3][0:1] == "+"):
        DiSign = False
    else:
        DiSign = True
    
    Ai = ref.parse_ra_string(split[2])
    Di = ref.parse_dec_string(split[3])
    devAlphaSum += (ref.convert_hms_to_deg(Ai[0], Ai[1], Ai[2]) - float(matrixOutput1[0]) - float(matrixOutput1[1]) * float(split[0]) - float(matrixOutput1[2]) * float(split[1])) ** 2
    devDeltaSum += (ref.convert_dms_to_deg(Di[0], Di[1], Di[2], Di[3]) - float(matrixOutput2[0]) - float(matrixOutput2[1]) * float(split[0]) - float(matrixOutput2[2]) * float(split[1])) ** 2

devAlpha = np.sqrt((devAlphaSum)/(N - 3)) * 3600
devAlphaSec = devAlpha/15
devDelta = np.sqrt((devDeltaSum)/(N - 3)) * 3600

devAlphaString = str(devAlpha)
devDeltaString = str(devDelta)

roundAlphaIndex = 0
roundDeltaIndex = 0
roundSecIndex = 0

'''
for i in range(len(devAlphaString)):
    if (devAlphaString[i] == 0):
        continue
    elif(devAlphaString[i] != 0 and devAlphaString[i] == 1):
        roundAlphaIndex = i + 1
        break
    elif(devAlphaString[i] != 0 and devAlphaString[i] != 1):
        roundAlphaIndex = i
        break
        

for i in range(len(devDeltaString)):
    if (devDeltaString[i] == 0):
        continue
    elif(devDeltaString[i] != 0 and devDeltaString[i] == 1):
        roundDeltaIndex = i + 1
        break
    elif(devDeltaString[i] != 0 and devDeltaString[i] != 1):
        roundDeltaIndex = i
        break
'''

caseAlpha = int(devAlpha * 10 ** (np.abs(np.floor(np.log10(devAlpha % 1))) + 1))
caseAlphaNext = int(devAlpha * 10 ** (np.abs(np.floor(np.log10(devAlpha % 1))) + 2))
if (caseAlpha == 1):
    roundAlphaIndex = int(np.abs(np.floor(np.log10(devAlpha % 1)))) + 1
elif(caseAlpha == 9 and caseAlphaNext >= 5):
    roundAlphaIndex = int(np.abs(np.floor(np.log10(devAlpha % 1)))) + 2
else:
    roundAlphaIndex = int(np.abs(np.floor(np.log10(devAlpha % 1))))


caseSec = int(devAlphaSec * 10 ** (np.abs(np.floor(np.log10(devAlphaSec % 1))) + 1))
caseSecNext = int(devAlphaSec * 10 ** (np.abs(np.floor(np.log10(devAlphaSec % 1))) + 2))
if (caseAlpha == 1):
    roundSecIndex = int(np.abs(np.floor(np.log10(devAlphaSec % 1)))) + 1
elif(caseSec == 9 and caseSecNext >= 5):
    roundSecIndex = int(np.abs(np.floor(np.log10(devAlphaSec % 1)))) + 2
    print("i am alive")
else:
    roundSecIndex = int(np.abs(np.floor(np.log10(devAlphaSec % 1))))


caseDelta = int(devDelta * 10 ** (np.abs(np.floor(np.log10(devDelta))) + 1))
caseDeltaNext = int(devDelta * 10 ** (np.abs(np.floor(np.log10(devDelta % 1))) + 2))
print(caseDelta)
print(caseDeltaNext)
if (caseDelta == 1):
    roundDeltaIndex = int(np.abs(np.floor(np.log10(devDelta)))) + 1
elif(caseDelta == 9 and caseDeltaNext >= 5):
    roundDeltaIndex = int(np.abs(np.floor(np.log10(devDelta % 1)))) + 2
    print("i am alive")
else:
    roundDeltaIndex = int(np.abs(np.floor(np.log10(devDelta))))

     

roundedAlpha = round(devAlpha, roundAlphaIndex)
roundedAlphaSec = round(devAlphaSec, roundSecIndex)
roundedDelta = round(devDelta, roundDeltaIndex)

bArr = np.array([matrixOutput1[0], matrixOutput2[0]])

aArr = np.array([[matrixOutput1[1], matrixOutput1[2]],
                 [matrixOutput2[1], matrixOutput2[2]]])

print("***************")
print("plate constants")
print("***************")
print(f"b1: {matrixOutput1[0]} deg")
print(f"b2: {matrixOutput2[0]} deg")
print(f"a11: {matrixOutput1[1]} deg/pix")
print(f"a12: {matrixOutput1[2]} deg/pix")
print(f"a21: {matrixOutput2[1]} deg/pix")
print(f"a22: {matrixOutput2[2]} deg/pix")
print("***********")
print("uncertainty")
print("***********")
print(devAlpha)
print(devAlphaSec)
print(devDelta)
print(f"RA: {roundedAlpha} arcsec = {roundedAlphaSec} sec")
print(f"Dec: {roundedDelta} arcsec")
print("*********************************")
print("astrometry for (x,y)")
print("Enter x-value")
x = input()
print("Enter y-value")
y = input()
xyArr = np.array([float(x), float(y)])
abArr = bArr + aArr @ xyArr
sign = "-"
if (abArr[1] > 0):
    sign = "+"

print("*********************************")
print(f" RA =  {ref.dec_to_RA(abArr[0], roundSecIndex)}")
print(f"Dec = {sign}{ref.dec_to_Dec(abArr[1], roundDeltaIndex)}")