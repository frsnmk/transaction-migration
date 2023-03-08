import pandas as pd

class CashIn:

    def __init__(self, path:str, columns:list = [
        'Tanggal', 'Nomor', 'Keterangan', 'Nama Anggota', 'Ref', 'Debit',
        'Angsuran Gudang', 'Angsuran Farm', 'Angsuran Security', 'Angsuran CAM', 'Angsuran PWM', 'Angsuran PMP',
        'Simpanan Gudang', 'Simpanan Farm', 'Simpanan Security', 'Simpanan CAM', 'Simpanan PWM', 'Simpanan PMP',
        'Simpanan Pokok Gudang', 'Simpanan Pokok Farm', 'Simpanan Pokok Security', 'Simpanan Pokok CAM', 'Simpanan Pokok PWM', 'Simpanan Pokok PMP',
        'Piutang Gudang', 'Piutang Farm', 'Piutang Security', 'Piutang CAM', 'Piutang PWM', 'Piutang PMP', 'Piutang P. Agen', 'Piutang Tunai',
        'Pemasukan Lain-lain'
    ]):
        '''Jembatan antara code dan excel sebagai sumber data'''
        self.columns = columns
        self.path = path

    
    def data_cash_in(self):
        df = pd.read_excel(self.path, sheet_name='Kas', names=self.columns, usecols='A:AG', skiprows=8, nrows=116)
        # Memfilter row menjadi kolom yang mempunyai nomor saja
        df = df[df['Nomor'].notna()]

        # Mengisi tanggal yang kosong berdasarkan tanggal pada row sebelumnya
        df['Tanggal'].fillna(method='ffill', inplace=True)
        df['Tanggal'] = df['Tanggal'].dt.strftime('%Y-%m-%d %H:%M')

        df['Kategori Transaksi'] = 'Kas Masuk'
        return df