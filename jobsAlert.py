from JobScraper import JobScraper
from datetime import datetime, timedelta
import pyautogui
import os
import time

domains = [
    {
        "url": "https://www.infojobs.com.br/empregos.aspx?palabra=Desenvolvedor&sprd=50&splat=-23.4952413&splng=-46.6838736",
        "selectors": {
        "job": '[class*="js_rowCard"]',
        "title": '[class*="h3 font-weight-bold text-body mb-8"]',
        "date": '[class*="text-medium small"]',
        "link": '[class*="py-16 pl-24 pr-16 cursor-pointer js_vacancyLoad js_cardLink"]'
        }
    },
    {
        "url": "https://portal.gupy.io/job-search/term=desenvolvedor&state=S%C3%A3o%20Paulo&city[]=S%C3%A3o%20Paulo",
        "selectors": {
            "job": '[class*="kokxPe"]',
            "title": '[class*="dZRYPZ"]',
            "date": '[class*="iUzUdL"]',
            "link": '[class*="IKqnq"]'
        }
    }
]

def scraperJobsDict(dateRegulator, dateRegulatorType):
    all_jobs = {"title": [], "date": [], "link": []}
    for domain in domains:
        scraper = JobScraper(domain['url'], domain['selectors'], dateRegulator, dateRegulatorType)
        try:
            jobs_per_domain = scraper.scrape()
            all_jobs["title"].extend(jobs_per_domain["title"])
            all_jobs["date"].extend(jobs_per_domain["date"])
            all_jobs["link"].extend(jobs_per_domain["link"])
        finally:
            scraper.driver.quit()
    print("Varredura de dados concluída! ✅")
    return all_jobs

def createMessage(jobs):
    message = "NOVAS VAGAS:\n\n"
    if not jobs["title"]:
        message = "Nenhuma vaga encontrada nas últimas 24 horas."
    else:
        for i in range(len(jobs["title"])):
            message += f"{jobs['title'][i]} ({jobs['date'][i]})\n> {jobs['link'][i]}\n\n"
    return message

def loadWhatsApp():
    """ Wait for the full loading of WhatsApp by verifying an interface element. """
    while True:
        try:
            if pyautogui.locateOnScreen('campo_pesquisa.png', confidence=0.8):
                print("WhatsApp carregado!")
                break
        except:
            pass
        time.sleep(1)

# Must be logged in on WhatsApp Desktop
def findContact(recipient):
    try:
        # Abre o WhatsApp Desktop
        os.startfile("C:\\Users\\SeuUsuario\\AppData\\Local\\WhatsApp\\WhatsApp.exe")  # Ajuste o caminho conforme necessário
        loadWhatsApp()  # Aguarda até que o WhatsApp esteja totalmente carregado
    except Exception as e:
        print(f"Não foi possível abrir o app: {e}")

    pyautogui.hotkey('ctrl', 'f')
    time.sleep(1)
    pyautogui.write(recipient)
    time.sleep(6)
    pyautogui.press('tab')
    time.sleep(1)
    pyautogui.press('enter')
    time.sleep(1)
    
def sendMessage(message):
    jobsNum = 0
    for line in message.split("\n"):
        pyautogui.write(line)
        if "https://" in line:
            jobsNum += 1
            if jobsNum == 10: # para evitar exceder o limite de caracteres
                jobsNum = 0
                pyautogui.press('enter')
                continue
        time.sleep(1)
        pyautogui.hotkey('shift', 'enter') # pula uma linha
    pyautogui.press('enter')
    print("Mensagem enviada com sucesso! ✅")

yesterday = datetime.now().date() - timedelta(days=1)
# Constante
dateRegulatorType = 'alert'

jobs = scraperJobsDict(yesterday, dateRegulatorType)
message = createMessage(jobs)

recipient = "Vagas do Igor"  # * contato ou grupo para enviar as mensagens

findContact(recipient)
sendMessage(message)
