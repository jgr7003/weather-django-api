

def validate_query_params(request, response: dict, fields: list):
    for field in fields:
        query_param = request.GET.get(field)
        if query_param is None:
            response[field] = "This query param is required"
