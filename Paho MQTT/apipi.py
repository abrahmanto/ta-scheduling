# isi endpoint
# isi import pahoSub dan pahoPub
# test API pake postman

# def tesParam():
  # import flask
  # import requests

  # url = "http://127.0.0.1:8000/trigger_selenium?process_id=Anto&url=http://updmember.pii.or.id/index.php"
  # # url = "http://192.168.195.129:8000/trigger_selenium?process_id=Anto&url=http://updmember.pii.or.id/index.php"
  # payload = ""
  # headers = {}

  # response = requests.request("POST", url, headers=headers, data=payload)

  # print(response.text)




# def tesInternal() :
#   import requests
#   import json

#   url = "http://127.0.0.1:8000/trigger_selenium"


#   objectTito = {
#     "process_id": "Tito Lihat Aku Menulis",
#     "url": "http://updmember.pii.or.id/index.php"
#   }
  
#   payload = json.dumps(objectTito)
#   headers = {
#     'Content-Type': 'application/json'
#   }

#   response = requests.request("POST", url, headers=headers, data=payload)
#   DBCollect = dbname['LatiahDB']
#   catatanDB = {
#       "ID" : objectTito['process_id'],
#       "Timestamp" : datetime.now(),
#       "Status" : "30 Maret"
#   }

#   DBCollect.insert_one(catatanDB)
#   print(response.text)

#   return(objectTito)


# def tesExternal(): 
  # import requests
  # import json

  # url = "http://192.168.195.83:8000/trigger_selenium"

  # payload = json.dumps({
  #   "process_id": "LogSudahKembali",
  #   "url": "http://localhost:3000/",
  #   "email": "eve.holt@regress.in",
  #   "password": "cityslicka"
  # })
  # headers = {
  #   'Content-Type': 'application/json'
  # }

  # response = requests.request("POST", url, headers=headers, data=payload)

  # print(response.text)


# pip install requests
# pip install APScheduler
# pip install pymongo
# pip install psutil

from datetime import datetime
import time
import os
import requests
import json
from pymongo import MongoClient
import psutil


def getDBClient():
                  linkDB = "mongodb://192.168.195.245:27017/"
                  # linkDB = "mongodb://192.168.195.83:27017/" #punya hafidz
                  # linkDB = "mongodb://192.168.195.241:27017/" #punya naufal

                  dbClient = MongoClient(linkDB)
                  return dbClient


from apscheduler.schedulers.background import BackgroundScheduler

batch = 0

def tesInturnul() :

  global batch

  # url = "http://127.0.0.1:8000/trigger_selenium" # uvicorn hafifis:app --reload
  url = "http://127.0.0.1:8000/trigger-selenium" # uvicorn hafizui:app --reload (lebih baru)
  # url = "http://192.168.195.83:8000/trigger-selenium" #external hafidz


  # status 2 jenis = perlu dikerjain dan sukses dikerjain

  # variabel dbClient nyimpen client balikan dari getDBClient()
  dbClient = getDBClient()
  # variabel piiCloneDB nyimpen database piiclone. Jadi dari variabel client sebelumnya, diakses database piiclone pake cara dbClient["piiclone"]
  piiCloneDB = dbClient["pii-reborn"]
  # variabel akuCobaDB nyimpen database akuCoba.
  # akuCobaDB = dbClient["pii-loggers"]

  DBCollect = piiCloneDB['form_penilaian']
  DBWrite = piiCloneDB['query_log']


  berhitung = 0

  cariBanyak = DBCollect.find({"status": "111-0"}) #normal 1 of 3
  AkuJumlahAwal = DBCollect.count_documents({"status": "111-0"}) #normal
  # cariBanyak = DBCollect.find({"status": "111-3"}) #reset run 1 of 3
  # AkuJumlahAwal = DBCollect.count_documents({"status": "111-3"}) #reset
  print("\njumlah dalam antrian saat ini: ",AkuJumlahAwal)


  tesCepewu = psutil.cpu_percent(interval=1)
  tesMemri = psutil.virtual_memory()
  print(f"sebelum mulai sele\nCPU Usage: {tesCepewu}%")
  print(f"Memory Usage: {tesMemri.percent}% \n")


  if cariBanyak >= 10: #starting condtition
    for printBanyak in cariBanyak:
      
      AkuJumlahBerjalan = DBCollect.count_documents({"status": "111-0"}) #normal 2 of 3
      DBCollect.update_one({'_id':printBanyak['_id']}, {"$set":{"status":"IN PROG 111-0" }}) #normal
      # AkuJumlahBerjalan = DBCollect.count_documents({"status": "111-3"}) #reset run 2 of 3
      # DBCollect.update_one({'_id':printBanyak['_id']}, {"$set":{"status":"IN PROG 111-3" }}) #reset

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

      DBWrite.insert_one(catatanDB)
      
      DBCollect.update_one({'_id':printBanyak['_id']}, {"$set":{"status":"111-3" }}) #normal 3 of 3
      # DBCollect.update_one({'_id':printBanyak['_id']}, {"$set":{"status":"111-0" }}) #reset run 3 of 3
      # replace di DB semula biar ngerjainnya ga loop
      
      print("TASK DONE", printBanyak['pid'])
      print("COMPLETION TIME:", time.ctime())

      berhitung+=1

      if berhitung >= 15: #stopping condition
        print("15 antrian pertama selesai") 
        batch += 1
        return
    

  else:
    print("\nbatch diatas standar, menunggu jadwal berikutnya\n", time.ctime())
    # scheduler.remove_all_jobs(jobstore=None) #terlalu bahaya
    scheduler.print_jobs()
    return
    



    

if __name__ == '__main__':
  scheduler = BackgroundScheduler()
  scheduler.add_job(tesInturnul, 'interval', seconds=20)
  scheduler.print_jobs()
  scheduler.start()
  print('Press Ctrl+{0} to exit'.format('Break' if os.name == 'nt' else 'C'))
  try:
    while True:
      tesCepewu = psutil.cpu_percent(interval=15)
      tesMemri = psutil.virtual_memory()
      print(f"\nCPU Usage: {tesCepewu}%")
      print(f"Memory Usage: {tesMemri.percent}% \n")
      time.sleep(45)          
  except (KeyboardInterrupt, SystemExit):
    scheduler.shutdown()




