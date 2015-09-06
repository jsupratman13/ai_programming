import sys
from simplegoap import List, Action

def example():
	model = List(['at_armory', 'empty_backpack', 'empty_hands'])
	print 'Initial Model: ',
	model.PrintList()
	
	action = Action('pickup_spear', 
			['at_armory','empty_hands'], 
			['hold_spear'],
			['empty_hands'])
	model.UpdateList(action)
	print 'Updated Model: ',
	model.PrintList()

	action = Action('dropoff_spear', 
			['at_armory', 'hold_spear'], 
			['empty_hands'], 
			['hold_spear'])
	model.UpdateList(action)
	print 'Updated Model: ',
	model.PrintList()


if __name__ == '__main__':
	try:
		example()
	
	except KeyboardInterrupt:
		sys.exit()
