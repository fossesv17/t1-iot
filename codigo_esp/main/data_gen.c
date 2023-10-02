#include <stdio.h>
#include <string.h>
#include <stdint.h>
#include <stdlib.h>
#include <math.h>

// Definicion de rangos de datos

// Acceloremeter_Kpi

#define MIN_AMPX 0.0059f
#define MAX_AMPX 0.12f
#define MIN_FREQX 29.0f
#define MAX_FREQX 31.0f
#define MIN_AMPY 0.0041f
#define MAX_AMPY 0.11f
#define MIN_FREQY 59.0f
#define MAX_FREQY 61.0f
#define MIN_AMPZ 0.008f
#define MAX_AMPZ 0.15f
#define MIN_FREQZ 89.0f
#define MAX_FREQZ 91.0f

// Acceloremeter Sensor

#define MIN_ACCX -16.0f
#define MAX_ACCX 16.0f
#define MIN_ACCY -16.0f
#define MAX_ACCY 16.0f
#define MIN_ACCZ -16.0f
#define MAX_ACCZ 16.0f
#define MIN_RGYR -1000.0f
#define MAX_RGYR 1000.0f

// THPC Sensor

#define MIN_TEMP 5
#define MAX_TEMP 30
#define MIN_HUM 30
#define MAX_HUM 80
#define MIN_PRES 1000
#define MAX_PRES 1200
#define MIN_CO 30.0f
#define MAX_CO 200.0f

// Batt Sensor

#define MIN_BATT 1
#define MAX_BATT 100

// Other Constant

#define ACC_ARR_SIZE 2000

int rand_int(int min, int max) {
    return min + rand() % (max - min + 1);
}

float rand_float(float min, float max) {
    return min + (float)rand() / RAND_MAX * (max - min); 
}

float* gen_rand_array(int size, float min, float max) {
    float* arr = (float*) malloc(size * sizeof(float));
    for (int i = 0; i < size; i++) {
        arr[i] = rand_float(min, max);
    }
    return arr;
}

float accel_kpi_ampx(){
    return rand_float(MIN_AMPX, MAX_AMPX);
}

float accel_kpi_ampy(){
    return rand_float(MIN_AMPY, MAX_AMPY);
}

float accel_kpi_ampz(){
    return rand_float(MIN_AMPZ, MAX_AMPZ);
}

float accel_kpi_freqx() {
    return rand_float(MIN_FREQX, MAX_FREQX);
}

float accel_kpi_freqy() {
    return rand_float(MIN_FREQY, MAX_FREQY);
}

float accel_kpi_freqz() {
    return rand_float(MIN_FREQZ, MAX_FREQZ);
}

float calc_rms(float ampx, float ampy, float ampz) {
    return sqrtf(ampx*ampx + ampy*ampy + ampz*ampz);
}

float* accel_sens_accx() {
    return gen_rand_array(ACC_ARR_SIZE, MIN_ACCX, MAX_ACCX);
}

float* accel_sens_accy() {
    return gen_rand_array(ACC_ARR_SIZE, MIN_ACCY, MAX_ACCY);
}

float* accel_sens_accz() {
    return gen_rand_array(ACC_ARR_SIZE, MIN_ACCZ, MAX_ACCZ);
}

float* accel_sens_rgyr() {
    return gen_rand_array(ACC_ARR_SIZE, MIN_RGYR, MAX_RGYR);
}

int thpc_sens_temp() {
    return rand_int(MIN_TEMP, MAX_TEMP);
}

int thpc_sens_hum() {
    return rand_int(MIN_HUM, MAX_HUM);
}

int thpc_sens_pres() {
    return rand_int(MIN_PRES, MAX_PRES);
}

float thpc_sens_co() {
    return rand_int(MIN_CO, MAX_CO);
}

uint8_t batt_sens() {
    return (uint8_t) (MIN_BATT + rand() % MAX_BATT);
}