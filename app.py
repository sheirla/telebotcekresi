import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import requests
from urllib.request import Request, urlopen
import urllib.parse as urlparse
from urllib.parse import parse_qs
from bs4 import BeautifulSoup

urlcekongkir = "https://pluginongkoskirim.com/cek-tarif-ongkir/front/resi-amp?__amp_source_origin=https%3A%2F%2Fpluginongkoskirim.com"
urlyoutube = "http://sosmeeed.herokuapp.com:80/api/youtube/video"
urltwitter = "http://sosmeeed.herokuapp.com:80/api/twitter/video"

bot = telebot.TeleBot("717811256:AAFpTRD8AZ90t6nqpayMvL5fpxG7ElFBf9c")


@bot.message_handler(commands=['start'])
def send_welcome(message):
	bot.reply_to(message, "Cari apa gan? /help untuk melihat list command")

@bot.message_handler(commands=[ 'help'])
def send_welcome(message):
	bot.reply_to(message, "List command bot: \n /cekresi - untuk cek resi \n /twitter - Twitter Video Downloader \n /tiktok - Download Video Tiktok Tanpa Watermark \n /youtube - Download Video Youtube \n /ytmp3 - Covert youtube ke mp3")


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
    response = requests.request("POST", urlcekongkir, data=payload)
    datakurir = response.json()
      
    try:
        resi_kurir = datakurir['data']['detail']['code']
        status_kurir = datakurir['data']['detail']['status']
        lokasi_terakhir = datakurir['data']['detail']['history'][0]['position']
        desc_terakhir = datakurir['data']['detail']['history'][0]['desc']
        waktu_terakhir = datakurir['data']['detail']['history'][0]['time']
        print('checking resi: '+resi_kurir)
        bot.reply_to(message, "RESI : " + resi_kurir + "\nSTATUS : " + status_kurir + "\n===========================" "\nLokasi : " + lokasi_terakhir + "\nDESC : " + desc_terakhir+ "\nWaktu : " + waktu_terakhir)
    except:
        check = datakurir['message']
        bot.reply_to(message, check)
""" ================================================================================================== """
@bot.message_handler(commands=['twitter'])
def starttwiter(message):
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
    print(vide_urlyt)
    req = Request(vide_urlyt, headers={'User-Agent': 'Mozilla/5.0'})
    bot.send_message(message.chat.id, 'Video sedang di upload kepada klean..')
    f = open('out.mp4','wb')
    f.write(urlopen(req).read())
    f.close()
    bot.send_chat_action(message.chat.id, 'upload_video')
    img = open('out.mp4', 'rb')
    bot.send_video(message.chat.id, img, reply_to_message_id=message.message_id)
    bot.send_message(message.chat.id, 'Video selesai terupload kepada klean..')
    img.close()
    responseyoutube.close() 
""" ================================================================================================== """
@bot.message_handler(commands=['ytmp3'])
def send_welcome(message):
	bot.reply_to(message, "Sedang dalam perbaikan")
 

""" ================================================================================================== """
@bot.message_handler(commands=['tiktok'])
# def send_welcome(message):
# 	bot.reply_to(message, "Sedang dalam perbaikan...")
def starttiktok(message):
    global tiktokurl
    sent3 = bot.send_message(message.chat.id, 'Input URL')
    bot.register_next_step_handler(sent3, tiktokstarted)

def tiktokstarted(message):
    tiktokurl = (message.text)
    url1 = "https://snaptik.app/check_token.php"
    headers = {
        'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.146 Safari/537.36',
        'origin':'https://snaptik.app',
        'referer':'https://snaptik.app/ID'
    }
    s = requests.Session()
    #s.get("https://snaptik.app/ID", headers=headers)
    response1 = s.post( url1, headers=headers)

    url = "https://snaptik.app/action_2021.php"
    payload={'url': tiktokurl}

    response = s.post(url, headers=headers, data=payload)
    datatiktok = response.text
    soup = BeautifulSoup(datatiktok, "html.parser")
    datavideomentah = soup.find("a",{"class":"abutton is-success is-fullwidth"})
    datavideojadi = datavideomentah['href']
    print(datavideojadi)
    req = Request(datavideojadi, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.146 Safari/537.36'})
    
    f = open('out.mp4','wb')
    f.write(urlopen(req).read())
    f.close()
    bot.send_chat_action(message.chat.id, 'upload_video')
    img = open('out.mp4', 'rb')
    bot.send_video(message.chat.id, img, reply_to_message_id=message.message_id)
    img.close()
    responsetiktok.close() 

bot.polling(none_stop=True)
