import pandas as pd
from dotenv import load_dotenv
import os

load_dotenv()

path = os.getenv('LAPORAN_KEUANGAN_PATH')

class Purchase:

    def __init__(self, path:str, columns:list = ['Tanggal', 'Nomor', 'Bahan Baku', 'Suplayer', 'Harga', 'Kuantum', 'Total']):
        '''Jembatan antara code dan excel sebagai sumber data'''
        self.columns = columns
        self.path = path
    
    def data_pembelian(self) -> pd.DataFrame:
        df = pd.read_excel(self.path, sheet_name='Beli - Jual', names=self.columns, skiprows=8, nrows=177, usecols='A:G') # Read data excel

        # Mengisi field yang kosong, berdasarkan nilai field dari row yang sebelumnya
        df['Tanggal'].fillna(method='ffill', inplace=True)
        df['Tanggal'] = df['Tanggal'].dt.strftime('%Y-%m-%d %H:%M')
        # Menghapus row yang nilai kolom suplayernya kosong
        df = df.drop(df[df['Suplayer'].isnull()].index)

 
        ################################
        df = df.groupby(['Tanggal','Suplayer']).agg({
            'Bahan Baku': lambda x: list(x),
            'Harga': lambda x: list(x),
            'Kuantum': lambda x: list(x),
            'Total': lambda x: list(x),
        }).reset_index()
        return df
