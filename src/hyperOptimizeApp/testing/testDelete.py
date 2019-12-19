import numpy as np
successRateList = []

successRateList.append(1)
successRateList.append(2)
successRateList.append(3)

print(successRateList)

lastSuccess = successRateList.__getitem__(len(successRateList) - 2)

print(lastSuccess)


a = np.random.rand(10,3)
print(a)
print(np.round(a, decimals=0))