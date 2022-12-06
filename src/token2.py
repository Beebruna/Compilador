class TOKEN:
    def __init__(self, classe, lexema, tipo):
        self.classe = classe
        self.lexema = ''.join(lexema)
        self.tipo = tipo
    
    
    def __str__(self):
        return f'Classe={self.classe}, lexema={self.lexema}, Tipo={self.tipo}'