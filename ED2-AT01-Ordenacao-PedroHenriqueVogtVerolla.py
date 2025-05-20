import sys
import time
import random
import copy


# ============================ UTILITÁRIOS ====================================================

comparacoes = 0

def resetaComparacoes():
    global comparacoes
    comparacoes = 0

def geraVetor(tamanho, modo):
    # Gera o vetor dependendo do modo: 'c' (crescente), 'd' (decrescente), 'r' (randomico).
    if modo == 'c':
        return list(range(1, tamanho + 1))
    elif modo == 'd':
        return list(range(tamanho, 0, -1))
    elif modo == 'r':
        return [random.randint(0, 32000) for _ in range(tamanho)]
    else:
        raise ValueError("Esse modo de geração de vetor não existe. Tente 'c' (crescente), 'd' (decrescente) ou 'r' (randomico)")
#============================================================================================================================= 



# ============================ ALGORITMOS DE ORDENAÇÃO ====================================================

#  InsertionSort
def insertionSort(vetor):
    global comparacoes
    for i in range(1, len(vetor)):
        auxiliar = vetor[i]
        j = i - 1
        while j >= 0 and vetor[j] > auxiliar:
            comparacoes += 1
            vetor[j + 1] = vetor[j]
            j -= 1
        if j >= 0:
            comparacoes += 1
        vetor[j + 1] = auxiliar
    return vetor

#  SelectionSort
def selectionSort(vetor):
    global comparacoes
    for i in range(len(vetor)):
        menor = i
        for j in range(i + 1, len(vetor)):
            comparacoes += 1
            if vetor[j] < vetor[menor]:
                menor = j
        vetor[i], vetor[menor] = vetor[menor], vetor[i]
    return vetor

#  BubbleSort
def bubbleSort(vetor):
    global comparacoes
    n = len(vetor)
    for i in range(n):
        for j in range(0, n - i - 1):
            comparacoes += 1
            if vetor[j] > vetor[j + 1]:
                vetor[j], vetor[j + 1] = vetor[j + 1], vetor[j]
    return vetor

#  MergeSort
def mergeSort(vetor):
    global comparacoes
    if len(vetor) <= 1:
        return vetor
    meio = len(vetor) // 2
    esquerda = mergeSort(vetor[:meio])
    direita = mergeSort(vetor[meio:])
    return merge(esquerda, direita)

def merge(esquerda, direita):
    global comparacoes
    aux = []
    i = j = 0
    while i < len(esquerda) and j < len(direita):
        comparacoes += 1
        if esquerda[i] <= direita[j]:
            aux.append(esquerda[i])
            i += 1
        else:
            aux.append(direita[j])
            j += 1
    aux.extend(esquerda[i:])
    aux.extend(direita[j:])
    return aux

#  QuickSort
def quickSort(vetor):
    global comparacoes
    def _quickSort(vetor, inicio, fim):
        if inicio < fim:
            pi = particiona(vetor, inicio, fim)
            _quickSort(vetor, inicio, pi - 1)
            _quickSort(vetor, pi + 1, fim)
        return vetor
    
    def particiona(vetor, inicio, fim):
        global comparacoes
        pivo = vetor[fim]
        i = inicio - 1
        for j in range(inicio, fim):
            comparacoes += 1
            if vetor[j] <= pivo:
                i += 1
                vetor[i], vetor[j] = vetor[j], vetor[i]
        vetor[i + 1], vetor[fim] = vetor[fim], vetor[i + 1]
        return i + 1
    
    return _quickSort(vetor, 0, len(vetor) - 1)

#  HeapSort
def heapSort(vetor):
    global comparacoes
    def heapify(vetor, n, i):
        global comparacoes
        maior = i
        esquerda = 2 * i + 1
        direita = 2 * i + 2
        if esquerda < n:
            comparacoes += 1
            if vetor[esquerda] > vetor[maior]:
                maior = esquerda
        if direita < n:
            comparacoes += 1
            if vetor[direita] > vetor[maior]:
                maior = direita
        if maior != i:
            vetor[i], vetor[maior] = vetor[maior], vetor[i]
            heapify(vetor, n, maior)
    
    n = len(vetor)
    for i in range(n // 2 - 1, -1, -1):
        heapify(vetor, n, i)
    for i in range(n - 1, 0, -1):
        vetor[0], vetor[i] = vetor[i], vetor[0]
        heapify(vetor, i, 0)
    return vetor

#  ShellSort
def shellSort(vetor):
    global comparacoes
    n = len(vetor)
    gap = n // 2
    while gap > 0:
        for i in range(gap, n):
            temp = vetor[i]
            j = i
            while j >= gap and vetor[j - gap] > temp:
                comparacoes += 1
                vetor[j] = vetor[j - gap]
                j -= gap
            if j >= gap:
                comparacoes += 1
            vetor[j] = temp
        gap //= 2
    return vetor
#=============================================================================================================================




#===========================================EFETIVAMENTE RODANDO O PROGRAMA NA MAIN============================================================================

if __name__ == "__main__":
    # Verifica se ta certo a entrada
    if len(sys.argv) != 3:
        print("Erro ao compilar o programa. Tente a estrutura: 'python teste.py entrada.txt saida.txt'")
        sys.exit(1)
    
    input = sys.argv[1]
    output = sys.argv[2]
    
    # Le o input
    try:
        with open(input, 'r') as f:
            linhas = f.readlinhas()
            if len(linhas) < 2:
                raise ValueError("Esse arquivo de entrada não ta certo não")
            
            tamanho = int(linhas[0].strip())
            if tamanho <= 0:
                raise ValueError("O tamanho do vetor PRECISA ser positivo")
            
            modo = linhas[1].strip()
            if modo not in ['c', 'd', 'r']:
                raise ValueError("Modo de geração de vetor invalido")
            
            # Gera um vetor para usar
            vetorOriginal = geraVetor(tamanho, modo)
            
            # Lista com nome e função de todos os algoritmos
            listaAlgoritmos = [
                ("InsertionSort", insertionSort),
                ("SelectionSort", selectionSort),
                ("BubbleSort", bubbleSort),
                ("MergeSort", mergeSort),
                ("QuickSort", quickSort),
                ("HeapSort", heapSort),
                ("ShellSort", shellSort)
            ]
            
            # Escrevendo no output:
            with open(output, 'w') as f:
                
                # Roda cada algoritmo (um por loop)
                for nome, funcao in listaAlgoritmos:
                    # cria uma copia do vetor original
                    vetorCopia = copy.deepcopy(vetorOriginal)
                    resetaComparacoes()
                    
                    # calcula o tempo gasto para executar
                    tempoIni = time.time()
                    vetorOrdenado = funcao(vetorCopia)
                    tempoFim = time.time()
                    tempoMs = (tempoFim - tempoIni) * 1000
                    
                    # Escreve no arquivo output
                    f.write(f"{nome}: {' '.join(map(str, vetorOrdenado))} "
                           f"Comparações: {comparacoes} Tempo gasto: {tempoMs:.3f} ms\n")
                    
    except FileNotFoundError:
        print(f"Erro: Arquivo '{input}' não encontrado")
        sys.exit(1)
    except ValueError as e:
        print(f"Erro: {str(e)}")
        sys.exit(1)
    except Exception as e:
        print(f"Erro: {str(e)}")
        sys.exit(1)
