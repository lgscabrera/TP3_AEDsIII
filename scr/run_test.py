#!/usr/bin/env python3

import os
import subprocess
import csv
import time
import glob
from pathlib import Path

def ensure_directory_exists(directory):
    """Garante que o diretório existe."""
    Path(directory).mkdir(parents=True, exist_ok=True)

def compile_program(scr_dir):
    """Compila o programa C."""
    print("Compilando o programa C...")
    
    makefile_path = os.path.join(scr_dir, "Makefile")
    
    if os.path.exists(makefile_path):
        # Usa make se disponível
        result = subprocess.run(["make", "-C", scr_dir], capture_output=True, text=True)
        if result.returncode == 0:
            print("✓ Compilação concluída com sucesso!")
            return True
        else:
            print(f"✗ Erro na compilação: {result.stderr}")
            return False
    else:
        # Compila manualmente se Makefile não existir
        c_files = ["base.c", "algorithms.c"]
        compile_cmd = ["gcc", "-O2", "-o", "programa"] + c_files
        result = subprocess.run(compile_cmd, cwd=scr_dir, capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✓ Compilação concluída com sucesso!")
            return True
        else:
            print(f"✗ Erro na compilação: {result.stderr}")
            return False

def parse_output(output):
    """
    Faz o parsing da saída do programa C.
    Espera o formato:
    Dijkstra: <custo> <tempo>
    Duan: <custo> <tempo>
    Outro: <custo> <tempo>
    """
    results = {}
    
    lines = output.strip().split('\n')
    for line in lines:
        if line.startswith('Dijkstra:'):
            parts = line.split()
            if len(parts) >= 3:
                results['custo_dijkstra'] = float(parts[1])
                results['tempo_dijkstra'] = float(parts[2])
        elif line.startswith('Duan:'):
            parts = line.split()
            if len(parts) >= 3:
                results['custo_duan'] = float(parts[1])
                results['tempo_duan'] = float(parts[2])
        elif line.startswith('Outro:'):
            parts = line.split()
            if len(parts) >= 3:
                results['custo_bellman'] = float(parts[1])
                results['tempo_bellman'] = float(parts[2])
    
    return results

def run_program_on_instance(program_path, instance_path):
    """Executa o programa C em uma instância específica."""
    try:
        # Executa o programa
        result = subprocess.run(
            [program_path, instance_path],
            capture_output=True,
            text=True,
            timeout=300  # 5 minutos de timeout para grafos grandes
        )
        
        if result.returncode == 0:
            return parse_output(result.stdout)
        else:
            print(f"  Erro na execução: {result.stderr}")
            return None
    except subprocess.TimeoutExpired:
        print(f"  Timeout (5 min) para {os.path.basename(instance_path)}")
        return None
    except Exception as e:
        print(f"  Erro: {e}")
        return None

def extract_vertex_count(filename):
    """Extrai o número de vértices do nome do arquivo."""
    # Formato: <numero_vertices>_<tipo>_grafo.txt
    try:
        basename = os.path.basename(filename)
        parts = basename.split('_')
        if parts and parts[0].isdigit():
            return int(parts[0])
    except:
        pass
    return 0

def extract_graph_type(filename):
    """Extrai o tipo do grafo do nome do arquivo."""
    # Formato: <numero_vertices>_<tipo>_grafo.txt
    try:
        basename = os.path.basename(filename)
        parts = basename.split('_')
        if len(parts) >= 2:
            return parts[1]
    except:
        pass
    return "unknown"

def run_all_tests():
    """Executa testes em todas as instâncias."""
    
    # Define os diretórios
    script_dir = os.path.dirname(os.path.abspath(__file__))
    scr_dir = script_dir  # O script está na pasta scr
    instance_dir = os.path.join(os.path.dirname(scr_dir), "instance")
    docs_dir = os.path.join(os.path.dirname(scr_dir), "docs")
    
    # Programa compilado
    program_path = os.path.join(scr_dir, "programa")
    
    # Arquivo de resultados
    results_path = os.path.join(docs_dir, "results.csv")
    
    print("="*80)
    print("AUTOMATIZAÇÃO DE TESTES - ALGORITMOS DE CAMINHO MÍNIMO")
    print("="*80)
    print(f"Diretório SCR: {scr_dir}")
    print(f"Diretório de instâncias: {instance_dir}")
    print(f"Arquivo de resultados: {results_path}")
    print("="*80)
    print()
    
    # Verifica se o diretório de instâncias existe
    if not os.path.exists(instance_dir):
        print(f"Erro: Diretório de instâncias não encontrado: {instance_dir}")
        print("Certifique-se de que a pasta 'instance' existe e contém os arquivos .txt")
        return False
    
    # Compila o programa
    if not compile_program(scr_dir):
        print("Erro na compilação. Verifique os arquivos fonte.")
        return False
    
    # Verifica se o programa foi gerado
    if not os.path.exists(program_path):
        print(f"Erro: Programa não encontrado em {program_path}")
        return False
    
    # Encontra todos os arquivos de instância
    instance_files = glob.glob(os.path.join(instance_dir, "*_grafo.txt"))
    
    if not instance_files:
        print(f"Erro: Nenhum arquivo de instância encontrado em {instance_dir}")
        print("Procure por arquivos no formato: <vertices>_<tipo>_grafo.txt")
        return False
    
    # Ordena os arquivos por número de vértices
    instance_files.sort(key=lambda x: extract_vertex_count(x))
    
    print(f"Encontradas {len(instance_files)} instâncias para teste\n")
    
    # Prepara o arquivo CSV
    ensure_directory_exists(docs_dir)
    
    # Cabeçalho do CSV
    headers = [
        "Quantidade_Vertices",
        "Tipo_Grafo",
        "Custo_Dijkstra",
        "Tempo_Dijkstra(s)",
        "Custo_Duan",
        "Tempo_Duan(s)",
        "Custo_BellmanFord",
        "Tempo_BellmanFord(s)"
    ]
    
    results = []
    
    # Executa os testes
    for i, instance_file in enumerate(instance_files, 1):
        vertices = extract_vertex_count(instance_file)
        graph_type = extract_graph_type(instance_file)
        
        print(f"[{i:3d}/{len(instance_files)}] Testando: {os.path.basename(instance_file)}")
        print(f"          Vértices: {vertices}, Tipo: {graph_type}")
        
        # Executa o programa na instância
        output = run_program_on_instance(program_path, instance_file)
        
        if output:
            result = {
                "Quantidade_Vertices": vertices,
                "Tipo_Grafo": graph_type,
                "Custo_Dijkstra": output.get('custo_dijkstra', 0),
                "Tempo_Dijkstra(s)": output.get('tempo_dijkstra', 0),
                "Custo_Duan": output.get('custo_duan', 0),
                "Tempo_Duan(s)": output.get('tempo_duan', 0),
                "Custo_BellmanFord": output.get('custo_bellman', 0),
                "Tempo_BellmanFord(s)": output.get('tempo_bellman', 0)
            }
            results.append(result)
            print(f"          ✓ Concluído")
        else:
            print(f"          ✗ Falha na execução")
            # Adiciona linha com erro
            result = {
                "Quantidade_Vertices": vertices,
                "Tipo_Grafo": graph_type,
                "Custo_Dijkstra": "ERROR",
                "Tempo_Dijkstra(s)": "ERROR",
                "Custo_Duan": "ERROR",
                "Tempo_Duan(s)": "ERROR",
                "Custo_BellmanFord": "ERROR",
                "Tempo_BellmanFord(s)": "ERROR"
            }
            results.append(result)
        
        print()
    
    # Salva os resultados no CSV
    with open(results_path, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=headers, delimiter=';')
        writer.writeheader()
        writer.writerows(results)
    
    # Estatísticas finais
    print("="*80)
    print("RESULTADOS")
    print("="*80)
    print(f"Total de instâncias processadas: {len(instance_files)}")
    print(f"Sucessos: {sum(1 for r in results if 'ERROR' not in str(r['Custo_Dijkstra']))}")
    print(f"Falhas: {sum(1 for r in results if 'ERROR' in str(r['Custo_Dijkstra']))}")
    print(f"\nResultados salvos em: {results_path}")
    print("="*80)
    
    # Mostra um resumo dos resultados
    if results:
        print("\nRESUMO DOS RESULTADOS:")
        print("-" * 80)
        print(f"{'Vértices':<12} {'Tipo':<12} {'Dijkstra(s)':<12} {'Duan(s)':<12} {'Bellman(s)':<12}")
        print("-" * 80)
        for r in results[:10]:  # Mostra apenas os 10 primeiros
            if 'ERROR' not in str(r['Custo_Dijkstra']):
                print(f"{r['Quantidade_Vertices']:<12} {r['Tipo_Grafo']:<12} {r['Tempo_Dijkstra(s)']:<12.4f} {r['Tempo_Duan(s)']:<12.4f} {r['Tempo_BellmanFord(s)']:<12.4f}")
        if len(results) > 10:
            print(f"... e mais {len(results) - 10} resultados")
    
    return True

def main():
    """Função principal."""
    try:
        success = run_all_tests()
        if not success:
            print("\nDica: Certifique-se de que:")
            print("  1. Os arquivos .txt estão na pasta 'instance'")
            print("  2. O formato dos arquivos é: <vertices>_<tipo>_grafo.txt")
            print("  3. O programa C compila corretamente")
            print("  4. Você está executando este script a partir da pasta 'scr'")
    except KeyboardInterrupt:
        print("\n\nTestes interrompidos pelo usuário.")
    except Exception as e:
        print(f"\nErro durante a execução: {e}")

if __name__ == "__main__":
    main()