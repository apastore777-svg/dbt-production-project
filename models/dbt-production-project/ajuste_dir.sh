#!/bin/bash

# Caminho raiz do projeto dbt (executar na raiz)
ROOT_DIR=$(pwd)

echo "Organizando projeto dbt em: $ROOT_DIR"

# Pastas principais
declare -A DIRS=(
    ["staging"]="$ROOT_DIR/models/staging"
    ["marts"]="$ROOT_DIR/models/marts"
    ["snapshots"]="$ROOT_DIR/snapshots"
    ["macros"]="$ROOT_DIR/macros"
    ["tests"]="$ROOT_DIR/tests"
    ["analyses"]="$ROOT_DIR/analyses"
)

# Criar pastas se não existirem
for d in "${DIRS[@]}"; do
    mkdir -p "$d"
done

echo "Pastas principais criadas ou verificadas."

# Mover arquivos SQL para staging ou marts
for file in "$ROOT_DIR"/models/*.sql; do
    if [[ -f $file ]]; then
        filename=$(basename "$file")
        if [[ $filename == stg_* ]]; then
            mv "$file" "${DIRS["staging"]}/"
            echo "Movendo $filename → staging"
        elif [[ $filename == dim_* || $filename == fact_* ]]; then
            mv "$file" "${DIRS["marts"]}/"
            echo "Movendo $filename → marts"
        else
            echo "Ignorando $filename (não corresponde a padrão de camada)"
        fi
    fi
done

# Criar schema.yml vazio se não existir
for layer in "staging" "marts"; do
    file_path="${DIRS[$layer]}/schema.yml"
    if [ ! -f "$file_path" ]; then
        touch "$file_path"
        echo "Criando $file_path"
    fi
done

# Mover snapshots, macros, tests, analyses para suas pastas correspondentes
# (somente arquivos, sem sobrescrever pastas já existentes)
for type in "snapshots" "macros" "tests" "analyses"; do
    for file in "$ROOT_DIR/$type"/*; do
        if [[ -f $file ]]; then
            mv "$file" "${DIRS[$type]}/"
            echo "Movendo $(basename $file) → $type"
        fi
    done
done

echo "Organização completa! Projeto pronto para CI/CD."

