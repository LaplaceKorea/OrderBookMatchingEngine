from order_matching.custom_enum import CustomEnum


class Execution(CustomEnum):
    """Order execution."""

    MARKET = 0
    LIMIT = 1
