//exercise2: using opengl

#include <windows.h>
#include <GL/glut.h>

void display(){
	glClear(GL_COLOR_BUFFER_BIT);
	glBegin(GL_LINE_LOOP);
	glVertex2d(-0.9, -0.9);
	glVertex2d(0.9, -0.9);
	glVertex2d(0, 0.9);
	glEnd();
	glFlush();
}

void init(){
	glClearColor(0.0, 1.0, 0.0, 1.0);
}

int main(int argc, char *argv[]){
	glutInit(&argc, argv);
	glutInitDisplayMode(GLUT_RGBA);
	glutCreateWindow(argv[0]);
	glutDisplayFunc(display);
	init();
	glutMainLoop();
	return 0;
}

