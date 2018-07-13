obj-m += enable-ccr.o
 
all:
	make -C /lib/modules/$(shell uname -r)/build M=$(PWD) modules
 
clean:
	make -C /lib/modules/$(shell uname -r)/build M=$(PWD) clean

install: 
	sudo insmod enable-ccr.ko