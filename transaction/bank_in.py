from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

from transaction.helper import find_barcode_by_item_name

class BankInTransaction:
    def __init__(self, driver, wait):
        '''driver: Driver chrome yang akan dijalankan
        wait: Object untuk explisit wait
        '''
        self.driver = driver
        self.wait = wait

    def non_division_account(self, keterangan, nama_anggota, amount, account, date):
        '''fungsi untuk melakukan penginputan otomatis untuk akun yang tidak memiliki divisi'''
        self.driver.get('http://localhost:8000/bank-transaction/incoming/create')
        self.driver.execute_script(f"document.getElementById('transactionDate').value='{date}'")

        self.driver.find_element(By.XPATH, '//*[@id="select2-account-container"]').click() # mencari element account dan mengkliknya
        
        account_search_el = self.wait.until(
            EC.presence_of_element_located((By.CLASS_NAME, 'select2-search__field'))
        ) # mencari element untuk melakukan input pencarian
        account_search_el.send_keys(account) # malakukan input pencarian

        account_search_result_el = self.wait.until(
            EC.presence_of_element_located(
                (By.XPATH, f"//ul[@id='select2-account-results']/li[contains(text(), '{account}')]")
            )
        )
        account_search_result_el.click()

        reference = self.wait.until(
            EC.presence_of_element_located(
                (By.ID, 'reference')
            )
        )
        reference.send_keys(nama_anggota)

        self.driver.find_element(By.ID, 'amount').send_keys(amount)

        self.driver.find_element(By.ID, 'desc').send_keys(keterangan)

        self.driver.find_element(By.ID, 'save').click()

        # Menunggu sweet alert muncul dan kemudian mengklik tombol ok
        try:
            self.wait.until(
                EC.text_to_be_present_in_element(
                    (By.CLASS_NAME, 'swal-title'),
                    'Berhasil'
                )
            )
            self.driver.find_element(by=By.CLASS_NAME, value='swal-button--confirm').send_keys(Keys.ENTER)
            self.driver.get('http://localhost:8000/bank-transaction/incoming/create')
        except:
            self.wait.until(
                EC.text_to_be_present_in_element(
                    (By.CLASS_NAME, 'swal-title'),
                    'Terjadi kesalahan'
                )
            )
            print(nama_anggota)
            self.driver.find_element(by=By.CLASS_NAME, value='swal-button--confirm').send_keys(Keys.ENTER)
            self.driver.get('http://localhost:8000/bank-transaction/incoming/create')

    def angsuran(self, keterangan, nama_anggota, amount, account, date):
        '''Bank in Transaction.\n
        Melakukan angsuran pembayaran pinjaman ke rekening bank.
        '''
        self.driver.get('http://localhost:8000/bank-transaction/incoming/create')

        self.driver.execute_script(f"document.getElementById('transactionDate').value='{date}'")

        self.driver.find_element(By.XPATH, '//*[@id="cashInForm"]/div[1]/div[3]/div/span/span[1]/span').click() # Mencari element clickable untuk membuka dropdown select2
        account_search_el = self.wait.until(
            EC.presence_of_element_located((By.CLASS_NAME, 'select2-search__field'))
        ) # mencari element untuk melakukan input pencarian
        account_search_el.send_keys(account) # malakukan input pencarian
        account_search_result_el = self.wait.until(
            EC.presence_of_element_located((By.XPATH, f"//ul[@id='select2-account-results']/li[contains(text(),'{account}')]"))
        ) # menunggu hasil pencarian element sampai ada tag li yang mengandung text dari akun
        account_search_result_el.click() # melakukan aksi klik pada element tersebut

        employee_select2_el = self.wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, '//*[@id="debtInstallmentCollapse"]/div[1]/div[1]/div/span/span[1]/span')
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
                    (By.XPATH, f'''//ul[@id='select2-debtInstallmentEmployee-results']/li[text()="{nama_anggota}"]''')
                )
            ) # menunggu sampai ada nama anggota yang mirip di dropdown hasil pencarian
        except:
            employee_search_result_el = self.wait.until(
                EC.presence_of_element_located(
                    (By.XPATH, f'''//ul[@id='select2-debtInstallmentEmployee-results']/li[contains(text(), "{nama_anggota}")]''')
                )
            ) # menunggu sampai ada nama anggota yang mirip di dropdown hasil pencarian

        employee_search_result_el.click() # dan kemudian mengkliknya

        self.wait.until(
            EC.text_to_be_present_in_element_value(
                (By.ID, 'debtInstallmentAmount'),
                '0'
            ) # mencari element jumlah
        )
        amount_el = self.driver.find_element(By.ID, 'debtInstallmentAmount') # menghapus dlu
        amount_el.clear()
        amount_el.send_keys(amount) # mengisi lagi
        self.driver.find_element(By.ID, 'debtInstallmentDesc').send_keys(keterangan) # mengisi keterangan
        
        self.driver.find_element(By.ID, 'save').click() # mengklik tombol save

        # Menunggu sweet alert muncul dan kemudian mengklik tombol ok
        try:
            self.wait.until(
                EC.presence_of_element_located(
                    (By.CLASS_NAME, 'swal-icon--success')
                )
            )
            self.driver.find_element(by=By.CLASS_NAME, value='swal-button--confirm').send_keys(Keys.ENTER)
            self.driver.get('http://localhost:8000/bank-transaction/incoming/create')
        except:
            self.wait.until(
                EC.presence_of_element_located(
                    (By.CLASS_NAME, 'swal-icon--error')
                )
            )
            print(nama_anggota)
            self.driver.find_element(by=By.CLASS_NAME, value='swal-button--confirm').send_keys(Keys.ENTER)
            self.driver.get('http://localhost:8000/bank-transaction/incoming/create')