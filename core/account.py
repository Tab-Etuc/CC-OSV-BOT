import csv
import time
import random
import pandas as pd
from discord_webhook.webhook import DiscordWebhook

def count():
    df = pd.read_csv('accounts.csv')
    return len(df.index)


def register(name):
    df = pd.read_csv('accounts.csv')

    if (df["UserId"] == int(name)).any():
        webhook = DiscordWebhook(url='https://discord.com/api/webhooks/847789988602183720/RVEzJMCjnMUCp8ToD0iIYC6DrwQUNVh1l0ZCZSk4Pu7Eych237rTZhzZNOvGO_GXWp7D', content='你已經開過戶了。')
        webhook.execute()
    else:
        with open('accounts.csv', 'a', newline='') as fd:
            fdw = csv.writer(fd)
            fdw.writerow([name, 0, 0, 0, 0, 0, 0, 0])
            webhook = DiscordWebhook(url='https://discord.com/api/webhooks/847789988602183720/RVEzJMCjnMUCp8ToD0iIYC6DrwQUNVh1l0ZCZSk4Pu7Eych237rTZhzZNOvGO_GXWp7D', content='開戶成功。')
            webhook.execute()


def bal(name):
    df = pd.read_csv('accounts.csv')

    if (df["UserId"] == int(name)).any():
        return int(df.loc[df["UserId"] == int(name), "Balance"])
    else:
        return None


def top():
    global top, top2, top3, top4, top5
    df = pd.read_csv('accounts.csv')
    df = df.sort_values(by=["Balance"], ascending=[0])
    df.to_csv('accounts.csv', index=False)

    with open('accounts.csv', 'r') as readin:
        counter = 0
        leaderboard = []

        next(readin)
        for row in readin:
            counter += 1
            if counter <= 5:
                leaderboard.append(row.split(','))

        if len(leaderboard) < 5:
            while len(leaderboard) < 5:
                leaderboard.append(["無", '0'])

        return leaderboard


def pay(startuser, enduser, amount):
    if amount < 1:
        webhook = DiscordWebhook(url='https://discord.com/api/webhooks/847789988602183720/RVEzJMCjnMUCp8ToD0iIYC6DrwQUNVh1l0ZCZSk4Pu7Eych237rTZhzZNOvGO_GXWp7D', content='可輸入的最小值為壹。')
        webhook.execute()
    balnum = bal(startuser)
    if balnum is None:
        webhook = DiscordWebhook(url='https://discord.com/api/webhooks/847789988602183720/RVEzJMCjnMUCp8ToD0iIYC6DrwQUNVh1l0ZCZSk4Pu7Eych237rTZhzZNOvGO_GXWp7D', content='請參照此格式`Creg` 開戶。')
        webhook.execute()
    if amount > int(balnum):
        webhook = DiscordWebhook(url='https://discord.com/api/webhooks/847789988602183720/RVEzJMCjnMUCp8ToD0iIYC6DrwQUNVh1l0ZCZSk4Pu7Eych237rTZhzZNOvGO_GXWp7D', content='你沒有足夠的簡明幣。使用Cbank 查看你當前的餘額。')
        webhook.execute()

    df = pd.read_csv('accounts.csv')

    if (df["UserId"] == int(enduser)).any():
        df = pd.read_csv('accounts.csv')
        df.loc[df["UserId"] == int(enduser), "Balance"] += amount
        df.to_csv('accounts.csv', index=False)

        df = pd.read_csv('accounts.csv')
        df.loc[df["UserId"] == int(startuser), "Balance"] -= amount
        df.to_csv('accounts.csv', index=False)

        webhook = DiscordWebhook(url='https://discord.com/api/webhooks/847789988602183720/RVEzJMCjnMUCp8ToD0iIYC6DrwQUNVh1l0ZCZSk4Pu7Eych237rTZhzZNOvGO_GXWp7D', content='轉帳成功！')
        webhook.execute()
    else:
        webhook = DiscordWebhook(url='https://discord.com/api/webhooks/847789988602183720/RVEzJMCjnMUCp8ToD0iIYC6DrwQUNVh1l0ZCZSk4Pu7Eych237rTZhzZNOvGO_GXWp7D', content='用戶不存在或尚未註冊銀行帳戶。')
        webhook.execute()

def 罰(startuser, enduser, amount):
    if amount < 1:
        webhook = DiscordWebhook(url='https://discord.com/api/webhooks/847789988602183720/RVEzJMCjnMUCp8ToD0iIYC6DrwQUNVh1l0ZCZSk4Pu7Eych237rTZhzZNOvGO_GXWp7D', content='可輸入的最小值為壹。')
        webhook.execute()
    balnum = bal(startuser)
    if balnum is None:
        webhook = DiscordWebhook(url='https://discord.com/api/webhooks/847789988602183720/RVEzJMCjnMUCp8ToD0iIYC6DrwQUNVh1l0ZCZSk4Pu7Eych237rTZhzZNOvGO_GXWp7D', content='請參照此格式`Creg`開戶。')
        webhook.execute()

    df = pd.read_csv('accounts.csv')

    if (df["UserId"] == int(enduser)).any():
        df = pd.read_csv('accounts.csv')
        df.loc[df["UserId"] == int(enduser), "Balance"] -= amount
        df.to_csv('accounts.csv', index=False)

        df.to_csv('accounts.csv', index=False)

        webhook = DiscordWebhook(url='https://discord.com/api/webhooks/847789988602183720/RVEzJMCjnMUCp8ToD0iIYC6DrwQUNVh1l0ZCZSk4Pu7Eych237rTZhzZNOvGO_GXWp7D', content='罰錢成功！')
        webhook.execute()
    else:
        webhook = DiscordWebhook(url='https://discord.com/api/webhooks/847789988602183720/RVEzJMCjnMUCp8ToD0iIYC6DrwQUNVh1l0ZCZSk4Pu7Eych237rTZhzZNOvGO_GXWp7D', content='用戶不存在或尚未註冊銀行帳戶。')
        webhook.execute()

def 賞(startuser, enduser, amount):
    if amount < 1:
        webhook = DiscordWebhook(url='https://discord.com/api/webhooks/847789988602183720/RVEzJMCjnMUCp8ToD0iIYC6DrwQUNVh1l0ZCZSk4Pu7Eych237rTZhzZNOvGO_GXWp7D', content='可輸入的最小值為壹。')
        webhook.execute()
    balnum = bal(startuser)
    if balnum is None:
        webhook = DiscordWebhook(url='https://discord.com/api/webhooks/847789988602183720/RVEzJMCjnMUCp8ToD0iIYC6DrwQUNVh1l0ZCZSk4Pu7Eych237rTZhzZNOvGO_GXWp7D', content='請參照此格式`Creg`開戶。')
        webhook.execute()

    df = pd.read_csv('accounts.csv')

    if (df["UserId"] == int(enduser)).any():
        df = pd.read_csv('accounts.csv')
        df.loc[df["UserId"] == int(enduser), "Balance"] += amount
        df.to_csv('accounts.csv', index=False)

        df.to_csv('accounts.csv', index=False)

        webhook = DiscordWebhook(url='https://discord.com/api/webhooks/847789988602183720/RVEzJMCjnMUCp8ToD0iIYC6DrwQUNVh1l0ZCZSk4Pu7Eych237rTZhzZNOvGO_GXWp7D', content='成功執行！')
        webhook.execute()
    else:
        webhook = DiscordWebhook(url='https://discord.com/api/webhooks/847789988602183720/RVEzJMCjnMUCp8ToD0iIYC6DrwQUNVh1l0ZCZSk4Pu7Eych237rTZhzZNOvGO_GXWp7D', content='查無此人')
        webhook.execute()


def payday(name):
    df = pd.read_csv('accounts.csv')

    if (df["UserId"] == int(name)).any():
        timer = int(df.loc[df["UserId"] == int(name), "Payday"])

        timeleft = int(time.time() - timer)
        timeleft = 7200 - timeleft
        if timeleft > 0:
            typeT = '秒'
            if timeleft > 60:
                timeleft = timeleft // 60
                typeT = '分鐘'
            webhook = DiscordWebhook(url='https://discord.com/api/webhooks/847789988602183720/RVEzJMCjnMUCp8ToD0iIYC6DrwQUNVh1l0ZCZSk4Pu7Eych237rTZhzZNOvGO_GXWp7D', content='你仍需等待{}{}!'.format(timeleft, typeT))
            webhook.execute()
        else:
          df.loc[df["UserId"] == int(name), "Balance"] += df.loc[df["UserId"] == int(name), "Money"]
          df.loc[df["UserId"] == int(name), "Payday"] = time.time()
          df.to_csv('accounts.csv', index=False)
          webhook = DiscordWebhook(url='https://discord.com/api/webhooks/847789988602183720/RVEzJMCjnMUCp8ToD0iIYC6DrwQUNVh1l0ZCZSk4Pu7Eych237rTZhzZNOvGO_GXWp7D', content='你已領取了你的薪資並已自動繳納所得稅，使用`Cbank`查看')
          webhook.execute()
    else:
        webhook = DiscordWebhook(url='https://discord.com/api/webhooks/847789988602183720/RVEzJMCjnMUCp8ToD0iIYC6DrwQUNVh1l0ZCZSk4Pu7Eych237rTZhzZNOvGO_GXWp7D', content='請參照此格式`Creg`開戶。')
        webhook.execute()

def numgame(name, guess, guessnum, answer):
    if guess == answer:
        reward = {1: 10000, 2: 9900, 3: 8750, 4: 7600, 5: 6450, 6: 5300}

        fmt = "你答對了！你僅猜測了{}個答案。作為獎勵，你得到{}簡明幣"

        df = pd.read_csv('accounts.csv')
        df.loc[df["UserId"] == int(name), "Balance"] += reward[guessnum]
        df.to_csv('accounts.csv', index=False)

        return fmt.format(guessnum, reward[guessnum])

    elif guessnum != 6:
        if guess < answer:
            return '`答案再高點...`'
        if guess > answer:
            return '`答案再低點...`'

    if guessnum == 6 and guess != answer:
            fmt = '你在六個數字內沒有猜測到答案。答案是 {}。'
            return fmt.format(answer)

def rob(name, ramount):

    df = pd.read_csv('accounts.csv')

    if (df["UserId"] == int(name)).any():
        timer = int(df.loc[df["UserId"] == int(name), "Rob"])
        balrob = int(df.loc[df["UserId"] == int(name), "Balance"])
    else:
        webhook = DiscordWebhook(url='https://discord.com/api/webhooks/847789988602183720/RVEzJMCjnMUCp8ToD0iIYC6DrwQUNVh1l0ZCZSk4Pu7Eych237rTZhzZNOvGO_GXWp7D', content='請參照此格式`Creg`開戶。')
        webhook.execute()

    timeleft = int(time.time()-timer)
    timeleft = 60 - timeleft
    if timeleft > 0:
        webhook = DiscordWebhook(url='https://discord.com/api/webhooks/847789988602183720/RVEzJMCjnMUCp8ToD0iIYC6DrwQUNVh1l0ZCZSk4Pu7Eych237rTZhzZNOvGO_GXWp7D', content='你仍需等待{}秒'.format(timeleft))
        webhook.execute()

    if ramount > 3000:
        webhook = DiscordWebhook(url='https://discord.com/api/webhooks/847789988602183720/RVEzJMCjnMUCp8ToD0iIYC6DrwQUNVh1l0ZCZSk4Pu7Eych237rTZhzZNOvGO_GXWp7D', content='可輸入的最大值為参仟。')
        webhook.execute()
    elif ramount < 1:
        webhook = DiscordWebhook(url='https://discord.com/api/webhooks/847789988602183720/RVEzJMCjnMUCp8ToD0iIYC6DrwQUNVh1l0ZCZSk4Pu7Eych237rTZhzZNOvGO_GXWp7D', content='可輸入的最大值為壹。')
        webhook.execute()
    elif balrob < ramount:
        webhook = DiscordWebhook(url='https://discord.com/api/webhooks/847789988602183720/RVEzJMCjnMUCp8ToD0iIYC6DrwQUNVh1l0ZCZSk4Pu7Eych237rTZhzZNOvGO_GXWp7D', content='你沒有足夠的餘額。使用Cbank查看你當前的餘額。')
        webhook.execute()
    else:
        if ramount > 2490:
            chance = 65
        elif ramount > 2000:
            chance = 60
        elif ramount > 1490:
            chance = 55
        elif ramount > 1000:
            chance = 50
        elif ramount > 0:
            chance = 45

    chancenum = random.randint(0, 100)
    if chancenum <= chance:
        df = pd.read_csv('accounts.csv')
        df.loc[df["UserId"] == int(name), "Balance"] += ramount
        df.loc[df["UserId"] == int(name), "Rob"] = time.time()
        df.to_csv('accounts.csv', index=False)
        webhook = DiscordWebhook(url='https://discord.com/api/webhooks/847789988602183720/RVEzJMCjnMUCp8ToD0iIYC6DrwQUNVh1l0ZCZSk4Pu7Eych237rTZhzZNOvGO_GXWp7D', content='恭喜！你賺到了{}元簡明幣。'.format(ramount))
        webhook.execute()
    else:
        df = pd.read_csv('accounts.csv')
        df.loc[df["UserId"] == int(name), "Balance"] -= ramount
        df.loc[df["UserId"] == int(name), "Rob"] = time.time()
        df.to_csv('accounts.csv', index=False)
        webhook = DiscordWebhook(url='https://discord.com/api/webhooks/847789988602183720/RVEzJMCjnMUCp8ToD0iIYC6DrwQUNVh1l0ZCZSk4Pu7Eych237rTZhzZNOvGO_GXWp7D', content='你失手了。你失去了{}元簡明幣。'.format(ramount))
        webhook.execute()

def roulette(name):
    df = pd.read_csv('accounts.csv')

    if (df["UserId"] == int(name)).any():
        timer = int(df.loc[df["UserId"] == int(name), "Roulette"])
    else:
        webhook = DiscordWebhook(url='https://discord.com/api/webhooks/847789988602183720/RVEzJMCjnMUCp8ToD0iIYC6DrwQUNVh1l0ZCZSk4Pu7Eych237rTZhzZNOvGO_GXWp7D', content='請參照此格式`Creg`開戶。 ')
        webhook.execute()

    timeleft = int(time.time() - timer)
    timeleft = 86400 - timeleft

    if timeleft > 0:
        typeT = '秒'
        if timeleft > 60:
            timeleft = timeleft // 60 + 1
            typeT = '分鐘'
            if timeleft > 60:
                timeleft = timeleft // 60
                typeT = '小時'
        webhook = DiscordWebhook(url='https://discord.com/api/webhooks/847789988602183720/RVEzJMCjnMUCp8ToD0iIYC6DrwQUNVh1l0ZCZSk4Pu7Eych237rTZhzZNOvGO_GXWp7D', content='你仍須等待{}{}!'.format(timeleft, typeT))
        webhook.execute()

    num = random.randint(1, 6)
    if num == 1:
        df.loc[df["UserId"] == int(name), "Balance"] = (bal(name) * 6)
        df.loc[df["UserId"] == int(name), "Roulette"] = time.time()
        df.to_csv('accounts.csv', index=False)
        webhook = DiscordWebhook(url='https://discord.com/api/webhooks/847789988602183720/RVEzJMCjnMUCp8ToD0iIYC6DrwQUNVh1l0ZCZSk4Pu7Eych237rTZhzZNOvGO_GXWp7D', content='你安全了！你將你的餘額翻了六倍！')
        webhook.execute()
    else:
        df.loc[df["UserId"] == int(name), "Balance"] = 0
        df.loc[df["UserId"] == int(name), "Roulette"] = time.time()
        df.to_csv('accounts.csv', index=False)
        webhook = DiscordWebhook(url='https://discord.com/api/webhooks/847789988602183720/RVEzJMCjnMUCp8ToD0iIYC6DrwQUNVh1l0ZCZSk4Pu7Eych237rTZhzZNOvGO_GXWp7D', content='BOOM! 你死了。 :(')
        webhook.execute()