#!/usr/bin/env python3
"""
Export validation data to CSV format with additional validation columns.
"""
import pandas as pd
import sys
import os

def export_to_csv(source_path=None, output_path=None):
    """Export validation data to CSV.
    
    Args:
        source_path: Path to source CSV file
        output_path: Path for output CSV file
    """
    if source_path is None:
        # Try multiple possible paths
        possible_paths = [
            '/app/ZLECAF_54_PAYS_DONNEES_COMPLETES.csv',  # Docker path
            'ZLECAF_54_PAYS_DONNEES_COMPLETES.csv',       # Current directory
        ]
        for path in possible_paths:
            if os.path.exists(path):
                source_path = path
                break
        
        if source_path is None:
            print("❌ Error: Could not find ZLECAF_54_PAYS_DONNEES_COMPLETES.csv")
            print(f"   Searched in: {possible_paths}")
            print("   Usage: python export_validation_csv.py [source.csv] [output.csv]")
            return None
    
    if not os.path.exists(source_path):
        print(f"❌ Error: File not found: {source_path}")
        return None
    
    if output_path is None:
        output_path = 'ZLECAF_VALIDATION.csv'
    
    print(f"📂 Reading source file: {source_path}")
    
    # Lire le fichier CSV original
    df = pd.read_csv(source_path)
    
    # Créer le fichier de validation avec colonnes supplémentaires
    validation_df = df.copy()
    
    # Ajouter les colonnes de validation
    validation_df['STATUT_VALIDATION'] = validation_df['Notes_Validation']
    validation_df['CORRECTIONS_PIB'] = ''
    validation_df['CORRECTIONS_POPULATION'] = ''
    validation_df['CORRECTIONS_IDH'] = ''
    validation_df['CORRECTIONS_SECTEURS'] = ''
    validation_df['SOURCES_SUPPLEMENTAIRES'] = ''
    validation_df['COMMENTAIRES'] = ''
    validation_df['VALIDE_PAR'] = ''
    validation_df['DATE_VALIDATION'] = ''
    
    # Réorganiser les colonnes pour faciliter la validation
    columns_final = [
        'Pays',
        'Code_ISO', 
        'STATUT_VALIDATION',
        'PIB_2024_Mds_USD',
        'CORRECTIONS_PIB',
        'Population_2024_M',
        'CORRECTIONS_POPULATION',
        'PIB_par_habitant_USD',
        'IDH_2024',
        'CORRECTIONS_IDH',
        'Rang_Afrique_IDH',
        'Croissance_2024_Pct',
        'Secteur_1',
        'Part_Secteur_1_Pct',
        'Secteur_2', 
        'Part_Secteur_2_Pct',
        'Secteur_3',
        'Part_Secteur_3_Pct',
        'CORRECTIONS_SECTEURS',
        'Sources_Principales',
        'SOURCES_SUPPLEMENTAIRES',
        'COMMENTAIRES',
        'VALIDE_PAR',
        'DATE_VALIDATION'
    ]
    
    validation_final = validation_df[columns_final]
    
    # Sauvegarder en CSV
    validation_final.to_csv(output_path, index=False, encoding='utf-8')
    
    print(f"✅ Fichier CSV de validation créé: {output_path}")
    
    # Afficher un aperçu
    print("\n📋 APERÇU DU FICHIER (5 premiers pays):")
    print(validation_final.head().to_string())
    
    # Statistiques
    status_counts = validation_df['Notes_Validation'].value_counts()
    print(f"\n📊 RÉPARTITION:")
    for status, count in status_counts.items():
        print(f"   • {status}: {count} pays")
    
    return validation_final

if __name__ == "__main__":
    # Get file paths from command line arguments if provided
    source = sys.argv[1] if len(sys.argv) > 1 else None
    output = sys.argv[2] if len(sys.argv) > 2 else None
    result = export_to_csv(source, output)
    sys.exit(0 if result is not None else 1)