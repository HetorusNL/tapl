class Type:
    def __init__(self, keyword: str, *syntactic_sugar: str):
        self._keyword: str = keyword
        self._syntactic_sugar: list[str] = list(syntactic_sugar)

    @property
    def keyword(self) -> str:
        """returns the keyword of the type"""
        return self._keyword

    @property
    def syntactic_sugar(self) -> list[str]:
        """returns the syntactic sugar list of the type"""
        return self._syntactic_sugar

    @property
    def all_keywords(self) -> list[str]:
        """returns, in any order, the keyword and syntactic sugars as list"""
        keywords: list[str] = [self.keyword]
        keywords.extend(self.syntactic_sugar)
        return keywords
