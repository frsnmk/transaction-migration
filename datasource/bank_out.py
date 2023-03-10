import pandas as pd

class BankOut:

    def __init__(self, path:str, columns:list = [
        'Tanggal', 'Nomor', 'Keterangan', 'Nama Anggota', 'Ref',
        'Kredit', 'Pengalihan Bank', 'Serba/i', 'PPOB',
        'Pinjaman Gudang', 'Pinjaman Farm', 'Pinjaman Security', 'Pinjaman CAM', 'Pinjaman PWM', 'Pinjaman PMP',
        'Simpanan Gudang', 'Simpanan Farm', 'Simpanan Security', 'Simpanan CAM', 'Simpanan PWM', 'Simpanan PMP',
        'Biaya Lain-lain', 'Hutang Dagang'
    ]):
        '''Jembatan antara code dan excel sebagai sumber data'''
        self.columns = columns
        self.path = path
    
    def data_bank_out(self):
        df = pd.read_excel(self.path, sheet_name='Bank-BRI', names=self.columns, skiprows=8, nrows=249, usecols='A:W')
        # Memfilter row menjadi kolom yang mempunyai nomor saja
        df = df[df['Nomor'].notna()]
        # Mengisi tanggal yang kosong berdasarkan tanggal pada row sebelumnya
        df['Tanggal'].fillna(method='ffill', inplace=True)
        df['Tanggal'] = df['Tanggal'].dt.strftime('%Y-%m-%d %H:%M')
        df['Kategori Transaksi'] = 'Bank Keluar'
        return df

