from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

import pandas as pd

class PPOBTransaction:
    def __init__(self, driver, wait):
        '''driver: Driver chrome yang akan dijalankan
        wait: Object untuk explisit wait
        '''
        self.driver = driver
        self.wait = wait

    def ppob_transaction(self, tanggal, invoice_number:str, pelanggan:str, jenis_transaksi:str, price:int, admin_fee:int, total_payment:str):
        self.driver.get('http://localhost:8000/transaction/create')

        # TOGGLE PPOB
        self.driver.find_element(By.XPATH, '//*[@id="app"]/div/div[3]/section/div[2]/div/div[1]/div/div[2]/div[1]/div[1]/div/label/span[1]').click()

        # INPUT DATA TANGGAL
        transaction_date_el = self.driver.find_element(By.ID, 'transaction_date') # mendapatkan element tanggal
        self.driver.execute_script("arguments[0].removeAttribute('disabled')", transaction_date_el) # menghilangkan disable pada field tanggal
        self.driver.execute_script(f"document.getElementById('transaction_date').value='{tanggal}'") # mengisi field tanggal

        # INPUT DATA NOTA
        self.wait.until(
            EC.text_to_be_present_in_element_value(
                (By.ID, 'invoice_number'),
                "PJ"
            )
        ) # menunggu sampai element yang memiliki id 'invoice_number' mengandung nilai 'PJ'
        invoice_number_el = self.driver.find_element(By.ID, 'invoice_number') # mengambil element yang memiliki id 'invoice_number' meng
        self.driver.execute_script("arguments[0].removeAttribute('disabled')", invoice_number_el) # menghilangkan attribute disabled
        invoice_number_el.clear() # menghapus nilai ada (yang digenerate otomatis oleh sistem)
        self.driver.execute_script(f"document.getElementById('invoice_number').value='{invoice_number}'") # mengisinya dengan nilai yang kita inginkan

        # Pilih pelanggan
        if pelanggan and pelanggan!= 'tunai':
            self.driver.find_element(By.XPATH, '//*[@id="app"]/div/div[3]/section/div[2]/div/div[1]/div/div[2]/div[3]/span/span[1]/span').click() # click element yang akan mentrigger text input muncul
            search_input_el = self.wait.until(
                EC.presence_of_element_located(
                    (By.CLASS_NAME, 'select2-search__field')
                )
            ) # menunggu element seaerch input muncul dan mendapatkan elementnya (dengan mengasign dia didalam variable)
            search_input_el.send_keys(pelanggan) # mengisi element text input dengan nama pelanggan
            self.wait.until(
                EC.presence_of_element_located(
                    (By.XPATH, f'''//ul[@id='select2-employee-results']/li[contains(text(), '{pelanggan}')]''')
                )
            ).click() # menunggu element menampilkan nama yang sesuai dengan nama pelanggan di dropdown dan kemudian mengkliknya
        
        self.driver.find_element(By.ID, 'name').send_keys(jenis_transaksi) # memasukan nama pembalian yang dilakukan
        
        self.driver.find_element(By.ID, 'price').send_keys(int(price))

        quantities_el = self.driver.find_element(By.ID, 'qty')
        quantities_el.send_keys(1)
        quantities_el.send_keys(Keys.ENTER)
        admin_fee = 0 if pd.isna(admin_fee) else admin_fee
        self.driver.find_element(By.ID, 'adminFee').send_keys(int(admin_fee))

        if pelanggan == 'tunai':
            cash_el = self.driver.find_element(By.ID, 'cash')
            cash_el.send_keys(int(total_payment))
        
        self.driver.find_element(By.ID, 'save').click()

        self.wait.until(
            EC.text_to_be_present_in_element(
                (By.CLASS_NAME, 'swal-title'),
                'Konfirmasi Transaksi'
            )
        )
        self.driver.find_element(By.CLASS_NAME, 'swal-button--confirm').click()

        self.wait.until(
            EC.text_to_be_present_in_element(
                (By.CLASS_NAME, 'swal-title'),
                'Berhasil'
            )
        )
        self.driver.find_element(By.CLASS_NAME, 'swal-button--confirm').click()

        self.wait.until(
            EC.text_to_be_present_in_element(
                (By.CLASS_NAME, 'swal-title'),
                'Peringatan'
            )
        )
        self.driver.find_element(By.CLASS_NAME, 'swal-button--cancel').click()