#!/usr/bin/env python3
"""
Analyze validation files (Excel) and display their structure.
"""
import pandas as pd
import numpy as np
import sys
import os

def analyze_validation_file(file_path=None):
    """Analyze an Excel validation file.
    
    Args:
        file_path: Path to the Excel file. If None, tries multiple default locations.
    """
    if file_path is None:
        # Try multiple possible paths
        possible_paths = [
            '/app/validation_master.xlsx',  # Docker path
            'validation_master.xlsx',       # Current directory
        ]
        for path in possible_paths:
            if os.path.exists(path):
                file_path = path
                break
        
        if file_path is None:
            print("❌ Error: Could not find validation_master.xlsx")
            print(f"   Searched in: {possible_paths}")
            print("   Usage: python analyze_validation_file.py [path/to/validation.xlsx]")
            return None, []
    
    if not os.path.exists(file_path):
        print(f"❌ Error: File not found: {file_path}")
        return None, []
    
    print(f"📂 Processing file: {file_path}")
    
    try:
        # Lire le fichier Excel
        print("📋 ANALYSE DU FICHIER DE VALIDATION FOURNI")
        print("=" * 60)
        
        # Lire toutes les feuilles
        excel_file = pd.ExcelFile(file_path)
        print(f"📊 Feuilles disponibles: {excel_file.sheet_names}")
        
        # Analyser chaque feuille
        for sheet_name in excel_file.sheet_names:
            print(f"\n📑 FEUILLE: {sheet_name}")
            print("-" * 40)
            
            try:
                df = pd.read_excel(file_path, sheet_name=sheet_name)
                print(f"   Dimensions: {df.shape[0]} lignes × {df.shape[1]} colonnes")
                print(f"   Colonnes: {list(df.columns)}")
                
                # Afficher un aperçu
                if not df.empty:
                    print("\n   📋 Aperçu (5 premières lignes):")
                    print(df.head().to_string())
                    
            except Exception as e:
                print(f"   ❌ Erreur lecture feuille {sheet_name}: {e}")
        
        # Se concentrer sur la feuille principale (probablement la première)
        main_sheet = excel_file.sheet_names[0]
        df_main = pd.read_excel(file_path, sheet_name=main_sheet)
        
        print(f"\n🎯 ANALYSE DÉTAILLÉE DE LA FEUILLE PRINCIPALE: {main_sheet}")
        print("=" * 60)
        print(f"Nombre de pays: {len(df_main)}")
        
        # Identifier les colonnes clés
        colonnes = df_main.columns.tolist()
        print(f"\n📊 COLONNES IDENTIFIÉES:")
        for i, col in enumerate(colonnes, 1):
            print(f"   {i:2d}. {col}")
        
        # Analyser le contenu
        print(f"\n📈 ÉCHANTILLON DE DONNÉES:")
        if not df_main.empty:
            # Afficher quelques pays pour analyse
            for i in range(min(3, len(df_main))):
                print(f"\n   Pays {i+1}: {df_main.iloc[i].to_dict()}")
        
        return df_main, excel_file.sheet_names
        
    except Exception as e:
        print(f"❌ Erreur lors de l'analyse: {e}")
        return None, []

if __name__ == "__main__":
    # Get file path from command line argument if provided
    file_path = sys.argv[1] if len(sys.argv) > 1 else None
    result, sheets = analyze_validation_file(file_path)
    sys.exit(0 if result is not None else 1)