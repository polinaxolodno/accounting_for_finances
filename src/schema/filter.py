from pydantic import BaseModel, Field, UUID4

class Filters(BaseModel):
    limit: int | None = Field(description = 'limit', default = 10)
    offset: int | None = Field(description = 'limit', default = 0)
    order_by: str | None = Field(description = 'orderby', default = 'username')
    order_desc: bool | None = Field(description = 'orderdesc', default = True)
    search_str: str | None = Field(description = 'search_str', default = None)
