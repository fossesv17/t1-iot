#include <stdlib.h>
#include <stdint.h>
#include <string.h>
#include "esp_system.h"
#include "esp_mac.h"
#include "esp_log.h"
#include "data_gen.c"
#include <math.h>

#define FRAG_LEN 1000
const uint16_t pack_length[] = {1, 5, 15, 43, 48015}; // se suma 1 para considerar el caracter \n

struct header {
    uint16_t pid;
    uint8_t mac[6];
    uint8_t tl;
    uint8_t protocol;
    uint16_t msglen;
};

struct proto0 {
    // HEADER
    struct header hd;
    // DATA
    uint8_t batt_sens;
};

struct proto1 {
    // HEADER
    struct header hd;
    //DATA
    uint8_t batt_sens;
    uint32_t timestamp;
};

struct proto2 {
      // HEADER
    struct header hd;
    //DATA
    uint8_t batt_sens;
    uint32_t timestamp;
    uint8_t temp;
    uint32_t pres;
    uint8_t hum;
    float co;
};

struct proto3 {
      // HEADER
    struct header hd;
    //DATA
    uint8_t batt_sens;
    uint32_t timestamp;
    uint8_t temp;
    uint32_t pres;
    uint8_t hum;
    float co;
    uint32_t ampx; 
    uint32_t ampy;
    uint32_t ampz; 
    uint32_t frecx;
    uint32_t frecy;
    uint32_t frecz;
    uint32_t rms;
};

struct proto4 {
      // HEADER
    struct header hd;
    //DATA
    uint8_t batt_sens;
    uint32_t timestamp;
    uint8_t temp;
    uint32_t pres;
    uint8_t hum;
    float co;
    float accx[2000];
    float accy[2000];
    float accz[2000];
    float rgyrx[2000];
    float rgyry[2000];
    float rgyrz[2000]; 
};

void initHeader(struct header *pHd, uint16_t msg_id, uint8_t *mac, uint8_t transport_layer, uint8_t protocol) {
    if (pHd != NULL) {
        pHd->pid = msg_id;
        for(int i=0; i < 6; i++) {
                pHd->mac[i] = mac[i];
        }
        pHd->tl = transport_layer;
        pHd->protocol = protocol;
        pHd->msglen = 12 + pack_length[protocol];
    }
}

void protocol0(struct proto0 *pPack, uint16_t msg_id, uint8_t *mac, uint8_t transport_layer) {
    struct header hd;
    initHeader(&hd, msg_id, mac, transport_layer, 0);
    pPack->hd = hd;
    pPack->batt_sens = batt_sens();
}

void protocol1(struct proto1 *pPack, uint16_t msg_id, uint8_t *mac, uint8_t transport_layer) {
    struct header hd;
    initHeader(&hd, msg_id, mac, transport_layer, 1);
    pPack->hd = hd;
    pPack->batt_sens = batt_sens();
    pPack->timestamp = esp_log_early_timestamp();
}

void protocol2(struct proto2 *pPack, uint16_t msg_id, uint8_t *mac, uint8_t transport_layer) {
    struct header hd;
    initHeader(&hd, msg_id, mac, transport_layer, 2);
    pPack->hd = hd;
    pPack->batt_sens = batt_sens();
    pPack->timestamp = esp_log_early_timestamp();
    pPack->temp = thpc_sens_temp();
    pPack->pres = thpc_sens_pres();
    pPack->hum = thpc_sens_hum();
    pPack->co = thpc_sens_co();
}

void protocol3(struct proto3 *pPack, uint16_t msg_id, uint8_t *mac, uint8_t transport_layer) {
    struct header hd;
    initHeader(&hd, msg_id, mac, transport_layer, 3);
    pPack->hd = hd;
    pPack->batt_sens = batt_sens();
    pPack->timestamp = esp_log_early_timestamp();
    pPack->temp = thpc_sens_temp();
    pPack->pres = thpc_sens_pres();
    pPack->hum = thpc_sens_hum();
    pPack->co = thpc_sens_co();
    pPack->ampx = accel_kpi_ampx();
    pPack->ampy = accel_kpi_ampy();
    pPack->ampz = accel_kpi_ampz();
    pPack->frecx = accel_kpi_freqx();
    pPack->frecy = accel_kpi_freqy();
    pPack->frecz = accel_kpi_freqz();
    pPack->rms = calc_rms(pPack->ampx, pPack->ampy, pPack->ampz);
}

void protocol4(struct proto4 *pPack, uint16_t msg_id, uint8_t *mac, uint8_t transport_layer) {
    struct header hd;
    initHeader(&hd, msg_id, mac, transport_layer, 4);
    pPack->hd = hd;
    pPack->batt_sens = batt_sens();
    pPack->timestamp = esp_log_early_timestamp();
    pPack->temp = thpc_sens_temp();
    pPack->pres = thpc_sens_pres();
    pPack->hum = thpc_sens_hum();
    pPack->co = thpc_sens_co();
    memcpy(pPack->accx, accel_sens_accx(), 2000);
    memcpy(pPack->accy, accel_sens_accy(), 2000);
    memcpy(pPack->accz, accel_sens_accz(), 2000);
    memcpy(pPack->rgyrx, accel_sens_rgyr(), 2000);
    memcpy(pPack->rgyry, accel_sens_rgyr(), 2000);  
    memcpy(pPack->rgyrz, accel_sens_rgyr(), 2000);
}

char* create_packet(uint16_t msg_id, uint8_t *mac, uint8_t transport_layer, uint8_t protocol) {
    struct proto0 p0;
    struct proto1 p1;
    struct proto2 p2;
    struct proto3 p3;
    struct proto4 p4;
    char* buf;
    if (protocol == 0) {
        size_t bufSize = sizeof(struct proto0);
        buf = (char*)malloc(bufSize);
        protocol0(&p0, msg_id, mac, transport_layer);
        memcpy(buf, &p0, bufSize);
    }
    else if (protocol == 1) {
        size_t bufSize = sizeof(struct proto0);
        buf = (char*)malloc(bufSize);
        protocol1(&p1, msg_id, mac, transport_layer);
        memcpy(buf, &p1, bufSize);
    }
    else if (protocol == 2) {
        size_t bufSize = sizeof(struct proto0);
        buf = (char*)malloc(bufSize);
        protocol2(&p2, msg_id, mac, transport_layer);
        memcpy(buf, &p2, bufSize);
    }
    else if (protocol == 3) {
        size_t bufSize = sizeof(struct proto0);
        buf = (char*)malloc(bufSize);
        protocol3(&p3, msg_id, mac, transport_layer);
        memcpy(buf, &p3, bufSize);
    }
    else {
        size_t bufSize = sizeof(struct proto0);
        buf = (char*)malloc(bufSize);
        protocol4(&p4, msg_id, mac, transport_layer);
        memcpy(buf, &p4, bufSize);
    }
    return buf;
}