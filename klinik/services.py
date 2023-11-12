from firebase_config import pasien, rekap
import random
import string


def generate_unique_code():
        letters = string.ascii_uppercase  
        unique_code = ''.join(random.choice(letters) for _ in range(3))
        return unique_code

class FireServices:
    @staticmethod
    def add_pasien(name: str, index: int):
        unique_code = generate_unique_code()
        data = {
            'name': name,
            'id': unique_code,
            'index': index,
        }
        key = pasien.push().key
        pasien.child(key).set(data)
        key = rekap.push().key
        rekap.child(key).set(data)
        return unique_code

    def next_pasien():
        first_entry_pasien = pasien.order_by_key().limit_to_first(1).get()

        if first_entry_pasien:
            pasien_ref = pasien.child(list(first_entry_pasien.keys())[0])
            pasien_ref.delete()