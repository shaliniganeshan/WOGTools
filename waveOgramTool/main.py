def process(value):
    value=range(value)
    sortlist= lambda value:(sorted(i) for i in range(value))
    print(sortlist)
    return sortlist

process(25)
