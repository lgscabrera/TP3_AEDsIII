# Compilador e flags
CC = gcc
CFLAGS = -Wall -Wextra -O2 -g
LDFLAGS = -lm

# Nome do executável
TARGET = programa

# Arquivos fonte
SOURCES = base.c algorithms.c
HEADERS = algorithms.h

# Objetos
OBJECTS = $(SOURCES:.c=.o)

# Regra padrão
all: $(TARGET)

# Linkagem
$(TARGET): $(OBJECTS)
	$(CC) $(CFLAGS) -o $(TARGET) $(OBJECTS) $(LDFLAGS)
	@echo "✅ Compilação concluída! Execute com: ./$(TARGET) <arquivo_grafo>"

# Compilação dos objetos
%.o: %.c $(HEADERS)
	$(CC) $(CFLAGS) -c $< -o $@

# Limpeza
clean:
	rm -f $(OBJECTS) $(TARGET)
	@echo "Arquivos objeto e executável removidos"

# Limpeza completa (inclui possíveis arquivos temporários)
clean-all: clean
	rm -f *.dat *.txt *.out
	@echo "Limpeza completa realizada"

# Execução padrão com exemplo
run: $(TARGET)
	@if [ -f instancia_exemplo.dat ]; then \
		./$(TARGET) instancia_exemplo.dat; \
	else \
		echo "Arquivo instancia_exemplo.dat não encontrado!"; \
		echo "Uso: ./$(TARGET) <arquivo_grafo>"; \
	fi

# Cria um grafo de exemplo para teste
create-example:
	@echo "Criando grafo de exemplo (instancia_exemplo.dat)..."
	@echo "5 6" > instancia_exemplo.dat
	@echo "0 1 4" >> instancia_exemplo.dat
	@echo "0 2 2" >> instancia_exemplo.dat
	@echo "1 2 1" >> instancia_exemplo.dat
	@echo "1 3 5" >> instancia_exemplo.dat
	@echo "2 3 8" >> instancia_exemplo.dat
	@echo "2 4 10" >> instancia_exemplo.dat
	@echo "Grafo exemplo criado: instancia_exemplo.dat"

# Ajuda
help:
	@echo "Comandos disponíveis:"
	@echo "  make          - Compila o programa"
	@echo "  make clean    - Remove arquivos objeto e executável"
	@echo "  make clean-all- Limpeza completa"
	@echo "  make run      - Executa com o arquivo padrão (instancia_exemplo.dat)"
	@echo "  make create-example - Cria um grafo exemplo para teste"
	@echo "  make help     - Mostra esta mensagem de ajuda"
	@echo ""
	@echo "Uso: ./$(TARGET) <arquivo_grafo>"

# Phony targets
.PHONY: all clean clean-all run create-example help