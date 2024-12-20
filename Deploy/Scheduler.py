from datetime import datetime
import time
import os
import requests
import json
from pymongo import MongoClient
import psutil


def getDBClient():
                  linkDB = "mongodb://localhost:27017"
                  dbClient = MongoClient(linkDB)
                  return dbClient


from apscheduler.schedulers.background import BackgroundScheduler

batch = 0

def tesInturnul() :

  global batch

  url = "http://127.0.0.1:8000/trigger-selenium" # uvicorn hafizui:app --reload (nama link baru)


  # variabel dbClient nyimpen client balikan dari getDBClient()
  dbClient = getDBClient()

  # variabel piiCloneDB nyimpen database piiclone. Jadi dari variabel client sebelumnya, diakses database piiclone pake cara dbClient["piiclone"]
  piiCloneDB = dbClient["piiclone"] #deployable
  DBWrite = piiCloneDB['log_result'] #deployable
  DBCollect = piiCloneDB['form_penilaian']

  # status formulir
  # 111-3 gagal 
  # 111-4 otw kerjain
  # 111-5 kelar kerjain berhasil

  berhitung = 0
  normalisasi = DBCollect.count_documents({"status": "111-2"})
  print("\nForm Nyangkut: ",normalisasi)
  DBCollect.update_many({"status": "111-4"}, {"$set":{"status":"111-3" }}) #normalisasi form nyangkut
  DBCollect.update_many({"status": "IN PROG 111-3"}, {"$set":{"status":"111-3" }})
  

  cariBanyak = DBCollect.find({"status": "111-3"})
  AkuJumlahAwal = DBCollect.count_documents({"status": "111-3"})
  print("\nJumlah dalam antrian saat ini: ",AkuJumlahAwal)


  tesCepewu = psutil.cpu_percent(interval=1)
  tesMemri = psutil.virtual_memory()
  print(f"\nkondisi awal batch "+str(batch+1)+ f"\nCPU Usage: {tesCepewu}%")
  print(f"Memory Usage: {tesMemri.percent}% \n")


  if AkuJumlahAwal >= 1: #starting condtition
    for printBanyak in cariBanyak:
      AkuJumlahBerjalan = DBCollect.count_documents({"status": "111-3"})
      DBCollect.update_one({'_id':printBanyak['_id']}, {"$set":{"status":"IN PROG 111-3" }})




      print("\njumlah dalam antrian saat ini: ",AkuJumlahBerjalan)
      print("Current Task: ", printBanyak['pid'])
      print("task start time :", datetime.now(), "\n")
      inputUlang = { #buat baca hasil search, bisa pilih attribute hasil search, PAYLOAD kirim ke selenium
        "process_id": printBanyak['pid'],
        "url": "http://updmember.pii.or.id/index.php",
        "status" : ['status'],
        "student_id":printBanyak['student_id']
      }
    
      payload = json.dumps(inputUlang)
      headers = {
        'Content-Type': 'application/json'
      }
      
      response = requests.request("POST", url, headers=headers, data=payload)
      printjeson = response.json()
      print("\n",printjeson) #dapet abc
      print(response, "\n") #dapet 200/500
      status_code = response.status_code
      print("Response Code:", status_code)  
      catatanDB = { #simpan di collection logging
          "pid" : inputUlang['process_id'],
          "Timestamp" : datetime.now(),
          "status" : "proses batch "+str(batch+1)+" nomor urut "+ str(berhitung +1),
          "deskripsi" : printjeson,
          "keterangan" : status_code}

      DBWrite.insert_one(catatanDB) # attempt update nov 28
      if catatanDB['keterangan'] == 200 : # update status db berdasarkan hasil selenium
        DBCollect.update_one({'_id':printBanyak['_id']}, {"$set":{"status":"111-5" }})
        print("SCHEDULING DONE", printBanyak['pid'])
      else:
         DBCollect.update_one({'_id':printBanyak['_id']}, {"$set":{"status":"111-4" }})
         print("SCHEDULING FAILED", printBanyak['pid'])

      
      print("COMPLETION TIME:", time.ctime())

      berhitung+=1

      if berhitung >= 14: #stopping condition
        print("14 antrian pertama selesai") 
        batch += 1
        return
      
      elif AkuJumlahBerjalan <= 1:
        print("Antrian kosong")
        return
    

  else:
    print("\nAntrian kosong, menunggu jadwal berikutnya\n", time.ctime())
    scheduler.print_jobs()
    return
    



    

if __name__ == '__main__':
  scheduler = BackgroundScheduler()
  scheduler.add_job(tesInturnul, 'interval', seconds=30)
  scheduler.print_jobs()
  scheduler.start()
  print('Press Ctrl+{0} to exit'.format('Break' if os.name == 'nt' else 'C'))
  try:
    while True:
      tesCepewu = psutil.cpu_percent(interval=15)
      tesMemri = psutil.virtual_memory()
      print(f"\nCPU Usage: {tesCepewu}%")
      print(f"Memory Usage: {tesMemri.percent}%")
      print("Util timestamp", time.ctime(), "\n")
      time.sleep(15)          
  except (KeyboardInterrupt, SystemExit):
    scheduler.shutdown()
