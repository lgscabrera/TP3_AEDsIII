import os
import sys
import random
import math
from pathlib import Path

def ensure_directory_exists(directory):
    """Garante que o diretório existe."""
    Path(directory).mkdir(parents=True, exist_ok=True)

def generate_erdos_renyi(n, p, seed=None):
    """Gera grafo Erdős-Rényi G(n,p)."""
    if seed:
        random.seed(seed)
    
    edges = []
    for i in range(n):
        for j in range(i + 1, n):
            if random.random() < p:
                weight = random.randint(1, 100)
                edges.append((i, j, weight))
    
    return n, edges

def generate_watts_strogatz(n, k, p, seed=None):
    """Gera grafo Watts-Strogatz."""
    if seed:
        random.seed(seed)
    
    if k % 2 != 0:
        k += 1
    
    edges = set()
    
    # Cria anel regular
    for i in range(n):
        for j in range(1, k // 2 + 1):
            neighbor = (i + j) % n
            u, v = sorted([i, neighbor])
            edges.add((u, v))
    
    # Rewiring
    edges_list = list(edges)
    for u, v in edges_list:
        if random.random() < p:
            edges.remove((u, v))
            while True:
                new_v = random.randint(0, n - 1)
                if new_v != u:
                    u_new, v_new = sorted([u, new_v])
                    if (u_new, v_new) not in edges:
                        edges.add((u_new, v_new))
                        break
    
    # Adiciona pesos
    result_edges = [(u, v, random.randint(1, 100)) for u, v in edges]
    return n, result_edges

def generate_barabasi_albert(n, m, seed=None):
    """Gera grafo Barabási-Albert."""
    if seed:
        random.seed(seed)
    
    if m >= n:
        m = n - 1
    
    edges = []
    degrees = [0] * n
    
    # Grafo inicial completo com m+1 nós
    for i in range(m + 1):
        for j in range(i + 1, m + 1):
            weight = random.randint(1, 100)
            edges.append((i, j, weight))
            degrees[i] += 1
            degrees[j] += 1
    
    # Adiciona novos nós
    for new_node in range(m + 1, n):
        total_degree = sum(degrees[:new_node])
        if total_degree == 0:
            total_degree = 1
        
        targets = set()
        while len(targets) < m:
            r = random.random()
            cumsum = 0
            for node in range(new_node):
                prob = degrees[node] / total_degree
                cumsum += prob
                if r < cumsum:
                    targets.add(node)
                    break
        
        for target in targets:
            weight = random.randint(1, 100)
            edges.append((target, new_node, weight))
            degrees[new_node] += 1
            degrees[target] += 1
    
    return n, edges

def generate_complete_graph(n, seed=None):
    """Gera grafo completo."""
    if seed:
        random.seed(seed)
    
    edges = []
    for i in range(n):
        for j in range(i + 1, n):
            weight = random.randint(1, 100)
            edges.append((i, j, weight))
    
    return n, edges

def generate_regular_graph(n, d, seed=None):
    """Gera grafo regular aleatório."""
    if seed:
        random.seed(seed)
    
    if d >= n:
        d = n - 1
    if (d * n) % 2 != 0:
        d -= 1
    
    if d <= 0:
        return n, []
    
    # Algoritmo de configuração
    max_attempts = 10
    for _ in range(max_attempts):
        edges = set()
        stubs = []
        for i in range(n):
            stubs.extend([i] * d)
        
        random.shuffle(stubs)
        
        for i in range(0, len(stubs), 2):
            if i + 1 < len(stubs):
                u, v = stubs[i], stubs[i + 1]
                if u != v:
                    u, v = sorted([u, v])
                    edges.add((u, v))
        
        if len(edges) >= n * d // 2:
            result_edges = [(u, v, random.randint(1, 100)) for u, v in edges]
            return n, result_edges
    
    # Fallback: grafo menos regular
    return generate_erdos_renyi(n, d/n, seed)

def save_graph(filename, n, edges):
    """Salva o grafo em arquivo."""
    with open(filename, 'w') as f:
        f.write(f"{n} {len(edges)}\n")
        for u, v, w in edges:
            f.write(f"{u} {v} {w}\n")

def generate_single_graph(graph_type, n, output_dir, args):
    """Gera um único grafo."""
    seed = random.randint(0, 2**32 - 1)
    
    generators = {
        "erdos": lambda: generate_erdos_renyi(n, args[0] if args else 0.01, seed),
        "watts": lambda: generate_watts_strogatz(n, int(args[0]) if args else 4, 
                                                  args[1] if len(args) > 1 else 0.3, seed),
        "barabasi": lambda: generate_barabasi_albert(n, int(args[0]) if args else 3, seed),
        "complete": lambda: generate_complete_graph(n, seed),
        "regular": lambda: generate_regular_graph(n, int(args[0]) if args else 3, seed)
    }
    
    if graph_type not in generators:
        print(f"Tipo desconhecido: {graph_type}")
        return False
    
    try:
        n, edges = generators[graph_type]()
        
        if len(edges) < n - 1:
            return False
        
        filename = f"{n}_{graph_type}_grafo.txt"
        filepath = os.path.join(output_dir, filename)
        save_graph(filepath, n, edges)
        return True
    except Exception as e:
        print(f"Erro: {e}")
        return False

def generate_all_graphs(num_graphs_per_type, min_vertices, max_vertices, output_dir, graph_types=None):
    """Gera múltiplos grafos."""
    
    if graph_types is None:
        graph_types = ["erdos", "watts", "barabasi", "complete", "regular"]
    
    # Gera números de vértices (distribuição logarítmica)
    vertex_counts = []
    if num_graphs_per_type == 1:
        vertex_counts = [(min_vertices + max_vertices) // 2]
    else:
        log_min = math.log(min_vertices)
        log_max = math.log(max_vertices)
        for i in range(num_graphs_per_type):
            fraction = i / (num_graphs_per_type - 1)
            log_value = log_min + fraction * (log_max - log_min)
            vertex_counts.append(int(math.exp(log_value)))
        vertex_counts = sorted(list(dict.fromkeys(vertex_counts)))
    
    # Argumentos padrão
    default_args = {
        "erdos": [0.01],
        "watts": [4, 0.3],
        "barabasi": [3],
        "complete": [],
        "regular": [3]
    }
    
    ensure_directory_exists(output_dir)
    
    print(f"\n{'='*70}")
    print(f"GERADOR DE GRAFOS")
    print(f"{'='*70}")
    print(f"Grafos por tipo: {num_graphs_per_type}")
    print(f"Vértices: {min_vertices} - {max_vertices}")
    print(f"Tipos: {', '.join(graph_types)}")
    print(f"Valores: {vertex_counts}")
    print(f"{'='*70}\n")
    
    total_success = 0
    total_attempts = 0
    
    for graph_type in graph_types:
        print(f"\n--- {graph_type.upper()} ---")
        args = default_args.get(graph_type, [])
        
        for n in vertex_counts:
            print(f"  Gerando {graph_type} com {n} vértices...", end=" ", flush=True)
            
            success = False
            for attempt in range(5):
                if generate_single_graph(graph_type, n, output_dir, args):
                    success = True
                    break
            
            total_attempts += 1
            if success:
                total_success += 1
                print("✓")
            else:
                print("✗")
    
    print(f"\n{'='*70}")
    print(f"RESUMO: {total_success}/{total_attempts} gerados com sucesso")
    print(f"Taxa: {(total_success/total_attempts*100):.1f}%")
    print(f"Local: {os.path.abspath(output_dir)}")
    print(f"{'='*70}\n")

def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="Gerador de Grafos")
    parser.add_argument('-n', '--num-graphs', type=int, default=5,
                       help='Número de grafos por tipo')
    parser.add_argument('-min', '--min-vertices', type=int, default=500,
                       help='Mínimo de vértices')
    parser.add_argument('-max', '--max-vertices', type=int, default=10000,
                       help='Máximo de vértices')
    parser.add_argument('-t', '--types', nargs='+',
                       help='Tipos de grafo')
    parser.add_argument('-o', '--output-dir', default='.',
                       help='Diretório de saída')
    
    args = parser.parse_args()
    
    if args.types is None:
        args.types = ["erdos", "watts", "barabasi", "complete", "regular"]
    
    generate_all_graphs(args.num_graphs, args.min_vertices, args.max_vertices,
                       args.output_dir, args.types)

if __name__ == "__main__":
    main()