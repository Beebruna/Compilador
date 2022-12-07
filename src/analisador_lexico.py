from token2 import TOKEN
from tabelas import TABELA_DE_SIMBOLOS, tabela_de_transicao, letras, digitos, alfabeto, estados_finais, delimitadores
from alphabet_error import AlphabetError

class AnalisadorLexico:
    """
    Classe usada para implementar o analisador léxico

    ...

    Atributos
    ----------
    fonte: str
        string com o texto do código fonte
    posicao: int
        posição do cursor na string fonte
    linha:
        quantidade de \n + 1
    coluna:
        posição do cursor que é zerada sempre que encontra \n

    Métodos
    -------
    classifica_token(self, estado, lexema, erro)
        Classifica um token a partir do estado em que se encontra
    chave(self, caractere, estado)
        Retorna a chave correta para a combinação de caractere e estado sendo lidos
    SCANNER(self)
        Consome os caracteres do fonte e retorna um token equivalente
    """
    
    def __init__(self, nome_arquivo):
        """
        Parâmetros
        ----------
        nome_arquivo : str
            nome do caminho incluindo o caminho
        """
        
        with open(nome_arquivo, 'r') as fp:
            self.fonte = fp.read()     
        
        self.posicao = 0
        self.linha = 1
        self.coluna = 1
        
    def classifica_token(self, estado, lexema, erro=False):
        """Classifica um token a partir do estado em que se encontra

        Parâmetros
        ---------
        estado: int
            Número do estado atual referente ao autômato representado na tabela_de_transicao
        lexema: string
            Lexema do token
        erro: boolean
            Informa se foi encontrado algum erro

        Retorno
        ---------
        Token da classe TOKEN
        """

        if (erro) or (estado not in estados_finais):
            return TOKEN('ERROR', lexema, None)
        
        # Verificando se já se encontra na tabela de símbolos ou se ainda deve ser adicionado
        elif estado == 7:
            for token in TABELA_DE_SIMBOLOS:
                if token.lexema == ''.join(lexema):
                    return token

            novo_id = TOKEN('id', lexema, None)
            TABELA_DE_SIMBOLOS.append(novo_id)
            
            return novo_id
        
        # Classificação do tipo com base nos parâmetros e nas especificações do trabalho
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
        """Retorna a chave correta para a combinação de caractere e estado sendo lidos

        Essa função recebe o estado e o caractere que está sendo lido naquele estado para retornar a chave correta
        de modo a evitar a criação de uma transição para cada caractere do alfabeto
        Parâmetros
        ---------
        caractere: char
            Caractere sendo lido
        estado: int
            Estado em que determinado caractere foi recebido

        Retorno
        ---------
        chave: string
            Argumento para a transição na tabela de transições
        """
        
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
        """Essa função retorna o tipo e localização do erro
        
        Parâmetros
        ---------
        estado: int
            Estado em que determinado caractere foi recebido
        c: char
            Caractere sendo lido caso seja esse o causador do erro
        """
        
        if estado == 10:
            print(f'ERRO LÉXICO - Comentário incompleto. Linha {self.linha}, coluna {self.coluna}')
        elif estado == 8:
            print(f'ERRO LÉXICO - Literal incompleto. Linha {self.linha}, coluna {self.coluna}')
        elif estado == 19:
            print(f'ERRO LÉXICO - Exponenciação incompleta. Linha {self.linha}, coluna {self.coluna}')
        else:
            print(f'ERRO LÉXICO - Caractere inválido: "{c}". Linha {self.linha}, coluna {self.coluna}')
            
    def avanca_posicao(self):
        """Essa função incrementa os contadores da posicão e coluna"""
        
        self.posicao = self.posicao + 1
        self.coluna = self.coluna + 1
    
    def SCANNER(self):
        """Consome os caracteres do fonte e retorna um token equivalente
        
        Retorno
        ---------
        Token da classe TOKEN
        """
        
        estado = 0
        lexema = []
        erro = False

        # Executa até consumir todos os caracters do fonte
        # Python não lê o caractere EOF então a condição = para uma iteração extra que retorna o token EOF
        while self.posicao <= len(self.fonte):
            try:
                c = self.fonte[self.posicao]
                
#                 print(f'lexema={lexema}, caractere={c}, estado={estado}') 

                if c not in alfabeto and estado != 10:
                    raise AlphabetError
                
                estado = tabela_de_transicao[estado][self.chave(c, estado)]

            # Caractere não encontrado no alfabeto
            except AlphabetError:
                if len(lexema) > 0:
                    return self.classifica_token(estado, lexema)
                
                self.mensagem_erro(estado, c)
                self.avanca_posicao()
                
                return self.classifica_token(estado, c, True)

            # Encontrou um caractere que quebrou o padrão e tentou realizar uma transição que não existe naquele estado
            except KeyError:
                # Saindo do estado de comentário
                if estado == 11:
                    self.avanca_posicao()
                    estado = 0
                    lexema.clear()
                    continue       
                     
                # Por exemplo no lexema: 1e
                if estado == 19:
                    self.mensagem_erro(estado)
                    return self.classifica_token(estado, lexema, True)
                
                # Quebrou o padrão pois chegou no fim do lexema atual
                if len(lexema) > 0:
                    return self.classifica_token(estado, lexema)                
                
                # Lexemas como ! e ?
                self.mensagem_erro(estado, c)
                self.avanca_posicao()
                return self.classifica_token(estado, c, True)
                
            # Chegou ao fim do fonte
            except IndexError:
                self.avanca_posicao()
                
                if len(lexema) > 0:
                    if estado not in estados_finais:
                        self.mensagem_erro(estado)
                    
                    return self.classifica_token(estado, lexema)

                else: 
                    break

            # Transição ocorreu normalmente
            else:
                self.avanca_posicao()
                
                if c == '\n':
                    self.linha = self.linha + 1
                    self.coluna = 1
                    
                    # Literais e comentários são uma única linha
                    if estado == 8:
                        self.mensagem_erro(estado)
                        return self.classifica_token(estado, lexema, True)
                    
                    if estado == 10:
                        self.mensagem_erro(estado)
                        return self.classifica_token(estado, lexema, True)
                
                # Adicionando ao lexema
                if (c not in delimitadores) or (estado == 8 or estado == 10):
                    lexema.append(c)

        
        return TOKEN('EOF', 'EOF', None)
    
    
if __name__ == '__main__':
    al = AnalisadorLexico('..\\Teste3\\teste.txt')
    
    while True:
        
        token = al.SCANNER()
        print(token)
        
        if token.classe == 'EOF':
            break