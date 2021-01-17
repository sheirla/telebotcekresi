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
    response = requests.request("POST", urlcekongkir, data=payload)
    datakurir = response.json()
      
    try:
        resi_kurir = datakurir['data']['detail']['code']
        status_kurir = datakurir['data']['detail']['status']
        lokasi_terakhir = datakurir['data']['detail']['history'][0]['position']
        desc_terakhir = datakurir['data']['detail']['history'][0]['desc']
        waktu_terakhir = datakurir['data']['detail']['history'][0]['time']
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
def startyoutubemp3(message):
    global youtubemp3url
    sent4 = bot.send_message(message.chat.id, 'Input URL')
    bot.register_next_step_handler(sent4, youtubemp3started)

def youtubemp3started(message):
    youtubemp3url = (message.text)
    
    parsed = urlparse.urlparse(youtubemp3url)
    checkurl = parse_qs(parsed.query).get('v')
    if checkurl is None:
        x = parsed.path
        ytquery = x.replace("/", "")
    else:
        ytquery = parse_qs(parsed.query).get('v')[0]
    
    print(ytquery)
    ytmp3url = "https://api.youtube-mp3.org.in/@audio/"+ytquery+"/?title="+ytquery
    headersytmp3 = {
    'Content-Type': 'application/json'
    }
    responseyoutubemp3 = requests.request("GET", ytmp3url, headers=headersytmp3)
    print(responseyoutubemp3)
    datayoutubemp3 = responseyoutubemp3.json()
      
    vide_urlytmp3 = datayoutubemp3['url']
    bot.send_message(message.chat.id, 'Klik Download untuk mengunduh Manual', reply_to_message_id=message.message_id,  reply_markup=InlineKeyboardMarkup([
        [InlineKeyboardButton(text='Download mp3', url=''+vide_urlytmp3)],
    ]))

    req = Request(vide_urlytmp3, headers={'User-Agent': 'Mozilla/5.0'})
    bot.send_message(message.chat.id, 'Audio sedang di upload kepada klean..')
    f = open('out.mp3','wb')
    f.write(urlopen(req).read())
    f.close()
    bot.send_chat_action(message.chat.id, 'upload_audio')
    mp3 = open('out.mp3', 'rb')
    bot.send_audio(message.chat.id, mp3, reply_to_message_id=message.message_id)
    bot.send_message(message.chat.id, 'Audio selesai terupload kepada klean..')
    mp3.close()
    responseyoutubemp3.close() 
 

""" ================================================================================================== """
@bot.message_handler(commands=['tiktok'])
def starttiktok(message):
    global tiktokurl
    sent3 = bot.send_message(message.chat.id, 'Input URL')
    bot.register_next_step_handler(sent3, tiktokstarted)

def tiktokstarted(message):
    tiktokurl = (message.text)
    urltiktok = "https://snaptik.app/action.php"
    urltiktok2 = "https://snaptik.app/check_token.php"
    payloadtiktok='url='+tiktokurl
    headerstiktok = {
     'Content-Type': 'application/x-www-form-urlencoded'
    }

    s = requests.Session()
    s.post(urltiktok2)
    responsetiktok = s.post(urltiktok, headers=headerstiktok, data=payloadtiktok)

    datatiktok = responsetiktok.text
      
    soup = BeautifulSoup(datatiktok, "html.parser")
    datavideomentah = soup.find("a",{"class":"abutton is-success is-fullwidth"})
    datavideojadi = datavideomentah['href']
    print(datavideojadi)
    req = Request(datavideojadi, headers={'User-Agent': 'Mozilla/5.0'})
    
    f = open('out.mp4','wb')
    f.write(urlopen(req).read())
    f.close()
    bot.send_chat_action(message.chat.id, 'upload_video')
    img = open('out.mp4', 'rb')
    bot.send_video(message.chat.id, img, reply_to_message_id=message.message_id)
    img.close()
    responsetiktok.close() 

bot.polling(none_stop=True)
