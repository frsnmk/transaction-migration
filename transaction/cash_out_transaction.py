from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

class CashOutTransaction:

    def __init__(self, driver, wait):
        '''driver: Driver chrome yang akan dijalankan
        wait: Object untuk explisit wait
        '''
        self.driver = driver
        self.wait = wait

    def pengalihan_kas(self, keterangan, nama_anggota, amount, account, date):
        '''Cash Out Transaction.\n
        Pengalihan saldo dari kas ke rekening bank.
        '''
        self.driver.get("http://localhost:8000/cash/create_out")
        self.driver.execute_script(f"document.getElementById('transactionDate').value='{date}'")

        self.driver.find_element(By.XPATH, '//*[@id="submit_cash_out"]/div[1]/div[3]/span/span[1]/span').click()
        account_search_el = self.wait.until(
            EC.presence_of_element_located((By.XPATH, '/html/body/span/span/span[1]/input'))
        )
        account_search_el.send_keys(account)
        account_search_result_el = self.wait.until(
            EC.presence_of_element_located(
                (By.XPATH, f'''//ul[@id="select2-account-results"]/li[contains(text(),'{account}')]''')
            )
        )
        account_search_result_el.click()
        
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
            self.driver.get('http://localhost:8000/bank-transaction/incoming/create')
        except:
            self.wait.until(
                EC.presence_of_element_located(
                    (By.CLASS_NAME, 'swal2-error')
                )
            )
            print(nama_anggota)
            self.driver.find_element(By.XPATH, '/html/body/div[4]/div/div[3]/button[1]').click()
            self.driver.get('http://localhost:8000/cash/create_in')

        self.driver.execute_script(f"document.getElementById('transactionDate').value='{date}'")
        self.driver.find_element(By.XPATH, '//*[@id="select2-account-container"]').click() # mencari element account dan mengkliknya
        search_account_el = self.wait.until(
            EC.presence_of_element_located((By.XPATH, '/html/body/span/span/span[1]/input'))
        ) # menunggu dan kemudian menangkap element text input untuk search akun
        search_account_el.send_keys("Buku Bank BRI Koperasi") # mengetikan akun
        search_result_account_el = self.wait.until(
            EC.presence_of_element_located(
                (By.XPATH, '''//*[@id="select2-account-results"]/li[contains(text(), "Buku Bank BRI Koperasi")]''')
             )
        )# menunggu dan menangkap element yang memiliki text yang sesuai dengan nama akun
        search_result_account_el.click() # mencari dan mengklik element hasil pencarian

        select_pengalihan = Select(self.driver.find_element(By.ID, 'diversionType'))
        select_pengalihan.select_by_visible_text("Ya")

        self.driver.find_element(By.ID, 'diversionReference').send_keys(nama_anggota)
        self.driver.find_element(By.ID, 'diversionAmount').send_keys(amount)
        self.driver.find_element(By.ID, 'diversionDesc').send_keys(keterangan)

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


    def pinjaman_cash(self, keterangan, nama_anggota, amount, account, date):
        '''Cash Out transaction.\n
        Melakukan pengajuan pinjaman yang langsung disepakati.
        '''
        self.driver.get('http://localhost:8000/cash/create_out')
        self.driver.execute_script(f"document.getElementById('transactionDate').value='{date}'")

        self.driver.find_element(By.XPATH, '//*[@id="submit_cash_out"]/div[1]/div[3]/span/span[1]/span').click();
        search_account_el = self.wait.until(
            EC.presence_of_element_located((By.XPATH, '/html/body/span/span/span[1]/input'))
        )
        search_account_el.send_keys(account)
        account_search_result_el = self.wait.until(
            EC.presence_of_element_located((By.XPATH, f"//ul[@id='select2-account-results']/li[contains(text(),'{account}')]"))
        ) # menunggu hasil pencarian element sampai ada tag li yang mengandung text dari akun
        account_search_result_el.click()

        employee_select2_el = self.wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, '//*[@id="loanCollapse"]/div[1]/div[2]/div/span/span[1]/span')
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
                    (By.XPATH, f'''//ul[@id='select2-loanEmployee-results']/li[text()="{nama_anggota}"]''')
                )
            ) # menunggu sampai ada nama anggota yang mirip di dropdown hasil pencarian
        except:
            employee_search_result_el = self.wait.until(
                EC.presence_of_element_located(
                    (By.XPATH, f'''//ul[@id='select2-loanEmployee-results']/li[contains(text(), "{nama_anggota}")]''')
                )
            ) # menunggu sampai ada nama anggota yang mirip di dropdown hasil pencarian

        employee_search_result_el.click() # dan kemudian mengkliknya

        self.driver.find_element(By.ID, 'loanDesc').send_keys(keterangan)

        self.driver.find_element(By.ID, 'loanAmount').send_keys(amount)
        installment_period = self.driver.find_element(By.ID, 'installmentPeriod')
        # installment_period.send_keys(find_angsuran(keterangan))
        installment_period.send_keys(2)
        installment_period.send_keys(Keys.TAB)
        self.driver.find_element(By.ID, 'purpose').send_keys('-')
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

    def pengambilan_simpanan(self, keterangan, nama_anggota, amount, account, date):
        '''Cash Out transaction.\n
        Melakukan penarikan simpanan dari kas.
        '''
        self.driver.get('http://localhost:8000/cash/create_out')
        self.driver.execute_script(f"document.getElementById('transactionDate').value='{date}'")

        self.driver.find_element(By.XPATH, '//*[@id="submit_cash_out"]/div[1]/div[3]/span/span[1]/span').click();
        search_account_el = self.wait.until(
            EC.presence_of_element_located((By.XPATH, '/html/body/span/span/span[1]/input'))
        )
        search_account_el.send_keys(account)
        account_search_result_el = self.wait.until(
            EC.presence_of_element_located((By.XPATH, f"//ul[@id='select2-account-results']/li[contains(text(),'{account}')]"))
        ) # menunggu hasil pencarian element sampai ada tag li yang mengandung text dari akun
        account_search_result_el.click()

        employee_select2_el = self.wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, '//*[@id="withdrawcollapse"]/div[1]/div[1]/span/span[1]/span')
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
                    (By.XPATH, f'''//ul[@id='select2-withdrawEmployee-results']/li[text()="{nama_anggota}"]''')
                )
            ) # menunggu sampai ada nama anggota yang mirip di dropdown hasil pencarian
        except:
            employee_search_result_el = self.wait.until(
                EC.presence_of_element_located(
                    (By.XPATH, f'''//ul[@id='select2-withdrawEmployee-results']/li[contains(text(), "{nama_anggota}")]''')
                )
            ) # menunggu sampai ada nama anggota yang mirip di dropdown hasil pencarian

        employee_search_result_el.click() # dan kemudian mengkliknya
        
        self.driver.find_element(By.ID, 'withdrawAmount').send_keys(amount)
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
            text_warning = self.driver.find_element(By.CLASS_NAME, 'swal-text').text
            print(nama_anggota, text_warning, account)
            self.driver.find_element(By.XPATH, '/html/body/div[4]/div/div[3]/button[1]').click()

    def hutang_usaha_kas(self, keterangan, nama_anggota, amount, account, date):
        '''Cash Out Transaction.\n
        Melakukan pembayaran hutang usaha.
        '''
        self.driver.get('http://localhost:8000/cash/create_out')
        self.driver.execute_script(f"document.getElementById('transactionDate').value='{date}'")
        self.driver.find_element(By.XPATH, '//*[@id="submit_cash_out"]/div[1]/div[3]/span/span[1]/span').click();
        search_account_el = self.wait.until(
            EC.presence_of_element_located((By.XPATH, '/html/body/span/span/span[1]/input'))
        )
        search_account_el.send_keys(account)
        account_search_result_el = self.wait.until(
            EC.presence_of_element_located((By.XPATH, f"//ul[@id='select2-account-results']/li[contains(text(),'{account}')]"))
        ) # menunggu hasil pencarian element sampai ada tag li yang mengandung text dari akun
        account_search_result_el.click()

        supplier_select2_el = self.wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, '//*[@id="purchasepaymentcollapse"]/div[1]/div[1]/span/span[1]/span')
            )
        ) # menunggu element select2 supplier ditampilkan
        # self.driver.implicitly_wait(5)
        supplier_select2_el.send_keys(Keys.ENTER)
        
        supplier_search_el = self.wait.until(
            EC.presence_of_element_located(
                (By.CLASS_NAME, 'select2-search__field')
            )
        ) # menunggu element untuk memasukan pencarian anggota keluar
        supplier_search_el.send_keys(nama_anggota) # mengtikan nama anggota
        try: 
            supplier_search_result_el = self.wait.until(
                EC.presence_of_element_located(
                    (By.XPATH, f'''//ul[@id='select2-purchasespaymentSupplier-results']/li[text()="{nama_anggota}"]''')
                )
            ) # menunggu sampai ada nama anggota yang mirip di dropdown hasil pencarian
        except:
            supplier_search_result_el = self.wait.until(
                EC.presence_of_element_located(
                    (By.XPATH, f'''//ul[@id='select2-purchasespaymentSupplier-results']/li[contains(text(), "{nama_anggota}")]''')
                )
            ) # menunggu sampai ada nama anggota yang mirip di dropdown hasil pencarian

        supplier_search_result_el.click() # dan kemudian mengkliknya

        self.driver.find_element(By.ID, 'purchasespaymentAmount').send_keys(amount)
        self.driver.find_element(By.ID, 'purchasespaymentDesc').send_keys(keterangan)

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


    def non_division_account_cash_out(self, keterangan, nama_anggota, amount, account, date):
        '''Cash out transction.\n
        Melakukan pengeluaran lainnya yang tidak terikat anggota sepeti:\n
        - Gaji
        - ATK
        - Operasional
        - Lain-lain
        '''
        self.driver.get('http://localhost:8000/cash/create_out')
        self.driver.execute_script(f"document.getElementById('transactionDate').value='{date}'")
        self.driver.find_element(By.XPATH, '//*[@id="submit_cash_out"]/div[1]/div[3]/span/span[1]/span').click();
        search_account_el = self.wait.until(
            EC.presence_of_element_located((By.XPATH, '/html/body/span/span/span[1]/input'))
        )
        search_account_el.send_keys(account)
        account_search_result_el = self.wait.until(
            EC.presence_of_element_located((By.XPATH, f"//ul[@id='select2-account-results']/li[contains(text(),'{account}')]"))
        ) # menunggu hasil pencarian element sampai ada tag li yang mengandung text dari akun
        account_search_result_el.click()
        
        employee_el = self.wait.until(
            EC.presence_of_element_located(
                (By.ID, 'defaultReference')
            )
        )
        employee_el.send_keys(nama_anggota)
        self.driver.find_element(By.ID, 'defaultAmount').send_keys(amount)
        self.driver.find_element(By.ID, 'defaultDesc').send_keys(keterangan)

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
    