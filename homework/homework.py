"""
Escriba el codigo que ejecute la accion solicitada.
"""

# pylint: disable=import-outside-toplevel


def clean_campaign_data():
    """
    En esta tarea se le pide que limpie los datos de una campaña de
    marketing realizada por un banco, la cual tiene como fin la
    recolección de datos de clientes para ofrecerls un préstamo.

    La información recolectada se encuentra en la carpeta
    files/input/ en varios archivos csv.zip comprimidos para ahorrar
    espacio en disco.

    Usted debe procesar directamente los archivos comprimidos (sin
    descomprimirlos). Se desea partir la data en tres archivos csv
    (sin comprimir): client.csv, campaign.csv y economics.csv.
    Cada archivo debe tener las columnas indicadas.

    Los tres archivos generados se almacenarán en la carpeta files/output/.

    client.csv:
    - client_id
    - age
    - job: se debe cambiar el "." por "" y el "-" por "_"
    - marital
    - education: se debe cambiar "." por "_" y "unknown" por pd.NA
    - credit_default: convertir a "yes" a 1 y cualquier otro valor a 0
    - mortage: convertir a "yes" a 1 y cualquier otro valor a 0

    campaign.csv:
    - client_id
    - number_contacts
    - contact_duration
    - previous_campaing_contacts
    - previous_outcome: cmabiar "success" por 1, y cualquier otro valor a 0
    - campaign_outcome: cambiar "yes" por 1 y cualquier otro valor a 0
    - last_contact_day: crear un valor con el formato "YYYY-MM-DD",
        combinando los campos "day" y "month" con el año 2022.

    economics.csv:
    - client_id
    - const_price_idx
    - eurobor_three_months



    """

    return


if __name__ == "__main__":
    clean_campaign_data()
"""
Escriba el codigo que ejecute la accion solicitada.
"""

# pylint: disable=import-outside-toplevel


def clean_campaign_data():
    """
    En esta tarea se le pide que limpie los datos de una campaña de
    marketing realizada por un banco, la cual tiene como fin la
    recolección de datos de clientes para ofrecerls un préstamo.

    La información recolectada se encuentra en la carpeta
    files/input/ en varios archivos csv.zip comprimidos para ahorrar
    espacio en disco.

    Usted debe procesar directamente los archivos comprimidos (sin
    descomprimirlos). Se desea partir la data en tres archivos csv
    (sin comprimir): client.csv, campaign.csv y economics.csv.
    Cada archivo debe tener las columnas indicadas.

    Los tres archivos generados se almacenarán en la carpeta files/output/.

    client.csv:
    - client_id
    - age
    - job: se debe cambiar el "." por "" y el "-" por "_"
    - marital
    - education: se debe cambiar "." por "_" y "unknown" por pd.NA
    - credit_default: convertir a "yes" a 1 y cualquier otro valor a 0
    - mortage: convertir a "yes" a 1 y cualquier otro valor a 0

    campaign.csv:
    - client_id
    - number_contacts
    - contact_duration
    - previous_campaing_contacts
    - previous_outcome: cmabiar "success" por 1, y cualquier otro valor a 0
    - campaign_outcome: cambiar "yes" por 1 y cualquier otro valor a 0
    - last_contact_day: crear un valor con el formato "YYYY-MM-DD",
        combinando los campos "day" y "month" con el año 2022.

    economics.csv:
    - client_id
    - const_price_idx
    - eurobor_three_months



    """

    import pandas as pd
    import glob
    import os

    # Obtener la lista de todos los archivos .csv.zip en la carpeta de entrada
    input_path = "files/input/*.csv.zip"
    all_files = glob.glob(input_path)
    
    # Lista para almacenar los DataFrames
    dataframes = []
    
    # Leer cada archivo. Pandas puede leer directamente archivos comprimidos
    for filename in all_files:
        # Se asume que los archivos comprimidos no tienen un índice en el CSV
        df = pd.read_csv(filename)
        dataframes.append(df)

    if not dataframes:
        print(f"Error: No se encontraron archivos en '{input_path}'.")
        return
    
    df_full = pd.concat(dataframes, ignore_index=True)
    
    # Crear la columna 'client_id' basada en el índice (0, 1, 2, ...)
    df_full['client_id'] = df_full.index


    ##### A. client.csv #####
    df_client = df_full.copy()
    
    # job: cambiar "." por "" y "-" por "_"
    df_client['job'] = df_client['job'].str.replace('.', '', regex=False).str.replace('-', '_', regex=False)
    
    # education: cambiar "." por "_" y "unknown" por pd.NA
    df_client['education'] = df_client['education'].str.replace('.', '_', regex=False).replace('unknown', pd.NA)
    
    # credit_default: "yes" a 1, otro valor a 0
    df_client['credit_default'] = (df_client['credit_default'] == 'yes').astype(int)
    
    # mortage: "yes" a 1, otro valor a 0
    df_client['mortgage'] = (df_client['mortgage'] == 'yes').astype(int)
    
    # Seleccionar y reordenar las columnas de client.csv
    client_cols = ['client_id', 'age', 'job', 'marital', 'education', 'credit_default', 'mortgage']
    df_client = df_client[client_cols]


    ##### B. campaign.csv #####
    df_campaign = df_full.copy()
    
    # previous_outcome: "success" por 1, otro valor a 0
    df_campaign['previous_outcome'] = (df_campaign['previous_outcome'] == 'success').astype(int)
    
    # campaign_outcome: "yes" por 1, otro valor a 0
    df_campaign['campaign_outcome'] = (df_campaign['campaign_outcome'] == 'yes').astype(int)
    
    # last_contact_day: Crear 'YYYY-MM-DD'
    month_mapping = {
        'jan': 1, 'feb': 2, 'mar': 3, 'apr': 4, 'may': 5, 'jun': 6,
        'jul': 7, 'aug': 8, 'sep': 9, 'oct': 10, 'nov': 11, 'dec': 12
    }
    # Las columnas 'month' y 'day' están en minúsculas debido a la normalización.
    df_campaign['month_num'] = df_campaign['month'].str.lower().map(month_mapping)
    
    df_campaign['last_contact_day'] = pd.to_datetime(
        '2022-' + df_campaign['month_num'].astype(str) + '-' + df_campaign['day'].astype(str),
        format='%Y-%m-%d',
        errors='coerce' 
    ).dt.strftime('%Y-%m-%d')

    df_campaign.rename(columns={'last_contact_day': 'last_contact_date'}, inplace=True)
    
    # Seleccionar y reordenar las columnas de campaign.csv
    campaign_cols = [
        'client_id', 'number_contacts', 'contact_duration', 
        'previous_campaign_contacts', 'previous_outcome', 
        'campaign_outcome', 'last_contact_date'
    ]
    df_campaign = df_campaign[campaign_cols]


    ##### C. economics.csv #####
    df_economics = df_full.copy()

    # Seleccionar las columnas de economics.csv
    economics_cols = ['client_id', 'cons_price_idx', 'euribor_three_months']
    df_economics = df_economics[economics_cols]


    ##### Guardar los DataFrames en la carpeta de salida #####
    output_dir = "files/output"
    os.makedirs(output_dir, exist_ok=True) 
    
    df_client.to_csv(os.path.join(output_dir, "client.csv"), index=False)
    df_campaign.to_csv(os.path.join(output_dir, "campaign.csv"), index=False)
    df_economics.to_csv(os.path.join(output_dir, "economics.csv"), index=False)

    return


if __name__ == "__main__":
    clean_campaign_data()