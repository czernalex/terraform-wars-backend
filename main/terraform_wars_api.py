from ninja import NinjaAPI
from ninja.operation import Operation


class TerraformWarsAPI(NinjaAPI):
    def _parse_operation_func_path(self, operation: Operation) -> str:
        app_name = operation.view_func.__module__.split(".")[2]
        return f"{app_name}_{operation.view_func.__name__}"

    def get_openapi_operation_id(self, operation: Operation) -> str:
        return self._parse_operation_func_path(operation)
