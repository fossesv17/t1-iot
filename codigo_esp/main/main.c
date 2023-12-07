#include "wifi.c"


void app_main(void){
    struct Configuration conf;
    initConfig(&conf);

    switch (conf.tlayer) {
        case 0: //UDP
            ESP_LOGI("WIFI", "Conectando a %s", conf.wifi_ssid);    
            nvs_init();
            wifi_init_sta(conf.wifi_ssid, conf.wifi_pw);
            ESP_LOGI(TAG,"Conectado a WiFi!\n");
            socket_udp(&conf);
            break;
        case 1: // TCP
            ESP_LOGI("WIFI", "Conectando a %s", conf.wifi_ssid);    
            nvs_init();
            wifi_init_sta(conf.wifi_ssid, conf.wifi_pw);
            ESP_LOGI(TAG,"Conectado a WiFi!\n");
            socket_tcp(&conf);
            break;
        case 2: // BLEC
            ESP_LOGI("BLE", "Continuo --- En Construcción");
            changeTransportLayer(&conf, 0);
            break;
        case 3: // BLED
            ESP_LOGI("BLE", "Discontinuo --- En Construcción");
            changeTransportLayer(&conf, 0);
            break;
        default:
            ESP_LOGI("ERROR", "Se paso manito");
            break;
    }
}
