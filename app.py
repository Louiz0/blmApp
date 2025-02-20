import time
import random

# n = quantidadeTarefas
# m = quantidadeMaquinas
# replicacao = n° de repetições
# iteracoes = n° de iteracoes realizadas
# valor = valor de makespan, tempo máx de execucao de todas as maquinas para a replicacao
# r = pode ser definido como complexidade do problema na tarefa

def simularTarefas(quantidadeMaquinas, r):
    quantidadeTarefas = int(quantidadeMaquinas ** r)
    tarefa = [random.randint(1, 100) for _ in range(quantidadeTarefas)]
    return quantidadeMaquinas, quantidadeTarefas, tarefa

def avaliarCarga(alocar, quantidadeMaquinas):
    return max(sum(alocar[i]) for i in range(quantidadeMaquinas))

def melhorMelhora(quantidadeMaquinas, tarefa):
    alocar = [[] for _ in range(quantidadeMaquinas)]
    for tarefas in tarefa:
        maquinaMenorCarga = min(range(quantidadeMaquinas), key=lambda i: sum(alocar[i]))
        alocar[maquinaMenorCarga].append(tarefas)
    
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
                melhorMakespan, iteracoes = melhorMelhora(quantidadeMaquinas, tarefa)
                tempoFinal = time.time() - tempo
                resultado.append(f"monotona,{quantidadeTarefas},{quantidadeMaquinas},{rep},{tempoFinal * 1000:.2f},{iteracoes},{melhorMakespan},NA")
    
    with open("resultados_blm.csv", "w") as excel:
        excel.write("heuristica,n,m,replicacao,tempo,iteracoes,valor,parametro\n")
        excel.write("\n".join(resultado))

if __name__ == "__main__":
    iniciarTestes()
    print("Simulação concluída. Resultados salvos em 'resultados_blm.csv'")