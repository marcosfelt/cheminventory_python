
def flatten_list(my_list):
    flat_list = []
    try:
        for sublist in my_list:
            iter(sublist)
            if type(sublist) is dict or type(sublist) is str:
                flat_list.append(sublist)
                continue
            flat_list = flat_list + flatten_list(sublist)
    except TypeError:
        for item in sublist:
            flat_list.append(item)
    return flat_list
