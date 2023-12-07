#include <stdio.h>
#include <string.h>
#include <stdint.h>
#include <stdlib.h>
#include <math.h>
#include "esp_event.h"
#include "esp_log.h"
#include "esp_system.h"
#include "esp_wifi.h"
#include "esp_sleep.h"
#include "freertos/FreeRTOS.h"
#include "freertos/event_groups.h"
#include "lwip/err.h"
#include "lwip/sys.h"
#include "nvs_flash.h"
#include "lwip/sockets.h" // Para sockets

#include "packaging.c"
#include "config.c"

// Variables de WiFi
#define WIFI_CONNECTED_BIT BIT0
#define WIFI_FAIL_BIT BIT1
static const char* TAG = "WIFI";
static int s_retry_num = 0;
static EventGroupHandle_t s_wifi_event_group;

#define TCP 1
#define UDP 0
#define FRAG_LEN 1000

uint8_t protocol = 1;

int fragTCP(char* pack, int size, int socket) {
    for (int i = 0; i < size; i+=FRAG_LEN) {
        int frag_size = fmin(FRAG_LEN, size - i);

        int err = send(socket, &(pack[i]), frag_size, 0);
        if (err < 0) {
            ESP_LOGE("SEND FRAG", "Error al enviar paquetitos fragmentados");
            return -1;
        }
    }
    ESP_LOGI("SEND FRAG", "Envio exitoso SIUUU");
    return 1;
}

int fragUDP(char* pack, int size, int socket, struct sockaddr* dest_addr, size_t dest_addr_size) {
    for (int i = 0; i < size; i+=FRAG_LEN) {
        int frag_size = fmin(FRAG_LEN, size - i);
        
        int err = sendto(socket, pack + i, frag_size, 0, dest_addr, dest_addr_size);

        if (err < 0) {
            ESP_LOGE("SEND FRAG", "Error al enviar paquetitos fragmentados");
            return -1;
        }
    }
    ESP_LOGI("SEND FRAG", "Envio exitoso SIUUU");
    return 1;
}

void event_handler(void* arg, esp_event_base_t event_base,
                          int32_t event_id, void* event_data) {
    if (event_base == WIFI_EVENT && event_id == WIFI_EVENT_STA_START) {
        esp_wifi_connect();
    } else if (event_base == WIFI_EVENT &&
               event_id == WIFI_EVENT_STA_DISCONNECTED) {
        if (s_retry_num < 10) {
            esp_wifi_connect();
            s_retry_num++;
            ESP_LOGI(TAG, "retry to connect to the AP");
        } else {
            xEventGroupSetBits(s_wifi_event_group, WIFI_FAIL_BIT);
        }
        ESP_LOGI(TAG, "connect to the AP fail");
    } else if (event_base == IP_EVENT && event_id == IP_EVENT_STA_GOT_IP) {
        ip_event_got_ip_t* event = (ip_event_got_ip_t*)event_data;
        ESP_LOGI(TAG, "got ip:" IPSTR, IP2STR(&event->ip_info.ip));
        s_retry_num = 0;
        xEventGroupSetBits(s_wifi_event_group, WIFI_CONNECTED_BIT);
    }
}

void wifi_init_sta(char* ssid, char* password) {
    s_wifi_event_group = xEventGroupCreate();

    ESP_ERROR_CHECK(esp_netif_init());

    ESP_ERROR_CHECK(esp_event_loop_create_default());
    esp_netif_create_default_wifi_sta();

    wifi_init_config_t cfg = WIFI_INIT_CONFIG_DEFAULT();
    ESP_ERROR_CHECK(esp_wifi_init(&cfg));

    esp_event_handler_instance_t instance_any_id;
    esp_event_handler_instance_t instance_got_ip;
    ESP_ERROR_CHECK(esp_event_handler_instance_register(
        WIFI_EVENT, ESP_EVENT_ANY_ID, &event_handler, NULL, &instance_any_id));
    ESP_ERROR_CHECK(esp_event_handler_instance_register(
        IP_EVENT, IP_EVENT_STA_GOT_IP, &event_handler, NULL, &instance_got_ip));

    wifi_config_t wifi_config;
    memset(&wifi_config, 0, sizeof(wifi_config_t));

    // Set the specific fields
    strcpy((char*)wifi_config.sta.ssid, ssid);
    strcpy((char*)wifi_config.sta.password, password);
    wifi_config.sta.threshold.authmode = WIFI_AUTH_WPA2_PSK;
    wifi_config.sta.pmf_cfg.capable = true;
    wifi_config.sta.pmf_cfg.required = false;
    ESP_ERROR_CHECK(esp_wifi_set_mode(WIFI_MODE_STA));
    ESP_ERROR_CHECK(esp_wifi_set_config(WIFI_IF_STA, &wifi_config));
    ESP_ERROR_CHECK(esp_wifi_start());

    ESP_LOGI(TAG, "wifi_init_sta finished.");

    EventBits_t bits = xEventGroupWaitBits(s_wifi_event_group,
                                           WIFI_CONNECTED_BIT | WIFI_FAIL_BIT,
                                           pdFALSE, pdFALSE, portMAX_DELAY);

    if (bits & WIFI_CONNECTED_BIT) {
        ESP_LOGI(TAG, "connected to ap SSID:%s password:%s", ssid,
                 password);
    } else if (bits & WIFI_FAIL_BIT) {
        ESP_LOGI(TAG, "Failed to connect to SSID:%s, password:%s", ssid,
                 password);
    } else {
        ESP_LOGE(TAG, "UNEXPECTED EVENT");
    }

    ESP_ERROR_CHECK(esp_event_handler_instance_unregister(
        IP_EVENT, IP_EVENT_STA_GOT_IP, instance_got_ip));
    ESP_ERROR_CHECK(esp_event_handler_instance_unregister(
        WIFI_EVENT, ESP_EVENT_ANY_ID, instance_any_id));
    vEventGroupDelete(s_wifi_event_group);
}

void nvs_init() {
    esp_err_t ret = nvs_flash_init();
    if (ret == ESP_ERR_NVS_NO_FREE_PAGES ||
        ret == ESP_ERR_NVS_NEW_VERSION_FOUND) {
        ESP_ERROR_CHECK(nvs_flash_erase());
        ret = nvs_flash_init();
    }
    ESP_ERROR_CHECK(ret);
}


void socket_tcp(struct Configuration *config){
    struct sockaddr_in server_addr;
    server_addr.sin_family = AF_INET;
    server_addr.sin_port = htons(config->Port_TCP);
    inet_pton(AF_INET, config->host_ip_addr, &server_addr.sin_addr.s_addr);

    // Crear un socket
    int sock = socket(AF_INET, SOCK_STREAM, IPPROTO_TCP);
    if (sock < 0) {
        ESP_LOGE(TAG, "Error al crear el socket");
        return;
    }

    // Conectar al servidor
    if (connect(sock, (struct sockaddr *)&server_addr, sizeof(server_addr)) != 0) {
        ESP_LOGE(TAG, "Error al conectar");
        close(sock);
        return;
    }

    // Recibir respuesta
    char rx_buffer[128];
    int rx_len = recv(sock, rx_buffer, sizeof(rx_buffer) - 1, 0);
    if (rx_len < 0) {
        ESP_LOGE(TAG, "Error al recibir datos");
        return;
    }
    ESP_LOGI(TAG, "Datos recibidos: %s", rx_buffer);
    

    uint16_t msg_id = 1;

    while (1) {
        char* msg = create_pack(msg_id, config->tlayer, config->protocol);
        if (msg != NULL) {
            if (protocol == 4) {
                int err = fragTCP(msg, pack_length[config->protocol], sock);
                if (err < 0) {
                    ESP_LOGI(TAG, "Manito se le cayo el paquete");
                    return;
                }
            }

            else {
                send(sock, msg, pack_length[config->protocol], 0);
                ESP_LOGI("WIFI TCP", "Enviando mensaje por protocolo %d", config->protocol);
            }
            // Recibir respuesta
            char rx_buffer[128];
            int rx_len = recv(sock, rx_buffer, sizeof(rx_buffer) - 1, 0);
            if (rx_len < 0) {
                ESP_LOGE(TAG, "Error al recibir datos");
                return;
            }
            ESP_LOGI(TAG, "Datos recibidos: %s", rx_buffer);
            msg_id++;
            free(msg);
            esp_deep_sleep(config->d_time);
        }
    }
    // Cerrar el socket
    close(sock);
}

void socket_udp(struct Configuration *config) {
    struct sockaddr_in server_addr;
    server_addr.sin_family = AF_INET;
    server_addr.sin_port = htons(config->Port_UDP);
    inet_pton(AF_INET, config->host_ip_addr, &server_addr.sin_addr.s_addr);

    // Crear Socket UDP
    int sock = socket(AF_INET, SOCK_DGRAM, IPPROTO_UDP);
    if (sock < 0) {
        ESP_LOGE(TAG, "Error al crear es socket");
    }

    char echo_buffer[128];
    char config_buf[128];
    uint8_t msg_id = 1;

    while (1) {
        recvfrom(sock, config_buf, sizeof(config_buf) - 1, 0, NULL, NULL);
        ESP_LOGI("WIFI UDP", "Config %s", config_buf);
        
        char* msg = create_pack(msg_id, config->tlayer, config->protocol);
        if (msg != NULL) {
            if (config->protocol == 4) {
                int err = fragUDP(msg, pack_length[config->protocol], sock, (struct sockaddr *)&server_addr, sizeof(server_addr));
                if (err < 0) {
                    ESP_LOGI(TAG, "Manito se le cayo el paquete");
                    return;
                }
            }
            else {
                sendto(sock, msg, pack_length[config->protocol], 0, (struct sockaddr *)&server_addr, sizeof(server_addr));
                ESP_LOGI("WIFI UPD", "Enviando mensaje de largo por protocolo %d", config->protocol);

                int echo_recv = recvfrom(sock, echo_buffer, sizeof(echo_buffer) - 1, 0, NULL, NULL);
                if (echo_recv < 0) {
                    ESP_LOGE(TAG, "Error al recibir echo");
                    return;
                }
            }
            ESP_LOGI(TAG, "TAMO JOYA");
            free(msg);
            msg_id++;
            vTaskDelay(2000 / portTICK_PERIOD_MS);
        }
        else {
            ESP_LOGI(TAG, "KE PASO MANITO?");
        }
    }
    close(sock);
}
