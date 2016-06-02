//behavior tree that models the behavior of a person whose goal is to open door
/*
       Root
         |
	 |
      Selector(OR)
      /      \
     /        \
    /          \
  Is door       \
  open?          \
               Sequence(AND)
	         /   \
		/     \
	       /       \
	   Approach    Open Door
	   Door
*/

#include <iostream>
#include <list>


//TEMPLATE

class Node {  // This class represents each node in the behaviour tree.
	public:
		virtual bool run() = 0;
};

class CompositeNode : public Node {  //  This type of Node follows the Composite Pattern, containing a list of other Nodes.
	private:
		std::list<Node*> children;
	public:
		const std::list<Node*>& getChildren() const {return children;}
		void addChild (Node* child) {children.emplace_back(child);}
};

class Selector : public CompositeNode {
	public:
		virtual bool run() override {
			for (Node* child : getChildren()) {  // The generic Selector implementation
				if (child->run())  // If one child succeeds, the entire operation run() succeeds.  Failure only results if all children fail.
					return true;
			}
			return false;  // All children failed so the entire run() operation fails.
		}
};

class Sequence : public CompositeNode {
	public:
		virtual bool run() override {
			for (Node* child : getChildren()) {  // The generic Sequence implementation.
				if (!child->run())  // If one child fails, then enter operation run() fails.  Success only results if all children succeed.
					return false;
			}
			return true;  // All children suceeded, so the entire run() operation succeeds.
		}
};

struct DoorStatus {
	bool doorIsOpen;
	int distanceToDoor;
};

class CheckIfDoorIsOpenTask : public Node {  // Each task will be a class (derived from Node of course).
	private:
		DoorStatus* status;
	public:
		CheckIfDoorIsOpenTask (DoorStatus* status) : status(status) {}
		virtual bool run() override {
			if (status->doorIsOpen == true)
				std::cout << "The person sees that the door is open." << std::endl;  // will return true
			else
				std::cout << "The person sees that the door is closed." << std::endl;  // will return false
			return status->doorIsOpen;
		}
};

class ApproachDoorTask : public Node {
	private:
		DoorStatus* status;
		bool obstructed;
	public:
		ApproachDoorTask (DoorStatus* status, bool obstructed) : status(status), obstructed(obstructed) {}
		virtual bool run() override {
			if (obstructed)
				return false;
			if (status->distanceToDoor > 0) {
				std::cout << "The person approaches the door." << std::endl;
				status->distanceToDoor--;  // thus run() is not a const function
				if (status->distanceToDoor > 1)
					std::cout << "The person is now " << status->distanceToDoor << " meters from the door." << std::endl;
				else if (status->distanceToDoor == 1)
					std::cout << "The person is now only one meter away from the door." << std::endl;
				else
					std::cout << "The person is at the door." << std::endl;
			}
			return true;
		}
};

class OpenDoorTask : public Node {
	private:
		DoorStatus* status;
	public:
		OpenDoorTask (DoorStatus* status) : status(status) {}
		virtual bool run() override {
			if (status->distanceToDoor > 0) {
				std::cout << "The person is still too far away from the door.  He cannot open the door." << std::endl;
				return false;	
			}
			status->doorIsOpen = true;  // run() not const because of this too
			std::cout << "The person opens the door." << std::endl;
			return true;
		}
};

int main() {
	Sequence *root = new Sequence, *sequence1 = new Sequence;  // Note that root can be either a Sequence or a Selector, since it has only one child.
	Selector* selector1 = new Selector;  // In general there will be several nodes that are Sequence or Selector, so they should be suffixed by an integer to distinguish between them.
	DoorStatus* doorStatus = new DoorStatus {false, 5};  // The door is initially closed and 5 meters away.
	CheckIfDoorIsOpenTask* checkOpen = new CheckIfDoorIsOpenTask (doorStatus);
	ApproachDoorTask* approach = new ApproachDoorTask (doorStatus, false);
	OpenDoorTask* open = new OpenDoorTask (doorStatus);
	
	root->addChild (selector1);
	
	selector1->addChild (checkOpen);
	selector1->addChild (sequence1);
	
	sequence1->addChild (approach);
	sequence1->addChild (open);
	
	while (!root->run())  // If the operation starting from the root fails, keep trying until it succeeds.
		std::cout << "--------------------" << std::endl;
	std::cout << std::endl << "Operation complete.  Behaviour tree exited." << std::endl;
	std::cin.get();
}


