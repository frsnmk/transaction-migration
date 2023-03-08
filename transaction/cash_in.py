from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select

class CashInTransaction:
    def __init__(self, driver, wait):
        '''driver: Driver chrome yang akan dijalankan
        wait: Object untuk explisit wait
        '''
        self.driver = driver
        self.wait = wait

    def non_division_account(self, keterangan, nama_anggota, amount, account, date):
        '''Cash in Transaction.\n
        Melakukan transaksi yang masuk ke kas yang tidak melibatkan anggota berdivisi:\n
        - Pemasukan lain-lain. 
        '''
        self.driver.get('http://localhost:8000/cash/create_in')

        self.driver.execute_script(f"document.getElementById('transactionDate').value='{date}'")

        self.driver.find_element(By.XPATH, '//*[@id="submit_cash_in"]/div[1]/div[3]/span/span[1]/span').click()

        account_search_el = self.wait.until(
            EC.presence_of_element_located((By.CLASS_NAME, 'select2-search__field'))
        ) # mencari element untuk melakukan input pencarian
        account_search_el.send_keys(account) # malakukan input pencarian
        account_search_result_el = self.wait.until(
            EC.presence_of_element_located((By.XPATH, f"//ul[@id='select2-account-results']/li[contains(text(),'{account}')]"))
        ) # menunggu hasil pencarian element sampai ada tag li yang mengandung text dari akun
        account_search_result_el.click()

        # Mencari dan mengetikan pada field refensi
        self.driver.find_element(By.ID, 'defaultReference').send_keys(nama_anggota)

        # Mencari dan mengetikan pada field Jumlah
        self.driver.find_element(By.ID, 'defaultAmount').send_keys(amount)

        # Mencari dan mengetikan pada field Deskripsi
        self.driver.find_element(By.ID, 'defaultDesc').send_keys(keterangan)

        # Mencari dan menglik tombol simpan
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
            print(nama_anggota)
            self.driver.find_element(By.XPATH, '/html/body/div[4]/div/div[3]/button[1]').click()
    
    def angsuran(self, keterangan, nama_anggota, amount, account, date):
        '''Cash in transaction.\n
        Melakukan angsuran pinjaman dari anggota menuju kas.
        '''
        self.driver.get('http://localhost:8000/cash/create_in')

        self.driver.execute_script(f"document.getElementById('transactionDate').value='{date}'")

        self.driver.find_element(By.XPATH, '//*[@id="submit_cash_in"]/div[1]/div[3]/span/span[1]/span').click()

        account_search_el = self.wait.until(
            EC.presence_of_element_located((By.CLASS_NAME, 'select2-search__field'))
        ) # mencari element untuk melakukan input pencarian
        account_search_el.send_keys(account) # malakukan input pencarian
        account_search_result_el = self.wait.until(
            EC.presence_of_element_located((By.XPATH, f"//ul[@id='select2-account-results']/li[contains(text(),'{account}')]"))
        ) # menunggu hasil pencarian element sampai ada tag li yang mengandung text dari akun
        account_search_result_el.click()

        employee_select2_el = self.wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, '//*[@id="installmentpaymentcollapse"]/div[1]/div[1]/span/span[1]/span')
            )
        ) # menunggu element select2 employee ditampilkan
        # self.driver.implicitly_wait(5)
        employee_select2_el.send_keys(Keys.ENTER)
        
        employee_search_el = self.wait.until(
            EC.presence_of_element_located(
                (By.CLASS_NAME, 'select2-search__field')
            )
        ) # menunggu element untuk memasukan pencarian anggota keluar
        employee_search_el.send_keys(nama_anggota) # mengtikan nama anggota
        try: 
            employee_search_result_el = self.wait.until(
                EC.presence_of_element_located(
                    (By.XPATH, f'''//ul[@id='select2-installmentPaymentEmployee-results']/li[text()="{nama_anggota}"]''')
                )
            ) # menunggu sampai ada nama anggota yang mirip di dropdown hasil pencarian
        except:
            employee_search_result_el = self.wait.until(
                EC.presence_of_element_located(
                    (By.XPATH, f'''//ul[@id='select2-installmentPaymentEmployee-results']/li[contains(text(), "{nama_anggota}")]''')
                )
            ) # menunggu sampai ada nama anggota yang mirip di dropdown hasil pencarian

        employee_search_result_el.click() # dan kemudian mengkliknya

        self.wait.until(
            EC.text_to_be_present_in_element_value(
                (By.ID, 'installmentPaymentAmount'),
                '0'
            ) # mencari element jumlah
        )
        amount_el = self.driver.find_element(By.ID, 'installmentPaymentAmount') # menghapus dlu
        amount_el.clear()
        amount_el.send_keys(amount) # mengisi lagi

        self.driver.find_element(By.ID, 'installmentPaymentDesc').send_keys(keterangan) # mengisi keterangan
        
        self.driver.find_element(By.ID, 'submit_cash').click() # mengklik tombol save

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
            print(nama_anggota)
            self.driver.find_element(By.XPATH, '/html/body/div[4]/div/div[3]/button[1]').click()

    def simpanan(self, keterangan, nama_anggota, amount, account, date):
        '''Cash in transaction.\n
        Melakukan aksi simpanan dari anggota ke kas.
        '''
        self.driver.get('http://localhost:8000/cash/create_in')

        self.driver.execute_script(f"document.getElementById('transactionDate').value='{date}'")

        self.driver.find_element(By.XPATH, '//*[@id="submit_cash_in"]/div[1]/div[3]/span/span[1]/span').click() # mencari element account dan mengkliknya
        search_account_el = self.wait.until(
            EC.presence_of_element_located((By.CLASS_NAME, 'select2-search__field'))
        ) # menunggu dan kemudian menangkap element text input untuk search akun
        search_account_el.send_keys(account) # mengetikan akun
        search_result_account_el = self.wait.until(
            EC.presence_of_element_located(
                (By.XPATH, f'''//*[@id="select2-account-results"]/li[contains(text(), "{account}")]''')
             )
        )# menunggu dan menangkap element yang memiliki text yang sesuai dengan nama akun
        search_result_account_el.click() # mencari dan mengklik element hasil pencarian

        employee_select2_el = self.wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, '//*[@id="depositcollapse"]/div[1]/div[1]/span/span[1]/span')
            )
        ) # menunggu element select2 employee ditampilkan
        employee_select2_el.send_keys(Keys.ENTER)
        
        employee_search_el = self.wait.until(
        EC.presence_of_element_located(
                (By.CLASS_NAME, 'select2-search__field')
            )
        ) # menunggu element untuk memasukan pencarian anggota keluar
        employee_search_el.send_keys(nama_anggota) # mengtikan nama anggota
        try: # handle error jika ada nama yang mirip tetapi yang kepilihnya itu malah yang kembarannya
            employee_search_result_el = self.wait.until(
                EC.presence_of_element_located(
                    (By.XPATH, f'''//ul[@id='select2-depositEmployee-results']/li[text()="{nama_anggota}"]''')
                )
            )# menunggu sampai ada nama anggota yang mirip di dropdown hasil pencarian
        except:
            employee_search_result_el = self.wait.until(
                EC.presence_of_element_located(
                    (By.XPATH, f'''//ul[@id='select2-depositEmployee-results']/li[contains(text(), "{nama_anggota}")]''')
                )
            )# menunggu sampai ada nama anggota yang mirip di dropdown hasil pencarian

        employee_search_result_el.click() # dan kemudian mengkliknya

        if "pokok" in account:
            deposit_type_select_el = Select(self.driver.find_element(By.ID, 'depositType'))
            deposit_type_select_el.select_by_value("Pokok")

        self.driver.find_element(By.ID, 'depositAmount').send_keys(amount)

        self.driver.find_element(By.ID, 'desc').send_keys(keterangan)

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
            print(nama_anggota)
            self.driver.find_element(By.XPATH, '/html/body/div[4]/div/div[3]/button[1]').click()