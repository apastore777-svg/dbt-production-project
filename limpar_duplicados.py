import os
import yaml

# Caminho raiz do projeto DBT
root_path = os.path.expanduser("~/meu_projeto/models")

# Dicionário para rastrear sources já vistos
sources_seen = {}

# Percorre todas as pastas e arquivos YAML
for subdir, dirs, files in os.walk(root_path):
    for file in files:
        if file.endswith("schema.yml"):
            file_path = os.path.join(subdir, file)
            with open(file_path, 'r') as f:
                try:
                    content = yaml.safe_load(f)
                except yaml.YAMLError:
                    print(f"Erro ao ler {file_path}, pulando...")
                    continue

            if not content:
                continue

            updated = False

            # Se houver sources, verificar duplicatas
            if "sources" in content:
                new_sources = []
                for source in content["sources"]:
                    for table in source.get("tables", []):
                        unique_id = f"{source['name']}.{table['name']}"
                        if unique_id in sources_seen:
                            print(f"Duplicado encontrado e removido: {unique_id} em {file_path}")
                            updated = True
                        else:
                            sources_seen[unique_id] = file_path
                            new_sources.append(source)
                            updated = updated or (len(new_sources) != len(content["sources"]))

                content["sources"] = new_sources

            # Sobrescreve o arquivo sem duplicatas
            if updated:
                with open(file_path, 'w') as f:
                    yaml.dump(content, f, sort_keys=False)
                print(f"Arquivo atualizado: {file_path}")

print("Limpeza de sources duplicados concluída!")

