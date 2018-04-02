def get_all_fields(items, depth=1):
    '''Recursive function for getting all keys in dictionary.'''

    fields = set()

    if isinstance(items, pd.DataFrame):
        items = items.to_dict(orient='records')

    if isinstance(items, list):
        for item in items:
            for key in item.keys():
                if isinstance(item[key], dict) and depth > 0:
                    fields.update(get_all_fields(item[key], depth=depth - 1))
                else:
                    fields.add(key)

    elif isinstance(items, dict):
        for key in items.keys():
            if isinstance(items[key], dict) and depth > 0:
                fields.update(get_all_fields(items[key], depth=depth - 1))
            else:
                fields.add(key)

    else:
        raise

    return fields


def get_ambiguous_field(obj, possible_names):
    '''Function for getting dict value that doesn\'t have one certain key.'''

    for n in possible_names:
        res = obj.get(n)
        if res is not None:
            return res


def get_multi(obj, fields):
    query = 'obj'
    for pf in fields:
        query += f'.get("{pf}")'

    return eval(query)
