from .ast import AST


class CodeGenerator:
    def __init__(self, ast: AST):
        self._ast = ast

    def generate_c(self) -> list[str]:
        # add the initial lines of code
        c_code: list[str] = [
            "#include <stdbool.h>\n",
            "#include <stdio.h>\n",
            "\n",
            "int main(int argc, char** argv) {\n",
            '    printf("hello world!\\n");\n',
        ]

        # compile the expressions in the AST to code
        for index, expression in enumerate(self._ast.expressions):
            expression_code: str = expression.c_code()
            c_code.append(
                f'    printf("expression {index+1}: %d\\n", {expression_code});\n'
            )

        # add the ending lines of code
        c_code.append("}\n")

        # return the full source code
        return c_code
