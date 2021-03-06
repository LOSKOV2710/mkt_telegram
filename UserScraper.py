print ("Bot https://t.me/nabievuz tomonidan yozildi")
print ("")

from telethon.sync import TelegramClient
from telethon.tl.functions.messages import GetDialogsRequest
from telethon.tl.types import InputPeerEmpty
import csv

api_id = 0000000   #7 raqamdan iborat bo'lgan Telegram API ID ni kiriting.
api_hash = '98c2e9dbec19ebb226c588c0c1afe2vr'   #32 ta raqam va harflardan iborat API Hash ni kiriting.
phone = '+998910001122'   #Telegramga biriktirilgan telefon raqamini kiriting.
client = TelegramClient(phone, api_id, api_hash)
async def main():
    await client.send_message('me', 'Assalomu alaykum')
with client:
    client.loop.run_until_complete(main())
client.connect()
if not client.is_user_authorized():
    client.send_code_request(phone)
    client.sign_in(phone, input('Tasdiqlash kodini kiriting: '))

chats = []
last_date = None
chunk_size = 200
groups=[]

result = client(GetDialogsRequest(
             offset_date=last_date,
             offset_id=0,
             offset_peer=InputPeerEmpty(),
             limit=chunk_size,
             hash = 0
         ))
chats.extend(result.chats)

for chat in chats:
    try:
        if chat.megagroup== True:
            groups.append(chat)
    except:
        continue

print('Qaysi guruh foydalanuvchilarini ro`yxatini shakillantirmoqchisiz: ')
i=0
for g in groups:
    print(str(i) + '- ' + g.title)
    i+=1

g_index = input("Iltimos tartib raqamini kiriting: ")
target_group=groups[int(g_index)]

print('Foydalanuvchilari ro`yxatga olinmoqda...')
all_participants = []
all_participants = client.get_participants(target_group, aggressive=True)

print('Ro`yxat saqlanmoqda...')
with open("Foydalanuvchilar.csv","w",encoding='UTF-8') as f:
    writer = csv.writer(f,delimiter=",",lineterminator="\n")
    writer.writerow(['username','user id', 'access hash','name','group', 'group id'])
    for user in all_participants:
        if user.username:
            username= user.username
        else:
            username= ""
        if user.first_name:
            first_name= user.first_name
        else:
            first_name= ""
        if user.last_name:
            last_name= user.last_name
        else:
            last_name= ""
        name= (first_name + ' ' + last_name).strip()
        writer.writerow([username,user.id,user.access_hash,name,target_group.title, target_group.id])
print('Ro`yxatga olish muvoffaqiyatli yakunlandi!')
print('Murojat uchun nabiev.uz')
