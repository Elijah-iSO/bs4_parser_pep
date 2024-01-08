class ParserFindTagException(Exception):
    """Вызывается, когда парсер не может найти тег."""
    pass


class NotMatchStatuses(Exception):
    """Вызывается, когда статусы на страницах не совпадают."""
    pass
