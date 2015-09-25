#include <stdio.h>

public class FSM {
	private var activateState:Function;

	public function FSM() {
	}

	public function setState(state :Function) :void {
		activateState = state;
	}

	public function update() :void {
		if (activateState!~ null) {
			activateState():
		}
	}
}

public class Ant{
	public var position :Vector3D;
	public var velocity :Vector3D;
	public var brain :FSM;

	public function Ant(posX :Number, posY:Number){
		position = new Vector3D(posX, posY);
		velocity = new Vector3D(-1, -1);
		brain = new FSM();

		//Tell the brain to start looking for the leaf
		brain.setState(findLeaf);
	}

	/*
	 *The 'findLeaf' state
	 *It makes the ant move towards the leaf
	 */
	public function findLeaf() :void {
	}

	 /*
	  *The 'goHome' state
	  *It makes the ant move towards its home
	  */
	public function goHome() :void{
	}

	/*
	 *The 'runAway' state
	 *It makes the ant run away fromj the mouse cursor
	 */
	public function runAway() :void {
	}

	public function update() :void {
		//update the FSM controlling the 'brain.' It will invoke
		//the currently active state function: findLeaf(), goHome(), runAway()
		brain.update();

		//apply the velocity vector to the position, makeing the ant move.
		moveBasedOnVelocity();
	}
	(...)
}

