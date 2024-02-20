def get_unique_list(list, sort = True):
    unique = []
    unique_list = set(list)

    for number in unique_list:
        unique.append(number)

    if (sort): unique.sort()

    return unique