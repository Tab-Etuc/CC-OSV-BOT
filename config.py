MAIN_COLOR = 0xa8e1fa
RED_COLOR = 0xfa5252
ORANGE_COLOR = 0xffc157
PINK_COLOR = 0xe0b3c7
PINK_COLOR_2 = 0xFFC0CB

Prefix = "C","c"
Owner_id = "806346991730819121"
好喔_pic = "https://cdn.discordapp.com/attachments/834074590720294912/854959330671591435/unknown.png"
WEBHOOK_URL = "https://discord.com/api/webhooks/859633422498398288/5JVnexiCnP3BIk-kLPuAk4xDqadplNzgv-85zyS25poVDjhFjPwXz1CX0SDkbUlkcSwb"

CHANGE_LOG = """
`-` \🟢 新增 商店功能`Cshop`。
`-` \🟢 新增 `Cmenu`指令。
`-` \🟢 合併 音樂機器人系統 \🎶
`-` \更多內容請查閱<#835138693101912104>......

"""

cmd_categories = [
  '經濟',
  '實用',
  '樂趣',
  '音樂',
  '圖片',
  '資訊',
  '遊戲',
  '政府高層專用指令',
  'nsfw',
]

經濟 = {
  'profile': "查看個人資訊。",
  'pay': "轉帳。",
  'salary': "顯示各職位薪資。",
  'count ': "顯示已於本銀行開戶數。",
  'shop': "展示商品。",
  'bag': "顯示你已購買的物品。",
  'buy': "購買物品。",
  'deposit': "將現金存入銀行。",
  'withdraw': "將銀行餘額領出。",
  'up': "升級銀行存款/利息額度。"
}

實用 = {
  'who': "說出你是誰。",
  'messages': "計算你在該頻道所傳送的訊息佔比。",
  'Translate': "對輸入的文本進行翻譯。",
  'Nitro': "發送一個免費領取Nitro的假訊息。",
  '編碼': "對輸入的文字進行加密。",
  '解碼': "對輸入的文字進行解密。",
}

樂趣 = {
  'whendie': "看看你剩多久壽命。",
  'owo': "和 OWO 聊天。",
  'burn': "Burn...",
  'howcute': "看看你有多可愛！",
  'tarsh': "Tarsh...",
  'comment': "對輸入的文字轉成YouTube留言圖片。",
  'wasted': "Wasted...",
}

音樂 = {
  'join': "讓CC-OSV加進音樂頻道。",
  'leave': "讓CC-OSV離開音樂頻道。",
  'volume': "調整音量。",
  'stop': "停止播放音樂。",
  'skip': "跳過當前播放的歌曲。",
  'queue': "顯示播放隊列。",
  'remove': "移除某首歌。",
  'loop': "循環播放某首歌",
  'play': "播放某首歌。",  
}

圖片 = {
  'meme': "從網路上抓取隨機的迷因圖。",
  'anime': "從網路上抓取隨機的動漫圖。",
  'cat': "從網路上抓取隨機的貓咪圖。",
  'dog': "從網路上抓取隨機的狗圖。",
  'fox': "從網路上抓取隨機的狐狸圖。",
  'panda': "從網路上抓取隨機的熊貓圖。",
  'redpanda': "從網路上抓取隨機的小貓熊圖。",
  'pikachu': "從網路上抓取隨機的皮卡丘圖。",
}

資訊 = {
  'weather': "顯示該地區的天氣。",  
  'Server': "顯示伺服器資訊。",  
  'ping': "顯示CC-OSV的延遲。",
  'help': "顯示幫助指令。",
  'bot': "顯示CC-OSV終端機資訊。",
  'covid-19': "顯示當地的中共肺炎疫情。"
}

遊戲 = {
  'slot': "老虎機。",
  'cointoss': "擲硬幣",
  'numgame': "數字遊戲。",
  'roulette': "輪盤。1:6的機率，成功將使餘額翻六倍。",
  'dice': "擲骰子。",
  '2048': "2048。",
  '8ball': "詢問8ball問題。",
  'minesweeper': "踩地雷。",
  'rps': "玩猜拳。",  
  'ttt': "井字遊戲。",  
  'wumpus': "wumpus。",      
}

政府高層專用指令 = {
  'clear': "清除指定數訊息。",
  'run': "使終端機執行code。",  
  'load': "裝載CC-OSV的Cog。",
  'unload': "卸載(大陸用語?)CC-OSV的Cog。",
  'reload': "重新裝載CC-OSV的Cog。",
  'embed': "傳送一個embed訊息。",      
  '課稅': "在特別時期強制執行一次課稅。",
  '賞': "強制印鈔予某人。",
  '罰': "扣除該人餘額。",  
  '國庫':"顯示國庫資訊。",
}

nsfw = {
  'hentai': "Hentai...",
  'thighs': "Thighs...",
  'nekogif': "Nekos but gifs",
}


經濟_with_emojis = """```
👥 -Profile
🏪 -Shop
🛒 -Buy
💱 -Pay
🛍️ -Bag
📜 -Salary
📜 -Count
💱 -Deposit
💱 -Withdraw
📊 -Top
💴 -Payday
👥 - Rob```
"""

實用_with_emojis = """```
😊 -who
💬 -Messages
💬 -Nitro
🔎 -wiki
🔎 -google
📑 -Translate
💾 -編碼
💾 -解碼```
"""

樂趣_with_emojis = """```
😊-Howcute
💀-Whendie
😊-OWO
💀-Wasted
🔥-Burn
🚮-Trash
💬-Comment```
"""

音樂_with_emojis = """```
🔊 -Join
🎶 -Play
🔁 -loop
🧾 -Queue
⏭ -Skip
❌ -Remove
⏹ -Stop
🔊 -Volume
👋 -Leave```
"""

圖片_with_emojis = """```
🤣-Meme
🥰-Anime
🐱-Cat
🐶-Dog
🦊-Fox
🐼-Panda
🐼-RedPanda
😻-Pikachu```
"""

資訊_with_emojis = """```
✅-Help
⛅-Weather
🦠-Covid-19
📈-Server
🤖-Bot
📉-Ping```
"""

遊戲_with_emojis = """```
🔢 -2048
🔢 -Numgame
🪙 -Cointoss
✅ -Tic-Tac-Toe
💣 -Minesweeper
🤖 -Wumpus
📃 -Rock-Paper-Scissors
🎰 -Slots
🎡 -Roulette
🎲 -Dice
🎱 -8ball```
"""

政府高層專用指令_with_emojis = """```
📨-Embed
💻-Run
❌ -Clear
💸 -課稅
💰 -賞
💰 -罰
💰 -國庫
⬆️ -Load
⬇️ -Unload
🔄-Reload```
"""

nsfw_with_emojis = """```
🔞-Hentai
🔞-Thighs
🔞-Nekogif```
"""

help_categories = [
    經濟,
    實用,
    樂趣,
    音樂,
    圖片,
    資訊,
    遊戲,
    政府高層專用指令,
    nsfw,
]
help_emoji_categories = [ 
    經濟_with_emojis,
    實用_with_emojis,
    樂趣_with_emojis,
    音樂_with_emojis,
    圖片_with_emojis,
    資訊_with_emojis,
    遊戲_with_emojis,
    政府高層專用指令_with_emojis,
    nsfw_with_emojis,
]
help_category_titles = [
    ":money_with_wings: • 經濟指令 (第 2 頁)",
    "⚙️ • 實用指令 (第 3 頁)",
    " :grinning: • 樂趣指令 (第 4 頁)",
    ":notes: • 音樂指令 (第 5 頁)",
    ":frame_photo: • 圖片指令 (第 6 頁)",
    "ℹ️ • 資訊指令 (第 7 頁)",
    ":video_game: • 遊戲指令 (第 8 頁)",
    ":tools: • 政府高層專用指令 (第 9 頁)",
    "🔞 • NSFW Commands (第 10 頁)",
]


total_cmds = 0
Supervisor_cmds = 0

for category in help_categories:
    total_cmds += len(category)