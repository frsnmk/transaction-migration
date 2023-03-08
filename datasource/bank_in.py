import pandas as pd

class BankIn:

    def __init__(self, path:str, columns:list = [
        'Tanggal', 'Nomor', 'Keterangan', 'Nama Anggota', 'Ref',
        'Debit', 'Pengalihan Kas', 'Lain-lain',
        'Angsuran Gudang', 'Angsuran Farm', 'Angsuran Security', 'Angsuran CAM', 'Angsuran PWM', 'Angsuran PMP',
        'Simpanan Gudang', 'Simpanan Farm', 'Simpanan Security', 'Simpanan CAM', 'Simpanan PWM', 'Simpanan PMP',
        'Simpanan Pokok Gudang', 'Simpanan Pokok Farm', 'Simpanan Pokok Security', 'Simpanan Pokok CAM', 'Simpanan Pokok PWM', 'Simpanan Pokok PMP',
        'Piutang Gudang', 'Piutang Farm', 'Piutang Pokok Security', 'Piutang Pokok CAM', 'Piutang Pokok PWM', 'Piutang Pokok PMP', 'Piutang P.Agen', 'Piutang Tunai'
    ]):
        '''Jembatan antara code dan excel sebagai sumber data'''
        self.columns = columns
        self.path = path

    
    def data_bank_in(self):
        df = pd.read_excel(self.path, sheet_name='Bank-BRI', names=self.column, skiprows=8, nrows=407, usecols='Z:BG')
        # Memfilter row menjadi kolom yang mempunyai nomor saja
        df = df[df['Nomor'].notna()]

        # Mengisi tanggal yang kosong berdasarkan tanggal pada row sebelumnya
        df['Tanggal'].fillna(method='ffill', inplace=True)

        # Menyamakan jumlah dan urutan kolom yang ada pada bank in ke kas in
        df = df.drop('Pengalihan Kas', axis=1) # Menghapus kolom pengalihan kas pada bank in. (Karena akan dilakukan secara otomatis oleh bank out transaction)

        lain2_column = df.pop('Lain-lain') # mengambil kolom lain-lain
        df['Pemasukan Lain-lain'] = lain2_column # memasukan kembali kolom lain-lain keurutan paling belakang
        return df