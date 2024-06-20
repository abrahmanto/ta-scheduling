from selenium import webdriver
from fastapi import FastAPI,Request
from selenium.webdriver.common.by import By
from pydantic import BaseModel #class buat terima body JSON

# baca body JSON
class terimaJSON(BaseModel):
    process_id: str
    url: str

app = FastAPI()

@app.post("/trigger_selenium")
# async def trigger_selenium(request: Request, process_id: str, url: str):
async def trigger_selenium(req: terimaJSON):
    try:
        req_dict = req.model_dump()
        driver = webdriver.Chrome()
        driver.get(req.url)
        driver.maximize_window()
        driver.implicitly_wait(5)
        #input username
        driver.find_element(By.ID, "email").send_keys("yosua@live.undip.ac.id")
        driver.find_element(By.ID, "password").send_keys("insinyurj4y4")
        
        #masuk login
        driver.find_element(By.ID, "m_login_signin_submit").click()
        driver.implicitly_wait(5)

        driver.close()
        print("Success")
        return {"message": "Selenium process completed successfully for process ID: " + req.process_id}
    except Exception as e:
        error_message = str(e)
        print("Error:", error_message)
        return {"error": "Error occurred while running Selenium process for process ID: " + req.process_id}


# uvicorn NamaFile:app --reload
#nama file = testSele1.py
#/!\IMPORTANT NOTES RUN WITH= uvicorn testSele1:app --host 0.0.0.0 --port 8000 --reload
#Second Note => template manggil= uvicorn main:app <= [main] diganti nama file kode

# Assume the MQTT broker will make an HTTP POST request to /trigger_selenium with process_id and url parameters.