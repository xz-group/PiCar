LIB = lib/
SRC = src/
INCLUDE = include/
ccflags-y = -O2 -g
LIBINSTALLDIR = /usr/local/lib
INCLUDEINSTALLDIR = /usr/local/include
obj-m += $(SRC)enable-ccr.o

.PHONY: all
all: $(LIB)liblsm9ds1.a $(LIB)liblsm9ds1.so $(LIB)liblsm9ds1cwrapper.so $(LIB)counter.so


LSM9DS1.o: $(SRC)LSM9DS1.cpp
	g++ -I$(INCLUDE) -Wall -O2 -fPIC -c -lwiringPi $(SRC)LSM9DS1.cpp -o LSM9DS1.o


# static library
$(LIB)liblsm9ds1.a: LSM9DS1.o
	mkdir -p $(LIB)
	ar rcs $(LIB)liblsm9ds1.a LSM9DS1.o

# dynamic library
$(LIB)liblsm9ds1.so: LSM9DS1.o
	mkdir -p $(LIB)
	g++ -I$(INCLUDE) -Wall -O2 -fPIC -fexceptions $(SRC)LSM9DS1.cpp -lwiringPi -shared -o $(LIB)liblsm9ds1.so


LSM9DS1_c_wrapper.o: $(SRC)LSM9DS1_c_wrapper.cpp
	$g++ -I$(INCLUDE) -Wall -O2 -fPIC -c -lwiringPi $(SRC)LSM9DS1_c_wrapper.cpp -o LSM9DS1_c_wrapper.o


$(LIB)liblsm9ds1cwrapper.so: LSM9DS1_c_wrapper.o LSM9DS1.o
	mkdir -p $(LIB)
	g++ -I$(INCLUDE) -Wall -O2 -shared -lwiringPi LSM9DS1.o LSM9DS1_c_wrapper.o -o $(LIB)liblsm9ds1cwrapper.so

counter.o: $(SRC)counter.c enable-ccr.ko
	gcc -Wall -O2 -fPIC -c $(SRC)counter.c -o counter.o


$(LIB)counter.so:  counter.o
	mkdir -p $(LIB)
	gcc -Wall -O2 -shared  counter.o -o $(LIB)counter.so

enable-ccr.ko: $(SRC)enable-ccr.c
	make -C /lib/modules/$(shell uname -r)/build M=$(PWD) modules


clean:
	rm -f *.o $(LIB)liblsm9ds1.a $(LIB)liblsm9ds1.so


install:
	sudo install -m 644 $(LIB)liblsm9ds1.a $(LIBINSTALLDIR)
	sudo install $(LIB)liblsm9ds1.so $(LIBINSTALLDIR)
	sudo cp include/* $(INCLUDEINSTALLDIR)
	sudo ldconfig
	sudo insmod $(SRC)enable-ccr.ko