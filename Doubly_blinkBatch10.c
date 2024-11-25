//Here below are the respective includes to allow the code to build and later on flash to the ESP32(especially the driver for PWM-Module aspect)

#include "freertos/FreeRTOS.h"
#include "freertos/task.h"
#include "driver/gpio.h"
#include "driver/ledc.h"  



//Here below are the corresponding connecting pins that are with respect to the connections of the ESP32
const int LED1_OUTPUT_PIN = GPIO_NUM_4;  // GPIO 2 for LED1 Designation(top)
const int LED2_OUTPUT_PIN = GPIO_NUM_12; // GPIO 12 for LED2 Designation(bottom)


//We will utilize the LEDC for each of the gpio pin LEDs so that we can use PWM to appropiately blink the leds without disrupting the watchdog timer
const int LED1_CHANNEL = LEDC_CHANNEL_0;
const int LED2_CHANNEL = LEDC_CHANNEL_1;
const int LEDC_MODE = LEDC_HIGH_SPEED_MODE;//Highspeed for better performance
const int LEDC_TIMER = LEDC_TIMER_0;
const int LEDC_FREQUENCY = 5000; // Frequency set to 5 kHz(for smooth LED transisitions)


//Here below are the timing constants for both the top and bottom LED(ie led1 and led2)
const int BIT_1_DURATION_MS_LED1 = 500; //bit 1 duration for 500ms 
const int BIT_0_DURATION_MS_LED1 = 1000;  // bit 0 dduration for 1000ms
const int OFF_DURATION_MS_LED1 = 500;     //offtime transition between leds


// Timing constants for LED2
const int BIT_1_DURATION_MS_LED2 = 500;   //bit 1 duration for 500ms
const int BIT_0_DURATION_MS_LED2 = 1000; // bit 0 dduration for 1000ms
const int OFF_DURATION_MS_LED2 = 500;     //offtime transition between leds


//Here below is the binary output pattern for the corresponding LEDs
//Here below is for batch1 set pattern
const int binaryPatternLED1[] = {1, 1, 0, 1, 1, 1, 0, 0}; // Pattern for LED1
const int binaryPatternLED2[] = {1, 1, 0, 1, 1, 0, 0, 0}; // Pattern for LED2



const int patternLengthLED1 = sizeof(binaryPatternLED1) / sizeof(binaryPatternLED1[0]);
// sizeof(binaryPatternLED1)` gives the total size (in bytes) of the array
// sizeof(binaryPatternLED1[0])` gives the size (in bytes) of one element in the array
// Dividing these gives the total number of elements in the array (pattern length)

const int patternLengthLED2 = sizeof(binaryPatternLED2) / sizeof(binaryPatternLED2[0]);
// Calculate the number of elements in the binary pattern array


void configure_led(int gpio_num, int channel) {
    // Configure LEDC channel
    ledc_channel_config_t ledc_channel = {
        .speed_mode = LEDC_MODE,//corresonds to the PWM for the leds as above designated
        .channel = channel,//channel LEDC Correspndence 
        .gpio_num = gpio_num,//coresponds to the gpio aspect of the leds
        .timer_sel = LEDC_TIMER,//specificed timer for the leds
        .duty = 0,  // Start with duty cycle of 0 (LED OFF)
        .hpoint = 0,
    };
    ledc_channel_config(&ledc_channel);
}


void configure_led_timer() {
    // Configure LEDC timer
    ledc_timer_config_t ledc_timer = {
        .speed_mode = LEDC_MODE,//speed mode that is designated 
        .timer_num = LEDC_TIMER,//corresponding timer aspect so that way watchdog is kept in correpsondence
        .duty_resolution = LEDC_TIMER_13_BIT,  // 13-bit duty resolution so again watchdog is kept in coorespondence
        .freq_hz = LEDC_FREQUENCY,//this sets up the pwm frequency aspect
        .clk_cfg = LEDC_AUTO_CLK,//clock Source
    };
    ledc_timer_config(&ledc_timer);
}


void set_led_state(int channel, int duty, int duration_ms) {
    //here below sets the corresponding duty cycle for the leds which then goes with the channel aspect
    ledc_set_duty(LEDC_MODE, channel, duty);
    ledc_update_duty(LEDC_MODE, channel);
    //locks in the state for each of the duration aspect
    vTaskDelay(duration_ms / portTICK_PERIOD_MS);
}



//Here below we loop thorugh each bit with respect to each state of leds and the channel paramters, allowing a corresponding blinking pattern
//Here bewlow is for LED1 that corresponds to the bit 1 and bit0 aspect
void led_task1(void *pvParameters) {
    while (true) {
        for (int i = 0; i < patternLengthLED1; i++) {
            if (binaryPatternLED1[i] == 1) {
                set_led_state(LED1_CHANNEL, 8191, BIT_1_DURATION_MS_LED1);  // For the bit1
            } else {
                set_led_state(LED1_CHANNEL, 8191, BIT_0_DURATION_MS_LED1);  // for the bit0
            }
            set_led_state(LED1_CHANNEL, 0, OFF_DURATION_MS_LED1);  // For the off duration 
        }
    }
}
//Here bewlow is for LED2 that corresponds to the bit 1 and bit0 aspect

void led_task2(void *pvParameters) {
    while (true) {
        for (int i = 0; i < patternLengthLED2; i++) {
            if (binaryPatternLED2[i] == 1) {
                set_led_state(LED2_CHANNEL, 8191, BIT_1_DURATION_MS_LED2);  // For the bit1
            } else {
                set_led_state(LED2_CHANNEL, 8191, BIT_0_DURATION_MS_LED2);  // for the bit0
            }
            set_led_state(LED2_CHANNEL, 0, OFF_DURATION_MS_LED2);  // For the off duration
        }
    }
}


//here below executes the led blinkings with respect to the output pin and channel

void app_main(void) {
    
    configure_led_timer();


    // Configure LEDs
    configure_led(LED1_OUTPUT_PIN, LED1_CHANNEL);
    configure_led(LED2_OUTPUT_PIN, LED2_CHANNEL);


    //RTOS Task configuration for the leds
    xTaskCreate(led_task1, "LED Task 1", 2048, NULL, 1, NULL);
    xTaskCreate(led_task2, "LED Task 2", 2048, NULL, 1, NULL);
}