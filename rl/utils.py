def transform(data_source, bound_source, bound_target):
    ratio = (bound_target[1] - bound_target[0]) / (bound_source[1] - bound_source[0])
    data_target = (data_source - bound_source[0]) * ratio + bound_target[0]
    return data_target
