from token2 import TOKEN
from tabelas import TABELA_DE_SIMBOLOS, tabela_de_transicao, letras, digitos, alfabeto, estados_finais, delimitadores
from alphabet_error import AlphabetError

class AnalisadorLexico:
    
    def __init__(self, nome_arquivo):
        
        with open(nome_arquivo, 'r') as fp:
            self.fonte = fp.read()     
        
        self.posicao = 0
        self.linha = 1
        self.coluna = 1
        
    def classifica_token(self, estado, lexema, erro=False):
        
        if (erro) or (estado not in estados_finais):
            return TOKEN('ERROR', lexema, None)
        
        elif estado == 7:
            for token in TABELA_DE_SIMBOLOS:
                if token.lexema == ''.join(lexema):
                    return token

            novo_id = TOKEN('id', lexema, None)
            TABELA_DE_SIMBOLOS.append(novo_id)
            
            return novo_id

        elif estado == 16:
            tipo = 'inteiro'

        elif estado == 18 or estado == 21:
            tipo = 'real'

        elif estado == 9:
            tipo = 'literal'

        else:
            tipo = None

        return TOKEN(estados_finais[estado], lexema, tipo)


    def chave(self, caractere, estado):
        
        if (estado == 16 or estado == 18) and (caractere =='e' or caractere == 'E'):
            chave = 'e'
        elif (estado == 8 and caractere != '"') or (estado == 10 and caractere != '}'):
            chave = 'curinga'
        elif caractere in letras:
            chave = 'letra'
        elif caractere in digitos:
            chave = 'digito'
        else:
            chave = caractere

        return chave

    def mensagem_erro(self, estado, c=''):

        if estado == 10:
            print(f'ERRO LÉXICO - Comentário incompleto. Linha {self.linha}, coluna {self.coluna}')
        elif estado == 8:
            print(f'ERRO LÉXICO - Literal incompleto. Linha {self.linha}, coluna {self.coluna}')
        elif estado == 19:
            print(f'ERRO LÉXICO - Exponenciação incompleta. Linha {self.linha}, coluna {self.coluna}')
        else:
            print(f'ERRO LÉXICO - Caractere inválido: "{c}". Linha {self.linha}, coluna {self.coluna}')
            
    def avanca_posicao(self):

        self.posicao = self.posicao + 1
        self.coluna = self.coluna + 1
    
    def SCANNER(self):

        estado = 0
        lexema = []
        erro = False

        while self.posicao <= len(self.fonte):
            try:
                c = self.fonte[self.posicao]

                if c not in alfabeto and estado != 10:
                    raise AlphabetError
                
                estado = tabela_de_transicao[estado][self.chave(c, estado)]

            except AlphabetError:
                if len(lexema) > 0:
                    return self.classifica_token(estado, lexema)
                
                self.mensagem_erro(estado, c)
                self.avanca_posicao()
                
                return self.classifica_token(estado, c, True)

            except KeyError:
            
                if estado == 11:
                    self.avanca_posicao()
                    estado = 0
                    lexema.clear()
                    continue       
                     
                if estado == 19:
                    self.mensagem_erro(estado)
                    return self.classifica_token(estado, lexema, True)
                
                if len(lexema) > 0:
                    return self.classifica_token(estado, lexema)                
                
                self.mensagem_erro(estado, c)
                self.avanca_posicao()
                return self.classifica_token(estado, c, True)
                
            except IndexError:
                self.avanca_posicao()
                
                if len(lexema) > 0:
                    if estado not in estados_finais:
                        self.mensagem_erro(estado)
                    
                    return self.classifica_token(estado, lexema)
                else: 
                    break
            else:
                self.avanca_posicao()
                
                if c == '\n':
                    self.linha = self.linha + 1
                    self.coluna = 1
                    
                    if estado == 8 or estado == 10:
                        self.mensagem_erro(estado)
                        return self.classifica_token(estado, lexema, True)
                
                if (c not in delimitadores) or (estado == 8 or estado == 10):
                    lexema.append(c)

        
        return TOKEN('EOF', 'EOF', None)
    
    
if __name__ == '__main__':
    al = AnalisadorLexico(r'Fonte\fonte2.txt')
    
    while True:
        
        token = al.SCANNER()
        print(token)
        
        if token.classe == 'EOF':
            break