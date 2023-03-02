from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

from transaction.helper import find_barcode_by_item_name

class SellingTransaction:
    def __init__(self, driver, wait):
        '''driver: Driver chrome yang akan dijalankan
        wait: Object untuk explisit wait
        '''
        self.driver = driver
        self.wait = wait

    def selling_transaction(self, tanggal, invoice_number:str, pelanggan:str, purchased_items:list, prices:list, quantities:list, items:list):
        self.driver.get('http://localhost:8000/transaction/create')

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

        # INPUT DATA ANGGOTA (JIKA ADA)
        if pelanggan:
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
        
        # INPUT DATA BARANG
        for purchased_item, price, quantity in zip(purchased_items, prices, quantities):
            barcode = find_barcode_by_item_name(purchased_item, items)
            barcode_el = self.driver.find_element(By.ID, 'barcode') # mengambil element yang memiliki id 'barcode'
            barcode_el.send_keys(barcode) # mengetikan nama barang pada barcode_el
            barcode_el.send_keys(Keys.ENTER) # mengetikan tombol enter
            self.wait.until(
                EC.text_to_be_present_in_element_value(
                    (By.ID, 'code'),
                    ''
                )
            )

            price_el = self.driver.find_element(By.ID, 'price')
            self.driver.execute_script("arguments[0].removeAttribute('disabled')", price_el) # menghilangkan disable pada field tanggal
            self.wait.until(
                EC.text_to_be_present_in_element_value(
                    (By.ID, 'price'),
                    'Rp. '
                )
            )
            price_el.clear()
            price_el.send_keys(int(price))

            qty_el = self.driver.find_element(By.ID, 'qty')
            qty_el.send_keys(quantity) # mengetikan enter
            qty_el.send_keys(Keys.ENTER) # mengetikan enter

        # INPUT DATA BAYAR JIKA DIA TUNAI
        if pelanggan.__contains__('Tunai'):
            grand_total  = self.driver.find_element(By.ID, 'grandTotal').get_attribute('value')
            print(grand_total)
            cash_el = self.driver.find_element(By.ID, 'cash')
            cash_el.send_keys(grand_total)
            cash_el.send_keys(Keys.ENTER)
        
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
