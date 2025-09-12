import os
import yaml

# Caminhos
project_dir = os.path.expanduser("~/meu_projeto/models")
staging_dir = os.path.join(project_dir, "staging")
marts_dir = os.path.join(project_dir, "marts")

# Criar pastas se não existirem
os.makedirs(staging_dir, exist_ok=True)
os.makedirs(marts_dir, exist_ok=True)

# --- Schema do Staging (baseado no seu schema.yml atual)
staging_schema = {
    "version": 2,
    "sources": [
        {
            "name": "raw",
            "database": "MY_DB",
            "schema": "RAW",
            "tables": [
                {"name": "customers"},
                {"name": "orders"}
            ]
        }
    ],
    "models": [
        {
            "name": "stg_customers",
            "description": "Tabela de staging para clientes",
            "columns": [
                {"name": "id", "description": "ID do cliente", "tests": ["not_null", "unique"]},
                {"name": "name", "description": "Nome do cliente", "tests": ["not_null"]},
                {"name": "email", "description": "Email do cliente"}
            ]
        },
        {
            "name": "stg_orders",
            "description": "Tabela de staging para pedidos",
            "columns": [
                {"name": "id", "description": "ID do pedido", "tests": ["not_null", "unique"]},
                {"name": "customer_id", "description": "ID do cliente que fez o pedido", "tests": ["not_null"]},
                {"name": "total_amount", "description": "Valor total do pedido"}
            ]
        }
    ]
}

# --- Schema do Marts (dependendo do staging)
marts_schema = {
    "version": 2,
    "models": [
        {
            "name": "dim_customers",
            "description": "Dimensão de clientes construída a partir do staging",
            "columns": [
                {"name": "id", "description": "ID do cliente", "tests": ["not_null", "unique"]},
                {"name": "name", "description": "Nome do cliente"},
                {"name": "email", "description": "Email do cliente"}
            ]
        },
        {
            "name": "fact_orders",
            "description": "Fatos de pedidos, agregados a partir do staging",
            "columns": [
                {"name": "id", "description": "ID do pedido", "tests": ["not_null", "unique"]},
                {"name": "customer_id", "description": "ID do cliente", "tests": ["not_null"]},
                {"name": "total_amount", "description": "Valor total do pedido"}
            ]
        }
    ]
}

# --- Salvar YAML
with open(os.path.join(staging_dir, "schema.yml"), "w") as f:
    yaml.dump(staging_schema, f, sort_keys=False)

with open(os.path.join(marts_dir, "schema.yml"), "w") as f:
    yaml.dump(marts_schema, f, sort_keys=False)

print("Arquivos schema.yml gerados para staging e marts!")

