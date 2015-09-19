import sys
from simplegoap import World, Action_List

def example():
	model = World(['at_armory', 'empty_backpack', 'empty_hands'])
	print 'Initial Model: ',
	model.PrintList()
	
	action = Action_List('pickup_spear', 
			['at_armory','empty_hands'], 
			['hold_spear'],
			['empty_hands'])
	model.UpdateList(action)
	print 'Updated Model: ',
	model.PrintList()

	action = Action_List('dropoff_spear', 
			['at_armory', 'hold_spear'], 
			['empty_hands'], 
			['hold_spear'])
	model.UpdateList(action)
	print 'Updated Model: ',
	model.PrintList()
	action.PrintList()


if __name__ == '__main__':
	try:
		example()
	
	except KeyboardInterrupt:
		sys.exit()
