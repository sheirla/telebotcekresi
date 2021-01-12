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
@bot.message_handler(commands=['tiktok')
def send_welcome(message):
	bot.reply_to(message, "Sedang dalam perbaikan")


bot.polling(none_stop=True)
