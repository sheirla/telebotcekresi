import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import requests
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup

urlcekongkir = "https://pluginongkoskirim.com/cek-tarif-ongkir/front/resi-amp?__amp_source_origin=https%3A%2F%2Fpluginongkoskirim.com"
urlyoutube = "http://sosmeeed.herokuapp.com:80/api/youtube/video"
urltwitter = "http://sosmeeed.herokuapp.com:80/api/twitter/video"
urltiktok = "https://snaptik.app/action.php"

bot = telebot.TeleBot("717811256:AAFpTRD8AZ90t6nqpayMvL5fpxG7ElFBf9c")
tb = telebot.TeleBot("717811256:AAFpTRD8AZ90t6nqpayMvL5fpxG7ElFBf9c")


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
	bot.reply_to(message, "Golek opo Su?")


""" ================================================================================================== """
@bot.message_handler(commands=['cekresi'])
def start(message):
    keyboard = telebot.types.ReplyKeyboardMarkup(True)
    keyboard.row('jnt', 'jne')
    sent = bot.send_message(message.chat.id, 'Pilih Kurir', reply_markup=keyboard)
    bot.register_next_step_handler(sent, resi)

def resi(message):
    global kurir
    kurir = (message.text)
    sent2 = bot.send_message(message.chat.id, 'Input Resi')
    bot.register_next_step_handler(sent2, botstarted)

def botstarted(message):
    resi = (message.text)
    
    payload={'kurir': kurir,'resi': resi}
    files=[]
    response = requests.request("POST", urlcekongkir, data=payload, files=files)
    datakurir = response.json()
      
    resi_kurir = datakurir['data']['detail']['code']
    status_kurir = datakurir['data']['detail']['status']
    lokasi_terakhir = datakurir['data']['detail']['history'][0]['position']
    desc_terakhir = datakurir['data']['detail']['history'][0]['desc']
    
    bot.reply_to(message, "RESI : " + resi_kurir + "\nSTATUS : " + status_kurir + "\n===========================" "\nLokasi : " + lokasi_terakhir + "\nDESC : " + desc_terakhir)
""" ================================================================================================== """
@bot.message_handler(commands=['twitter'])
def starttwiter(message):
    global tiktokurl
    sent3 = bot.send_message(message.chat.id, 'Input URL')
    bot.register_next_step_handler(sent3, twitterstarted)

def twitterstarted(message):
    twitterurl = (message.text)
    
    payloadtwitter='url='+twitterurl
    headerstwitter = {
    'Content-Type': 'application/x-www-form-urlencoded'
    }
    responsetwitter = requests.request("POST", urltwitter, headers=headerstwitter, data=payloadtwitter)

    datatwitter = responsetwitter.json()
    
    checkdata = datatwitter['success']
    if checkdata == True:
        vide_urltwt = datatwitter['data']['data'][0]['link']
        bot.send_video(message.chat.id,vide_urltwt)
    else:
        bot.send_message(message.chat.id, 'URL yg anda masukan salah / tidak valid')
        

""" ================================================================================================== """
@bot.message_handler(commands=['youtube'])
def startyoutube(message):
    global youtubeurl
    sent4 = bot.send_message(message.chat.id, 'Input URL')
    bot.register_next_step_handler(sent4, youtubestarted)

def youtubestarted(message):
    youtubeurl = (message.text)
    
    payloadyoutube='url='+youtubeurl
    headersyt = {
    'Content-Type': 'application/x-www-form-urlencoded'
    }
    responseyoutube = requests.request("POST", urlyoutube, headers=headersyt, data=payloadyoutube)

    datayoutube = responseyoutube.json()
      
    vide_urlyt = datayoutube['data'][0]['video']['url']
    req = Request(vide_urlyt, headers={'User-Agent': 'Mozilla/5.0'})
    f = open('out.mp4','wb')
    f.write(urlopen(req).read())
    f.close()
    bot.send_chat_action(message.chat.id, 'upload_video')
    img = open('out.mp4', 'rb')
    bot.send_video(message.chat.id, img, reply_to_message_id=message.message_id)
    img.close()

""" ================================================================================================== """
@bot.message_handler(commands=['tiktok'])
def starttiktok(message):
    global tiktokurl
    sent3 = bot.send_message(message.chat.id, 'Input URL')
    bot.register_next_step_handler(sent3, tiktokstarted)

def tiktokstarted(message):
    tiktokurl = (message.text)
    
    payloadtiktok='url='+tiktokurl+'&token=2fd0de11cb3f0cf7d507ee33869e70709a3fd428744d8b5730d003776db98ebf'
    headerstiktok = {
    'cookie': '__cfduid=d33d3b6499977fe797170dbc8ec5309431610126208; __cflb=0H28vNadMLAyXKUf1Fe7hcf2dQRRDpKqwQZqnTjqcom; __gads=ID=4e6278d305e8c0b2-22ed10d597c5005b:T=1610126209:RT=1610126209:S=ALNI_MbX5ZJ6GMrDdCIE9LCgkcWSMSO6Bg; current_language=ID; PHPSESSID=vo1km7l3o55ira5ko14d21b3io; _gid=GA1.2.172905107.1610434680; __atssc=google%3B2; _gat=1; _gat_gtag_UA_162798444_8=1; _ga_2KT415JS53=GS1.1.1610434679.2.1.1610435206.60; _ga=GA1.1.188138072.1610126209; __atuvc=1%7C1%2C2%7C2; __atuvs=5ffd48781d044837001; __cflb=025XBJYGdEpTJNVqnGV9cshdcjdDhTekAYgBF19Urk735WnTwHVtXSsdFVkTJdpdqdXcKXD1tyUhr98KZBW4xT; current_language=ID',
    'Content-Type': 'application/x-www-form-urlencoded'
    }
    responsetiktok = requests.request("POST", urltiktok, headers=headerstiktok, data=payloadtiktok)

    datatiktok = responsetiktok.text
      
    soup = BeautifulSoup(datatiktok, "html.parser")
    datavideomentah = soup.find("a",{"class":"abutton is-success is-fullwidth"})
    datavideojadi = datavideomentah['href']
    print(datavideomentah)
    req = Request(datavideomentah, headers={'User-Agent': 'Mozilla/5.0'})
    
    f = open('out.mp4','wb')
    f.write(urlopen(req).read())
    f.close()
    bot.send_chat_action(message.chat.id, 'upload_video')
    img = open('out.mp4', 'rb')
    bot.send_video(message.chat.id, img, reply_to_message_id=message.message_id)
    img.close()


bot.polling(none_stop=True)
