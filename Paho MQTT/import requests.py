import requests
import json

url = "http://192.168.195.241:8000/auth/register"

payload = json.dumps({
  "email": "Superindo@Superindo.com",
  "password": "AyamUtuh40k",
  "username": "Superindo",
  "nomerInduk": "202008",
  "posisiKuliah": "Mahasiswa",
  "nama": "Emados Shawarma",
  "angkatan": "2019",
  "gelar": "S.T.",
  "jenisKelamin": "Laki-Laki",
  "tempatLahir": "Wonogiri",
  "tanggalLahir": "30 Agustus 1999",
  "nomorIdentifikasi": "081312308788",
  "nomorPonsel": "621899468",
  "alamat": "Jl. Padang Panjang, Semarang",
  "Website": "",
  "Deskripsi": ""
})
headers = {
  'Content-Type': 'application/json'
}

response = requests.request("POST", url, headers=headers, data=payload)

print(response.text)
