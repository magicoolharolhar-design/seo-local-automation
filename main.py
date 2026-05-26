#!/usr/bin/env python3
"""
Ponto de entrada principal da automação SEO Local.

Este script automatiza a geração de conteúdo para Google Meu Negócio,
incluindo descrições SEO, FAQs e posts para Google Business Profile.
"""

import argparse
from pathlib import Path

from src.config import Config
from src.csv_handler import CSVHandler
from src.content_generator import ContentGenerator


def main():
    """Função principal do script."""
    # Configuração de argumentos
    parser = argparse.ArgumentParser(
        description='Automação SEO Local - Geração de conteúdo para Google Meu Negócio'
    )
    parser.add_argument(
        '-i', '--input',
        type=str,
        default=str(Config.DEFAULT_INPUT_FILE),
        help=f'Arquivo CSV de entrada (padrão: {Config.DEFAULT_INPUT_FILE})'
    )
    parser.add_argument(
        '-o', '--output',
        type=str,
        default=str(Config.DEFAULT_OUTPUT_FILE),
        help=f'Arquivo CSV de saída (padrão: {Config.DEFAULT_OUTPUT_FILE})'
    )
    parser.add_argument(
        '--create-sample',
        action='store_true',
        help='Cria um arquivo CSV de exemplo'
    )
    
    args = parser.parse_args()
    
    print("=" * 60)
    print("🚀 Automação SEO Local - Google Meu Negócio")
    print("=" * 60)
    
    # Garante que os diretórios existem
    Config.ensure_directories()
    
    # Cria arquivo de exemplo se solicitado
    if args.create_sample:
        sample_path = Config.INPUT_DIR / 'empresas_exemplo.csv'
        CSVHandler.create_sample_file(sample_path)
        return
    
    # Valida configurações
    try:
        Config.validate()
    except ValueError as e:
        print(f"❌ Erro de configuração: {e}")
        return
    
    # Caminhos dos arquivos
    input_path = Path(args.input)
    output_path = Path(args.output)
    
    # Verifica se o arquivo de entrada existe
    if not input_path.exists():
        print(f"❌ Arquivo de entrada não encontrado: {input_path}")
        print(f"\n💡 Dica: Use --create-sample para criar um arquivo de exemplo")
        return
    
    print(f"\n📂 Arquivo de entrada: {input_path}")
    print(f"📂 Arquivo de saída: {output_path}")
    
    # Lê as empresas do CSV
    print("\n📖 Lendo empresas do CSV...")
    try:
        businesses = CSVHandler.read_businesses(input_path)
        print(f"✅ {len(businesses)} empresa(s) encontrada(s)")
    except Exception as e:
        print(f"❌ Erro ao ler CSV: {e}")
        return
    
    # Inicializa o gerador de conteúdo
    print("\n🤖 Inicializando gerador de conteúdo com IA...")
    generator = ContentGenerator()
    
    # Processa cada empresa
    print("\n⚙️  Processando empresas...\n")
    for i, business in enumerate(businesses, 1):
        print(f"[{i}/{len(businesses)}] {business.nome_empresa}")
        try:
            generator.generate_all_content(business)
            print(f"   ✅ Concluído!\n")
        except Exception as e:
            print(f"   ❌ Erro: {e}\n")
            # Continua para a próxima empresa
            continue
    
    # Salva os resultados
    print("\n💾 Salvando resultados...")
    try:
        CSVHandler.save_results(businesses, output_path)
        print("\n" + "=" * 60)
        print("✨ Processo concluído com sucesso!")
        print("=" * 60)
    except Exception as e:
        print(f"❌ Erro ao salvar resultados: {e}")


if __name__ == '__main__':
    main()
