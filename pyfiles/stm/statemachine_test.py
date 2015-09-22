from statemachine import StateMachine

positive_adjectives = ['great', 'super', 'fun', 'entertaining', 'easy']
negative_adjectives = ['boring', 'difficult', 'ugly', 'bad']

def start_transitions(txt):
	splitted_txt = txt.split(None, 1)
	word, txt = splitted_txt if len(splitted_txt) > 1 else (txt, '')
	if word == 'Python':
		newState = 'Python_state'
	else:
		newState = 'error_state'
	return (newState, txt)

def python_state_transitions(txt):
	splitted_txt = txt.split(None, 1)
	word, txt = splitted_txt if len(splitted_txt) > 1 else (txt, '')
	if word == 'is':
		newState = 'is_state'
	else:
		newState = 'error_state'
	return (newState, txt)

def is_state_transitions(txt):
	splitted_txt = txt.split(None, 1)
	word, txt = splitted_txt if len(splitted_txt) > 1 else (txt, '')
	if word == 'not':
		newState = 'not_state'
	elif word in positive_adjectives:
		newState = 'pos_state'
	elif word in negative_adjectives:
		newState = 'neg_state'
	else:
		newState ='error_state'
	return (newState, txt)

def not_state_transitions(txt):
	splitted_txt = txt.split(None,1)
	word, txt = splitted_txt if len(splitted_txt) > 1 else (txt,'')
	if word in positive_adjectives:
		newState = 'neg_state'
	elif word in negative_adjectives:
		newState = 'pos_state'
	else:
		newState = 'error_state'
	return (newState, txt)

def neg_state(txt):
	print 'Hello'
	return ('neg_state', '')

if __name__ == '__main__':
	m = StateMachine()
	m.add_state('Start', start_transitions)
	m.add_state('Python_state', python_state_transitions)
	m.add_state('is_state', is_state_transitions)
	m.add_state('not_state', not_state_transitions)
	m.add_state('neg_state', None, end_state = 1)
	m.add_state('pos_state', None, end_state = 1)
	m.add_state('error_state', None, end_state=1)
	m.set_start('Start')
	m.run('Python is great')
	m.run('Python is difficult')
#	m.run('perl is ugly')

