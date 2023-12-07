#include <stdlib.h>
#include <string.h>
#include <stdio.h>

struct Configuration {
    uint8_t tlayer; // UDP = 0; TCP = 1; BLEC = 2; BLED = 3;
    uint8_t protocol; // WIFI (0-4); BLE (0-3);
    int32_t Port_TCP;
    int32_t Port_UDP;
    float gyro_samp_rate;
    float gyro_sens;
    float acc_sens;
    float acc_samp_rate;
    uint32_t d_time;
    char host_ip_addr[40];
    char wifi_ssid[20];
    char wifi_pw[20];
};

void initConfig(struct Configuration *config) {
    if (config != NULL) {
        config->tlayer = 0;
        config->protocol = 0;
        snprintf(config->host_ip_addr, sizeof(config->host_ip_addr), "192.168.4.1");
        snprintf(config->wifi_ssid, sizeof(config->wifi_ssid), "pdfteamWifi");
        snprintf(config->wifi_pw, sizeof(config->wifi_pw), "teamPDF3");
        config->Port_TCP = 1234;
        config->Port_UDP = 1234;
        config->gyro_samp_rate = 0.5;
        config->gyro_sens = 50;
        config->acc_sens = 50;
        config->acc_samp_rate = 0.5;
        config->d_time = 20;
    }
}

void modifyConf(struct Configuration *config, 
                uint8_t tlayer, 
                uint8_t protocol,
                float gyro_samp_rate,
                float gyro_sens,
                float acc_sens,
                float acc_samp_rate,
                uint32_t d_time) {    
    
    config->tlayer = tlayer;
    config->protocol = protocol; 
    config->gyro_samp_rate = gyro_samp_rate;
    config->gyro_sens = gyro_sens;
    config->acc_sens = acc_sens;
    config->acc_samp_rate = acc_samp_rate;
    config->d_time = d_time;
}

void changeProtocolAndTransportLayer(struct Configuration *config, uint8_t tlayer, uint8_t protocol) {
    config->tlayer = tlayer;
    config->protocol = protocol;
}

void changeProtocol(struct Configuration *config, uint8_t protocol) {
    config->protocol = protocol;
}

void changeTransportLayer(struct Configuration *config, uint8_t tlayer) {
    config->tlayer = tlayer;
}