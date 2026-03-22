from fastapi import Query


class PaginationParams:
    def __init__(
        self,
        skip: int = Query(0, ge=0, description="Number of records to skip"),
        limit: int = Query(10, ge=1, le=100, description="Max records to return"),
    ) -> None:
        self.skip = skip
        self.limit = limit
