import collections

class UpgradeGroup(Enum):
	permanent = 0, 'Permanent'
	melee = 1, 'Melee Attack'
	ranged = 2, 'Ranged Attack'
	boost = 3, 'Boost'
	
	def __new__(cls, value, name):
		member = object.__new__(cls)
		member._value_ = value
		member.fullname = name
		return member
	
	def __int__(self):
		return self.value

class UpgradeType(Enum):
	sword = 0, 'Sword'
	hammer = 1, 'Hammer'
	axe = 2, 'Axe'
	lance = 3, 'Lance'
	bow = 100, 'Bow'
  magic = 101, 'Magic'
  thrown = 102, 'Thrown Weapon'
  gear = 201, 'Gear'
  bling = 202, 'Bling'
  shield = 203, 'Shield'
  ability = 204, 'Ability'
  armor = 205, 'Armor'
	
	def __new__(cls, value, name):
		member = object.__new__(cls)
		member._value_ = value
		member.fullname = name
		member.group 
		return member
	
	def __int__(self):
		return self.valuelass Upgrade:
	
class Upgrade:
	def __init__(self, id, name, ug, ut, dice=0, block=0, reroll=0)
	  self.id = id
	  self.name = name
	  self.group = ug
	  self.utype = ut
	  self.dice = dice
	  self.block = block
	  self.reroll = reroll
	
upgrades = (
	Upgrade('S-01', 'Rusty Blade', UpgradeGroup.melee, UpgradeType.sword, dice=3),
	Upgrade('S-02', 'Parrying Blade', UpgradeGroup.melee, UpgradeType.sword, dice=2, block=1),
	Upgrade('S-03', 'Slingshot', UpgradeGroup.ranged, UpgradeType.bow, dice=2),
	Upgrade('S-04', 'Nova Bolt', UpgradeGroup.ranged, UpgradeType.magic, dice=2)
	)

