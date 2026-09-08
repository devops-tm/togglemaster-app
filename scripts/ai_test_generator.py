#!/usr/bin/env python3
"""
AI Test Generator usando Google Gemini
Gera testes unitários auto-suficientes para Go ou Python.
"""

import os
import sys
import json
import argparse
import re
import time
from pathlib import Path
from typing import Optional

API_KEY = os.getenv("GEMINI_API_KEY")
if not API_KEY:
    print("ERRO: GEMINI_API_KEY não definida")
    sys.exit(1)

# Tenta usar a nova API (google.genai) primeiro
try:
    from google import genai
    client = genai.Client(api_key=API_KEY)
    USE_NEW_API = True
    print("Usando API google.genai (recomendada)")
except ImportError:
    import google.generativeai as genai
    genai.configure(api_key=API_KEY)
    USE_NEW_API = False
    print("Usando API google.generativeai (fallback)")

def generate_with_retry(prompt: str, model_name: str = "gemini-3.8-flash", max_retries: int = 5) -> Optional[str]:
    """
    Gera conteúdo com retry automático para erros 503 (sobrecarga) e 500.
    """
    for attempt in range(max_retries):
        try:
            if USE_NEW_API:
                # Nova API: google.genai
                response = client.models.generate_content(
                    model=model_name,
                    contents=prompt
                )
                return response.text
            else:
                model = genai.GenerativeModel(model_name)
                response = model.generate_content(prompt)
                return response.text
        except Exception as e:
            error_msg = str(e)
            # Erros de sobrecarga ou indisponibilidade
            if "503" in error_msg or "UNAVAILABLE" in error_msg or "500" in error_msg:
                wait_time = 2 ** attempt  # backoff exponencial: 1,2,4,8,16
                print(f"⚠️ Tentativa {attempt+1}/{max_retries} falhou: {error_msg}")
                print(f"   Aguardando {wait_time}s antes de tentar novamente...")
                time.sleep(wait_time)
            else:
                print(f"❌ Erro não recuperável: {e}")
                return None
    print("❌ Todas as tentativas falharam.")
    return None

def detect_language(filepath: str) -> str:
    ext = Path(filepath).suffix.lower()
    return 'go' if ext == '.go' else 'python' if ext == '.py' else 'unknown'

def read_file(filepath: str) -> str:
    with open(filepath, 'r', encoding='utf-8') as f:
        return f.read()

def generate_tests_go(source_code: str, filename: str) -> Optional[str]:
    prompt = f"""
    Você é um engenheiro de QA especialista em Go. Gere testes unitários COMPLETOS E AUTO-SUFICIENTES para o seguinte código.

    IMPORTANTE: Os testes devem ser executáveis ISOLADAMENTE, sem depender do código original.
    Use apenas a biblioteca padrão do Go (testing). NÃO use testify ou outros frameworks externos.

    Arquivo: {filename}

    Código original:
    ```
    {source_code}
    ```

    Requisitos:
    1. Use APENAS o pacote "testing"
    2. Não importe pacotes do projeto original
    3. Crie funções auxiliares (mocks) dentro do próprio arquivo de teste
    4. Cubra cenários: sucesso, erro, borda
    5. Gere APENAS o código dos testes, sem explicações

    Formato de saída (exemplo):
    ```go
    package main

    import "testing"

    // Funções auxiliares (mocks) internas
    func mockConnectDB() string {{
        return "mock-db-string"
    }}

    func TestSomething(t *testing.T) {{
        result := mockConnectDB()
        expected := "mock-db-string"
        if result != expected {{
            t.Errorf("expected %v, got %v", expected, result)
        }}
    }}
    ```
    """
    return generate_with_retry(prompt, "gemini-3.8-flash")

def generate_tests_python(source_code: str, filename: str, framework: str = "pytest") -> Optional[str]:
    test_import = "import pytest" if framework == "pytest" else "import unittest"
    prompt = f"""
    Você é um engenheiro de QA especialista em Python. Gere testes unitários AUTO-SUFICIENTES para o seguinte código.

    IMPORTANTE: Os testes devem ser executáveis ISOLADAMENTE, sem depender do código original.
    Não importe módulos do projeto. Use mocks/stubs internos.

    Arquivo: {filename}

    Código original:
    ```
    {source_code}
    ```

    Requisitos:
    1. Use {framework}
    2. Não dependa de código externo
    3. Defina funções auxiliares (mocks) dentro do próprio arquivo
    4. Cubra cenários de sucesso e erro
    5. Gere APENAS o código dos testes

    Formato de saída:
    ```python
    {test_import}
    # Funções auxiliares (mocks)
    def mock_db():
        return "mock-db"

    def test_xxx():
        assert mock_db() == "mock-db"
    ```
    """
    return generate_with_retry(prompt, "gemini-3.8-flash")

def extract_code(text: str) -> str:
    pattern = r"```(?:\w+)?\n(.*?)```"
    match = re.search(pattern, text, re.DOTALL)
    if match:
        return match.group(1).strip()
    return text.strip()

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('source', help="Arquivo fonte")
    parser.add_argument('--lang', choices=['go', 'python', 'auto'], default='auto')
    parser.add_argument('-o', '--output', help="Arquivo de saída (sem extensão)")
    parser.add_argument('-f', '--framework', default='pytest', choices=['pytest', 'unittest'])
    args = parser.parse_args()

    if not os.path.exists(args.source):
        print(f"ERRO: Arquivo não encontrado: {args.source}")
        sys.exit(1)

    source_code = read_file(args.source)
    if not source_code.strip():
        print("ERRO: Arquivo vazio")
        sys.exit(1)

    lang = args.lang if args.lang != 'auto' else detect_language(args.source)
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

    output_file = args.output + ext if args.output else f"tests/test_{Path(args.source).stem}{ext}"
    Path(output_file).parent.mkdir(parents=True, exist_ok=True)
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(test_code)

    print(f"✅ Testes salvos em: {output_file}")

if __name__ == "__main__":
    main()
