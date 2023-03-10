import os
import pandas as pd

from dotenv import load_dotenv

from datasource.selling import Selling
from datasource.purchase import Purchase
from datasource.ppob import PPOB
from datasource.bank_in import BankIn
from datasource.cash_in import CashIn
from datasource.bank_out import BankOut
from datasource.cash_out import CashOut

from database.employee import Employee
from database.item import Item
from database.supplier import Supplier

from transaction.helper import most_similar_word, nama_anggota, supplier_name_adjustment, find_employe_name_by_code, member_name_adjusment
from transaction.transaction import Transaction
from transaction.selling_transaction import SellingTransaction
from transaction.purchase_transaction import PurchaseTransaction
from transaction.ppob_transaction import PPOBTransaction
from transaction.bank_in import BankInTransaction
from transaction.cash_in import CashInTransaction
from transaction.bank_out import BankOutTransaction
from transaction.cash_out_transaction import CashOutTransaction

load_dotenv()

path = os.getenv('LAPORAN_KEUANGAN_PATH')

employees_name = Employee().fetch_all_name()
items = Item().fetch_all() # dibutuhkan untuk generate barcode
supplier_name = Supplier().fetch_all_name()

sellings = Selling(path).data_penjualan()
purchases = Purchase(path).data_pembelian()
ppob =  PPOB(path).data_ppob()
bank_in = BankIn(path).data_bank_in()
cash_in = CashIn(path).data_cash_in()
bank_out = BankOut(path).data_bank_out()
cash_out = CashOut(path).data_cash_out()

merged_data = pd.concat([sellings, purchases, ppob, bank_in, cash_in, bank_out, cash_out])
merged_data = merged_data.sort_values('Tanggal', ascending=True)
bot = Transaction()

for i, row in merged_data.iterrows():
    if row['Kategori Transaksi'] == 'Penjualan':
        SellingTransaction(bot.driver, bot.wait).selling_transaction(row['Tanggal'], row['Nomor'], most_similar_word(nama_anggota(row['Pelanggan']), employees_name, 65), row['Jenis Barang'], row['Harga'], row['Kuantum'], items)
    if row['Kategori Transaksi'] == 'Pembelian':
        PurchaseTransaction(bot.driver, bot.wait).purchase_transaction(supplier_name_adjustment(row['Suplayer'], supplier_name), pd.to_datetime(row['Tanggal']).strftime('%d-%m-%Y'), row['Bahan Baku'], row['Harga'], row['Kuantum'], items)
    if row['Kategori Transaksi'] == 'PPOB':
        PPOBTransaction(bot.driver, bot.wait).ppob_transaction(row['Tanggal'], row['Nomor'], row['Jenis Pembayaran'], row['Jenis Transaksi'], row['Jumlah Tagihan'], row['Admin'], row['Total Pembayaran'])
    if row['Kategori Transaksi'] == 'Bank Masuk':
        if not pd.isna(row['Pemasukan Lain-lain']):
            BankInTransaction(bot.driver, bot.wait).non_division_account(row['Keterangan'], row['Nama Anggota'], int(row['Pemasukan Lain-lain']), "Pemasukan Bunga Rekening BRI", row['Tanggal'])
        if not pd.isna(row['Angsuran Gudang']):
            BankInTransaction(bot.driver, bot.wait).angsuran(row['Keterangan'], find_employe_name_by_code(row['Nama Anggota']), int(row['Angsuran Gudang']), "Pinjaman karyawan Feedmill", row['Tanggal'])
        if not pd.isna(row['Angsuran Farm']):
            BankInTransaction(bot.driver, bot.wait).angsuran(row['Keterangan'], find_employe_name_by_code(row['Nama Anggota']), int(row['Angsuran Farm']), "Pinjaman karyawan Farm", row['Tanggal'])
        if(not pd.isna(row['Angsuran Security'])):
            BankInTransaction(bot.driver, bot.wait).angsuran(row['Keterangan'], find_employe_name_by_code(row['Nama Anggota']), int(row['Angsuran Security']), "Pinjaman karyawan Security dan Pupuk", row['Tanggal'])
        if(not pd.isna(row['Angsuran CAM'])):
            BankInTransaction(bot.driver, bot.wait).angsuran(row['Keterangan'], find_employe_name_by_code(row['Nama Anggota']), int(row['Angsuran CAM']), "Pinjaman karyawan CAM", row['Tanggal'])
        if(not pd.isna(row['Angsuran PWM'])):
            BankInTransaction(bot.driver, bot.wait).angsuran(row['Keterangan'], find_employe_name_by_code(row['Nama Anggota']), int(row['Angsuran PWM']), "Pinjaman karyawan PWM", row['Tanggal'])
        if(not pd.isna(row['Angsuran PMP'])):
            BankInTransaction(bot.driver, bot.wait).angsuran(row['Keterangan'], find_employe_name_by_code(row['Nama Anggota']), int(row['Angsuran PMP']), "Pinjaman karyawan PMP", row['Tanggal'])
        
        if(not pd.isna(row['Simpanan Gudang'])):
            BankInTransaction(bot.driver, bot.wait).simpanan(row['Keterangan'], find_employe_name_by_code(row['Nama Anggota']), int(row['Simpanan Gudang']), "Simpanan wajib dan sukarela karyawan Gudang", row['Tanggal'])
        if(not pd.isna(row['Simpanan Farm'])):
            BankInTransaction(bot.driver, bot.wait).simpanan(row['Keterangan'], find_employe_name_by_code(row['Nama Anggota']), int(row['Simpanan Farm']), "Simpanan wajib dan sukarela karyawan Farm", row['Tanggal'])
        if(not pd.isna(row['Simpanan Security'])):
            BankInTransaction(bot.driver, bot.wait).simpanan(row['Keterangan'], find_employe_name_by_code(row['Nama Anggota']), int(row['Simpanan Security']), "Simpanan wajib dan sukarela karyawan Security", row['Tanggal'])
        if(not pd.isna(row['Simpanan CAM'])):
            BankInTransaction(bot.driver, bot.wait).simpanan(row['Keterangan'], find_employe_name_by_code(row['Nama Anggota']), int(row['Simpanan CAM']), "Simpanan wajib dan sukarela karyawan CAM", row['Tanggal'])
        if(not pd.isna(row['Simpanan PWM'])):
            BankInTransaction(bot.driver, bot.wait).simpanan(row['Keterangan'], find_employe_name_by_code(row['Nama Anggota']), int(row['Simpanan PWM']), "Simpanan wajib dan sukarela karyawan PWM", row['Tanggal'])
        if(not pd.isna(row['Simpanan PMP'])):
            BankInTransaction(bot.driver, bot.wait).simpanan(row['Keterangan'], find_employe_name_by_code(row['Nama Anggota']), int(row['Simpanan PMP']), "Simpanan wajib dan sukarela karyawan PMP", row['Tanggal'])

        if(not pd.isna(row['Simpanan Pokok Gudang'])):
            BankInTransaction(bot.driver, bot.wait).simpanan(row['Keterangan'], find_employe_name_by_code(row['Nama Anggota']), int(row['Simpanan Pokok Gudang']), "Simpanan pokok karyawan gudang", row['Tanggal'])
        if(not pd.isna(row['Simpanan Pokok Farm'])):
            BankInTransaction(bot.driver, bot.wait).simpanan(row['Keterangan'], find_employe_name_by_code(row['Nama Anggota']), int(row['Simpanan Pokok Farm']), "Simpanan pokok karyawan farm", row['Tanggal'])
        if(not pd.isna(row['Simpanan Pokok Security'])):
            BankInTransaction(bot.driver, bot.wait).simpanan(row['Keterangan'], find_employe_name_by_code(row['Nama Anggota']), int(row['Simpanan Pokok Security']), "Simpanan pokok karyawan security", row['Tanggal'])
        if(not pd.isna(row['Simpanan Pokok CAM'])):
            BankInTransaction(bot.driver, bot.wait).simpanan(row['Keterangan'], find_employe_name_by_code(row['Nama Anggota']), int(row['Simpanan Pokok CAM']), "Simpanan pokok karyawan cam", row['Tanggal'])
        if(not pd.isna(row['Simpanan Pokok PWM'])):
            BankInTransaction(bot.driver, bot.wait).simpanan(row['Keterangan'], find_employe_name_by_code(row['Nama Anggota']), int(row['Simpanan Pokok PWM']), "Simpanan pokok karyawan pwm", row['Tanggal'])
        if(not pd.isna(row['Simpanan Pokok PMP'])):
            BankInTransaction(bot.driver, bot.wait).simpanan(row['Keterangan'], find_employe_name_by_code(row['Nama Anggota']), int(row['Simpanan Pokok PMP']), "Simpanan pokok karyawan pmp", row['Tanggal'])

    if row['Kategori Transaksi'] == 'Kas Masuk':
        if(not pd.isna(row['Angsuran Gudang'])):
            CashInTransaction(bot.driver, bot.wait).angsuran(row['Keterangan'], find_employe_name_by_code(row['Nama Anggota']), int(row['Angsuran Gudang']), "Pinjaman karyawan Feedmill", row['Tanggal'])
        if(not pd.isna(row['Angsuran Farm'])):
            CashInTransaction(bot.driver, bot.wait).angsuran(row['Keterangan'], find_employe_name_by_code(row['Nama Anggota']), int(row['Angsuran Farm']), "Pinjaman karyawan Farm", row['Tanggal'])
        if(not pd.isna(row['Angsuran Security'])):
            CashInTransaction(bot.driver, bot.wait).angsuran(row['Keterangan'], find_employe_name_by_code(row['Nama Anggota']), int(row['Angsuran Security']), "Pinjaman karyawan Security dan Pupuk", row['Tanggal'])
        if(not pd.isna(row['Angsuran CAM'])):
            CashInTransaction(bot.driver, bot.wait).angsuran(row['Keterangan'], find_employe_name_by_code(row['Nama Anggota']), int(row['Angsuran CAM']), "Pinjaman karyawan CAM", row['Tanggal'])
        if(not pd.isna(row['Angsuran PWM'])):
            CashInTransaction(bot.driver, bot.wait).angsuran(row['Keterangan'], find_employe_name_by_code(row['Nama Anggota']), int(row['Angsuran PWM']), "Pinjaman karyawan PWM", row['Tanggal'])
        if(not pd.isna(row['Angsuran PMP'])):
            CashInTransaction(bot.driver, bot.wait).angsuran(row['Keterangan'], find_employe_name_by_code(row['Nama Anggota']), int(row['Angsuran PMP']), "Pinjaman karyawan PMP", row['Tanggal'])
        
        if(not pd.isna(row['Simpanan Gudang'])):
            CashInTransaction(bot.driver, bot.wait).simpanan(row['Keterangan'], find_employe_name_by_code(row['Nama Anggota']), int(row['Simpanan Gudang']), "Simpanan wajib dan sukarela karyawan Gudang", row['Tanggal'])
        if(not pd.isna(row['Simpanan Farm'])):
            CashInTransaction(bot.driver, bot.wait).simpanan(row['Keterangan'], find_employe_name_by_code(row['Nama Anggota']), int(row['Simpanan Farm']), "Simpanan wajib dan sukarela karyawan Farm", row['Tanggal'])
        if(not pd.isna(row['Simpanan Security'])):
            CashInTransaction(bot.driver, bot.wait).simpanan(row['Keterangan'], find_employe_name_by_code(row['Nama Anggota']), int(row['Simpanan Security']), "Simpanan wajib dan sukarela karyawan Security", row['Tanggal'])
        if(not pd.isna(row['Simpanan CAM'])):
            CashInTransaction(bot.driver, bot.wait).simpanan(row['Keterangan'], find_employe_name_by_code(row['Nama Anggota']), int(row['Simpanan CAM']), "Simpanan wajib dan sukarela karyawan CAM", row['Tanggal'])
        if(not pd.isna(row['Simpanan PWM'])):
            CashInTransaction(bot.driver, bot.wait).simpanan(row['Keterangan'], find_employe_name_by_code(row['Nama Anggota']), int(row['Simpanan PWM']), "Simpanan wajib dan sukarela karyawan PWM", row['Tanggal'])
        if(not pd.isna(row['Simpanan PMP'])):
            CashInTransaction(bot.driver, bot.wait).simpanan(row['Keterangan'], find_employe_name_by_code(row['Nama Anggota']), int(row['Simpanan PMP']), "Simpanan wajib dan sukarela karyawan PMP", row['Tanggal'])

        if(not pd.isna(row['Simpanan Pokok Gudang'])):
            CashInTransaction(bot.driver, bot.wait).simpanan(row['Keterangan'], find_employe_name_by_code(row['Nama Anggota']), int(row['Simpanan Pokok Gudang']), "Simpanan pokok karyawan Gudang", row['Tanggal'])
        if(not pd.isna(row['Simpanan Pokok Farm'])):
            CashInTransaction(bot.driver, bot.wait).simpanan(row['Keterangan'], find_employe_name_by_code(row['Nama Anggota']), int(row['Simpanan Pokok Farm']), "Simpanan pokok karyawan Farm", row['Tanggal'])
        if(not pd.isna(row['Simpanan Pokok Security'])):
            CashInTransaction(bot.driver, bot.wait).simpanan(row['Keterangan'], find_employe_name_by_code(row['Nama Anggota']), int(row['Simpanan Pokok Security']), "Simpanan pokok karyawan Security", row['Tanggal'])
        if(not pd.isna(row['Simpanan Pokok CAM'])):
            CashInTransaction(bot.driver, bot.wait).simpanan(row['Keterangan'], find_employe_name_by_code(row['Nama Anggota']), int(row['Simpanan Pokok CAM']), "Simpanan pokok karyawan Cam", row['Tanggal'])
        if(not pd.isna(row['Simpanan Pokok PWM'])):
            CashInTransaction(bot.driver, bot.wait).simpanan(row['Keterangan'], find_employe_name_by_code(row['Nama Anggota']), int(row['Simpanan Pokok PWM']), "Simpanan pokok karyawan Pwm", row['Tanggal'])
        if(not pd.isna(row['Simpanan Pokok PMP'])):
            CashInTransaction(bot.driver, bot.wait).simpanan(row['Keterangan'], find_employe_name_by_code(row['Nama Anggota']), int(row['Simpanan Pokok PMP']), "Simpanan pokok karyawan Pmp", row['Tanggal'])
        if(not pd.isna(row['Pemasukan Lain-lain'])):
            if(row['Nama Anggota'].__contains__('Rumput Endang')):
                CashInTransaction(bot.driver, bot.wait).non_division_account(row['Keterangan'], row['Nama Anggota'], row['Pemasukan Lain-lain'], "Pemasukan ex Rumput Endang", row['Tanggal'])

    if row['Kategori Transaksi'] == 'Bank Keluar':
        if(not pd.isna(row['Pengalihan Bank'])):
           BankOutTransaction(bot.driver, bot.wait).pengalihan(row['Keterangan'], row['Nama Anggota'], int(row['Pengalihan Bank']), "Buku Bank BRI Koperasi", row['Tanggal'])
        if(not pd.isna(row['Serba/i'])):
            if (row['Keterangan'].__contains__('Pembayaran biaya') or row['Keterangan'].__contains__('Pembayaran pajak')):
                BankOutTransaction(bot.driver, bot.wait).non_division_account(row['Keterangan'], row['Nama Anggota'], int(row['Serba/i']), "Biaya administrasi bank", row['Tanggal'])
        if(not pd.isna(row['PPOB'])):
            BankOutTransaction(bot.driver, bot.wait).non_division_account(row['Keterangan'], row['Nama Anggota'], int(row['PPOB']), "Uang muka pembelian PPOB", row['Tanggal'])

        if(not pd.isna(row['Biaya Lain-lain'])):
            if(row['Keterangan'].__contains__('Pembayaran gaji karyawan') or row['Keterangan'].__contains__('Pembayaran insentif karyawan')):
                BankOutTransaction(bot.driver, bot.wait).non_division_account(row['Keterangan'], row['Nama Anggota'], int(row['Biaya Lain-lain']), "Gaji Manajemen", row['Tanggal'])
        if(not pd.isna(row['Hutang Dagang'])):
            BankOutTransaction(bot.driver, bot.wait).hutang_usaha(row['Keterangan'], supplier_name_adjustment(row['Nama Anggota'], supplier_name), int(row['Hutang Dagang']), "Hutang Usaha", row['Tanggal'])

        if(not pd.isna(row['Pinjaman Gudang'])):
            BankOutTransaction(bot.driver, bot.wait).pinjaman(row['Keterangan'], member_name_adjusment(nama_anggota(row['Nama Anggota']), employees_name), int(row['Pinjaman Gudang']), "Pinjaman karyawan Feedmill", row['Tanggal'])
        if(not pd.isna(row['Pinjaman Farm'])):
            BankOutTransaction(bot.driver, bot.wait).pinjaman(row['Keterangan'], member_name_adjusment(nama_anggota(row['Nama Anggota']), employees_name), int(row['Pinjaman Farm']), "Pinjaman karyawan Farm", row['Tanggal'])
        if(not pd.isna(row['Pinjaman Security'])):
            BankOutTransaction(bot.driver, bot.wait).pinjaman(row['Keterangan'], member_name_adjusment(nama_anggota(row['Nama Anggota']), employees_name), int(row['Pinjaman Security']), "Pinjaman karyawan Security", row['Tanggal'])
        if(not pd.isna(row['Pinjaman CAM'])):
            BankOutTransaction(bot.driver, bot.wait).pinjaman(row['Keterangan'], member_name_adjusment(nama_anggota(row['Nama Anggota']), employees_name), int(row['Pinjaman CAM']), "Pinjaman karyawan CAM", row['Tanggal'])
        if(not pd.isna(row['Pinjaman PWM'])):
            BankOutTransaction(bot.driver, bot.wait).pinjaman(row['Keterangan'], member_name_adjusment(nama_anggota(row['Nama Anggota']), employees_name), int(row['Pinjaman PWM']), "Pinjaman karyawan PWM", row['Tanggal'])
        if(not pd.isna(row['Pinjaman PMP'])):
            BankOutTransaction(bot.driver, bot.wait).pinjaman(row['Keterangan'], member_name_adjusment(nama_anggota(row['Nama Anggota']), employees_name), int(row['Pinjaman PMP']), "Pinjaman karyawan PMP", row['Tanggal'])
        
        if(not pd.isna(row['Simpanan Gudang'])):
            BankOutTransaction(bot.driver, bot.wait).simpanan(row['Keterangan'], member_name_adjusment(nama_anggota(row['Nama Anggota']), employees_name), int(row['Simpanan Gudang']), "Simpanan wajib dan sukarela karyawan Gudang", row['Tanggal'])
        if(not pd.isna(row['Simpanan Farm'])):
            BankOutTransaction(bot.driver, bot.wait).simpanan(row['Keterangan'], member_name_adjusment(nama_anggota(row['Nama Anggota']), employees_name), int(row['Simpanan Farm']), "Simpanan wajib dan sukarela karyawan Farm", row['Tanggal'])
        if(not pd.isna(row['Simpanan Security'])):
            BankOutTransaction(bot.driver, bot.wait).simpanan(row['Keterangan'], member_name_adjusment(nama_anggota(row['Nama Anggota']), employees_name), int(row['Simpanan Security']), "Simpanan wajib dan sukarela karyawan Security", row['Tanggal'])
        if(not pd.isna(row['Simpanan CAM'])):
            BankOutTransaction(bot.driver, bot.wait).simpanan(row['Keterangan'], member_name_adjusment(nama_anggota(row['Nama Anggota']), employees_name), int(row['Simpanan CAM']), "Simpanan wajib dan sukarela karyawan CAM", row['Tanggal'])
        if(not pd.isna(row['Simpanan PWM'])):
            BankOutTransaction(bot.driver, bot.wait).simpanan(row['Keterangan'], member_name_adjusment(nama_anggota(row['Nama Anggota']), employees_name), int(row['Simpanan PWM']), "Simpanan wajib dan sukarela karyawan PWM", row['Tanggal'])
        if(not pd.isna(row['Simpanan PMP'])):
            BankOutTransaction(bot.driver, bot.wait).simpanan(row['Keterangan'], member_name_adjusment(nama_anggota(row['Nama Anggota']), employees_name), int(row['Simpanan PMP']), "Simpanan wajib dan sukarela karyawan PMP", row['Tanggal'])

    if row['Kategori Transaksi'] == 'Kas Keluar':
        if(not pd.isna(row["Pengalihan Kas"])):
            if(row["Keterangan"].__contains__('Pengalihan kas ke rek bank')): # make sure lagi untuk yang akan melakukan pengalihan kas
                CashOutTransaction(bot.driver, bot.wait).pengalihan_kas(row["Keterangan"], row["Nama Anggota"], int(row["Pengalihan Kas"]), "Buku kas", row["Tanggal"])
        # Pengajulan Pinjaman cash out
        if(not pd.isna(row['Pinjaman Gudang'])):
            CashOutTransaction(bot.driver, bot.wait).pinjaman_cash(row['Keterangan'], find_employe_name_by_code(row['Nama Anggota']), int(row['Pinjaman Gudang']), "Pinjaman karyawan Feedmill", row['Tanggal'])
        if(not pd.isna(row['Pinjaman Farm'])):
            CashOutTransaction(bot.driver, bot.wait).pinjaman_cash(row['Keterangan'], find_employe_name_by_code(row['Nama Anggota']), int(row['Pinjaman Farm']), "Pinjaman karyawan Feedmill", row['Tanggal'])
        if(not pd.isna(row['Pinjaman Security'])):
            CashOutTransaction(bot.driver, bot.wait).pinjaman_cash(row['Keterangan'], find_employe_name_by_code(row['Nama Anggota']), int(row['Pinjaman Security']), "Pinjaman karyawan Feedmill", row['Tanggal'])
        if(not pd.isna(row['Pinjaman CAM'])):
            CashOutTransaction(bot.driver, bot.wait).pinjaman_cash(row['Keterangan'], find_employe_name_by_code(row['Nama Anggota']), int(row['Pinjaman CAM']), "Pinjaman karyawan Feedmill", row['Tanggal'])
        if(not pd.isna(row['Pinjaman PWM'])):
            CashOutTransaction(bot.driver, bot.wait).pinjaman_cash(row['Keterangan'], find_employe_name_by_code(row['Nama Anggota']), int(row['Pinjaman PWM']), "Pinjaman karyawan Feedmill", row['Tanggal'])
        if(not pd.isna(row['Pinjaman PMP'])):
            CashOutTransaction(bot.driver, bot.wait).pinjaman_cash(row['Keterangan'], find_employe_name_by_code(row['Nama Anggota']), int(row['Pinjaman PMP']), "Pinjaman karyawan Feedmill", row['Tanggal'])

        # Pengambilan simpanan
        if(not pd.isna(row['Pengambilan Simpanan Gudang'])):
            CashOutTransaction(bot.driver, bot.wait).pengambilan_simpanan(row['Keterangan'], find_employe_name_by_code(row['Nama Anggota']), int(row['Pengambilan Simpanan Gudang']), "Simpanan wajib dan sukarela karyawan Gudang", row['Tanggal'])
        if(not pd.isna(row['Pengambilan Simpanan Farm'])):
            CashOutTransaction(bot.driver, bot.wait).pengambilan_simpanan(row['Keterangan'], find_employe_name_by_code(row['Nama Anggota']), int(row['Pengambilan Simpanan Farm']), "Simpanan wajib dan sukarela karyawan Farm", row['Tanggal'])
        if(not pd.isna(row['Pengambilan Simpanan Security'])):
            CashOutTransaction(bot.driver, bot.wait).pengambilan_simpanan(row['Keterangan'], find_employe_name_by_code(row['Nama Anggota']), int(row['Pengambilan Simpanan Security']), "Simpanan wajib dan sukarela karyawan Security dan Pupuk", row['Tanggal'])
        if(not pd.isna(row['Pengambilan Simpanan CAM'])):
            CashOutTransaction(bot.driver, bot.wait).pengambilan_simpanan(row['Keterangan'], find_employe_name_by_code(row['Nama Anggota']), int(row['Pengambilan Simpanan CAM']), "Simpanan wajib dan sukarela karyawan CAM", row['Tanggal'])
        if(not pd.isna(row['Pengambilan Simpanan PWM'])):
            CashOutTransaction(bot.driver, bot.wait).pengambilan_simpanan(row['Keterangan'], find_employe_name_by_code(row['Nama Anggota']), int(row['Pengambilan Simpanan PWM']), "Simpanan wajib dan sukarela karyawan PWM", row['Tanggal'])
        if(not pd.isna(row['Pengambilan Simpanan PMP'])):
            CashOutTransaction(bot.driver, bot.wait).pengambilan_simpanan(row['Keterangan'], find_employe_name_by_code(row['Nama Anggota']), int(row['Pengambilan Simpanan PMP']), "Simpanan wajib dan sukarela karyawan PMP", row['Tanggal'])
        
        # Gaji
        if(not pd.isna(row['Gaji'])):
            CashOutTransaction(bot.driver, bot.wait).non_division_account_cash_out(row['Keterangan'], row['Nama Anggota'], int(row['Gaji']), "Gaji Manajemen", row['Tanggal'])
        # Hutang usaha
        if(not pd.isna(row['Hutang Usaha'])):
            if row['Keterangan'].__contains__('Pembayaran hutang usaha'):
                CashOutTransaction(bot.driver, bot.wait).hutang_usaha_kas(row['Keterangan'], most_similar_word(row['Nama Anggota'], supplier_name), int(row['Hutang Usaha']), "Hutang Usaha", row['Tanggal'])
        # ATK
        if(not pd.isna(row['ATK'])):
            CashOutTransaction(bot.driver, bot.wait).non_division_account_cash_out(row['Keterangan'], row['Nama Anggota'], int(row['ATK']), "Biaya Alat Tulis Kantor", row['Tanggal'])

        # Operasional
        if(not pd.isna(row['Operasional'])):
            if row['Nama Anggota'].__contains__('Operasional'):
                CashOutTransaction(bot.driver, bot.wait).non_division_account_cash_out(row['Keterangan'], row['Nama Anggota'], int(row['Operasional']), "Biaya Serba-Serbi", row['Tanggal'])
        
        # Lain-lain
        if(not pd.isna(row['Lain-lain'])):
            if row['Nama Anggota'].__contains__('Bahan Pembantu'): # Pembelian bahan pembantu 
                CashOutTransaction(bot.driver, bot.wait).non_division_account_cash_out(row['Keterangan'], row['Nama Anggota'], int(row['Lain-lain']), "Pembelian bahan pembantu", row['Tanggal'])