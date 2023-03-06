from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import pandas as pd

from transaction.helper import find_barcode_by_item_name

class PurchaseTransaction:
    def __init__(self, driver, wait):
        '''driver: Driver chrome yang akan dijalankan
        wait: Object untuk explisit wait
        '''
        self.driver = driver
        self.wait = wait

    def purchase_transaction(self, supplier, tanggal, materials, prices, quantities, items):
        self.driver.get('http://localhost:8000/purchase/create')

        # CHOOSE SUPPLIER
        self.driver.find_element(By.XPATH, '//*[@id="app"]/div/div[3]/section/div[2]/div/div[2]/div[2]/div/div[1]/div/span/span[1]/span').click() # Mencari element clickable dari form group select2
        suplier_select2_el = self.wait.until(
            EC.presence_of_element_located(
                (By.CLASS_NAME, 'select2-search__field')
            )
        )

        suplier_select2_el.send_keys(supplier)
        self.wait.until(
            EC.presence_of_element_located(
                (By.XPATH, f'''//ul[@id="select2-supplier-results"]/li[contains(text(), '{supplier}')]''')
            )
        ).click()
        self.driver.find_element(By.ID, 'date').send_keys(tanggal) # mengisi field tanggal
        for material, price, quantity in zip(materials, prices, quantities):
            barcode = find_barcode_by_item_name(material, items)
            barcode_el = self.driver.find_element(By.ID, 'barcode')
            barcode_el.send_keys(barcode)
            barcode_el.send_keys(Keys.ENTER)

            price_el = self.driver.find_element(By.ID, 'item-price')
            self.wait.until(
                EC.text_to_be_present_in_element_value(
                    (By.ID, 'item-price'),
                    'Rp. '
                )
            )
            price_el.clear()
            price_el.send_keys(int(price))

            quantity_el = self.driver.find_element(By.ID, 'item-qty')
            quantity_el.send_keys(int(quantity))
            quantity_el.send_keys(Keys.ENTER)
        
        self.driver.find_element(By.ID, 'submit_purchase').click()

        self.wait.until(
            EC.text_to_be_present_in_element(
                (By.ID,"swal2-title"),
                "Konfirmasi Pembelian"
            )
        )
        self.driver.find_element(By.CLASS_NAME, 'swal2-confirm').click()

        self.wait.until(
            EC.text_to_be_present_in_element(
                (By.ID,"swal2-title"),
                "Berhasil"
            )
        )
        self.driver.find_element(By.CLASS_NAME, 'swal2-confirm').click()



