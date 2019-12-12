import numpy as np
lognr1 = "7"
lognr2 = "5"

logCalculated1 = 10 ** -int(lognr1)
logCalculated2 = 10 ** -int(lognr2)

number1 = 1
number2 = 0.1
number3 = float(0.0001)
number4 = 1e-4
number5 = 1e-7
print(type(number1))
print(type(number2))
print(type(number3))
print(type(number4))
print(type(number5))
print(type(logCalculated1))
print(type(logCalculated2))
print(np.log10(number1))
print(np.log10(number2))
print(np.log10(number3))
print(np.log10(number4))
print(np.log10(number5))

learningRateDict = {'min': number3, 'max': number3}
learningRateDict2 = dict({'min': logCalculated1, 'max': logCalculated2})

print(np.log10(learningRateDict.get('max')))
