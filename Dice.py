import ui
import console
import random
import collections
import threading
from CounterView import makeCounterView
from time import *
from enum import Enum

class RollType(Enum):
	melee = 0, 'Melee', 3
	ranged = 1, 'Ranged', 2
	defense = 2, 'Defense', 1
	
	def __new__(cls, value, name, dice):
		member = object.__new__(cls)
		member._value_ = value
		member.fullname = name
		member.success = dice
		return member
	
	def __int__(self):
		return self.value
		
mainView = 0

Roll = collections.namedtuple('Roll', ['hit', 'crit', 'damage', 'reroll', 'dice'])
diceCount = 1
rerollCount = 0
defenseCount = 1
random.seed()
rollCountdown = 0
rollResult = ''
diceResult = ''
numDice = 0
rollType = RollType.melee
critImage = (
	ui.Image.named('assets/AttackCrit100.png'), 
	ui.Image.named('assets/AttackCrit100.png'), 
	ui.Image.named('assets/DefenseCrit100.png'))
hitImage = (
	ui.Image.named('assets/AttackMelee100.png'), 
	ui.Image.named('assets/AttackRanged100.png'), 
	ui.Image.named('assets/DefenseSave100.png'))
missImage = (
	ui.Image.named('assets/Attack100.png'), 
	ui.Image.named('assets/Attack100.png'), 
	ui.Image.named('assets/Defense100.png'))

def roll(
	rollType, 
	dice, 
	reroll, 
	hitsAddDice=False, 
	rerollForCrit=False):
	hit = 0
	crit = 0
	rs = ''
	miss = 0
	addDice = 0
	while dice > 0:
		while dice > 0:
			dice -= 1
			d = random.randint(0, 5)
			if d == 0:
				rs += 'C'
				addDice += 1
				crit += 1
			elif d <= rollType.success:
				hit += 1
				rs += 'H'
				if hitsAddDice:
					addDice += 1
			else:
				miss += 1
				rs += 'M'
		if miss > 0 and reroll > 0:
			dice = min(miss, reroll)
			reroll -= dice
			miss -= dice
			rs += 'R'
		elif addDice > 0:
			rs += 'A'
			dice = addDice
			addDice = 0
		elif rerollForCrit and reroll > 0 and hit > 0 and crit == 0:
			hit -= 1
			reroll -= 1
			dice = 1
			rs += 'R'
	return Roll(hit, crit, hit + crit, reroll, rs)


def clearDice():
	i = 0
	while i < numDice:
		iv = mainView['die'+str(i)]
		iv.image = None
		i += 1

def calculateOdds(sender):
	global diceCount, defenseCount
	global rerollCount
	clearDice()
	hitsAddDice = mainView['switchHitsAddDice'].value
	count = 10000
	s = 'Average of %d rolls:\n' % (count)
	damage = 0
	crit = 0
	mmax = 0
	rdamage = 0
	rcrit = 0
	rmax = 0
	ddamage = 0
	dcrit = 0
	dmax = 0
	count = 10000
	loop = count
	while loop > 0:
		loop -= 1
		r = roll(RollType.melee, diceCount, rerollCount)
		damage += r.damage
		crit += r.crit
		mmax = max(mmax, r.damage)
		r = roll(RollType.ranged, diceCount, rerollCount, hitsAddDice=hitsAddDice)
		rdamage += r.damage
		rcrit += r.crit
		rmax = max(rmax, r.damage)
		r = roll(RollType.defense, defenseCount, rerollCount)
		ddamage += r.damage
		dcrit += r.crit
		dmax = max(dmax, r.damage)
	damage /= float(count)
	crit /= float(count)
	rdamage /= float(count)
	rcrit /= float(count)
	ddamage /= float(count)
	dcrit /= float(count)
	s += 'Melee:%.1f crit:%.1f max:%d\nRanged:%.1f crit:%.1f max:%d\nDefense:%.1f crit:%.1f max:%d' % (damage, crit, mmax, rdamage, rcrit, rmax, ddamage, dcrit, dmax)
	sender.superview['textRollResult'].text = s


def counterUpdate(sender):
	global diceCount
	global rerollCount
	global defenseCount
	if sender.name == 'labelCountDice':
		diceCount = int(sender.text)
	elif sender.name == 'labelCountReroll':
		rerollCount = int(sender.text)
	elif sender.name == 'labelCountDefense':
		defenseCount = int(sender.text)
	
	
def enableButtons(enable):
	mainView['buttonAttack'].enabled = enable
	mainView['buttonDefense'].enabled = enable
	mainView['buttonOdds'].enabled = enable

def showReroll(die):
	iv = mainView['die'+str(die)]
	img = iv.image
	with ui.ImageContext(img.size.width, img.size.height) as ctx:
		img.draw()
		#x = ui.Image.named()
		ui.set_color((1, 0, 0))
		x = ui.Path()
		x.line_width = 5
		x.move_to(0,0)
		x.line_to(100,100)
		x.move_to(100,0)
		x.line_to(0,100)
		x.stroke()
		out=ctx.get_image()
		iv.image = out

def showDice(rollType, rollStr):
	global numDice
	reroll = False
	skip = False
	i = 0
	while i < numDice:
		iv = mainView['die'+str(i)]
		if i >= len(rollStr):
			iv.image = None
			reroll = False
		elif rollStr[i] == 'H':
			iv.image = hitImage[int(rollType)]
		elif rollStr[i] == 'C':
			iv.image = critImage[int(rollType)]
		elif rollStr[i] == 'M':
			iv.image = missImage[int(rollType)]
		elif rollStr[i] == 'R':
			iv.image = ui.Image.named('typb:Loop')
			reroll = True
			skip = True
		elif rollStr[i] == 'A':
			iv.image = ui.Image.named('iob:ios7_plus_empty_256')
			reroll = False
		else:
			iv.image = ui.Image.named('iob:help_256')
		if skip:
			skip = False
		elif reroll:
			r = rollStr.find('M')
			old = 'M'
			new = 'm'
			if r >= i or r == -1:
				r = rollStr.find('H')
				old = 'H'
				new = 'h'
			rollStr = rollStr.replace(old, new, 1)
			showReroll(r)
		i += 1
			
	
def rollTimer():
	global rollSched, rollCountdown, rollResult, rollType, diceResult
	if rollCountdown > 0:
		s = '%d...' % (rollCountdown)
		mainView['textRollResult'].text += s
		rollCountdown -= 1
		threading.Timer(0.5, rollTimer).start()
	else:
		mainView['textRollResult'].text += rollResult
		enableButtons(True)
		showDice(rollType, diceResult)
	
	
def rollAttack(sender):
	global diceCount, rerollCount, rollCountdown, rollResult, diceResult, rollType
	hitsAddDice = mainView['switchHitsAddDice'].value
	rerollForCrit = mainView['switchRerollForCrit'].value
	hitsCritsStr = ''
	if rollCountdown == 0:
		enableButtons(False)
		melee = mainView['segmentedcontrolMelee']
		if melee.selected_index == 0:
			rollType = RollType.melee
			r = roll(rollType, diceCount, rerollCount, rerollForCrit=rerollForCrit)
		else:
			if hitsAddDice:
				hitsCritsStr = ', hits add dice'
			rollType = RollType.ranged
			r = roll(rollType, diceCount, rerollCount, hitsAddDice=hitsAddDice, rerollForCrit=rerollForCrit)
		rollResult = '\nHits:%d Crits:%d Damage:%d\n%d reroll left\n' % (r.hit, r.crit, r.damage, r.reroll)
		diceResult = r.dice
		s = 'Rolling %d %s (%d reroll%s) in 3...' % (diceCount, melee.segments[melee.selected_index], rerollCount, hitsCritsStr)
		mainView['textRollResult'].text = s
		rollCountdown = 2
		threading.Timer(0.5, rollTimer).start()
		clearDice()
	
	
def rollDefense(sender):
	global defenseCount, rerollCount, rollCountdown, rollResult, rollType, diceResult
	rerollForCrit = mainView['switchRerollForCrit'].value
	if rollCountdown == 0:
		enableButtons(False)
		rollType = RollType.defense
		r = roll(rollType, defenseCount, rerollCount, rerollForCrit=rerollForCrit)
		rollResult = '\nSaves:%d Crits:%d Blocked:%d\n%d reroll left\n' % (r.hit, r.crit, r.damage, r.reroll)
		s = 'Rolling defense %s (%d reroll) in 3...' % (defenseCount, rerollCount)
		mainView['textRollResult'].text = s
		diceResult = r.dice
		rollCountdown = 2
		threading.Timer(0.5, rollTimer).start()
		clearDice()
	
	
v = ui.load_view()
mainView = v
makeCounterView(v, "Reroll", 128, 8, rerollCount, counterUpdate)
makeCounterView(v, "Dice", 128, 48, diceCount, counterUpdate)
makeCounterView(v, "Defense", 128, 88, defenseCount, counterUpdate)
i = 0
sx, sy = 16, 360
y = 0
while y < (v.height - sy) / 32:
	x = 0
	while x < (v.width - sx) / 32 - 1:
		iv = ui.ImageView(frame=(sx + x * 32, sy + y * 32, 30, 30))
		iv.name = 'die%d' % (i)
		v.add_subview(iv)
		x += 1
		i += 1
	y += 1
numDice = i
v.present(orientations=['portrait'])
