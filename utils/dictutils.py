def zip_responses(precepts, response):
    mapping = {}

    zippedItem = zip(precepts, response)
    for item in zippedItem:
        mapping[item[0]] = item[1]
    
    return mapping