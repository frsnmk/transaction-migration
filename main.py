import os
import pandas as pd

from dotenv import load_dotenv

from datasource.selling import Selling
from datasource.purchase import Purchase
from datasource.ppob import PPOB
from datasource.bank_in import BankIn

from database.employee import Employee
from database.item import Item

from transaction.helper import most_similar_word, nama_anggota, supplier_name_adjustment, find_employe_name_by_code
from transaction.transaction import Transaction
from transaction.selling_transaction import SellingTransaction
from transaction.purchase_transaction import PurchaseTransaction
from transaction.ppob_transaction import PPOBTransaction
from transaction.bank_in import BankInTransaction 

load_dotenv()

path = os.getenv('LAPORAN_KEUANGAN_PATH')

employees_name = Employee().fetch_all_name()
items = Item().fetch_all() # dibutuhkan untuk generate barcode

sellings = Selling(path).data_penjualan()
purchases = Purchase(path).data_pembelian()
ppob =  PPOB(path).data_ppob()
bank_in = BankIn(path).data_bank_in()

merged_data = pd.concat([sellings, purchases, ppob, bank_in])
merged_data = merged_data.sort_values('Tanggal', ascending=True)
bot = Transaction()

for i, row in bank_in.iterrows():
    if row['Kategori Transaksi'] == 'Penjualan':
        SellingTransaction(bot.driver, bot.wait).selling_transaction(row['Tanggal'], row['Nomor'], most_similar_word(nama_anggota(row['Pelanggan']), employees_name, 65), row['Jenis Barang'], row['Harga'], row['Kuantum'], items)
    if row['Kategori Transaksi'] == 'Pembelian':
        PurchaseTransaction(bot.driver, bot.wait).purchase_transaction(supplier_name_adjustment(row['Suplayer']), pd.to_datetime(row['Tanggal']).strftime('%d-%m-%Y'), row['Bahan Baku'], row['Harga'], row['Kuantum'], items)
    if row['Kategori Transaksi'] == 'PPOB':
        PPOBTransaction(bot.driver, bot.wait).ppob_transaction(row['Tanggal'], row['Nomor'], row['Jenis Pembayaran'], row['Jenis Transaksi'], row['Jumlah Tagihan'], row['Admin'], row['Total Pembayaran'])
    if row['Kategori Transaksi'] == 'Bank Masuk':
        if not pd.isna(row['Pemasukan Lain-lain']):
            BankInTransaction(bot.driver, bot.wait).non_division_account(row['Keterangan'], row['Nama Anggota'], int(row['Pemasukan Lain-lain']), "Pemasukan Bunga Rekening BRI", row['Tanggal'])
        if not pd.isna(row['Angsuran Gudang']):
            BankInTransaction(bot.driver, bot.wait).angsuran(row['Keterangan'], find_employe_name_by_code(row['Nama Anggota']), int(row['Angsuran Gudang']), "Pinjaman karyawan Feedmill", row['Tanggal'])