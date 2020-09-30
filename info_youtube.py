from __future__ import unicode_literals
from youtube_dl import YoutubeDL
import json
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import pandas as pd


options = Options()
options.headless = True
chromedriver_path = r"C:\Users\lmgb8\Desktop\chromedriver"
driver = webdriver.Chrome(chromedriver_path, options=options)
channel = ['https://www.youtube.com/c/M%C3%A9tododeEstudo/videos', ]
filenames = []

for i in channel:
    print(f'acessando canal {i}')
    driver.get(i)

    # Get scroll height
    last_height = driver.execute_script("return document.documentElement.scrollHeight")
    SCROLL_PAUSE_TIME = 3
    # abriu tudo
    while True:
        # Scroll down to bottom
        print('fazendo scroll')
        driver.execute_script("window.scrollTo(0, document.documentElement.scrollHeight);")

        # Wait to load page
        time.sleep(SCROLL_PAUSE_TIME)

        # Calculate new scroll height and compare with last scroll height
        new_height = driver.execute_script("return document.documentElement.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

    print('gerando links')
    links = driver.find_elements_by_id("video-title")
    print('gerando links_list')
    links_list = [i.get_attribute('href') for i in links]
    print(f'total de videos: {len(links_list)}')
    print('incluindo na lista de arquivos chamada filenames')
    filename = i.split('/')[-2] + '.txt'
    filenames.append(filename)
    with open(filename, 'w') as f:
        print(f'escrevendo links em {filename}')
        for i in links_list:
            f.write(i + '\n')
print('fechando webdriver')
driver.close()

print('término de busca urls em canais')

print('início download arquivos de informação')

ydl_opts = {}
for file in filenames:
    dirname = file.split('.')[-2]
    if not os.path.isdir(dirname):
        os.mkdir(dirname)
    with open(file, 'r') as f:
        urls = f.read().splitlines()
        with YoutubeDL(ydl_opts) as ydl:
            for i in urls:
                dicio = ydl.extract_info(i, download=False)
                with open(f'./{dirname}/' + i.split('=')[-1] + '.json', 'w') as file:
                    file.write(json.dumps(dicio))


# def create_df(file):
#     with open(file, 'r') as f:
#         data = [json.loads(lines) for lines in f]
#     return pd.DataFrame(data)

os.chdir('./metododeestudo')
files = [os.path.join(os.getcwd(), i) for i in os.listdir()]
df_all = pd.DataFrame()
lista = []
for filename in files:
    try:
        with open(f'{filename}', 'r') as f:
            data = [json.loads(i) for i in f]
        df = pd.DataFrame(data)
        filtered = df[
            ['uploader', 'upload_date', 'title', 'tags', 'description', 'duration', 'webpage_url', 'view_count', 'average_rating',
             'thumbnail', 'width', 'height']]
        filtered['upload_date'] = pd.to_datetime(filtered['upload_date'], )
        lista.append(filtered)
    except Exception as e:
        print(f'nao foi possivel carregar {filename}: {e}')

print('concatenando tabelas...')
df = pd.concat(lista)
print('exportando')
df.to_excel('teste.xlsx')

