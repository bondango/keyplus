# old test board build settings

ifndef MCU
    MCU = atxmega32a4u
endif

C_SRC += # extra includes

# vbus check pin
CDEFS += -DVBUS_PIN_PORT=R
CDEFS += -DVBUS_PIN_NUM=1
CDEFS += -DVBUS_PIN_INT_NUM=0

# nrf24 pins
CDEFS += -DNRF24_CE_PORT=PORTR
CDEFS += -DNRF24_CE_PIN=PIN0_bm

# old test board doesn't have IRQ pin connected
CDEFS += -DRF_POLLING=1
# CDEFS += -DNRF24_IRQ_PIN_PORT=R
# CDEFS += -DNRF24_IRQ_PIN_NUM=1
# CDEFS += -DNRF24_IRQ_INT_NUM=1

USE_USB := 1
USE_SCANNER := 1
USE_NRF24 := 1
USE_CHECK_PIN := 1
USE_I2C := 1
USE_HARDWARE_SPECIFIC_SCAN := 0
