import pandas as pd

class PPOB:

    def __init__(self, path:str, columns:list = ['Tanggal', 'Nomor', 'Jenis Pembayaran', 'Jenis Transaksi', 'Jumlah Tagihan', 'Admin', 'Total Pembayaran', 'ID Pelanggan', 'Pelanggan', 'Ket.']):
        '''Jembatan antara code dan excel sebagai sumber data'''
        self.columns = columns
        self.path = path

    def data_ppob(self) -> pd.DataFrame:
        df = pd.read_excel(self.path, sheet_name='PPOB', names=self.columns, skiprows=8, nrows=265, usecols='C:L')
        
        # Mengisi field yang kosong, berdasarkan nilai field dari row yang sebelumnya
        df['Tanggal'].fillna(method='ffill', inplace=True)
        df['Tanggal'] = df['Tanggal'].dt.strftime('%Y-%m-%d %H:%M')

        # Menghapus row yang nilai Jenis Transaksiya kosong
        df = df.drop(df[df['Jenis Transaksi'].isnull()].index)
        df['Kategori Transaksi'] = 'PPOB'
        return df