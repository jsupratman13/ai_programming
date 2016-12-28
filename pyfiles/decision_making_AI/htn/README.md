#Hierarchial Task Network

Hierarchical Task Network Planner (HTN Planner) is a non reactive-type agent architecture planner.
Compose of Tasks which can be decomposed into smaller primative task.

##Pros
* Easy to manage
* Easy to maintain
* Designer have control

##Cons
* Loss of uniquness

##Comparing to GOAP:
* goap can only plan primative while HTN can plan from abstract to primative
* doesnt use goals so therefore moves forward in planning
* comparing to goap, loses its ability to plan the unexpected

##Pseudocode
```
working_word_state = current_world_state.copy()
tasktoprocess.push(ROOTTASK)
while tasktoprocess.not_empty:
	CURRENTTASK = tasktoprocess.pop()
	if CURRENTTASK == compoundttask:
		satisfiedmethod = currenttask.findstaisfiedmethod(working_current_state)
		if statisfiedmethod:
			recorddecomposetask(currenttask, final plan, decomphistory)
			taskproceess.push(satsifeidmethod.subtask)
		else:
			restoretolastdecomptask
	elif CURRENTTASK == primitive task:
		if conditionmet(currenttask):
			apply_update_to_worldstate
			FinalPlan.push(currenttask)
		else:	
			retoretolastdecomptask
```
