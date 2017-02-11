all: mylc
LIBS = -lpthread
mylc: mylc.c
	gcc -g -W -Wall $(LIBS) -o $@ $<

clean:
	rm mylc core*
