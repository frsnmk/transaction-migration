import pandas as pd
class Selling:

    def __init__(self, path:str, columns:list = ['Tanggal', 'Nomor', 'Pelanggan', 'Jenis Barang', 'Harga', 'Kuantum', 'Piutang', 'Ref']):
        '''Jembatan antara code dan excel sebagai sumber data'''
        self.columns = columns
        self.path = path

    def data_penjualan(self) -> pd.DataFrame:
        df = pd.read_excel(self.path, sheet_name='Beli - Jual', names=self.columns, skiprows=8, nrows=4664, usecols='J:Q') # Read data excel
        df['Nomor'].loc[df['Nomor'].isnull() & (df['Pelanggan']=='PENJUALAN TUNAI - DP')] = 'Uncode' # Mengisi yang tidak memiliki nomor transaksi dengna nomor transaksi 'Uncode'
        
        # Mengisi field yang kosong, berdasarkan nilai field dari row yang sebelumnya
        df['Tanggal'].fillna(method='ffill', inplace=True)
        df['Tanggal'] = df['Tanggal'].dt.strftime('%Y-%m-%d %H:%M')
        df['Nomor'].fillna(method='ffill', inplace=True)
        df['Pelanggan'].fillna(method='ffill', inplace=True)

        # Melakukan group by dan membuat kolom jenis barang, harga, kuantum dan piutang menjadi array
        df = df.groupby(['Tanggal', 'Nomor', 'Pelanggan']).agg({
            'Jenis Barang' : lambda x:list(x),
            'Harga' : lambda x:list(x),
            'Kuantum' : lambda x:list(x),
            'Piutang' : lambda x:list(x)
        }).reset_index()
        df['Kategori Transaksi'] = 'Penjualan'
        return df
        