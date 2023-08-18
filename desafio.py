import pandas as pd
import requests,openai, json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import WebDriverException
import time
#consumo da API SDW2023
sdw2023_api_url = 'https://sdw-2023-prd.up.railway.app'

df = pd.read_csv('SDW2023.csv')
user_ids = df['UserID'].tolist()
print(user_ids)

def get_user(id):
  response = requests.get(f'{sdw2023_api_url}/users/{id}')
  return response.json() if response.status_code == 200 else None

users = [user for id in user_ids if (user := get_user(id)) is not None]
print(json.dumps(users, indent=2))



#mensagem gerada com chat gpt
openai.api_key = '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'

def generate_ai_news(user):
  completion = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[
      {
          "role": "system",
          "content": "Você é um especialista em markting bancário."
      },
      {
          "role": "user",
          "content": f"Crie uma mensagem para {user['name']} sobre a importância dos investimentos (máximo de 100 caracteres)"
      }
    ]
  )
  return completion.choices[0].message.content.strip('\"')

def generate_ai_email_title(user):
  completion = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[
      {
          "role": "system",
          "content": "Você é um especialista em markting bancário."
      },
      {
          "role": "user",
          'content': f'Crie um título chamativo para um email sobre investimentos',
      }
    ]
  )
  return completion.choices[0].message.content.strip('\"')


  
#bot que envia emails com as mensagens personalizadas


navegador = webdriver.Chrome()
navegador.get("https://login.live.com/")
wait = WebDriverWait(navegador, 200)


def entrar_no_email():
    #preenchimento do email
    campo_email = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="i0116"]')))
    campo_email.send_keys('email')
    botão1 = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="idSIButton9"]')))
    botão1.click()
    #senha
    campo_senha = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="i0118"]')))
    campo_senha.send_keys('senha/password')
    time.sleep(1)
    botao2 = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="idSIButton9"]')))
    botao2.click()
    #não manter conectado
    botao3 = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="idBtn_Back"]')))
    botao3.click()
    #entrar no outlook
    botao_outlook = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="main-content-landing-react"]/div[2]/div/div[1]/div/div[1]/div/div/div/div[2]/a[2]/span')))
    botao_outlook.click()


def preencher_email(destinatario, sobre, mensagem):
    #entrar no email
    criar_email = wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="id__139"]')))
    criar_email.click()  
    #preencher o email de destino
    campo_destinatario = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="docking_InitVisiblePart_0"]/div/div[3]/div[1]/div/div[3]/div/div/div[1]')))
    campo_destinatario.send_keys(destinatario)
    #Título do email----
    campo_sobre = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="TextField249"]')))
    campo_sobre.send_keys(sobre)
    #Mensagem-----------------
    campo_mensagem = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="editorParent_1"]/div')))
    campo_mensagem.send_keys(mensagem)
    #enviar ------------------
    enviar_email = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="docking_InitVisiblePart_0"]/div/div[2]/div[1]/div/span/button[1]/span/i')))
    enviar_email.click()
for user in users:
  news = generate_ai_news(user)
  print(news)
  user['news'].append({
      "icon": "https://digitalinnovationone.github.io/santander-dev-week-2023-api/icons/credit.svg",
      "description": news
  })

for user in users:  
    entrar_no_email()
    preencher_email(destinatario=user['email'], sobre=generate_ai_email_title(user), mensagem=generate_ai_news(user))