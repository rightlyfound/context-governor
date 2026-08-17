def format_user(user_id: int) -> str:
    return f"user-{user_id}"


def handle() -> str:
    return format_user("42")
