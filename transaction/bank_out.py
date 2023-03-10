from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select

from transaction.helper import find_angsuran

class BankOutTransaction:

    def __init__(self, driver, wait):
        '''driver: Driver chrome yang akan dijalankan
        wait: Object untuk explisit wait
        '''
        self.driver = driver
        self.wait = wait

    def pengalihan(self, keterangan, nama_anggota, amount, account, date):
        '''Bank Out Transction.\n
        Melakukan pengalihan saldo dari bank ke kas.
        '''
        self.driver.get('http://localhost:8000/bank-transaction/outgoing/create')
        self.driver.execute_script(f"document.getElementById('transactionDate').value='{date}'")
        self.driver.find_element(By.XPATH, '//*[@id="cashOutForm"]/div[1]/div[3]/div/span/span[1]/span').click() # Click acount text field
        search_account_input_el = self.wait.until(
            EC.presence_of_element_located((By.XPATH, '/html/body/span/span/span[1]/input'))
        ) # Wait account input element ditampilkan
        search_account_input_el.send_keys(account) # mengetikan nama akun (kondisi wait sudah selesai)
        account_search_result_el = self.wait.until(
            EC.presence_of_element_located(
                (By.XPATH, f'''//ul[@id="select2-account-results"]/li[contains(text(),'{account}')]''')
            )
        ) # menunggu hasil list hasil pencarian ditampilkan
        account_search_result_el.click() # klik element hasil pencarian

        self.driver.find_element(by=By.ID, value='diversionReference').send_keys(nama_anggota) # Mencari dan mengetikan pada field refensi
        self.driver.find_element(by=By.ID, value='diversionAmount').send_keys(amount) # Mencari dan mengetikan pada field Jumlah
        self.driver.find_element(by=By.ID, value='diversionDesc').send_keys(keterangan) # Mencari dan mengetikan pada field Deskripsi
        self.driver.find_element(by=By.ID, value='save').click() # Mencari dan menglik tombol simpan

        # Menunggu sweet alert muncul dan kemudian mengklik tombol ok
        try:
            self.wait.until(
                EC.presence_of_element_located(
                    (By.CLASS_NAME, 'swal-icon--success')
                )
            )
            self.driver.find_element(by=By.CLASS_NAME, value='swal-button--confirm').send_keys(Keys.ENTER)
            self.driver.get('http://localhost:8000/cash/create_in')
        except:
            self.wait.until(
                EC.presence_of_element_located(
                    (By.CLASS_NAME, 'swal-icon--error')
                )
            )
            text_warning = self.driver.find_element(By.CLASS_NAME, 'swal-text').text
            print(nama_anggota, text_warning, account)
            self.driver.find_element(by=By.CLASS_NAME, value='swal-button--confirm').send_keys(Keys.ENTER)
            self.driver.get('http://localhost:8000/bank-transaction/outgoing/create')

        self.driver.execute_script(f"document.getElementById('transactionDate').value='{date}'")

        self.driver.find_element(By.XPATH, '//*[@id="submit_cash_in"]/div[1]/div[3]/span/span[1]/span').click() # Click acount text field
        search_account_input_el = self.wait.until(
            EC.presence_of_element_located((By.XPATH, '/html/body/span/span/span[1]/input'))
        ) # Wait account input element ditampilkan
        search_account_input_el.send_keys("Buku Kas") # mengetikan nama akun (kondisi wait sudah selesai)
        self.wait.until(
            EC.text_to_be_present_in_element(
                (By.XPATH, '//*[@id="select2-account-results"]/li'),
                 "Buku kas"
            )
        ) # menunggu hasil list hasil pencarian ditampilkan
        self.driver.find_element(By.XPATH, '//*[@id="select2-account-results"]/li').click() # klik element hasil pencarian

        self.driver.find_element(By.ID, 'diversionType').click()

        select_pengalihan = Select(self.driver.find_element(By.ID, 'diversionType'))
        select_pengalihan.select_by_visible_text("Ya")

        self.driver.find_element(By.ID, 'diversionReference').send_keys(nama_anggota)
        self.driver.find_element(By.ID, 'diversionAmount').send_keys(amount)
        self.driver.find_element(By.ID, 'diversionDesc').send_keys(keterangan)

        self.driver.find_element(By.ID, 'submit_cash').click()

         # Menunggu sweet alert muncul dan kemudian mengklik tombol ok
        try:
            self.wait.until(
                EC.presence_of_element_located(
                    (By.CLASS_NAME, 'swal2-success')
                )
            )
            self.driver.find_element(By.XPATH, '/html/body/div[4]/div/div[3]/button[1]').click()
        except:
            self.wait.until(
                EC.presence_of_element_located(
                    (By.CLASS_NAME, 'swal2-error')
                )
            )
            text_warning = self.driver.find_element(By.CLASS_NAME, 'swal-text').text
            print(nama_anggota, text_warning, account)
            self.driver.find_element(By.XPATH, '/html/body/div[4]/div/div[3]/button[1]').click()
    
    def non_division_account(self, keterangan, nama_anggota, amount, account, date):
        '''Bank Out Transaction.\n
        Transaksi bank keluar yang tidak membutuhkan divisi:
        - Serba/i
        - PPOB
        - Biaya lain-lain
        '''
        self.driver.get('http://localhost:8000/bank-transaction/outgoing/create')
        self.driver.execute_script(f"document.getElementById('transactionDate').value='{date}'")
        self.driver.find_element(By.XPATH, '//*[@id="cashOutForm"]/div[1]/div[3]/div/span/span[1]/span').click() # Click acount text field
        search_account_input_el = self.wait.until(
            EC.presence_of_element_located((By.XPATH, '/html/body/span/span/span[1]/input'))
        ) # Wait account input element ditampilkan
        search_account_input_el.send_keys(account) # mengetikan nama akun (kondisi wait sudah selesai)
        self.wait.until(
            EC.text_to_be_present_in_element(
                (By.XPATH, '//*[@id="select2-account-results"]/li'),
                 account
            )
        ) # menunggu hasil list hasil pencarian ditampilkan
        self.driver.find_element(By.XPATH, '//*[@id="select2-account-results"]/li').click() # klik element hasil pencarian

        # Mencari dan mengetikan pada field refensi
        self.driver.find_element(by=By.NAME, value='reference').send_keys(nama_anggota)

        # Mencari dan mengetikan pada field Jumlah
        self.driver.find_element(by=By.NAME, value='amount').send_keys(amount)

        # Mencari dan mengetikan pada field Deskripsi
        self.driver.find_element(by=By.NAME, value='desc').send_keys(keterangan)

        # Mencari dan menglik tombol simpan
        self.driver.find_element(by=By.ID, value='save').click()

         # Menunggu sweet alert muncul dan kemudian mengklik tombol ok
        try:
            self.wait.until(
                EC.presence_of_element_located(
                    (By.CLASS_NAME, 'swal-icon--success')
                )
            )
            self.driver.find_element(by=By.CLASS_NAME, value='swal-button--confirm').send_keys(Keys.ENTER)
        except:
            self.wait.until(
                EC.presence_of_element_located(
                    (By.CLASS_NAME, 'swal-icon--error')
                )
            )
            text_warning = self.driver.find_element(By.CLASS_NAME, 'swal-text').text
            print(nama_anggota, text_warning, account)
            self.driver.find_element(by=By.CLASS_NAME, value='swal-button--confirm').send_keys(Keys.ENTER)

    def hutang_usaha(self, keterangan, nama_anggota, amount, account, date):
        '''Bank Out Transction.\n
        Pembayaran hutang usaha dari rekening bank
        '''
        self.driver.get('http://localhost:8000/bank-transaction/outgoing/create')
        self.driver.execute_script(f"document.getElementById('transactionDate').value='{date}'")
        self.driver.find_element(By.XPATH, '//*[@id="cashOutForm"]/div[1]/div[3]/div/span/span[1]/span').click() # Click acount text field
        search_account_input_el = self.wait.until(
            EC.presence_of_element_located((By.XPATH, '/html/body/span/span/span[1]/input'))
        ) # Wait account input element ditampilkan
        search_account_input_el.send_keys(account) # mengetikan nama akun (kondisi wait sudah selesai)
        self.wait.until(
            EC.text_to_be_present_in_element(
                (By.XPATH, '//*[@id="select2-account-results"]/li'),
                 account
            )
        ) # menunggu hasil list hasil pencarian ditampilkan
        self.driver.find_element(By.XPATH, '//*[@id="select2-account-results"]/li').click() # klik element hasil pencarian

        supllier_el = self.wait.until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="accountPayableCollapse"]/div[1]/div[1]/div/span/span[1]/span'))
        ) # menunggu element supplier ditampilkan
        supllier_el.click() # click supplier text field

        search_supllier_el = self.wait.until(
            EC.presence_of_element_located((By.XPATH, '/html/body/span/span/span[1]/input'))
        ) # menunggu text field untuk search ditampilkan
        search_supllier_el.send_keys(nama_anggota) # mengetikan keyword untuk pencarian
      
        self.wait.until(
            EC.text_to_be_present_in_element(
                (By.XPATH, '//*[@id="select2-accountPayableSupplier-results"]/li'),
                nama_anggota)
        ) # Menunggu hasil element yang dicari mucul
        self.driver.find_element(By.XPATH, '//*[@id="select2-accountPayableSupplier-results"]/li').click() # klik element yang dicari

        self.driver.find_element(By.ID, 'accountPayableSupplierAmount').send_keys(amount) 

        self.driver.find_element(By.ID, 'accountPayableSupplierDesc').send_keys(keterangan)
        
        # Mencari dan menglik tombol simpan
        self.driver.find_element(by=By.ID, value='save').click()
        
        # Menunggu sweet alert muncul dan kemudian mengklik tombol ok
        try:
            self.wait.until(
                EC.presence_of_element_located(
                    (By.CLASS_NAME, 'swal-icon--success')
                )
            )
            self.driver.find_element(by=By.CLASS_NAME, value='swal-button--confirm').send_keys(Keys.ENTER)
        except:
            self.wait.until(
                EC.presence_of_element_located(
                    (By.CLASS_NAME, 'swal-icon--error')
                )
            )
            text_warning = self.driver.find_element(By.CLASS_NAME, 'swal-text').text
            print(nama_anggota, text_warning, account)
            self.driver.find_element(by=By.CLASS_NAME, value='swal-button--confirm').send_keys(Keys.ENTER)

    def pinjaman(self, keterangan, nama_anggota, amount, account, date):
        '''Transaksi Bank Keluar.\n
        Pengajuan pinjaman dari anggota ke rekening bank  yang lansung diacc.
        '''        
        self.driver.get('http://localhost:8000/bank-transaction/outgoing/create')
        self.driver.execute_script(f"document.getElementById('transactionDate').value='{date}'")

        self.driver.find_element(By.XPATH, '//*[@id="cashOutForm"]/div[1]/div[3]/div/span/span[1]/span').click() # mencari dan mengklik element account (agar muncul text input)
        search_account_el = self.wait.until(
            EC.presence_of_element_located((By.XPATH, '/html/body/span/span/span[1]/input'))
        ) # menunggu element text input ditampilkan
        search_account_el.send_keys(account) # mengetikan akun pada text input yang telah tersedia
        self.wait.until(
            EC.presence_of_element_located(
                (By.XPATH, f'''//*[@id="select2-account-results"]/li[contains(text(),'{account}')]''')
            )
        ) # Menunggu hasil pencarian akun tampil
        self.driver.find_element(By.XPATH, '//*[@id="select2-account-results"]/li').click() # mecari dan mengklik element hasil pencarian akun
        
        select2_employee_el = self.wait.until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="loanCollapse"]/div[1]/div[1]/div/span/span[1]/span'))
        ) # mengunggu element employee ditampilkan
        select2_employee_el.send_keys(Keys.ENTER) # mengklik element tersebut agar tampil text input pencariannya.
        search_employee_el = self.wait.until(
            EC.presence_of_element_located(
                (By.XPATH, '/html/body/span/span/span[1]/input'),
            )
        ) # Menunggu text input ditampilkan
        search_employee_el.send_keys(nama_anggota) # mengetikan nama anggota pada text input yang ditampilkan
        try: # handle error jika ada nama yang mirip tetapi yang kepilihnya itu malah yang kembarannya
            employee_search_result_el = self.wait.until(
                EC.presence_of_element_located(
                    (By.XPATH, f'''//*[@id="select2-loanEmployee-results"]/li[contains(text()='{nama_anggota}')]''')
                )
            ) # menunggu text hasil pencarian ditampilkan
        except:
            employee_search_result_el = self.wait.until(
                EC.presence_of_element_located(
                    (By.XPATH, f'''//*[@id="select2-loanEmployee-results"]/li[contains(text(),'{nama_anggota}')]''')
                )
            ) # menunggu text hasil pencarian ditampilkan

        employee_search_result_el.click() # dann= kmeudian mengkliknya

        self.driver.find_element(By.ID, 'loanDesc').send_keys(keterangan)

        self.driver.find_element(By.ID, 'loanAmount').send_keys(amount)
        installment_period = self.driver.find_element(By.ID, 'installmentPeriod')
        installment_period.send_keys(find_angsuran(keterangan))
        installment_period.send_keys(Keys.TAB)
        self.driver.find_element(By.ID, 'purpose').send_keys('-')
        self.driver.find_element(By.ID, 'save').click()
        
        try:
            self.wait.until(
                EC.presence_of_element_located(
                    (By.CLASS_NAME, 'swal-icon--success')
                )
            )
            self.driver.find_element(by=By.CLASS_NAME, value='swal-button--confirm').send_keys(Keys.ENTER)
        except:
            self.wait.until(
                EC.presence_of_element_located(
                    (By.CLASS_NAME, 'swal-icon--error')
                )
            )
            text_warning = self.driver.find_element(By.CLASS_NAME, 'swal-text').text
            print(nama_anggota, text_warning, account)
            self.driver.find_element(by=By.CLASS_NAME, value='swal-button--confirm').send_keys(Keys.ENTER)

    def simpanan(self, keterangan, nama_anggota, amount, account, date):
        '''Bank Out Transction.\n
        Penarikan simpanan oleh anggota.
        '''
        self.driver.get('http://localhost:8000/bank-transaction/outgoing/create')
        self.driver.execute_script(f"document.getElementById('transactionDate').value='{date}'")
        self.driver.find_element(By.XPATH, '//*[@id="cashOutForm"]/div[1]/div[3]/div/span/span[1]/span').click() # mencari dan mengklik element account (agar muncul text input)
        search_account_el = self.wait.until(
            EC.presence_of_element_located((By.XPATH, '/html/body/span/span/span[1]/input'))
        ) # menunggu element text input ditampilkan
        search_account_el.send_keys(account) # mengetikan akun pada text input yang telah tersedia
        self.wait.until(
            EC.text_to_be_present_in_element(
                (By.XPATH, '//*[@id="select2-account-results"]/li'),
                account
            )
        ) # Menunggu hasil pencarian akun tampil
        self.driver.find_element(By.XPATH, '//*[@id="select2-account-results"]/li').click() # mecari dan mengklik element hasil pencarian akun

        select2_employee_el = self.wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, '//*[@id="depositCollapse"]/div[1]/div[1]/div/span/span[1]/span')
            )
        )
        select2_employee_el.send_keys(Keys.ENTER)

        search_employee_el = self.wait.until(
            EC.presence_of_element_located((By.XPATH, '/html/body/span/span/span[1]/input'))
        )
        search_employee_el.send_keys(nama_anggota)

        try: # handle error jika ada nama yang mirip tetapi yang kepilihnya itu malah yang kembarannya
            employee_search_result_el = self.wait.until(
                EC.presence_of_element_located(
                    (By.XPATH, f'''//*[@id="select2-depositWithdrawalEmployee-results"]/li[contains(text()='{nama_anggota}')]''')
                )
            ) # menunggu text hasil pencarian ditampilkan
        except:
            employee_search_result_el = self.wait.until(
                EC.presence_of_element_located(
                    (By.XPATH, f'''//*[@id="select2-depositWithdrawalEmployee-results"]/li[contains(text(),'{nama_anggota}')]''')
                )
            ) # menunggu text hasil pencarian ditampilkan

        employee_search_result_el.click() # dann= kmeudian mengkliknya

        self.driver.find_element(By.ID, 'depositWithdrawalAmount').send_keys(amount)
        self.driver.find_element(By.ID, 'depositWithdrawalDesc').send_keys(keterangan)
        self.driver.find_element(By.ID, 'save').click()
        # Menunggu sweet alert muncul dan kemudian mengklik tombol ok
        try:
            self.wait.until(
                EC.presence_of_element_located(
                    (By.CLASS_NAME, 'swal-icon--success')
                )
            )
            self.driver.find_element(by=By.CLASS_NAME, value='swal-button--confirm').send_keys(Keys.ENTER)
        except:
            self.wait.until(
                EC.presence_of_element_located(
                    (By.CLASS_NAME, 'swal-icon--error')
                )
            )
            text_warning = self.driver.find_element(By.CLASS_NAME, 'swal-text').text
            print(nama_anggota, text_warning, account)
            self.driver.find_element(by=By.CLASS_NAME, value='swal-button--confirm').send_keys(Keys.ENTER)