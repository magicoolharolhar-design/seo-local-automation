"""
Manipulação de arquivos CSV.
"""

import pandas as pd
from pathlib import Path
from typing import List, Optional

from .models import Business


class CSVHandler:
    """Classe para leitura e escrita de arquivos CSV."""
    
    @staticmethod
    def read_businesses(file_path: Path) -> List[Business]:
        """
        Lê empresas de um arquivo CSV.
        
        Args:
            file_path: Caminho para o arquivo CSV.
            
        Returns:
            Lista de objetos Business.
        """
        if not file_path.exists():
            raise FileNotFoundError(f"Arquivo não encontrado: {file_path}")
        
        df = pd.read_csv(file_path)
        
        # Valida colunas obrigatórias
        required_columns = ['nome_empresa', 'segmento', 'cidade']
        missing_columns = [col for col in required_columns if col not in df.columns]
        
        if missing_columns:
            raise ValueError(
                f"Colunas obrigatórias ausentes: {', '.join(missing_columns)}"
            )
        
        businesses = []
        for _, row in df.iterrows():
            business = Business.from_dict(row.to_dict())
            businesses.append(business)
        
        return businesses
    
    @staticmethod
    def save_results(
        businesses: List[Business],
        output_path: Path,
        include_input_data: bool = True
    ) -> None:
        """
        Salva os resultados em um arquivo CSV.
        
        Args:
            businesses: Lista de objetos Business com conteúdo gerado.
            output_path: Caminho para o arquivo de saída.
            include_input_data: Se True, inclui dados originais no output.
        """
        data = [business.to_dict() for business in businesses]
        df = pd.DataFrame(data)
        
        # Reordena colunas para melhor visualização
        column_order = [
            'nome_empresa', 'segmento', 'cidade',
            'diferenciais', 'publico_alvo',
            'descricao_seo', 'faqs', 'posts_gbp'
        ]
        
        # Mantém apenas colunas existentes
        existing_columns = [col for col in column_order if col in df.columns]
        df = df[existing_columns]
        
        # Garante que o diretório de saída existe
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Salva o CSV
        df.to_csv(output_path, index=False, encoding='utf-8-sig')
        
        print(f"Resultados salvos em: {output_path}")
        print(f"Total de empresas processadas: {len(businesses)}")
    
    @staticmethod
    def create_sample_file(output_path: Path) -> None:
        """
        Cria um arquivo CSV de exemplo.
        
        Args:
            output_path: Caminho para o arquivo de exemplo.
        """
        sample_data = {
            'nome_empresa': [
                'Padaria Doce Sabor',
                'Clínica Sorriso Odontológico',
                'Academia Corpo & Saúde',
                'Restaurante Sabor da Terra',
                'Pet Shop Amigo Fiel'
            ],
            'segmento': [
                'Panificadora e Confeitaria',
                'Clínica Odontológica',
                'Academia e Centro de Fitness',
                'Restaurante de Comida Caseira',
                'Pet Shop e Veterinária'
            ],
            'cidade': [
                'São Paulo - SP',
                'Rio de Janeiro - RJ',
                'Belo Horizonte - MG',
                'Curitiba - PR',
                'Porto Alegre - RS'
            ],
            'diferenciais': [
                'Produtos artesanais, entrega em domicílio, ambiente familiar',
                'Atendimento especializado, tecnologia de ponta, plano de pagamento',
                'Equipamentos modernos, personal trainers, aulas em grupo',
                'Ingredientes orgânicos, receitas tradicionais, delivery',
                'Banho e tosa, veterinário 24h, produtos premium'
            ],
            'publico_alvo': [
                'Famílias e moradores do bairro',
                'Famílias e pessoas de todas as idades',
                'Jovens e adultos interessados em fitness',
                'Famílias e trabalhadores da região',
                'Tutores de pets de todos os portes'
            ]
        }
        
        df = pd.DataFrame(sample_data)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        df.to_csv(output_path, index=False, encoding='utf-8-sig')
        
        print(f"Arquivo de exemplo criado em: {output_path}")
