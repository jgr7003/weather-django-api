

def validate_query_params(request, response: dict, fields: list):
    for field in fields:
        query_param = request.GET.get(field)
        if query_param is None:
            response[field] = "This query param is required"


def validate_character_quantity(request, response: dict, fields: list, quantities: list):
    for (f, q) in zip(fields, quantities):
        query_param = request.GET.get(f)
        if len(query_param) != q:
            response[f] = "This field required %s character(s)" % q
