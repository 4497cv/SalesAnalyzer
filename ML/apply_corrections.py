"""
Aplica correcciones manuales a ML/tf_idf_matrix_clases.csv
basadas en la lectura completa de ML/summaries.json.
"""
import sys, unicodedata
import pandas as pd

sys.stdout.reconfigure(encoding='utf-8')

def norm(s):
    return unicodedata.normalize('NFC', str(s))

# Mapa de correcciones: chat_normalizado -> nueva_clase
CORRECTIONS = {
    # ── T2 Jaime 47559 ── Seguimiento de Ventas (seller checking if client needs toner) ──
    "T2 Jaime 47559/08-08-2025": "Seguimiento de Ventas",
    "T2 Jaime 47559/10-02-2026": "Seguimiento de Ventas",
    "T2 Jaime 47559/10-03-2026": "Seguimiento de Ventas",
    "T2 Jaime 47559/10-04-2025": "Seguimiento de Ventas",
    "T2 Jaime 47559/10-06-2025": "Seguimiento de Ventas",
    "T2 Jaime 47559/15-01-2024": "Seguimiento de Ventas",
    "T2 Jaime 47559/16-02-2026": "Seguimiento de Ventas",
    "T2 Jaime 47559/16-11-2023": "Seguimiento de Ventas",
    "T2 Jaime 47559/18-01-2024": "Seguimiento de Ventas",
    "T2 Jaime 47559/18-08-2025": "Seguimiento de Ventas",
    "T2 Jaime 47559/20-02-2026": "Seguimiento de Ventas",
    "T2 Jaime 47559/22-08-2024": "Seguimiento de Ventas",
    "T2 Jaime 47559/23-04-2024": "Seguimiento de Ventas",
    "T2 Jaime 47559/24-02-2026": "Seguimiento de Ventas",
    "T2 Jaime 47559/26-12-2024": "Seguimiento de Ventas",
    "T2 Jaime 47559/27-12-2023": "Seguimiento de Ventas",
    "T2 Jaime 47559/29-05-2024": "Seguimiento de Ventas",
    "T2 Jaime 47559/31-05-2024": "Seguimiento de Ventas",
    "T2 Jaime 47559/12-09-2025": "Seguimiento de Ventas",
    "T2 Jaime 47559/12-08-2025": "Seguimiento de Ventas",
    "T2 Jaime 47559/19-06-2024": "Seguimiento de Ventas",
    "T2 Jaime 47559/16-06-2025": "Seguimiento de Ventas",
    # T2 Jaime 47559 ── Facturación_Documentos
    "T2 Jaime 47559/09-10-2024": "Facturación_Documentos",
    "T2 Jaime 47559/10-12-2025": "Facturación_Documentos",
    "T2 Jaime 47559/11-01-2025": "Facturación_Documentos",
    "T2 Jaime 47559/12-02-2025": "Facturación_Documentos",
    "T2 Jaime 47559/17-09-2025": "Facturación_Documentos",
    "T2 Jaime 47559/20-06-2024": "Facturación_Documentos",
    "T2 Jaime 47559/26-11-2025": "Facturación_Documentos",
    "T2 Jaime 47559/29-11-2023": "Facturación_Documentos",
    "T2 Jaime 47559/24-10-2024": "Facturación_Documentos",
    # T2 Lesli 47721
    "T2 Lesli 47721/11-04-2026": "Facturación_Documentos",
    "T2 Lesli 47721/13-04-2026": "Facturación_Documentos",
    "T2 Lesli 47721/29-12-2025": "Facturación_Documentos",
    "T2 Lesli 47721/24-03-2026": "Seguimiento de Ventas",
    # T4 Carnes selec compras 19256 Sel
    "T4  Carnes selec compras 19256 Sel/05-03-2026": "Cotización/Presupuesto",
    "T4  Carnes selec compras 19256 Sel/11-02-2026": "Facturación_Documentos",
    "T4  Carnes selec compras 19256 Sel/13-03-2026": "Gestión de Pedidos/Entregas",
    "T4  Carnes selec compras 19256 Sel/19-02-2026": "Seguimiento de Ventas",
    "T4  Carnes selec compras 19256 Sel/27-01-2026": "Gestión de Pedidos/Entregas",
    # T4 Cuprum Constitucion 44531
    "T4 Cuprum Constitucion 44531/03-02-2026": "Seguimiento de Ventas",
    "T4 Cuprum Constitucion 44531/04-03-2026": "Seguimiento de Ventas",
    "T4 Cuprum Constitucion 44531/06-04-2026": "Seguimiento de Ventas",
    # T4 Electrica Aselco 19649
    "T4 Electrica Aselco 19649/05-02-2026": "Seguimiento de Ventas",
    "T4 Electrica Aselco 19649/07-02-2026": "Facturación_Documentos",
    "T4 Electrica Aselco 19649/08-04-2026": "Gestión de Pedidos/Entregas",
    "T4 Electrica Aselco 19649/10-02-2026": "Facturación_Documentos",
    "T4 Electrica Aselco 19649/10-03-2026": "Seguimiento de Ventas",
    "T4 Electrica Aselco 19649/17-03-2026": "Facturación_Documentos",
    "T4 Electrica Aselco 19649/19-01-2026": "Seguimiento de Ventas",
    "T4 Electrica Aselco 19649/23-02-2026": "Seguimiento de Ventas",
    "T4 Electrica Aselco 19649/26-01-2026": "Seguimiento de Ventas",
    # T4 Jesús Meléndez 31713
    "T4 Jesús Meléndez 31713/06-03-2026": "Facturación_Documentos",
    "T4 Jesús Meléndez 31713/13-04-2026": "Facturación_Documentos",
    # T4 Jova Fabiola 47173
    "T4 Jova Fabiola 47173/06-02-2026": "Seguimiento de Ventas",
    "T4 Jova Fabiola 47173/11-03-2026": "Seguimiento de Ventas",
    "T4 Jova Fabiola 47173/13-02-2026": "Seguimiento de Ventas",
    "T4 Jova Fabiola 47173/23-01-2026": "Seguimiento de Ventas",
    "T4 Jova Fabiola 47173/28-01-2026": "Seguimiento de Ventas",
    # T4 Copycos 16807
    "T4 Copycos 16807/13-02-2026": "Facturación_Documentos",
    "T4 Copycos 16807/16-04-2026": "Consulta de Precio",
    "T4 Copycos 16807/23-04-2026": "Soporte",
    # T5 Alberto 31892 Inmobiliaria Caravi
    "T5 Alberto 31892 Inmobiliaria Caravi/23-02-2026": "Seguimiento de Ventas",
    "T5 Alberto 31892 Inmobiliaria Caravi/26-03-2026": "Seguimiento de Ventas",
    # T5 Castilla Shaula
    "T5 Castilla Shaula/13-03-2026": "Soporte",
    "T5 Castilla Shaula/14-04-2026": "Facturación_Documentos",
    # T5 Elizabeth Productora De Alimentos
    "T5 Elizabeth Productora De Alimentos/07-04-2026": "Seguimiento de Ventas",
    "T5 Elizabeth Productora De Alimentos/09-02-2026": "Seguimiento de Ventas",
    "T5 Elizabeth Productora De Alimentos/12-02-2026": "Seguimiento de Ventas",
    "T5 Elizabeth Productora De Alimentos/19-02-2026": "Soporte",
    "T5 Elizabeth Productora De Alimentos/20-01-2026": "Soporte",
    # T5 Raul Vama
    "T5 Raul Vama/03-03-2026": "Seguimiento de Ventas",
    "T5 Raul Vama/16-04-2026": "Seguimiento de Ventas",
    "T5 Raul Vama/17-02-2026": "Seguimiento de Ventas",
    "T5 Raul Vama/28-02-2026": "Facturación_Documentos",
    # t6 CASSANDRA ADMINISTRACION CHINIZA
    "t6 CASSANDRA ADMINISTRACION CHINIZA/09-02-2026": "Facturación_Documentos",
    "t6 CASSANDRA ADMINISTRACION CHINIZA/14-04-2026": "Facturación_Documentos",
    "t6 CASSANDRA ADMINISTRACION CHINIZA/23-03-2026": "Facturación_Documentos",
    "t6 CASSANDRA ADMINISTRACION CHINIZA/28-03-2026": "Facturación_Documentos",
    # T6 Maricela (41378) Jose Ángel Perez
    "T6 Maricela (41378) Jose Ángel Perez/28-02-2026": "Seguimiento de Ventas",
    # T6 Michelle GPS (45574)
    "T6 Michelle GPS (45574)/09-04-2026": "Facturación_Documentos",
    # T6 Sistemas de Impresion Elect. Compras
    "T6 Sistemas de Impresion Elect. Compras/06-03-2026": "Facturación_Documentos",
    "T6 Sistemas de Impresion Elect. Compras/07-03-2026": "Facturación_Documentos",
    "T6 Sistemas de Impresion Elect. Compras/10-04-2026": "Facturación_Documentos",
    "T6 Sistemas de Impresion Elect. Compras/19-01-2026": "Facturación_Documentos",
    "T6 Sistemas de Impresion Elect. Compras/23-01-2026": "Soporte",
    # T9 Anahí Ingresos Maco
    "T9 Anahí Ingresos Maco/23-04-2026": "Seguimiento de Ventas",
    "T9 Anahí Ingresos Maco/25-04-2026": "Seguimiento de Ventas",
    # T9 Drenax 42513
    "T9 Drenax 42513/09-03-2026": "Seguimiento de Ventas",
    "T9 Drenax 42513/13-04-2026": "Seguimiento de Ventas",
    "T9 Drenax 42513/14-04-2026": "Seguimiento de Ventas",
    "T9 Drenax 42513/18-03-2026": "Seguimiento de Ventas",
    "T9 Drenax 42513/22-04-2026": "Seguimiento de Ventas",
    "T9 Drenax 42513/24-04-2026": "Seguimiento de Ventas",
    "T9 Drenax 42513/25-04-2026": "Seguimiento de Ventas",
    # T9 Ferre laminas 46266
    "T9 Ferre laminas 46266/22-04-2026": "Seguimiento de Ventas",
    # T9 Huma Uniformes Y Bordados 41403
    "T9 Huma Uniformes Y Bordados 41403/21-04-2026": "Seguimiento de Ventas",
    # T9 Miriam Fienmont 45737 Miriam
    "T9 Miriam Fienmont 45737 Miriam/06-04-2026": "Facturación_Documentos",
    "T9 Miriam Fienmont 45737 Miriam/14-04-2026": "Facturación_Documentos",
    "T9 Miriam Fienmont 45737 Miriam/18-04-2026": "Facturación_Documentos",
    "T9 Miriam Fienmont 45737 Miriam/25-04-2026": "Facturación_Documentos",
    "T9 Miriam Fienmont 45737 Miriam/27-03-2026": "Facturación_Documentos",
    # T9 Sergio M paper plus 10592
    "T9 Sergio M paper plus 10592/09-02-2026": "Seguimiento de Ventas",
    "T9 Sergio M paper plus 10592/14-02-2026": "Facturación_Documentos",
    "T9 Sergio M paper plus 10592/21-03-2026": "Seguimiento de Ventas",
    "T9 Sergio M paper plus 10592/31-03-2026": "Facturación_Documentos",
}

# Normalizar claves del mapa
CORRECTIONS_NORM = {norm(k): v for k, v in CORRECTIONS.items()}

def main():
    clases_path = 'ML/tf_idf_matrix_clases.csv'
    df = pd.read_csv(clases_path, encoding='utf-8-sig')
    df['Chat'] = df['Chat'].apply(norm)

    # Fix typo "Interación/Relacional" → "Interacción/Relacional"
    typo_mask = df['Clase'] == 'Interación/Relacional'
    typo_count = typo_mask.sum()
    if typo_count:
        df.loc[typo_mask, 'Clase'] = 'Interacción/Relacional'
        print(f"Typo corregido 'Interación/Relacional' → 'Interacción/Relacional': {typo_count} filas")

    applied = 0
    not_found = []
    for chat_key, new_clase in CORRECTIONS_NORM.items():
        mask = df['Chat'] == chat_key
        if mask.sum() == 0:
            not_found.append(chat_key)
            continue
        old = df.loc[mask, 'Clase'].iloc[0]
        if old != new_clase:
            df.loc[mask, 'Clase'] = new_clase
            applied += 1

    df.to_csv(clases_path, index=False, encoding='utf-8-sig')

    print(f"\nCorrecciones aplicadas: {applied}")
    if not_found:
        print(f"No encontrados ({len(not_found)}):")
        for c in not_found:
            print(f"  {c}")

    print("\nDistribución final:")
    print(df['Clase'].value_counts(dropna=False).to_string())

if __name__ == '__main__':
    main()
