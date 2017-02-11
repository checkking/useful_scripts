/**
 * @file mylc.c
 * @desc a simple fast line counter program
 * @author checkking <checkking@foxmail.com>
 */
#include <stdio.h>
#include <stdlib.h>
#include <sys/stat.h>
#include <sys/types.h>
#include <fcntl.h>
#include <unistd.h>
#include <sys/stat.h>
#include <string.h>

#define SMALL_FILE_MAX_SIZE 4096
#define DEFAULT_LINE_NUM 100

void show_usage(char **argv) {
    fprintf(stdout, "Usage: %s FILE\n", argv[0]);
}

int small_file_line_counter(int fd, size_t* lines) {
    char buffer[SMALL_FILE_MAX_SIZE] = {0};
    char* buf = buffer;
    *lines = 0;
    int ret = 0;
    int i = 0;
    while ((ret = read(fd, (void *)buf, SMALL_FILE_MAX_SIZE)) > 0) {
        i = 0;
        while (i != ret) {
            if (*(buf + i) == '\n') {
                *lines = *lines + 1;
            }
            ++i;
        }
        buf = buffer;
    }

    return ret;
}

int large_file_line_counter(int fd, size_t total_size, size_t* lines) {
   int ret = 0;
   char buffer[SMALL_FILE_MAX_SIZE] = {0};
   char* buf = buffer;
   int i = 0;
   int cnt = 0;
   size_t size = 0;
   size_t line_size = 0;
   double size_of_each_line = 0.0;
   while (cnt < DEFAULT_LINE_NUM) {
       ret = read(fd, buf, SMALL_FILE_MAX_SIZE);
       if (ret == 0) {
           break;
       }
       if (ret == -1) {
           return -1;
       }
       i = 0;
       while (i != ret) {
           line_size += 1;
           if (*(buf + i) == '\n') {
               size += line_size;
               line_size = 0;
               cnt += 1;
               if (cnt == DEFAULT_LINE_NUM) {
                   break;
               }
           }
           ++i;
       }
       memset((void *)buffer, 0, SMALL_FILE_MAX_SIZE);
       buf = buffer;
   }
   size_of_each_line = (double)size / cnt;
   *lines = (int)(total_size / size_of_each_line);
   return 0;
}

int main (int argc, char **argv)
{
    int fd = -1;
    struct stat st;
    size_t line_count = 0;
    if (argc != 2) {
        show_usage(argv);
        exit(1);
    }
    if (stat(argv[1], &st) != 0) {
        fprintf(stderr, "Cannot get state of file: %s\n", argv[1]);
        exit(1);
    }

    fd = open(argv[1], O_RDONLY);
    if (fd == -1) {
        fprintf(stderr, "Cannot open file: %s\n", argv[1]);
        exit(1);
    }
    if (st.st_size < SMALL_FILE_MAX_SIZE) {
        if (small_file_line_counter(fd, &line_count) == -1) {
            fprintf(stderr, "Get line count of file: %s failed!\n", argv[1]);
            exit(1);
        }
    } else {
        if(large_file_line_counter(fd, st.st_size, &line_count) == -1) {
            fprintf(stderr, "Get line count of file: %s failed!\n", argv[1]);
            exit(1);
        }
    }
    close(fd);

    fprintf(stdout, "%s\t%d\n", argv[1], (int)line_count);

    return 0;
}
