class Expression:
    def __init__(self):
        pass

    def c_code(self) -> str:
        assert False, f"we can't generate code for a bare expression!"

    def __str__(self) -> str:
        return f""

    def __repr__(self) -> str:
        return f"<Expression >"
