#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "algorithms.h"

// ==================== IMPLEMENTAÇÃO DO HEAP MÍNIMO ====================

MinHeap* criar_heap(int capacidade) {
    MinHeap* heap = (MinHeap*)malloc(sizeof(MinHeap));
    heap->vertices = (int*)malloc(capacidade * sizeof(int));
    heap->distancias = (int*)malloc(capacidade * sizeof(int));
    heap->tamanho = 0;
    heap->capacidade = capacidade;
    return heap;
}

void heapify(MinHeap* heap, int idx) {
    int menor = idx;
    int esquerdo = 2 * idx + 1;
    int direito = 2 * idx + 2;
    
    if (esquerdo < heap->tamanho && heap->distancias[esquerdo] < heap->distancias[menor])
        menor = esquerdo;
    
    if (direito < heap->tamanho && heap->distancias[direito] < heap->distancias[menor])
        menor = direito;
    
    if (menor != idx) {
        // Troca vértices
        int temp_vert = heap->vertices[idx];
        heap->vertices[idx] = heap->vertices[menor];
        heap->vertices[menor] = temp_vert;
        
        // Troca distâncias
        int temp_dist = heap->distancias[idx];
        heap->distancias[idx] = heap->distancias[menor];
        heap->distancias[menor] = temp_dist;
        
        heapify(heap, menor);
    }
}

void inserir_heap(MinHeap* heap, int vertice, int distancia) {
    if (heap->tamanho == heap->capacidade) return;
    
    int i = heap->tamanho;
    heap->tamanho++;
    heap->vertices[i] = vertice;
    heap->distancias[i] = distancia;
    
    while (i > 0 && heap->distancias[(i - 1) / 2] > heap->distancias[i]) {
        // Troca com o pai
        int temp_vert = heap->vertices[i];
        heap->vertices[i] = heap->vertices[(i - 1) / 2];
        heap->vertices[(i - 1) / 2] = temp_vert;
        
        int temp_dist = heap->distancias[i];
        heap->distancias[i] = heap->distancias[(i - 1) / 2];
        heap->distancias[(i - 1) / 2] = temp_dist;
        
        i = (i - 1) / 2;
    }
}

int extrair_min(MinHeap* heap) {
    if (heap->tamanho == 0) return -1;
    
    int raiz = heap->vertices[0];
    heap->tamanho--;
    heap->vertices[0] = heap->vertices[heap->tamanho];
    heap->distancias[0] = heap->distancias[heap->tamanho];
    
    heapify(heap, 0);
    return raiz;
}

void diminuir_chave(MinHeap* heap, int vertice, int nova_distancia) {
    int i;
    for (i = 0; i < heap->tamanho; i++) {
        if (heap->vertices[i] == vertice) {
            heap->distancias[i] = nova_distancia;
            break;
        }
    }
    
    while (i > 0 && heap->distancias[(i - 1) / 2] > heap->distancias[i]) {
        int temp_vert = heap->vertices[i];
        heap->vertices[i] = heap->vertices[(i - 1) / 2];
        heap->vertices[(i - 1) / 2] = temp_vert;
        
        int temp_dist = heap->distancias[i];
        heap->distancias[i] = heap->distancias[(i - 1) / 2];
        heap->distancias[(i - 1) / 2] = temp_dist;
        
        i = (i - 1) / 2;
    }
}

bool heap_vazio(MinHeap* heap) {
    return heap->tamanho == 0;
}

void liberar_heap(MinHeap* heap) {
    if (heap) {
        free(heap->vertices);
        free(heap->distancias);
        free(heap);
    }
}

// ==================== ALGORITMO DE DIJKSTRA ====================
// Complexidade: O(V²) com matriz de adjacência
double dijkstra(int **matriz, int num_nos, int origem) {
    int *dist = (int*)malloc(num_nos * sizeof(int));
    bool *visitado = (bool*)calloc(num_nos, sizeof(bool));
    double custo = 0;
    
    // Inicializa distâncias como infinito
    for (int i = 0; i < num_nos; i++) {
        dist[i] = INF;
    }
    dist[origem] = 0;
    
    // Encontra o caminho mais curto para todos os vértices
    for (int count = 0; count < num_nos - 1; count++) {
        // Encontra o vértice não visitado com menor distância
        int u = -1;
        int min_dist = INF;
        for (int i = 0; i < num_nos; i++) {
            if (!visitado[i] && dist[i] < min_dist) {
                min_dist = dist[i];
                u = i;
            }
        }
        
        if (u == -1) break; // Não há mais vértices alcançáveis
        
        visitado[u] = true;
        
        // Relaxa as arestas adjacentes
        for (int v = 0; v < num_nos; v++) {
            if (!visitado[v] && matriz[u][v] != 0 && dist[u] != INF) {
                if (dist[u] + matriz[u][v] < dist[v]) {
                    dist[v] = dist[u] + matriz[u][v];
                }
            }
        }
    }
    
    // Calcula o custo total (soma das distâncias)
    for (int i = 0; i < num_nos; i++) {
        if (dist[i] != INF) {
            custo += dist[i];
        }
    }
    
    free(dist);
    free(visitado);
    return custo;
}

// ==================== ALGORITMO DE DUAN ====================
// Implementação baseada no artigo de 2025
// Versão otimizada com heap mínimo: O((V+E) log V)
double duan(int **matriz, int num_nos, int origem) {
    int *dist = (int*)malloc(num_nos * sizeof(int));
    bool *processado = (bool*)calloc(num_nos, sizeof(bool));
    double custo = 0;
    
    // Inicializa distâncias
    for (int i = 0; i < num_nos; i++) {
        dist[i] = INF;
    }
    dist[origem] = 0;
    
    // Cria heap mínimo
    MinHeap* heap = criar_heap(num_nos);
    inserir_heap(heap, origem, 0);
    
    while (!heap_vazio(heap)) {
        int u = extrair_min(heap);
        
        if (processado[u]) continue;
        processado[u] = true;
        
        // Relaxa todas as arestas do vértice u
        for (int v = 0; v < num_nos; v++) {
            if (matriz[u][v] != 0 && !processado[v]) {
                int nova_dist = dist[u] + matriz[u][v];
                if (nova_dist < dist[v]) {
                    dist[v] = nova_dist;
                    inserir_heap(heap, v, nova_dist);
                }
            }
        }
    }
    
    // Calcula o custo total
    for (int i = 0; i < num_nos; i++) {
        if (dist[i] != INF) {
            custo += dist[i];
        }
    }
    
    free(dist);
    free(processado);
    liberar_heap(heap);
    return custo;
}

// ==================== TERCEIRO ALGORITMO: BELLMAN-FORD ====================
// Complexidade: O(V * E) - Lida com pesos negativos
double outro(int **matriz, int num_nos, int origem) {
    int *dist = (int*)malloc(num_nos * sizeof(int));
    double custo = 0;
    
    // Inicializa distâncias
    for (int i = 0; i < num_nos; i++) {
        dist[i] = INF;
    }
    dist[origem] = 0;
    
    // Relaxa todas as arestas V-1 vezes
    for (int i = 0; i < num_nos - 1; i++) {
        bool atualizado = false;
        
        // Percorre todas as arestas
        for (int u = 0; u < num_nos; u++) {
            if (dist[u] == INF) continue;
            
            for (int v = 0; v < num_nos; v++) {
                if (matriz[u][v] != 0) {
                    if (dist[u] + matriz[u][v] < dist[v]) {
                        dist[v] = dist[u] + matriz[u][v];
                        atualizado = true;
                    }
                }
            }
        }
        
        // Se não houve atualização, podemos parar mais cedo
        if (!atualizado) break;
    }
    
    // Verifica ciclo de peso negativo (opcional para grafos não orientados)
    for (int u = 0; u < num_nos; u++) {
        for (int v = 0; v < num_nos; v++) {
            if (matriz[u][v] != 0 && dist[u] != INF) {
                if (dist[u] + matriz[u][v] < dist[v]) {
                    printf("Aviso: Ciclo de peso negativo detectado!\n");
                    break;
                }
            }
        }
    }
    
    // Calcula o custo total
    for (int i = 0; i < num_nos; i++) {
        if (dist[i] != INF) {
            custo += dist[i];
        }
    }
    
    free(dist);
    return custo;
}