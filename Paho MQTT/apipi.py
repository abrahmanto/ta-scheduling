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

from datetime import datetime
import time
import os

from pymongo import MongoClient

def getDBClient():
                  linkDB = "mongodb://dbusr:dbusrpasswd@192.168.195.203:27017/backend?authSource=admin&w=1"
                  dbClient = MongoClient(linkDB)
                  return dbClient

from apscheduler.schedulers.background import BackgroundScheduler

batch = 0

def tesInturnul() :
  import requests
  import json
  global batch

  url = "http://127.0.0.1:8000/trigger_selenium" #run hafifis.py


  # variabel dbClient nyimpen client balikan dari getDBClient()
  dbClient = getDBClient()
  # variabel piiCloneDB nyimpen database piiclone. Jadi dari variabel client sebelumnya, diakses database piiclone pake cara dbClient["piiclone"]
  piiCloneDB = dbClient["piiclone"]
  # variabel akuCobaDB nyimpen database akuCoba.
  akuCobaDB = dbClient["akuCoba"]

  DBCollect = piiCloneDB['form_penilaian']
  DBWrite = akuCobaDB['LatiahDB']


  berhitung = 0

  # cariBanyak = DBCollect.find({"status": "111-0"}) #normal
  cariBanyak = DBCollect.find({"status": "999-9"}) #reset run


  for printBanyak in cariBanyak:
    print("Current Task: ", printBanyak['pid'])
    print("task start time :", datetime.now(), "\n")

    if len(printBanyak) >= berhitung: # soft stop kalo udah kelar semua kerjaan
      inputUlang = { #buat baca hasil search, bisa pilih attribute hasil search
        "process_id": printBanyak['pid'],
        "url": "http://updmember.pii.or.id/index.php",
        "status" : ['status']
      }
    
      payload = json.dumps(inputUlang)
      headers = {
        'Content-Type': 'application/json'
      }

      response = requests.request("POST", url, headers=headers, data=payload)
      catatanDB = {
          "pid" : inputUlang['process_id'],
          "Timestamp" : datetime.now(),
          "status" : "proses batch "+str(batch+1)+" nomor urut "+ str(berhitung +1) + " diubah menjadi 111-999"}
    
      DBWrite.insert_one(catatanDB)
      
      # DBCollect.update_one({'_id':printBanyak['_id']}, {"$set":{"status":"999-9" }}) #normal
      DBCollect.update_one({'_id':printBanyak['_id']}, {"$set":{"status":"111-0" }}) #reset run
      # replace di DB semula biar ngerjainnya ga loop
      
      print("TASK DONE", printBanyak['pid'])
      print("COMPLETION TIME:", time.ctime(), "\n")      
    else:
      scheduler.remove_all_jobs(jobstore=None) #terlalu bahaya
      print("ALL TASK DONE", "\n", time.ctime())
      return
    
    berhitung+=1

  batch += 1

    

if __name__ == '__main__':
  scheduler = BackgroundScheduler()
  scheduler.add_job(tesInturnul, 'interval', minutes=10)
  scheduler.print_jobs()
  scheduler.start()
  print('Press Ctrl+{0} to exit'.format('Break' if os.name == 'nt' else 'C'))
  try:
    while True:
        time.sleep(3600)          
  except (KeyboardInterrupt, SystemExit):
    scheduler.shutdown()
