def normalize_query_param(value):
    return value if len(value) > 1 else value[0]


def normalize(params):
    params_non_flat = params.to_dict(flat=False)
    return {k: normalize_query_param(v) for k, v in params_non_flat.items()}