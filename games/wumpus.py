# Wumpus Game

# Importing random function library.
import random
import asyncio

async def play(bot, ctx):
	# Initialize the map array.

	world = [['  ' for _ in range(10)] for _ in range(7)]

	# Hide the wumpus (w).
	row = random.randint(1, 5)
	col = random.randint(1, 8)
	world[row][col] = 'w'

	# Hide the 2 pits (p).
	needit = True
	while needit:
		row = random.randint(1, 5)
		col = random.randint(1, 8)
		if world[row][col] == '  ':
			world[row][col] = 'p'
			needit = False
	needit = True
	while needit:
		row = random.randint(1, 5)
		col = random.randint(1, 8)
		if world[row][col] == '  ':
			world[row][col] = 'p'
			needit = False

	# Hide the 2 bats (b)
	needit = True
	while needit:
		row = random.randint(1, 5)
		col = random.randint(1, 8)
		if world[row][col] == '  ':
			world[row][col] = 'b'
			needit = False
	needit = True
	while needit:
		row = random.randint(1, 5)
		col = random.randint(1, 8)
		if world[row][col] == '  ':
			world[row][col] = 'b'
			needit = False
	# Place the user in a safe spot.
	needit = True
	while needit:
		row = random.randint(1, 5)
		col = random.randint(1, 8)
		if world[row][col] == '  ':
			userRow = row
			userCol = col
			needit = False

	# Initialize variables
	arrows = 2
	alive = True

	def printBoard(r, c):
		out = []
		w = [['  ' for _ in range(10)] for _ in range(7)]
		w[r][c] = '💂🏻‍♂️'
		for i in w:
			out.append('|'.join(i[1:-1]))
		return '```\n' + '\n--+--+--+--+--+--+--+--\n'.join(out[1:-1]) + '\n```'

	async def endBoard(r, c, sys_msg):
		out = []
		world[r][c] = '💂🏻‍♂️'
		for i in world:
			out.append('|'.join(i[1:-1]))
		await sys_msg.edit(content='```\n' + '\n--+--+--+--+--+--+--+--\n'.join(out[1:-1]).replace('w', '👹').replace('b', '🦇').replace('p', '⚫') + '\n```')
		return await p_msg.delete()

	# brd_msg 
	brd_msg = await ctx.send(printBoard(userRow, userCol))
	sys_msg = await ctx.send(f":bow_and_arrow:  `{arrows}`")
	# obs_msg
	p_msg = await ctx.send(":grinning:  `讀取中...`")
	# addreactions
	reactions = ['⬆', '⬇', '⬅', '➡', '🏹', '❌']
	# async with ctx.typing():
	for reaction in reactions:
		await p_msg.add_reaction(reaction)
	while alive:
		# Tell user where he is.
		# brd_msg
		await brd_msg.edit(content=printBoard(userRow, userCol))

		# Tells user if he is near the wumpus
		if world[userRow - 1][userCol] == 'w' or world[userRow + 1][userCol] == 'w' or world[userRow][userCol - 1] == 'w' or \
						world[userRow][userCol + 1] == 'w':
			# p_msg
			await p_msg.edit(content=':nauseated_face:  `我感覺到了周遭的異常...`')

		# Tells user if he is near a pit
		elif world[userRow - 1][userCol] == 'p' or world[userRow + 1][userCol] == 'p' or world[userRow][userCol - 1] == 'p' or \
						world[userRow][userCol + 1] == 'p':
			# p_msg
			await p_msg.edit(content=':dizzy_face:  `有股噁心的味道再周遭...`')

		# Tell the user if he is near a bat
		elif world[userRow - 1][userCol] == 'b' or world[userRow + 1][userCol] == 'b' or world[userRow][userCol - 1] == 'b' or \
						world[userRow][userCol + 1] == 'b':
			# p_msg
			await p_msg.edit(content=':rolling_eyes:  `我聽到了翅膀拍動聲...`')
		else:
			await p_msg.edit(content=':grinning:  `沒什麼特別的。`')



		# Ask user what to do next (n/s/e/w/f).
		# sys_msg
		# 'What do you want to do next?'
		def check(reaction, user):
			# print(str(reaction.emoji))
			return user != bot.user and (str(reaction.emoji) == '⬆' or '⬇' or '⬅' or '➡' or '🏹' or '❌')
		try:
			action, user = await bot.wait_for('reaction_add', timeout=10.0, check=check)
			action = str(action.emoji)
			await p_msg.remove_reaction(action, user)
		except asyncio.TimeoutError:
			await ctx.send(f"時間到! :stopwatch:\n遊戲結束 :coffin:")
			await endBoard(userRow, userCol, sys_msg)
			return

		# If direction, move
		if action == '⬆':
			userRow = userRow - 1
		if action == '⬇':
			userRow = userRow + 1
		if action == '➡':
			userCol = userCol + 1
		if action == '⬅':
			userCol = userCol - 1

		# Do not allow user to walk off the face of the Earth.
		if userRow == 0:
			userRow = 1
		elif userRow == 6:
			userRow = 5

		if userCol == 9:
			userCol = 8
		elif userCol == 0:
			userCol = 1

		# If wumpus then user dies.
		if world[userRow][userCol] == 'w':
			await ctx.send('你成了蝙蝠的晚餐...')
			await endBoard(userRow, userCol, sys_msg)
			return

		# If pit then user dies.
		if world[userRow][userCol] == 'p':
			await ctx.send('"Aaaaaaaaaah!"(尖叫聲)')
			await endBoard(userRow, userCol, sys_msg)
			return

		# If bat then hyperspace.
		if world[userRow][userCol] == 'b':
			await ctx.send('你被蝙蝠撿到了。')
			await endBoard(userRow, userCol, sys_msg)
			return

		# Arrow/Shooting Stuff

		if action == '🏹':
			s_msg = await ctx.send("往何處射擊？", delete_after=12.0)
			# async with ctx.typing():
			for reaction in reactions[:-2]:
				await s_msg.add_reaction(reaction)

			def checkf(reaction, user):
				return user != bot.user and user == ctx.author and (str(reaction.emoji) == '⬆' or '⬇' or '⬅' or '➡')
			try:
				flight, user = await bot.wait_for('reaction_add', timeout=10.0, check=checkf)
			except asyncio.TimeoutError:
				await ctx.send(f"時間到! :stopwatch:\n遊戲結束 :coffin:")
				await endBoard(userRow, userCol, sys_msg)
				return
			await s_msg.delete()

			flight = str(flight.emoji)
			# Check if the arrow hit the wumpus.
			if flight == '⬆':
				arrowRow = userRow - 1
				arrowCol = userCol
			if flight == '⬇':
				arrowRow = userRow + 1
				arrowCol = userCol
			if flight == '➡':
				arrowRow = userRow
				arrowCol = userCol + 1
			if flight == '⬅':
				arrowRow = userRow
				arrowCol = userCol - 1

			# Do not allow the arrow to fly off the face of the Earth
			if arrowRow == 0:
				arrowRow = 1
			if arrowRow == 6:
				arrowRow = 5
			if arrowCol == 0:
				arrowCol = 1
			if arrowCol == 9:
				arrowCol = 8

			# Check what is in the spaces that he fired into.
			lookup = world[arrowRow][arrowCol]
			if lookup == 'w':
				try:
					await brd_msg.delete()
				except Exception:
					continue
				else:
					await ctx.send('**You win :trophy:**')
					await p_msg.edit(content=":star_struck:")
					await endBoard(userRow, userCol, sys_msg)
					return
			else:
				await ctx.send(':bow_and_arrow: Miss!', delete_after=1.5)

			arrows = arrows - 1
			await sys_msg.edit(content=f":bow_and_arrow:  `{arrows}`")
			if arrows==0:
				await ctx.send(":bow_and_arrow:\n遊戲結束 :coffin:")
				await endBoard(userRow, userCol, sys_msg)
				return

		if action == '❌':
			await ctx.send('已退出 :x:')
			await endBoard(userRow, userCol, sys_msg)
			return