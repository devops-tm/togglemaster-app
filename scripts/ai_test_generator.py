#!/usr/bin/env python3
"""
AI Test Generator usando Google Gemini
Gera testes unitários para Go ou Python.
"""

import os
import sys
import json
import argparse
import re
from pathlib import Path
from typing import Optional
import google.generativeai as genai

API_KEY = os.getenv("GEMINI_API_KEY")
if not API_KEY:
    print("ERRO: GEMINI_API_KEY não definida")
    sys.exit(1)

genai.configure(api_key=API_KEY)
MODEL = genai.GenerativeModel('gemini-3.8-flash')

def detect_language(filepath: str) -> str:
    """Detecta a linguagem baseado na extensão do arquivo"""
    ext = Path(filepath).suffix.lower()
    if ext == '.go':
        return 'go'
    elif ext == '.py':
        return 'python'
    else:
        return 'unknown'

def read_file(filepath: str) -> str:
    with open(filepath, 'r', encoding='utf-8') as f:
        return f.read()

def generate_tests_go(source_code: str, filename: str) -> Optional[str]:
    """Gera testes Go usando a IA"""
    prompt = f"""
    Você é um engenheiro de QA especialista em Go. Gere testes unitários completos para o seguinte código Go.

    Arquivo: {filename}

    Código:
    ```
    {source_code}
    ```

    Requisitos:
    1. Use o pacote "testing" e a biblioteca padrão
    2. Use testify/assert ou apenas testing
    3. Cubra casos normais, borda e exceções
    4. Inclua mocks onde necessário (ex: interfaces)
    5. Gere APENAS o código dos testes, sem explicações
    6. Use o padrão: func TestXxx(t *testing.T)

    Formato de saída:
    ```go
    package main // ou o pacote correto

    import "testing"

    func TestXxx(t *testing.T) { ... }
    ```
    """
    try:
        response = MODEL.generate_content(prompt)
        return response.text
    except Exception as e:
        print(f"Erro ao gerar testes Go: {e}", file=sys.stderr)
        return None

def generate_tests_python(source_code: str, filename: str, framework: str = "pytest") -> Optional[str]:
    """Gera testes Python usando a IA"""
    test_import = "import pytest" if framework == "pytest" else "import unittest"
    prompt = f"""
    Você é um engenheiro de QA especialista em Python. Gere testes unitários completos para o seguinte código.

    Arquivo: {filename}

    Código:
    ```
    {source_code}
    ```

    Requisitos:
    1. Use {framework} como framework de teste
    2. Cubra casos normais, borda e exceções
    3. Inclua mocks onde necessário (ex: requests, banco de dados)
    4. Gere APENAS o código dos testes, sem explicações
    5. Use fixtures quando apropriado

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
        print(f"Erro ao gerar testes Python: {e}", file=sys.stderr)
        return None

def extract_code(text: str) -> str:
    """Extrai código de blocos ```lang ... ```"""
    pattern = r"```(?:\w+)?\n(.*?)```"
    match = re.search(pattern, text, re.DOTALL)
    if match:
        return match.group(1).strip()
    return text.strip()

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('source', help="Arquivo fonte")
    parser.add_argument('--lang', choices=['go', 'python', 'auto'], default='auto',
                        help="Linguagem (auto detecta)")
    parser.add_argument('-o', '--output', help="Arquivo de saída")
    parser.add_argument('-f', '--framework', default='pytest',
                        choices=['pytest', 'unittest'],
                        help="Framework Python (default: pytest)")
    args = parser.parse_args()

    if not os.path.exists(args.source):
        print(f"ERRO: Arquivo não encontrado: {args.source}")
        sys.exit(1)

    source_code = read_file(args.source)
    if not source_code.strip():
        print("ERRO: Arquivo vazio")
        sys.exit(1)

    lang = args.lang
    if lang == 'auto':
        lang = detect_language(args.source)
        print(f"Linguagem detectada: {lang}")

    if lang == 'go':
        response = generate_tests_go(source_code, args.source)
        ext = '.go'
    elif lang == 'python':
        response = generate_tests_python(source_code, args.source, args.framework)
        ext = '.py'
    else:
        print(f"ERRO: Linguagem não suportada: {lang}")
        sys.exit(1)

    if not response:
        print("❌ Falha ao gerar testes")
        sys.exit(1)

    test_code = extract_code(response)
    if not test_code:
        print("❌ Não foi possível extrair o código")
        sys.exit(1)

    if args.output:
        output_file = args.output
    else:
        base = Path(args.source).stem
        output_file = f"tests/test_{base}{ext}"

    Path(output_file).parent.mkdir(parents=True, exist_ok=True)
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(test_code)

    print(f"✅ Testes salvos em: {output_file}")

if __name__ == "__main__":
    main()