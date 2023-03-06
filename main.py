import os
import pandas as pd

from dotenv import load_dotenv

from datasource.selling import Selling
from datasource.purchase import Purchase

from database.employee import Employee
from database.item import Item

from transaction.helper import most_similar_word, nama_anggota, supplier_name_adjustment
from transaction.transaction import Transaction
from transaction.selling_transaction import SellingTransaction
from transaction.purchase_transaction import PurchaseTransaction

load_dotenv()

path = os.getenv('LAPORAN_KEUANGAN_PATH')

employees_name = Employee().fetch_all_name()
items = Item().fetch_all() # dibutuhkan untuk generate barcode

sellings = Selling(path).data_penjualan()
purchases = Purchase(path).data_pembelian()

merged_data = pd.concat([sellings, purchases])
merged_data.sort_values(by='Tanggal', ascending=True)
bot = Transaction()

for i, row in merged_data.iterrows():
    if isinstance(row['Pelanggan'], str):
        pass
        # SellingTransaction(bot.driver, bot.wait).selling_transaction(row['Tanggal'], row['Nomor'], most_similar_word(nama_anggota(row['Pelanggan']), employees_name, 65), row['Jenis Barang'], row['Harga'], row['Kuantum'], items)
    if isinstance(row['Suplayer'], str):
        PurchaseTransaction(bot.driver, bot.wait).purchase_transaction(supplier_name_adjustment(row['Suplayer']), pd.to_datetime(row['Tanggal']).strftime('%d-%m-%Y'), row['Bahan Baku'], row['Harga'], row['Kuantum'], items)
        input('Press any key ...')
        bot.close()
