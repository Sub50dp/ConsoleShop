from drf_yasg import openapi

delete_user_response_schema = {
    "200": openapi.Response(
        description="OK: The user was successfully deleted",
        examples={"application/json": {"message": "User(id=1) was deleted successfully"}},
    ),
    "401": openapi.Response(
        description="Permission denied: Non-admin User attempting to delete someone else's profile",
        examples={"application/json": {"message": "You do not have permission to perform this action"}},
    ),
    "403": openapi.Response(
        description="Forbidden: Access denied to the resource",
        examples={"application/json": {"message": "You do not have permission to perform this action"}},
    ),
    "404": openapi.Response(
        description="Not Found: The specified user was not found",
        examples={"application/json": {"message": "User not found"}},
    ),
    "417": openapi.Response(
        description="Expectation Failed: User deletion failed",
        examples={"application/json": {"message": "User has not been deleted"}},
    ),
}
