import os
import pandas as pd

from dotenv import load_dotenv
from datasource.selling import Selling

load_dotenv()

path = os.getenv('LAPORAN_KEUANGAN_PATH')

selling = Selling(path).data_penjualan()