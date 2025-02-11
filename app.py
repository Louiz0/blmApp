import time
import random

# n = quantidadeTarefas
# m = quantidadeMaquinas
# replicacao = n° de repetições
# iteracoes = n° de iteracoes realizadas
# valor = valor de makespan, tempo máx de execucao de todas as maquinas para a replicacao
# r = pode ser definido como complexidade do problema na tarefa

def simularTarefas(quantidadeMaquinas, r):
    quantidadeTarefas = int(quantidadeMaquinas * r)
    tarefa = [random.randint(1, 100) for _ in range(quantidadeTarefas)]
    return quantidadeMaquinas, quantidadeTarefas, tarefa

def avaliarCarga(alocar, quantidadeMaquinas):
    return max(sum(alocar[i]) for i in range(quantidadeMaquinas)) # makespan maximo

def melhorMelhora(quantidadeMaquinas, tarefa, alocarInicial):
    alocar = alocarInicial[:]
    melhorMakespan = avaliarCarga(alocar, quantidadeMaquinas)
    teveMelhora = True
    iteracoes = 0
    
    while teveMelhora:
        teveMelhora = False
        iteracoes += 1
        melhorSwap = None
        novoMelhorMakespan = melhorMakespan
        
        for i in range(quantidadeMaquinas):
            tarefaSemAlteracao = alocar[i][:]
            for tarefa in tarefaSemAlteracao:
                for k in range(quantidadeMaquinas):
                    if i != k: # validar troca de  tarefas, para nao cair na mesma maquina
                        alocar[i].remove(tarefa)
                        alocar[k].append(tarefa)

                        novoMakespan = avaliarCarga(alocar, quantidadeMaquinas)
                        
                        if novoMakespan < novoMelhorMakespan:
                            novoMelhorMakespan = novoMakespan
                            melhorSwap = (tarefa, i, k)
                        
                        alocar[k].remove(tarefa)
                        alocar[i].append(tarefa)
        
        if melhorSwap:
            tarefa, i, k = melhorSwap
            alocar[i].remove(tarefa)
            alocar[k].append(tarefa)
            melhorMakespan = novoMelhorMakespan
            teveMelhora = True

    return melhorMakespan, iteracoes

def melhorMelhoraRepetir(quantidadeMaquinas, tarefa, reinicializacoes):
    melhorMakespanGlobal = float('inf')
    melhorAlocacaoGlobal = None

    for _ in range(reinicializacoes):
        # Gera uma nova solução inicial aleatória
        alocarInicial = [[] for _ in range(quantidadeMaquinas)]
        for t in tarefa:
            maquina = random.randint(0, quantidadeMaquinas - 1)
            alocarInicial[maquina].append(t)

        melhor_makespan_local, iteracoes_local = melhorMelhora(quantidadeMaquinas, tarefa, alocarInicial)

        if melhor_makespan_local < melhorMakespanGlobal:
            melhorMakespanGlobal = melhor_makespan_local
            melhorAlocacaoGlobal = alocarInicial
            iteracoesGlobal = iteracoes_local

    return melhorMakespanGlobal, iteracoesGlobal

def iniciarTestes():
    valorQuantidadeMaquinas = [10, 20, 50]
    complexidadeR = [1.5, 2.0]
    repeticoes = 10
    resultado = []
    
    for quantidadeMaquinas in valorQuantidadeMaquinas:
        for valorR in complexidadeR:
            for rep in range(1, repeticoes + 1):
                _, quantidadeTarefas, tarefa = simularTarefas(quantidadeMaquinas, valorR)
                tempo = time.time()
                melhorMakespan, iteracoes = melhorMelhoraRepetir(quantidadeMaquinas, tarefa, 10)  # Chama a nova função com 10 reinicializações
                tempoFinal = time.time() - tempo
                resultado.append(f"monotona,{quantidadeTarefas},{quantidadeMaquinas},{rep},{tempoFinal:.2f},{iteracoes},{melhorMakespan},NA")
    
    with open("resultados_blm.csv", "w") as excel:
        excel.write("heuristica,n,m,replicacao,tempo,iteracoes,valor,parametro\n")
        excel.write("\n".join(resultado))

if __name__ == "__main__":
    iniciarTestes()
    print("Resultados salvos em 'resultados_blm.csv'")