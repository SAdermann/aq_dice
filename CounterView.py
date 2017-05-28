import ui
import console
import collections

def minusTapped(sender):
	count = int(sender.counter.text)
	count = max(0, count - 1)
	sender.counter.text = str(count)
	sender.counter.updateAction(sender.counter)
	
def plusTapped(sender):
	count = int(sender.counter.text)
	count += 1
	sender.counter.text = str(count)
	sender.counter.updateAction(sender.counter)
	
def makeCounterView(v, name, x, y, startValue, updateAction):
	lbl = ui.Label(frame=(x+32, y, 64, 32))
	lbl.border_width = 1
	lbl.flex = ''
	lbl.name = 'labelCount' + name
	lbl.font = ('<System-Bold>', 18)
	lbl.alignment = ui.ALIGN_CENTER
	lbl.text = str(startValue)
	lbl.updateAction = updateAction
	v.add_subview(lbl)
	btn = ui.Button()
	btn.frame = (x, y, 33, 32)
	btn.border_width = 1
	btn.flex = ''
	btn.name = "buttonMinus" + name
	btn.font = ('<System-Bold>', 18)
	btn.title = "-"
	btn.action = minusTapped
	btn.counter = lbl
	v.add_subview(btn)
	btn = ui.Button()
	btn.frame = (x+95, y, 33, 32)
	btn.border_width = 1
	btn.flex = ''
	btn.name = "buttonPlus" + name
	btn.font = ('<System-Bold>', 18)
	btn.title = "+"
	btn.action = plusTapped
	btn.counter = lbl
	v.add_subview(btn)

