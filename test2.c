#define _XOPEN_SOURCE 500
#include <stdio.h>
#include <time.h>

extern int getdate_err;



int main(void)
{

    char const *time_str = "2011-07-20 17:30:18";
    struct tm *time_tm; 
    time_tm = getdate(time_str);
    printf("%p\n",time_tm);
    getchar();
    time_t t = mktime(time_tm);

    printf("str: %s and time: %s", time_str, ctime(&t));
    return 0;




//
//    time_t t;
//    struct tm *time_tm = getdate("2015-01-01 07:00:00");
//    printf("%p\n",time_tm);
//    getchar();
//    printf("%d\n",getdate_err);
//    if (!time_tm)
//        exit(3);
//    t=mktime(time_tm);
//
//    //printf("%s\n",ctime(&t));
//    return 0;


//int y,m1,d,h,m,s;
//sscanf("2015-09-15T20:07:02", "%d-%d-%dT%d:%d:%d",&y,&m1,&d,&h,&m,&s);
//printf("&&&&&%d %d %d %d %d %d\n",y,m1,d,h,m,s);
//struct tm p;
//p.tm_sec = s;
//p.tm_min = m;
//p.tm_hour = h;
//p.tm_year = y-1900;
//p.tm_mon = m1-1;
//p.tm_mday = d;
//time_t timep;
//timep = mktime(&p);
//printf("time=%lld\n",timep);


}
