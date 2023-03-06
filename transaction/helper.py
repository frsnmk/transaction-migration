from fuzzywuzzy import fuzz
from fuzzywuzzy import process

def most_similar_word(word:str, words:list, limit_score=70):
    '''word : Kata yang ingin dicari kemiripannya
    words : Kumpulan kata
    limit_score :  nilai termirip dari kata
    '''
    best_match_word, score = process.extractOne(word, words, scorer=fuzz.token_sort_ratio)
    if score >= limit_score:
        return best_match_word
    else:
        return None
    
def find_barcode_by_item_name(selected_item, items):
    # Inisialisasi nilai terbaik dan indeks terbaik
    best_match_ratio = 0
    best_match_index = -1

    # Loop melalui setiap item dalam daftar
    for i, item in enumerate(items):
        item_name = item['name']
        # Cari rasio kesamaan antara selected_item dan item saat ini
        match_ratio = fuzz.ratio(selected_item, item_name)
        # Perbarui nilai terbaik dan indeks terbaik jika cocok lebih baik
        if match_ratio > best_match_ratio:
            best_match_ratio = match_ratio
            best_match_index = i
            # Jika item cocok sempurna, hentikan loop dan kembalikan barocde
            if match_ratio == 100:
                return item['barcode']

    # Jika tidak ada yang cocok sempurna, kembalikan indeks terbaik atau -1 jika tidak ada yang cocok
    if best_match_ratio > 0:
        return items[best_match_index]['barcode']
    else:
        return -1

def nama_anggota(text):
    text = text.split('-')
    return text[1].strip()


def supplier_name_adjustment(supplier):
    if supplier == 'Yans Mart':
        return 'Yan Mart'
    elif supplier == 'BP.YAYAN':
        return 'Yan Mart'
    elif supplier == 'BP.YAYAN(klanting)':
        return 'Yan Mart'
    elif supplier == 'DAFMART':
        return 'Yan Mart'
    else:
        raise "Data tidak supplier tidak tersedia"