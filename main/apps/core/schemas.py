from ninja import Schema


class ForbiddenErrorSchema(Schema):
    detail: str


class NotFoundErrorSchema(Schema):
    detail: str
