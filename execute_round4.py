#!/usr/bin/env python3
"""
Script para ejecutar la Ronda 4 del método Delphi
"""
import json
import sys
import os

# Cambiar al directorio del notebook
os.chdir('/Users/alex/tesis/hyperpersonalization')

# Cargar el notebook
with open('app/notebooks/37-delphi-with-anchors-52.ipynb', 'r') as f:
    nb = json.load(f)

print("="*80)
print("EJECUTANDO RONDA 4 DEL MÉTODO DELPHI")
print("="*80)

# Extraer y ejecutar todas las celdas necesarias en orden
# Necesitamos ejecutar desde el inicio para tener todas las variables definidas

code_cells = []
for i, cell in enumerate(nb['cells']):
    if cell['cell_type'] == 'code':
        source = ''.join(cell.get('source', []))
        code_cells.append((i, source))

print(f"\nTotal de celdas de código a ejecutar: {len(code_cells)}")
print("\nEjecutando celdas en orden...")

# Crear un namespace global para mantener el estado
namespace = {}

# Ejecutar todas las celdas de código en orden
for idx, (cell_num, source) in enumerate(code_cells):
    try:
        # Detectar si es una celda de Ronda 4
        is_round4 = 'semilla = 4' in source and 'delphi_4_prompt' in source
        
        if is_round4:
            print(f"\n{'='*60}")
            print(f"⚡ EJECUTANDO CELDA {cell_num} - RONDA 4")
            print(f"{'='*60}")
        
        # Ejecutar el código
        exec(source, namespace)
        
        if is_round4:
            print(f"✅ Celda {cell_num} ejecutada exitosamente")
            
            # Mostrar un preview del resultado si está disponible
            if 'delphi_4_results' in namespace:
                results = namespace['delphi_4_results']
                if results:
                    lines = results.split('\n')
                    preview = '\n'.join(lines[-10:]) if len(lines) > 10 else results
                    print(f"\nÚltimas líneas del resultado:")
                    print(preview[:500] + "..." if len(preview) > 500 else preview)
        
    except Exception as e:
        print(f"\n❌ Error en celda {cell_num}: {str(e)}")
        if is_round4:
            print(f"   Continuando con la siguiente celda...")
            continue
        # Para celdas no-Round4, continuar silenciosamente

print("\n" + "="*80)
print("EJECUCIÓN COMPLETADA")
print("="*80)

# Verificar que df_round tenga datos de 4 rondas
if 'df_round' in namespace:
    df = namespace['df_round']
    rounds = sorted(df['round_id'].unique())
    print(f"\n✅ df_round contiene datos de {len(rounds)} rondas: {rounds}")
    print(f"   Total de registros: {len(df)}")
else:
    print("\n⚠️  df_round no encontrado en el namespace")

print("\nGuardando el notebook actualizado...")

# Actualizar las salidas en el notebook con los resultados
# (Esto es opcional, pero ayuda a que el notebook muestre los resultados)

try:
    with open('app/notebooks/37-delphi-with-anchors-52.ipynb', 'w') as f:
        json.dump(nb, f, indent=1)
    print("✅ Notebook guardado exitosamente")
except Exception as e:
    print(f"⚠️  Error guardando notebook: {e}")

print("\n🎉 ¡Listo! Ahora puedes ejecutar las celdas de análisis de convergencia.")
