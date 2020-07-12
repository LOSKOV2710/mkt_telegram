print ("Bot https://t.me/nabievuz tomonidan yozildi")
print ("")

from telethon.sync import TelegramClient
from telethon.tl.functions.messages import GetDialogsRequest
from telethon.tl.types import InputPeerEmpty, InputPeerChannel, InputPeerUser
from telethon.errors.rpcerrorlist import PeerFloodError, UserPrivacyRestrictedError
from telethon.tl.functions.channels import InviteToChannelRequest
import sys
import csv
import traceback
import time
import random

api_id = 0000000   #7 raqamdan iborat bo'lgan Telegram API ID ni kiriting.
api_hash = '98c2e9dbec19ebb226c588c0c1afe2vr'   #32 ta raqam va harflardan iborat API Hash ni kiriting.
phone = '+998910001122'   #Telegramga biriktirilgan telefon raqamini kiriting.
client = TelegramClient(phone, api_id, api_hash)
async def main():
    await client.send_message('me', 'Assalomu alaykum')


SLEEP_TIME_1 = 100
SLEEP_TIME_2 = 100
with client:
    client.loop.run_until_complete(main())
client.connect()
if not client.is_user_authorized():
    client.send_code_request(phone)
    client.sign_in(phone, input('40779'))

users = []
with open(r"Foydalanuvchilar.csv", encoding='UTF-8') as f:
    rows = csv.reader(f,delimiter=",",lineterminator="\n")
    next(rows, None)
    for row in rows:
        user = {}
        user['username'] = row[0]
        user['id'] = int(row[1])
        user['access_hash'] = int(row[2])
        user['name'] = row[3]
        users.append(user)

chats = []
last_date = None
chunk_size = 200
groups = []

result = client(GetDialogsRequest(
    offset_date=last_date,
    offset_id=0,
    offset_peer=InputPeerEmpty(),
    limit=chunk_size,
    hash=0
))
chats.extend(result.chats)

for chat in chats:
    try:
        if chat.megagroup == True:
            groups.append(chat)
    except:
        continue

print('Foydalanuvchilarni qo`shish uchun siz adminlik qilayotgan guruhni tanlang: ')
i = 0
for group in groups:
    print(str(i) + '- ' + group.title)
    i += 1

g_index = input("Tartib raqamini kiriting: ")
target_group = groups[int(g_index)]

target_group_entity = InputPeerChannel(target_group.id, target_group.access_hash)

mode = int(input("1 - username yoki 2 - ID orqali saralash rejimini tanlang: "))

n = 0

for user in users:
    n += 1
    if n % 80 == 0:
        sleep(60)
    try:
        print("Jarayon boshlandi {}".format(user['id']))
        if mode == 1:
            if user['username'] == "":
                continue
            user_to_add = client.get_input_entity(user['username'])
        elif mode == 2:
            user_to_add = InputPeerUser(user['id'], user['access_hash'])
        else:
            sys.exit("Tanlangan rejim ish bermadi. Iltimos, yana bir bor urinib ko'ring.")
        client(InviteToChannelRequest(target_group_entity, [user_to_add]))
        print("60-180 soniya kuting...")
        time.sleep(random.randrange(0, 5))
    except PeerFloodError:
        print("Telegramda xato aniqlandi. Hozir bot to'xtaydi. Biroz vaqtdan keyin yana urinib ko'ring.")
        print("{} soniya kuting".format(SLEEP_TIME_2))
        time.sleep(SLEEP_TIME_2)
    except UserPrivacyRestrictedError:
        print("Foydalanuvchining maxfiylik sozlamalari amaliyot o'tkazishga ruxsat bermadi. O'tkazib yuborildi")
        print("5 soniya kutilmoqda...")
        time.sleep(random.randrange(0, 5))
    except:
        traceback.print_exc()
        print("Kutilmagan xatolik")
        continue
