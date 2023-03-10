import pandas as pd

class CashOut:

    def __init__(self, path:str, columns:list = [
        'Tanggal', 'Nomor', 'Keterangan', 'Nama Anggota', 'Ref', 'Kredit', 'Pengalihan Kas', 'Hutang SHU 2015',
        'Pinjaman Gudang', 'Pinjaman Farm', 'Pinjaman Security', 'Pinjaman CAM', 'Pinjaman PWM', 'Pinjaman PMP',
        'Pengambilan Simpanan Gudang', 'Pengambilan Simpanan Pokok', 'Pengambilan Simpanan Farm', 'Pengambilan Simpanan Security', 'Pengambilan Simpanan CAM', 'Pengambilan Simpanan PWM', 'Pengambilan Simpanan PMP',
        'Gaji', 'Hutang Usaha', 'ATK', 'Operasional', 'Lain-lain'
    ]):
        '''Jembatan antara code dan excel sebagai sumber data'''
        self.columns = columns
        self.path = path

    def data_cash_out(self):
        df = pd.read_excel(self.path, sheet_name='Kas', names=self.columns, usecols='AI:BH', skiprows=8, nrows=38)
        # Memfilter row menjadi kolom yang mempunyai nomor saja
        df = df[df['Nomor'].notna()]
        # Mengisi tanggal yang kosong berdasarkan tanggal pada row sebelumnya
        df['Tanggal'].fillna(method='ffill', inplace=True)
        df['Tanggal'] = df['Tanggal'].dt.strftime('%Y-%m-%d %H:%M')
        df['Kategori Transaksi'] = 'Kas Keluar'
        return df
