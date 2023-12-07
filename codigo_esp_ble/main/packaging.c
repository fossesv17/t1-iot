#include <stdlib.h>
#include <stdint.h>
#include <string.h>
#include "esp_system.h"
#include "esp_mac.h"
#include "esp_log.h"
#include "data_gen.c"

const uint16_t pack_length[] = {2, 6, 16, 44, 48016}; // se suma 1 para considerar el caracter \n

char* header(uint16_t msg_id, uint8_t transport_layer, uint8_t protocol) {
    char* hd = (char*) malloc(12);
    memcpy(hd, &msg_id, 2);
    
    uint8_t* mac = (uint8_t*) malloc(6);
    esp_err_t mac_esp_err = esp_read_mac(mac, ESP_MAC_WIFI_STA);
    if (mac_esp_err == ESP_OK) {
        memcpy(&(hd[2]), mac, 6);
    }
    free(mac);

    uint16_t msg_len = 12 + pack_length[protocol];
    
    memcpy(&(hd[8]), &transport_layer, 1);
    memcpy(&(hd[9]), &protocol, 1);
    memcpy(&(hd[10]), &msg_len, 2);
    return hd;
}

char* protocol0() {
    char* msg = (char*) malloc(pack_length[0]);
    uint8_t batt = batt_sens();
    memcpy(msg, &batt, 1);
    return msg;
}

char* protocol1() {
    char* msg = (char*) malloc(pack_length[1]);
    uint8_t batt = batt_sens();
    uint32_t timestamp = esp_log_early_timestamp();
    memcpy(msg, &batt, 1);
    memcpy(&(msg[1]), &timestamp, 4);
    return msg;
}

char* protocol2() {
    char* msg = (char*) malloc(pack_length[2]);
    uint8_t batt = batt_sens();
    uint32_t timestamp = esp_log_early_timestamp();
    uint8_t temp = thpc_sens_temp();
    uint32_t pres = thpc_sens_pres();
    uint8_t hum = thpc_sens_hum();
    float co = thpc_sens_co();

    memcpy(msg, &batt, 1);
    memcpy(&(msg[1]), &timestamp, 4);
    memcpy(&(msg[5]), &temp, 1);
    memcpy(&(msg[6]), &pres, 4);
    memcpy(&(msg[10]), &hum, 1);
    memcpy(&(msg[11]), &co, 4);

    return msg;
}

char* protocol3() {
    char* msg = (char*) malloc(pack_length[3]);
    uint8_t batt = batt_sens();
    uint32_t timestamp = esp_log_early_timestamp();
    uint8_t temp = thpc_sens_temp();
    uint32_t pres = thpc_sens_pres();
    uint8_t hum = thpc_sens_hum();
    float co = thpc_sens_co();
    uint32_t ampx = accel_kpi_ampx();
    uint32_t ampy = accel_kpi_ampy();
    uint32_t ampz = accel_kpi_ampz();
    uint32_t frecx = accel_kpi_freqx();
    uint32_t frecy = accel_kpi_freqy();
    uint32_t frecz = accel_kpi_freqz();
    uint32_t rms = calc_rms(ampx, ampy, ampz);

    memcpy(msg, &batt, 1);
    memcpy(&(msg[1]), &timestamp, 4);
    memcpy(&(msg[5]), &temp, 1);
    memcpy(&(msg[6]), &pres, 4);
    memcpy(&(msg[10]), &hum, 1);
    memcpy(&(msg[11]), &co, 4);
    memcpy(&(msg[15]), &rms, 4);
    memcpy(&(msg[19]), &ampx, 4);
    memcpy(&(msg[23]), &ampy, 4);
    memcpy(&(msg[27]), &ampz, 4);
    memcpy(&(msg[31]), &frecx, 4);
    memcpy(&(msg[35]), &frecy, 4);
    memcpy(&(msg[39]), &frecz, 4);

    return msg;
}

char* protocol4() {
    char* msg = (char*) malloc(pack_length[4]);
    uint8_t batt = batt_sens();
    uint32_t timestamp = esp_log_early_timestamp();
    uint8_t temp = thpc_sens_temp();
    uint32_t pres = thpc_sens_pres();
    uint8_t hum = thpc_sens_hum();
    float co = thpc_sens_co();

    float* accx = accel_sens_accx();
    float* accy = accel_sens_accy();
    float* accz = accel_sens_accz();
    float* rgyrx = accel_sens_rgyr();
    float* rgyry = accel_sens_rgyr();
    float* rgyrz = accel_sens_rgyr();

    memcpy(msg, &batt, 1);
    memcpy(&(msg[1]), &timestamp, 4);
    memcpy(&(msg[5]), &temp, 1);
    memcpy(&(msg[6]), &pres, 4);
    memcpy(&(msg[10]), &hum, 1);
    memcpy(&(msg[11]), &co, 4);
    memcpy(&(msg[15]), accx, 8000);
    memcpy(&(msg[8015]), accy, 8000);
    memcpy(&(msg[16015]), accz, 8000);
    memcpy(&(msg[24015]), rgyrx, 8000);
    memcpy(&(msg[32015]), rgyry, 8000);
    memcpy(&(msg[40015]), rgyrz, 8000);

    return msg;
}

char* create_pack(uint16_t msg_id, uint8_t transport_layer, uint8_t protocol) {
    char* pack = (char*) malloc(12 + pack_length[protocol]);
    char* hd = header(msg_id, transport_layer, protocol);
    char* data;
    if (protocol == 0) {
        data = protocol0();
    }
    else if (protocol == 1) {
        data = protocol1();
    }
    else if (protocol == 2) {
        data = protocol2();
    }
    else if (protocol == 3) {
        data = protocol3();
    }
    else {
        data = protocol4();
    }

    memcpy(pack, hd, 12);
    memcpy(&(pack[12]), data, pack_length[protocol]);
    
    free(hd);
    free(data);

    return pack;
}
