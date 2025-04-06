#!/usr/bin/env python
#
# Copyright (c) 2025 Tim Klein Nijenhuis <tim@hetorus.nl>
#
# This file is part of compyler, a TAPL compiler.

from ..expressions.expression import Expression
from ..tokens.var_decl_token import VarDeclToken
from .statement import Statement


class VarDeclStatement(Statement):
    def __init__(self, var_decl_token: VarDeclToken, initial_value: Expression | None = None):
        super().__init__()
        self._var_decl_token: VarDeclToken = var_decl_token
        self._initial_value: Expression | None = initial_value

    @property
    def var_decl_token(self) -> VarDeclToken:
        return self._var_decl_token

    @var_decl_token.setter
    def var_decl_token(self, var_decl_token: VarDeclToken) -> None:
        self._var_decl_token: VarDeclToken = var_decl_token

    @property
    def initial_value(self) -> Expression | None:
        return self._initial_value

    @initial_value.setter
    def initial_value(self, initial_value: Expression | None) -> None:
        self._initial_value: Expression | None = initial_value

    def c_code(self) -> str:
        keyword: str = self.var_decl_token.var_type.keyword
        name: str = self.var_decl_token.name

        # if we have an initial value, also generate code for that
        if self.initial_value:
            initial_value: str = self.initial_value.c_code()
            return f"{keyword} {name} = {initial_value};"

        # otherwise it's a default initialized variable
        return f"{keyword} {name};"

    def __str__(self) -> str:
        return self.var_decl_token.__str__()

    def __repr__(self) -> str:
        return f"<VarDeclStatement {self.var_decl_token.__repr__()}"
