import time
import random

def simularTarefas(quantidadeMaquinas, r):
    quantidadeTarefas = int(quantidadeMaquinas * r)
    tarefa = [random.randint(1, 100) for _ in range(quantidadeTarefas)]
    return quantidadeMaquinas, quantidadeTarefas, tarefa

def avaliarCarga(alocar, quantidadeMaquinas):
    return max(sum(alocar[i]) for i in range(quantidadeMaquinas)) # makespan máximo

def melhorMelhora(quantidadeMaquinas, tarefa, permitir_neutras=False):
    # Mudança na distribuição inicial (mais aleatória)
    alocar = [[] for _ in range(quantidadeMaquinas)]
    random.shuffle(tarefa)  # Bagunça as tarefas antes de distribuir
    for i, tarefas in enumerate(tarefa):
        alocar[i % quantidadeMaquinas].append(tarefas)  # Distribuição inicial menos balanceada

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
                    if i != k: # validar troca de tarefas, para não cair na mesma máquina
                        alocar[i].remove(tarefa)
                        alocar[k].append(tarefa)

                        novoMakespan = avaliarCarga(alocar, quantidadeMaquinas)

                        # Mudança aqui: aceitar trocas que não pioram a solução
                        if novoMakespan < novoMelhorMakespan or (permitir_neutras and novoMakespan == melhorMakespan):
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
    complexidadeR = [1.5, 2.0]  # Adicionamos 3.0 para ver se muda algo
    repeticoes = 10
    resultado = []

    for quantidadeMaquinas in valorQuantidadeMaquinas:
        for valorR in complexidadeR:
            for rep in range(1, repeticoes + 1):
                _, quantidadeTarefas, tarefa = simularTarefas(quantidadeMaquinas, valorR)
                tempo = time.time()
                melhorMakespan, iteracoes = melhorMelhora(quantidadeMaquinas, tarefa, permitir_neutras=True)  # Permitir trocas neutras
                tempoFinal = time.time() - tempo
                resultado.append(f"monotona,{quantidadeTarefas},{quantidadeMaquinas},{rep},{tempoFinal * 1000:.2f},{iteracoes},{melhorMakespan},NA")

    with open("resultados_blm_modificado.csv", "w") as excel:
        excel.write("heuristica,n,m,replicacao,tempo,iteracoes,valor,parametro\n")
        excel.write("\n".join(resultado))

if __name__ == "__main__":
    iniciarTestes()
    print("Resultados salvos em 'resultados_blm_modificado.csv'")
