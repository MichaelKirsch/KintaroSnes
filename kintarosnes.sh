#!/usr/bin/env bash

rp_module_id="kintaro"
rp_module_desc="kintaro Driver"
rp_module_section="config"

function pwm_menu() {
    local cmd=(dialog --backtitle "$__backtitle" --menu "Choose an option." 22 86 16)
    local options=(
        1 "Start at 40 deg. 100% at 60 deg."
        2 "Start at 50 deg. 100% at 70 deg."

    )
    local choice=$("${cmd[@]}" "${options[@]}" 2>&1 >/dev/tty)
    if [[ -n "$choice" ]]; then
        case "$choice" in
            1)

                printMsgs "dialog" "Enabled ControlBlock driver."
                ;;
            2)
                #change to normal fan here
                printMsgs "Using default I/O-Fan controll !"
                ;;
        esac
    fi
}


function change_fan() {
    local cmd=(dialog --backtitle "$__backtitle" --menu "Choose an option." 22 86 16)
    local options=(
        1 "Activate and setup PWM-Fan"
        2 "Use default fan mode"

    )
    local choice=$("${cmd[@]}" "${options[@]}" 2>&1 >/dev/tty)
    if [[ -n "$choice" ]]; then
        case "$choice" in
            1)
                pwm_menu
                printMsgs "dialog" "Enabled ControlBlock driver."
                ;;
            2)
                #change to normal fan here
                printMsgs "Using default I/O-Fan controll !"
                ;;
        esac
    fi
}

function gui_kintaro() {
   addAutoConf "8bitdo_hack" 0

    while true; do
        local connect_mode="$(_get_connect_mode)"

        local cmd=(dialog --backtitle "$__backtitle" --menu "Configure Bluetooth Devices" 22 76 16)
        local options=(
            R "Fan-Setup"
            X "Update the package"
            D "Play custom video"
            U "LED"
            C "Remove Kintaro Driver"
        )

        local choice=$("${cmd[@]}" "${options[@]}" 2>&1 >/dev/tty)
        if [[ -n "$choice" ]]; then
            # temporarily restore Bluetooth stack (if needed)
            service sixad status >/dev/null && sixad -r
            case "$choice" in
                R)
                    change_fan
                    ;;
                X)
                    remove_device_bluetooth
                    ;;
                D)
                    display_active_and_registered_bluetooth
                    ;;
                U)
                    udev_bluetooth
                    ;;
                C)
                    connect_bluetooth
                    ;;
                M)
                    connect_mode_bluetooth
                    ;;
            esac
        fi
    done
}

