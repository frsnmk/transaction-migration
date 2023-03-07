import os
import pandas as pd

from dotenv import load_dotenv

from datasource.selling import Selling
from datasource.purchase import Purchase
from datasource.ppob import PPOB

from database.employee import Employee
from database.item import Item

from transaction.helper import most_similar_word, nama_anggota, supplier_name_adjustment
from transaction.transaction import Transaction
from transaction.selling_transaction import SellingTransaction
from transaction.purchase_transaction import PurchaseTransaction
from transaction.ppob_transaction import PPOBTransaction

load_dotenv()

path = os.getenv('LAPORAN_KEUANGAN_PATH')

employees_name = Employee().fetch_all_name()
items = Item().fetch_all() # dibutuhkan untuk generate barcode

sellings = Selling(path).data_penjualan()
purchases = Purchase(path).data_pembelian()
ppob =  PPOB(path).data_ppob()

merged_data = pd.concat([sellings, purchases, ppob])
merged_data = merged_data.sort_values('Tanggal', ascending=True)
bot = Transaction()

for i, row in ppob.iterrows():
    if row['Kategori Transaksi'] == 'Penjualan':
        SellingTransaction(bot.driver, bot.wait).selling_transaction(row['Tanggal'], row['Nomor'], most_similar_word(nama_anggota(row['Pelanggan']), employees_name, 65), row['Jenis Barang'], row['Harga'], row['Kuantum'], items)
    if row['Kategori Transaksi'] == 'Pembelian':
        PurchaseTransaction(bot.driver, bot.wait).purchase_transaction(supplier_name_adjustment(row['Suplayer']), pd.to_datetime(row['Tanggal']).strftime('%d-%m-%Y'), row['Bahan Baku'], row['Harga'], row['Kuantum'], items)
    if row['Kategori Transaksi'] == 'PPOB':
        PPOBTransaction(bot.driver, bot.wait).ppob_transaction(row['Tanggal'], row['Nomor'], row['Jenis Pembayaran'], row['Jenis Transaksi'], row['Jumlah Tagihan'], row['Admin'], row['Total Pembayaran'])