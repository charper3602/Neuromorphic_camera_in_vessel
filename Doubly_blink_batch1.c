#include "freertos/FreeRTOS.h"
#include "freertos/task.h"
#include "driver/gpio.h"
#include "driver/ledc.h"  //This is the  Include the LEDC library for PWM


// Define output pins for the LEDs
const int LED1_OUTPUT_PIN = GPIO_NUM_4;  // GPIO 2 for LED1
const int LED2_OUTPUT_PIN = GPIO_NUM_12; // GPIO 22 for LED2


// Define LEDC configuration for each LED
const int LED1_CHANNEL = LEDC_CHANNEL_0;
const int LED2_CHANNEL = LEDC_CHANNEL_1;
const int LEDC_MODE = LEDC_HIGH_SPEED_MODE;
const int LEDC_TIMER = LEDC_TIMER_0;
const int LEDC_FREQUENCY = 5000; // Frequency set to 5 kHz


// Timing constants for LED1
const int BIT_1_DURATION_MS_LED1 = 333;  // LED1 ON for 1 second for bit 1
const int BIT_0_DURATION_MS_LED1 = 666;  // LED1 ON for 2 seconds for bit 0
const int OFF_DURATION_MS_LED1 = 200;     // LED1 OFF for 100ms between bits


// Timing constants for LED2
const int BIT_1_DURATION_MS_LED2 = 100;   // LED2 ON for 500ms for bit 1
const int BIT_0_DURATION_MS_LED2 = 50;  // LED2 ON for 1.5 seconds for bit 0
const int OFF_DURATION_MS_LED2 = 200;     // LED2 OFF for 200ms between bits


// Define the binary patterns to display
const int binaryPatternLED1[] = {1, 1, 0, 1, 0, 1, 0, 0};  // Pattern for LED1
const int binaryPatternLED2[] = {1, 1, 0, 1, 1, 1, 0, 0};  // Pattern for LED2
const int patternLengthLED1 = sizeof(binaryPatternLED1) / sizeof(binaryPatternLED1[0]);
const int patternLengthLED2 = sizeof(binaryPatternLED2) / sizeof(binaryPatternLED2[0]);


void configure_led(int gpio_num, int channel) {
    // Configure LEDC channel
    ledc_channel_config_t ledc_channel = {
        .speed_mode = LEDC_MODE,
        .channel = channel,
        .gpio_num = gpio_num,
        .timer_sel = LEDC_TIMER,
        .duty = 0,  // Start with duty cycle of 0 (LED OFF)
        .hpoint = 0,
    };
    ledc_channel_config(&ledc_channel);
}


void configure_led_timer() {
    // Configure LEDC timer
    ledc_timer_config_t ledc_timer = {
        .speed_mode = LEDC_MODE,
        .timer_num = LEDC_TIMER,
        .duty_resolution = LEDC_TIMER_13_BIT,  // 13-bit duty resolution
        .freq_hz = LEDC_FREQUENCY,
        .clk_cfg = LEDC_AUTO_CLK,
    };
    ledc_timer_config(&ledc_timer);
}


void set_led_state(int channel, int duty, int duration_ms) {
    ledc_set_duty(LEDC_MODE, channel, duty);
    ledc_update_duty(LEDC_MODE, channel);
    vTaskDelay(duration_ms / portTICK_PERIOD_MS);
}


void led_task1(void *pvParameters) {
    while (true) {
        for (int i = 0; i < patternLengthLED1; i++) {
            if (binaryPatternLED1[i] == 1) {
                set_led_state(LED1_CHANNEL, 8191, BIT_1_DURATION_MS_LED1);  // ON for bit 1
            } else {
                set_led_state(LED1_CHANNEL, 8191, BIT_0_DURATION_MS_LED1);  // ON for bit 0
            }
            set_led_state(LED1_CHANNEL, 0, OFF_DURATION_MS_LED1);  // OFF
        }
    }
}


void led_task2(void *pvParameters) {
    while (true) {
        for (int i = 0; i < patternLengthLED2; i++) {
            if (binaryPatternLED2[i] == 1) {
                set_led_state(LED2_CHANNEL, 8191, BIT_1_DURATION_MS_LED2);  // ON for bit 1
            } else {
                set_led_state(LED2_CHANNEL, 8191, BIT_0_DURATION_MS_LED2);  // ON for bit 0
            }
            set_led_state(LED2_CHANNEL, 0, OFF_DURATION_MS_LED2);  // OFF
        }
    }
}


void app_main(void) {
    // Configure LEDC timer
    configure_led_timer();


    // Configure LEDs
    configure_led(LED1_OUTPUT_PIN, LED1_CHANNEL);
    configure_led(LED2_OUTPUT_PIN, LED2_CHANNEL);


    // Create FreeRTOS tasks for the two LEDs
    xTaskCreate(led_task1, "LED Task 1", 2048, NULL, 1, NULL);
    xTaskCreate(led_task2, "LED Task 2", 2048, NULL, 1, NULL);
}
