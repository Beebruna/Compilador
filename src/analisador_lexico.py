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
        
        
    def classifica_token(self, estado, lexema, erro):
        if erro:
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

   
    def SCANNER(self):
        estado = 0
        lexema = []
        erro = False

        
        while self.posicao <= len(self.fonte): # <= ? Não existe a posição = len(self.fonte), deveria ser apenas <, não?
            try:
                if self.fonte[self.posicao] not in alfabeto:
                    raise AlphabetError
                estado = tabela_de_transicao[estado][self.chave(self.fonte[self.posicao], estado)]

            except AlphabetError:
                if (len(lexema) > 0) and (estado in estados_finais):
                    return self.classifica_token(estado, lexema, erro)
                erro = 1
                print(f'ERRO LÉXICO - Caractere inválido na linguagem: {self.fonte[self.posicao]}. Linha {self.linha}, coluna {self.coluna}')
                lexema.append(self.fonte[self.posicao])

            except KeyError:
                if (len(lexema)) > 0 and (estado in estados_finais.keys()):
                    return self.classifica_token(estado, lexema, erro)
                elif estado == 19:
                    erro = True
                    print(f'ERRO LÉXICO - Exponenciação incompleta. Linha {self.linha}, coluna {self.coluna}') 
                    return self.classifica_token(estado, lexema, erro)
                
            except IndexError:
                if len(lexema) > 0:
                    return self.classifica_token(estado, lexema, erro)
                else: 
                    break

            else:
                if self.fonte[self.posicao] == '\n':
                    self.linha = self.linha + 1
                    self.coluna = 0
                    
                    if estado == 8:
                        print(f'ERRO LÉXICO - Literal incompleto. Linha {self.linha}, coluna {self.coluna}')
                        return self.classifica_token(estado, lexema, True)
                    elif estado == 10:
                        print(f'ERRO LÉXICO - Comentário incompleto. Linha {self.linha}, coluna {self.coluna}')
                        return self.classifica_token(estado, lexema, True)

                if (self.fonte[self.posicao] not in delimitadores) or (estado == 8 or estado == 10):
                    lexema.append(self.fonte[self.posicao])

            finally:
                self.posicao = self.posicao + 1
                self.coluna = self.coluna + 1

        return TOKEN('EOF', 'EOF', None)
    
if __name__ == "__main__":
    al = AnalisadorLexico('..\\Teste\\teste3.txt')
    
    while True:
        token = al.SCANNER()
        print(token)
        
        if token.classe == 'EOF':
            break