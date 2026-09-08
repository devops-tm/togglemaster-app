#!/usr/bin/env python3
"""
AI Test Generator usando Google Gemini
Gera testes unitários automaticamente a partir do código fonte de serviços alterados.
Uso: python scripts/ai_test_generator.py --changed-files <file1> <file2> ...
"""

import os
import sys
import json
import argparse
import re
from pathlib import Path
from typing import List, Dict, Optional
import google.generativeai as genai

# ============================================================
# CONFIGURAÇÃO
# ============================================================

API_KEY = os.getenv("GEMINI_API_KEY")
if not API_KEY:
    print("ERRO: GEMINI_API_KEY não definida. Configure o secret no GitHub Actions.")
    sys.exit(1)

genai.configure(api_key=API_KEY)

# Usa o modelo mais rápido disponível no tier gratuito
MODEL = genai.GenerativeModel('gemini-1.5-flash')

# Mapeamento de serviços para seus caminhos
SERVICE_PATHS = {
    'auth-service': 'src/auth-service',
    'flag-service': 'src/flag-service',
    'targeting-service': 'src/targeting-service',
    'evaluation-service': 'src/evaluation-service',
    'analytics-service': 'src/analytics-service',
}

# ============================================================
# FUNÇÕES AUXILIARES
# ============================================================

def detect_changed_services(changed_files: List[str]) -> List[str]:
    """
    Detecta quais serviços foram alterados com base nos arquivos modificados.
    Retorna uma lista com os nomes dos serviços (ex: ['auth-service', 'flag-service'])
    """
    changed_services = set()
    
    for file_path in changed_files:
        # Normaliza o caminho
        path = Path(file_path)
        
        # Verifica se o arquivo está dentro de algum serviço
        for service_name, service_dir in SERVICE_PATHS.items():
            if str(path).startswith(service_dir):
                changed_services.add(service_name)
                break
    
    return list(changed_services)

def find_python_files(service_path: str) -> List[str]:
    """Encontra todos os arquivos Python em um serviço"""
    service_dir = Path(service_path)
    if not service_dir.exists():
        return []
    
    python_files = []
    for py_file in service_dir.rglob("*.py"):
        # Ignora __pycache__, tests, venv
        if "__pycache__" in str(py_file) or "tests" in str(py_file) or "venv" in str(py_file):
            continue
        python_files.append(str(py_file))
    
    return python_files

def read_file(filepath: str) -> str:
    """Lê o conteúdo de um arquivo"""
    with open(filepath, 'r', encoding='utf-8') as f:
        return f.read()

def generate_tests(source_code: str, filename: str, test_framework: str = "pytest") -> Optional[str]:
    """Gera testes para o código fonte usando Gemini"""
    
    # Define o prompt baseado no framework
    if test_framework == "pytest":
        test_import = "import pytest"
        assert_pattern = "assert"
    elif test_framework == "unittest":
        test_import = "import unittest"
        assert_pattern = "self.assertEqual"
    else:
        test_import = ""

    prompt = f"""
    Você é um engenheiro de QA especialista. Gere testes unitários completos para o seguinte código Python.

    Arquivo: {filename}

    Código:
    ```
    {source_code}
    ```

    Requisitos:
    1. Use {test_framework} como framework de teste
    2. Cubra casos normais, borda e exceções
    3. Inclua mocks onde necessário (ex: requests, banco de dados)
    4. Gere APENAS o código dos testes, sem explicações
    5. Seja específico e prático
    6. Use fixtures quando apropriado

    Formato de saída:
    ```python
    {test_import}
    # Testes gerados aqui
    ```
    """

    try:
        response = MODEL.generate_content(prompt)
        return response.text
    except Exception as e:
        print(f"Erro ao gerar testes para {filename}: {e}", file=sys.stderr)
        return None

def extract_test_code(response_text: str) -> str:
    """Extrai o código Python dos testes da resposta"""
    pattern = r"```python\n(.*?)```"
    match = re.search(pattern, response_text, re.DOTALL)
    if match:
        return match.group(1).strip()
    return response_text.strip()

def save_tests(test_code: str, output_path: str) -> None:
    """Salva os testes gerados em um arquivo"""
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Adiciona header informando que foi gerado por IA
    header = f'''# Testes gerados automaticamente por AI Test Generator (Gemini)
# Data: {__import__('datetime').datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
# ⚠️ Revise antes de usar em produção

'''
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(header + test_code)
    
    print(f"✅ Testes salvos em: {output_path}")

def generate_tests_for_service(service_name: str, service_path: str, test_framework: str = "pytest") -> Dict[str, str]:
    """Gera testes para todos os arquivos Python de um serviço"""
    results = {}
    python_files = find_python_files(service_path)
    
    if not python_files:
        print(f"⚠️ Nenhum arquivo Python encontrado em {service_path}")
        return results
    
    print(f"\n📦 Gerando testes para {service_name} ({len(python_files)} arquivos)")
    
    for py_file in python_files:
        print(f"  📄 Processando: {py_file}")
        source_code = read_file(py_file)
        
        if not source_code.strip():
            print(f"    ⚠️ Arquivo vazio, ignorando")
            continue
        
        # Gera os testes
        response = generate_tests(source_code, py_file, test_framework)
        
        if not response:
            print(f"    ❌ Falha ao gerar testes para {py_file}")
            continue
        
        # Extrai o código
        test_code = extract_test_code(response)
        
        if not test_code:
            print(f"    ❌ Não foi possível extrair o código de teste")
            continue
        
        # Define o caminho de saída
        relative_path = Path(py_file).relative_to(service_path)
        output_file = f"tests/{service_name}/{relative_path.parent}/test_{relative_path.stem}.py"
        
        # Salva os testes
        save_tests(test_code, output_file)
        results[py_file] = output_file
        print(f"    ✅ Testes gerados: {output_file}")
    
    return results

def generate_summary(results: Dict[str, Dict[str, str]]) -> str:
    """Gera um resumo dos testes gerados para o comentário do PR"""
    summary = "## 🤖 Testes Gerados por IA (Gemini)\n\n"
    
    if not results:
        summary += "Nenhum teste foi gerado."
        return summary
    
    total_files = 0
    total_tests = 0
    
    for service_name, files in results.items():
        summary += f"### 📦 {service_name}\n"
        for source_file, test_file in files.items():
            total_files += 1
            summary += f"- `{source_file}` → `{test_file}`\n"
        summary += "\n"
    
    summary += f"\n**Total:** {total_files} arquivo(s) de teste gerados.\n\n"
    summary += "> ⚠️ **Revise os testes antes de mesclar.** A IA pode cometer erros."
    
    return summary

# ============================================================
# MAIN
# ============================================================

def main():
    parser = argparse.ArgumentParser(
        description="Gerador de testes com IA (Gemini) para serviços alterados"
    )
    parser.add_argument(
        '--changed-files',
        nargs='+',
        help="Lista de arquivos alterados (para detectar serviços)"
    )
    parser.add_argument(
        '--service',
        help="Nome específico do serviço para gerar testes (ex: auth-service)"
    )
    parser.add_argument(
        '--framework',
        default='pytest',
        choices=['pytest', 'unittest'],
        help="Framework de teste (default: pytest)"
    )
    parser.add_argument(
        '--all',
        action='store_true',
        help="Gerar testes para todos os serviços (ignora detecção)"
    )
    parser.add_argument(
        '--output-dir',
        default='tests',
        help="Diretório de saída para os testes (default: tests)"
    )
    
    args = parser.parse_args()
    
    # ============================================================
    # 1. DETECTA QUAIS SERVIÇOS GERAR TESTES
    # ============================================================
    
    services_to_test = []
    
    if args.service:
        # Serviço específico
        if args.service in SERVICE_PATHS:
            services_to_test = [args.service]
        else:
            print(f"ERRO: Serviço '{args.service}' não encontrado")
            print(f"Serviços disponíveis: {list(SERVICE_PATHS.keys())}")
            sys.exit(1)
    
    elif args.all:
        # Todos os serviços
        services_to_test = list(SERVICE_PATHS.keys())
    
    elif args.changed_files:
        # Detecção automática baseada nos arquivos alterados
        services_to_test = detect_changed_services(args.changed_files)
        if not services_to_test:
            print("✅ Nenhum serviço foi alterado. Nada a fazer.")
            sys.exit(0)
        print(f"🔍 Serviços alterados detectados: {services_to_test}")
    
    else:
        print("ERRO: Especifique --service, --all ou --changed-files")
        parser.print_help()
        sys.exit(1)
    
    # ============================================================
    # 2. GERA TESTES PARA CADA SERVIÇO
    # ============================================================
    
    all_results = {}
    
    for service_name in services_to_test:
        service_path = SERVICE_PATHS[service_name]
        
        # Verifica se o diretório existe
        if not Path(service_path).exists():
            print(f"⚠️ Diretório do serviço não encontrado: {service_path}")
            continue
        
        # Gera os testes
        results = generate_tests_for_service(service_name, service_path, args.framework)
        if results:
            all_results[service_name] = results
    
    # ============================================================
    # 3. GERA SUMÁRIO PARA OUTPUT DO GITHUB
    # ============================================================
    
    if all_results:
        summary = generate_summary(all_results)
        
        # Salva o sumário em um arquivo para usar no workflow
        with open('test_summary.md', 'w', encoding='utf-8') as f:
            f.write(summary)
        
        print("\n" + "="*50)
        print("✅ GERAÇÃO DE TESTES CONCLUÍDA")
        print("="*50)
        print(summary)
    else:
        print("⚠️ Nenhum teste foi gerado.")
        sys.exit(1)

if __name__ == "__main__":
    main()

