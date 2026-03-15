def get_query_string_filter(request, *args: str) -> dict[str, str]:
    """
    쿼리 파라미터에서 허용된 키만 필터링하여 반환합니다.
    Args:
        request: DRF Request 객체
        *args: 허용할 쿼리 파라미터 키 목록
    Returns:
        허용된 키-값 쌍의 딕셔너리
    """
    return {
        key: value
        for key, value in request.query_params.items()
        if key in args
    }
