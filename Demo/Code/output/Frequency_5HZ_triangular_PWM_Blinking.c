
///Here below is the aspect of initiation in such that we have the packages that weill be installed

#include <stdio.h>
#include "freertos/FreeRTOS.h"
#include "freertos/task.h"
#include "driver/ledc.h"
#include "esp_task_wdt.h"
#include "esp_rom_sys.h"  // for esp_rom_delay_us()

//here below are the installed unique GPIO pins that will be designated for the GPiO12(gpio4 as backup in case if there is not any reference for gpio12)
#define LED_GPIO 12
#define LEDC_CHANNEL LEDC_CHANNEL_0
#define LEDC_TIMER LEDC_TIMER_0
#define LEDC_MODE LEDC_LOW_SPEED_MODE
#define LEDC_RES LEDC_TIMER_8_BIT
#define LEDC_FREQ 5000

//Here below are the initiation for the triangular time(we chose steps to be 100 for the total triangle period aspect)
#define STEPS 100
#define WDT_TIMEOUT_S 5

//here are the two hertz that are being initiated for the different
// We utilized the the same lines of frequency instead of different alternating freuquncies for blinking radio communication
#define FREQ_3HZ 5
#define FREQ_5HZ 5

//Here below is the duration to help with the watchdog timer offset so that the watchdog timer isnt triggered
#define DURATION_3HZ 10
#define DURATION_5HZ 10


void triangle_pwm_task(void *pvParameters) {
    int duty_cycle_steps[STEPS];


    // Build triangle waveform
    //here below is the initial rise of the triangle patten which goes up to the peak(max)
    for (int i = 0; i < STEPS / 2; i++) {
        duty_cycle_steps[i] = (255 * i) / (STEPS / 2);
    }
    //going from the peak to start of triangle, restarting the periodic aspect
    for (int i = STEPS / 2; i < STEPS; i++) {
        duty_cycle_steps[i] = (255 * (STEPS - i - 1)) / (STEPS / 2);
    }


    esp_task_wdt_add(NULL); // Updates the current task to the watchdog timer after the execution of the triangle behaviour


    while (1) {
        //first phase
        //the first alternating phase alternates LED brightness in a triangle wave pattern at desired, uniform Hz for a set duration.
        int triangle_period_us = 1000000 / FREQ_3HZ;
        int step_delay_us = triangle_period_us / STEPS;
        int total_cycles = (DURATION_3HZ * 1000000) / triangle_period_us;

// Gradually adjust LED duty cycle through predefined steps for a given number of cycles,
        for (int cycle = 0; cycle < total_cycles; cycle++) {
            for (int i = 0; i < STEPS; i++) {
                ledc_set_duty(LEDC_MODE, LEDC_CHANNEL, duty_cycle_steps[i]);
                ledc_update_duty(LEDC_MODE, LEDC_CHANNEL);
                esp_rom_delay_us(step_delay_us);
                esp_task_wdt_reset(); // Reset watchdog timer 
                // updating the duty and resetting the watchdog timer during each step to prevent timeouts.
            }
        }


        //2nd phase; the second alternating phase alternates LED brightness in a triangle wave pattern at desired, uniform Hz for a set duration.
        triangle_period_us = 1000000 / FREQ_5HZ;
        step_delay_us = triangle_period_us / STEPS;
        total_cycles = (DURATION_5HZ * 1000000) / triangle_period_us;

// Sweep through the duty cycle steps to create the triangle wave pattern, 
// repeating for the total number of cycles while maintaining watchdog resets.
        for (int cycle = 0; cycle < total_cycles; cycle++) {
            for (int i = 0; i < STEPS; i++) {
                ledc_set_duty(LEDC_MODE, LEDC_CHANNEL, duty_cycle_steps[i]);
                ledc_update_duty(LEDC_MODE, LEDC_CHANNEL);
                esp_rom_delay_us(step_delay_us);
                esp_task_wdt_reset(); 
            }
        }
    }
}

// Generate the triangle waveform by updating the LED duty cycle over multiple cycles.
void app_main(void) {
    // LEDC timer configuration
    ledc_timer_config_t ledc_timer = {
        .speed_mode = LEDC_MODE,
        .duty_resolution = LEDC_RES,
        .timer_num = LEDC_TIMER,
        .freq_hz = LEDC_FREQ,
        .clk_cfg = LEDC_AUTO_CLK
    };
    ledc_timer_config(&ledc_timer);


    // LEDC channel configuration
    //points to the aspect of the led channel and accesses the directory aspect of the channels timing and enabling wrt to esp32
    ledc_channel_config_t ledc_channel = {
        .gpio_num = LED_GPIO,
        .speed_mode = LEDC_MODE,
        .channel = LEDC_CHANNEL,
        .intr_type = LEDC_INTR_DISABLE,
        .timer_sel = LEDC_TIMER,
        .duty = 0,
        .hpoint = 0
    };
    ledc_channel_config(&ledc_channel);


    //Here below is the construction of the watchdong timer configuration and the timout chekcer
    const esp_task_wdt_config_t wdt_config = {
        .timeout_ms = WDT_TIMEOUT_S * 1000,
        .idle_core_mask = BIT(0),
        .trigger_panic = true,
    };
    esp_task_wdt_init(&wdt_config);


    // Launches the PWM taks and operations wrt to the timing aspect
    xTaskCreate(triangle_pwm_task, "triangle_pwm_task", 4096, NULL, 5, NULL);
}





