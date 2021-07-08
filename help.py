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