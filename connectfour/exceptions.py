class ExceptionConnect4(Exception):
    def __init__(self):
        super().__init__()


class ExceptionLimite(ExceptionConnect4):

    def __init__(self, message):
        super().__init__()
        self.message = message

    def __str__(self):
        return self.message


class ExceptionColonne(ExceptionConnect4):

    def __init__(self, message):
        super().__init__()
        self.message = message

    def __str__(self):
        return self.message


class ExceptionVide(ExceptionConnect4):

    pass
