import os
import pandas as pd

from dotenv import load_dotenv

from datasource.selling import Selling

from database.employee import Employee
from database.item import Item

from transaction.helper import most_similar_word, nama_anggota
from transaction.transaction import Transaction
from transaction.selling_transaction import SellingTransaction

load_dotenv()

path = os.getenv('LAPORAN_KEUANGAN_PATH')

employees_name = Employee().fetch_all_name()
items = Item().fetch_all() # dibutuhkan untuk generate barcode

sellings = Selling(path).data_penjualan()

bot = Transaction()

for i, row in sellings.iterrows():
    if isinstance(row['Pelanggan'], str):
        SellingTransaction(bot.driver, bot.wait).selling_transaction(row['Tanggal'], row['Nomor'], most_similar_word(nama_anggota(row['Pelanggan']), employees_name, 65), row['Jenis Barang'], row['Harga'], row['Kuantum'], items)