def get_query_string_filter(request, *args) -> dict[str, str]:
    return {
        key: value
        for key, value in request.query_params.items()
        if key in args
    }
