# Compilador
Armazena os trabalhos da Disciplina de Compiladores


# T1 - Analisador Léxico

- [x] - Implementar uma estrutura composta heterogênea (nó, registro, classe, ...) denominada TOKEN.
* Armazenará a **classificação** da palavra e seus **atributos**.
* Possuirá três campos:
    1. **Classe**: armazenará a classificação do lexema reconhecido;
    2. **Lexema**: armazenará a palavra computada;
    3. **Tipo**: armazenará o tipo de dado do lexema: inteiro, real, literal ou NULO.
<p>

3.2 - Implementar uma estrutura de dados (*hash table*, *map*, *lista*, ...) denominada **TABELA DE SÍMBOLOS**.
1. Armazenará **tokens ID** e **palavras reservadas**.
2. Cada item da tabela será um nó do tipo TOKEN;
3. Operações permitidas: Inserção e Busca e Atualização;
4. A tabela de símbolos deverá ser preenchida com todas as palavras reservadas.
    * Os campos classe, lexema e tipo serão todos preenchidos com a própria palavra reservada

Token | Significado
:------|:------------
inicio | Delimita o início do programa
varinicio | Delimita o início da declaração de variáveis
varfim | Delimita o fim da declaração de variáveis
escreva | Imprime na saída padrão
leia | Lê da saída padrão
se | Estrutura condicional
entao | Elemento de estrutura condicional
fimse | Elemento de estrutura condicional
fim | Delimita o fim do programa
inteiro | Tipo de dado inteiro
literal | Tipo de dado literal
real | Tipo de dado real

***Palavras Reservadas da Linguagem MGOL***

3.3 - Implementar uma função SCANNER.
1. Possua o cabeçalho: ```token SCANNER (parâmetros de entrada)```
    * Retornará um único TOKEN a cada chamada;
    * SCANNER é o nome do procedimento;
    * Parâmetros de entrada serão definidos pelo programador para ajustar a leitura do arquivo fonte para palavra por palavra;