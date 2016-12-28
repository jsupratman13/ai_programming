#include<stdio.h>
#include<stdlib.h>
#include<time.h>

int main()
{
    double i,imax,n;
    double x,y,pi;
   
    srand((unsigned)time(NULL));
    n=0.0;
    imax=10000000.0;
    int r = 1;
    int d = r*2;
    for(i=0;i<=imax;i++){
        x=rand()/(RAND_MAX+1.0);
        y=rand()/(RAND_MAX+1.0);
        if((x*x+y*y)<=1.0)    n+=1.0;
    }
    pi=n/imax*4.0;
    printf("%f\n",pi);
    return 0;
}
