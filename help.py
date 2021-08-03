CHANGE_LOG = """
`-` \🟢 新增 升級利息、存額功能。
`-` \🟢 新增 自動匯入薪資。
`-` \🟠 分開 現金、銀行餘額。
`-` \🔴 刪除 音樂機器人系統 \🎶
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
👥 - Rob
🆙 -Up```
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
all_cmds= {

  #經濟
  'profile':[
    "顯示你的個人資訊。\n將包含：[薪資，現金、銀行餘額，銀行存款等階，銀行會員等階，暱稱，帳號創建、加入時間]",
    "p,bank,BANK,Bank,P",
    "profile"
  ],
  'pay':[
    "將銀行餘額轉帳給指定國民。\n註：若超過對方之銀行存款額度，此操作將被禁止。",
    "send",
    "pay [@提及] [金額]"
  ],
  'salary':[
    "顯示本國各職位之薪資表。",
    "SY,薪水,Salary,SALARY",
    "salary"
  ],
  'count':[
    "顯示已於本銀行開戶數。",
    "無",
    "count"
  ],
  'shop':[
    "展示商品。",
    "無",
    "shop"
  ],
  'bag':[
    "顯示你已購買的物品。",
    "無",
    "bag"
  ],
  'buy':[
    "購買物品。",
    "無",
    "buy [商品名] (數量)"
  ],
  'deposit':[
    "將現金存入銀行。",
    "dep",
    "deposit [金額]"
  ],
  'withdraw':[
    "將銀行餘額領出。",
    "with",
    "withdraw [金額]"
  ],
  'up':[
    "升級銀行存款/利息額度。可以使用[all/max]一次升級到最大值。",
    "無",
    "up [存額/信用卡] (all/max)"
  ],

  #樂趣
  'whendie':[
    "看看你多久後會過世......",
    "WHENDIE,BET,Whendie",
    "whendie"
  ],
  'owo':[
    "和 OWO 聊天。",
    "無",
    "owo [文字]"
  ],
  'burn':[
    "將某人的頭貼印上Burn...",
    "BURN,Burn",
    "burn (@提及)"
  ],
  'trash':[
    "將某人的頭貼印上Tarsh...",
    "Trash,TRASH",
    "trash (@提及)"
  ],
  'howcute':[
    "看看你有多可愛！",
    "HowCute,HOWCUTE,Howcute",
    "howcute"
  ],
  'comment':[
    "對輸入的文字轉成YouTube留言圖片。(僅限英文)",
    "COMMENT,Comment",
    "comment [文字]"
  ],
  'wasted':[
    "wasted",
    "wasted...",
    "Wasted,WASTED",
  ],

  #實用
  'who':[
    "說出你是誰。",
    "WHO,Who",
    "who"
  ],
  'messages':[
    "計算你在該頻道所傳送的訊息佔比。\n註：該頻道訊息數大於萬，將有可能失效。",
    "msg,MSG",
    "messages"
  ],
  'Translate':[
    "此功能暫時關閉中。\n註：\"[tr]\"內的[]為必輸入之中括號，而非表示[]內的文字為必填。",
    "無",
    "\"[tr]\" [訊息]"
  ],
  'Nitro':[
    "發送一個免費領取Nitro的假訊息。",
    "NITRO,nitro",
    "Nitro"
  ],
  '編碼':[
    "對輸入的文字進行加密。\n\n編碼方式：\nASCII85\nbase32 \nbase64 \nbase85 \nhex \nrot13 ",
    "encode,ENCODE",
    "C編碼 [編碼方式]"
  ],
  '解碼':[
    "對輸入的文字進行解密。\n\n解碼方式：\nASCII85\nbase32 \nbase64 \nbase85 \nhex \nrot13 ",
    "decode,DECODE",
    "comment [文字]"
  ],

  #圖片
  'meme':[
    "從網路上抓取隨機的迷因圖。",
    "MEME,Meme",
    "meme",
  ],
  'anime':[
    "從網路上抓取隨機的動漫圖。",
    "ANIME,Anime",
    "anime",
  ],
  'cat':[
    "從網路上抓取隨機的貓咪圖。",
    "meow,cats,CAT",
    "cat",
  ],
  'dog':[
    "從網路上抓取隨機的狗圖。",
    "dogs,DOG",
    "dog",
  ],
  'fox':[
    "從網路上抓取隨機的狐狸圖。",
    "FOX,Fox",
    "fox",
  ],
  'panda':[
    "從網路上抓取隨機的熊貓圖。",
    "PANDA,Panda",
    "panda",
  ],    
  'redpanda':[
    "從網路上抓取隨機的小貓熊圖。",
    "REDPANDA,Redpanda",
    "redpanda",
  ],
  'pikachu':[
    "從網路上抓取隨機的皮卡丘圖。",
    "pika,PIKA",
    "pikachu",
  ],      

  #資訊
  'weather':[
    "顯示該地區的天氣。",
    "無",
    "weather",
  ],
  'server':[
    "顯示伺服器資訊。",
    "sinfo,serverinfo",
    "server",
  ],
  'ping':[
    "顯示CC-OSV的延遲。",
    "Ping,PING",
    "ping",
  ],
  'help':[
    "顯示幫助指令。",
    "無",
    "help (類別/指令)",
  ],    
  'bot':[
    "顯示CC-OSV終端機資訊。",
    "python,botinfo,BOT",
    "bot",
  ],
  'covid-19':[
    "顯示當地的中共肺炎疫情。",
    "covid,covid19,COVID",
    "covid-19 [地區(英文)]",
  ],        

  #遊戲
  'slot':[
    "老虎機。",
    "老虎機,slots,bet",
    "slot",
  ],
  'cointoss':[
    "擲硬幣",
    "toss,flip",
    "cointoss",
  ],
  'numgame':[
    "猜數字遊戲。",
    "nungame,num,NUNGAME",
    "numgame",
  ],
  'roulette':[
    "輪盤。1:6的機率，成功將使餘額翻六倍。",
    "輪盤,RL",
    "roulette",
  ],    
  'dice':[
    "擲骰子。",
    "DICE,Dice",
    "dice [骰面]",
  ],
  '2048':[
    "2048。",
    "無",
    "2048",
  ],        
    '8ball':[
    "詢問8ball問題。",
    "8BALL,8ball",
    "8ball [問題]",
  ],
  'minesweeper':[
    "踩地雷。",
    "ms",
    "minesweeper",
  ],
  'rps':[
    "玩猜拳。",
    "rockpaperscissors",
    "rps",
  ],
  'ttt':[
    "井字遊戲。",
    "tictactoe",
    "ttt",
  ],    
  'wumpus':[
    "wumpus。",
    "WUMPUS,Wumpus",
    "wumpus。",
  ],
      
  #政府高層專用指令
  
}