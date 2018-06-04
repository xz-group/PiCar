#include <stdio.h>
#include <stdlib.h>
#include <errno.h>
#include <time.h>
#include <sys/time.h>
#include <unistd.h>
#include "LSM9DS1_Types.h"
#include "LSM9DS1.h"

int main(int argc, char *argv[]) {
    LSM9DS1 imu(IMU_MODE_I2C, 0x6b, 0x1e);
    imu.begin();
    if (!imu.begin()) {
        fprintf(stderr, "Failed to communicate with LSM9DS1.\n");
        exit(EXIT_FAILURE);
    }
    imu.calibrate();

    for (;;) {
        while (!imu.gyroAvailable()) ;
        imu.readGyro();
        while(!imu.accelAvailable()) ;
        imu.readAccel();
        while(!imu.magAvailable()) ;
        imu.readMag();

        printf("Gyro: %f, %f, %f [deg/s]\n", imu.calcGyro(imu.gx), imu.calcGyro(imu.gy), imu.calcGyro(imu.gz));
        printf("Accel: %f, %f, %f [Gs]\n", imu.calcAccel(imu.ax), imu.calcAccel(imu.ay), imu.calcAccel(imu.az));
        printf("Mag: %f, %f, %f [gauss]\n", imu.calcMag(imu.mx), imu.calcMag(imu.my), imu.calcMag(imu.mz));
        sleep(1.0);
    }

    exit(EXIT_SUCCESS);
}
