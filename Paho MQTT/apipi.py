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



from pymongo import MongoClient

def conski_databussy():
                  linkDB = "mongodb://dbusr:dbusrpasswd@192.168.195.203:27017/backend?authSource=admin&w=1"
                  dbClient = MongoClient(linkDB)
                  return dbClient['piiclone']



from datetime import datetime
import time
import os

from apscheduler.schedulers.background import BackgroundScheduler

berhitung = 0

def tesInturnul() :
  import requests
  import json
  global berhitung

  url = "http://127.0.0.1:8000/trigger_selenium" #run hafifis.py

  dbname = conski_databussy()
  DBCollect = dbname['form_penilaian']
  cariBanyak = DBCollect.find({"status": "111-0"})
  taskMakinBanyak = []
  for printBanyak in cariBanyak:
      print("Current Task: ", printBanyak['pid'])
      taskMakinBanyak.append(printBanyak)
  print(datetime.now)

  if berhitung >= len(taskMakinBanyak):
    scheduler.remove_all_jobs(jobstore=None)
    return
  
  inputUlang = { #buat baca hasil search, bisa pilih attribute hasil search
    "process_id": taskMakinBanyak[berhitung]['pid'],
    "url": "http://updmember.pii.or.id/index.php",
    "status" : ['status']
  }
  
  payload = json.dumps(inputUlang)
  headers = {
    'Content-Type': 'application/json'
  }

  response = requests.request("POST", url, headers=headers, data=payload)
  DB2 = dbClient['akuCoba']
  DBWrite = dbname['temp_logigiging'] #tulis di DB logging
  catatanDB = {
      "pid" : inputUlang['process_id'],
      "Timestamp" : datetime.now(),
      "status" : "proses nomor urut "+ str(berhitung +1) + " diubah menjadi 112-1"}
  DBWrite.insert_one(catatanDB)

  DBCollect.update_one({'_id':taskMakinBanyak[berhitung]['_id']}, {"$set":{"status":"111-9" }}) 
  #replace di DB semula biar ngerjainnya ga loop

  berhitung = berhitung + 1

  return (inputUlang)


if __name__ == '__main__':
  scheduler = BackgroundScheduler()
  scheduler.add_job(tesInturnul, 'interval', seconds=15)
  scheduler.print_jobs()
  scheduler.start()
  joblis = scheduler.get_jobs()
  print('Press Ctrl+{0} to exit'.format('Break' if os.name == 'nt' else 'C'))
  
  try:
      # This is here to simulate application activity (which keeps the main thread alive).
    while True:
        time.sleep(10)
        if berhitung > len(joblis):
          break
  except (KeyboardInterrupt, SystemExit):
        # Not strictly necessary if daemonic mode is enabled but should be done if possible
    scheduler.shutdown()

# cari cara biar scheduler bisa standby dan kerjain task yg ditambahin belakangan
#coba cari logic garis besar cara biar si scheduler bisa di trigger sesuai keinginan dan sekalinya nge-trigger, ngelakuin semua task yg ada di database
