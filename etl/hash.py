import pandas as pd
from datetime import datetime


def check_hash(df, time, hash_table):

    hash_temp = pd.DataFrame(columns=['ID', 'hash', 'DateUpdate'])
    df['Tarikh_komaki'] = df['Tarikh_komaki'].astype(float).astype(int)

    if time < 14040401:
        filter_df = df[df['Tarikh_komaki'] < time & df['Tarikh_komaki'] > 14040101].copy()
    else:
        filter_df = df[(df['Tarikh_komaki'] < time) & (df['Tarikh_komaki'] > (time - 300))].copy()

    df['Tarikh_komaki'] = df['Tarikh_komaki'].astype(str)

    filter_df['hash'] = (
            filter_df['ID'].astype(str) +
            filter_df['netvalue'].astype(str).str.replace("-", "", regex=True)
    )

    risk_row = []

    for _, row in filter_df.iterrows():

        if hash_table[(hash_table['ID'] == row['ID']) & (hash_table['hash'] == row['hash'])].empty:
            risk_row.append(row['ID'])
            if hash_table[hash_table['ID'] == row['ID']].empty:
                hash_temp.append(create_hash(row))
            elif not hash_table[(hash_table['ID'] == row['ID']) & (hash_table['hash'] != row['hash'])].empty:
                hash_table = update_hash(row, hash_table)

    hash_table = pd.concat([hash_temp, hash_table], ignore_index=True)

    return hash_table


def create_hash(df):

    hash_df = pd.DataFrame(columns=['ID', 'hash', 'DateUpdate'])
    hash_df ['ID'] = df['ID'].copy()
    hash_df['hash'] = (
            df['ID'].astype(str)
            + df['netvalue'].astype(int).astype(str).str.replace("-", "", regex=True)
    )
    hash_df['DateUpdate'] = datetime.date(datetime.now())


    return hash_df




def update_hash(row, hash_table):

        hash_table[hash_table['ID'] == row['ID']]['hash'] = str(row['ID']) + str(int(row['netvalue'])).replace("-", "")
        hash_table[hash_table['ID'] == row['ID']]['DateUpdate'] = datetime.date(datetime.now())

        return hash_table



