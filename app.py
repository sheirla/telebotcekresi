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
def gen_markup_yt():
    markup = InlineKeyboardMarkup()
    markup.row_width = 2
    markup.add(InlineKeyboardButton("mp4", callback_data="cb_mp4"),
                               InlineKeyboardButton("mp3", callback_data="cb_mp3"))
    return markup

@bot.message_handler(commands=['youtube'])
def startyt(message):
    sent4 = bot.send_message(message.chat.id, 'Input URL')
    bot.register_next_step_handler(sent4, youtubestarted)

def youtubestarted(message):
    rr = message.text
    bot.send_message(message.chat.id, rr, reply_markup=gen_markup_yt())

@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):

    rrl = call.message.text
    url = "https://yt1s.com/api/ajaxSearch/index"
    url2 = "https://yt1s.com/api/ajaxConvert/convert"
    if call.data == "cb_mp4":
        payload1='q='+rrl+'&vt=home'
        headers2 = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'origin':'https://yt1s.com',
        'referer':'https://yt1s.com/',
        }
        sss = requests.Session()
        response2 = sss.post(url, headers=headers2, data=payload1)
        r2 = response2.json()
        vids = r2['links']['mp4']
        for value in vids:
            if vids[value]['q'] == "360p":
                dk = vids[value]['k']
                sk = vids[value]['size']
                qk = vids[value]['q']

        payload2='vid='+r2['vid']+'&k='+dk+''
        response = sss.post(url2, headers=headers2, data=payload2) 
        arr = response.json()
        dlink = arr['dlink']
        print(dlink)
        resultt = arr['title']+'\n'+qk+'\n'+sk+'\n'+arr['c_status']
        bot.send_message(call.message.chat.id, resultt) 
        
        req = Request(dlink, headers={'User-Agent': 'Mozilla/5.0'})
        bot.send_message(call.message.chat.id, 'Video sedang di Upload..')
        f = open('out.mp4','wb')
        f.write(urlopen(req).read())
        f.close()
        bot.send_chat_action(call.message.chat.id, 'upload_video')
        mp4 = open('out.mp4', 'rb')
        bot.send_video(call.message.chat.id, mp4, reply_to_message_id=call.message.message_id)
        bot.send_message(call.message.chat.id, 'Video Selsai di Upload..')
        mp4.close()
        sss.close()
# MP3
    if call.data == "cb_mp3":
        payloadmp31='q='+rrl+'&vt=home'
        headers2z = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'origin':'https://yt1s.com',
        'referer':'https://yt1s.com/',
        }
        sssmp3 = requests.Session()
        responsemp32 = sssmp3.post(url, headers=headers2z, data=payloadmp31)
        r2z = responsemp32.json()
        vidsz = r2z['links']['mp3']
        for valuez in vidsz:
                dkz = vidsz[valuez]['k']
                skz = vidsz[valuez]['size']
                qkz = vidsz[valuez]['q']


        payloadmp32='vid='+r2z['vid']+'&k='+dkz+''
        responsemp3 = sssmp3.post(url2, headers=headers2z, data=payloadmp32) 
        arr2 = responsemp3.json()
        dlinkmp3 = arr2['dlink']
        print(dlinkmp3)
        resulttmp3 = arr2['title']+'\n'+qkz+'\n'+skz+'\n'+arr2['c_status']
        bot.send_message(call.message.chat.id, resulttmp3) 
        
        reqz = Request(dlinkmp3, headers={'User-Agent': 'Mozilla/5.0'})
        bot.send_message(call.message.chat.id, 'Audio sedang di Upload kepada klean..')
        f = open('out.mp3','wb')
        f.write(urlopen(reqz).read())
        f.close()
        bot.send_chat_action(call.message.chat.id, 'upload_audio')
        mp3 = open('out.mp3', 'rb')
        bot.send_audio(call.message.chat.id, mp3, reply_to_message_id=call.message.message_id)
        bot.send_message(call.message.chat.id, 'Audio Selesai di Upload..')
        mp3.close()
        sssmp3.close() 

""" ================================================================================================== """
@bot.message_handler(commands=['ytmp3'])
def send_welcome(message):
	bot.reply_to(message, "Gunakan /youtube")
 

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
    s = requests.Session()
    headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.146 Safari/537.36',
    'origin':'https://ttdownloader.com',
    'referer':'https://ttdownloader.com/',
    }
    restik1 = s.get("https://ttdownloader.com/", headers=headers)
    datatiktok = restik1.text
    soup = BeautifulSoup(datatiktok, "html.parser")
    datatoken = soup.find("input",{"id":"token"})
    token = datatoken['value']
    # print(s.cookies.get_dict())
    payloadTiktok={'url':tiktokurl,'token':token}
    responsez = s.post("https://ttdownloader.com/download_ajax/", headers=headers, data=payloadTiktok)
    dataDownload = responsez.text
    soup = BeautifulSoup(dataDownload, "html.parser")
    datatoken2 = soup.find("a",{"class":"download-link"})
    datavideojadi = datatoken2['href']
    print(datavideojadi)
    req = Request(datavideojadi, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.146 Safari/537.36'})
    
    f = open('out.mp4','wb')
    f.write(urlopen(req).read())
    f.close()
    bot.send_chat_action(message.chat.id, 'upload_video')
    img = open('out.mp4', 'rb')
    bot.send_video(message.chat.id, img, reply_to_message_id=message.message_id)
    img.close()
    s.close() 

bot.polling(none_stop=True)
