#ifndef ALGORITHMS_H
#define ALGORITHMS_H

#include <limits.h>
#include <stdbool.h>
#include <stdlib.h>

#define INF INT_MAX

// Estrutura para fila de prioridade (heap mínimo)
typedef struct {
    int *vertices;
    int *distancias;
    int tamanho;
    int capacidade;
} MinHeap;

// Executa o algoritmo de Dijkstra a partir de um nó de origem
double dijkstra(int **matriz, int num_nos, int origem);

// Executa o algoritmo de Duan a partir de um nó de origem
double duan(int **matriz, int num_nos, int origem);

// Executa o terceiro algoritmo (Bellman-Ford) a partir de um nó de origem
double outro(int **matriz, int num_nos, int origem);

// Funções auxiliares para o heap mínimo
MinHeap* criar_heap(int capacidade);
void heapify(MinHeap* heap, int idx);
void inserir_heap(MinHeap* heap, int vertice, int distancia);
int extrair_min(MinHeap* heap);
void diminuir_chave(MinHeap* heap, int vertice, int nova_distancia);
bool heap_vazio(MinHeap* heap);
void liberar_heap(MinHeap* heap);

#endif