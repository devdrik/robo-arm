
def map(value, sourceMin, sourceMax, targetMin, targetMax):
    if value > sourceMax:
        value = sourceMax
    if value < sourceMin:
        value = sourceMin
    sourceRange = sourceMax - sourceMin
    targetRange = targetMax - targetMin
    mappedValue = (value - sourceMin) * targetRange/sourceRange + targetMin
    return mappedValue
    