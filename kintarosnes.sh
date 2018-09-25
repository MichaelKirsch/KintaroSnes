#!/usr/bin/env bash

rp_module_id="kintaro"
rp_module_desc="kintaro Driver"
rp_module_section="config"

function pwm_menu() {
    local cmd=(dialog --backtitle "$__backtitle" --menu "Choose an option." 22 86 16)
    local options=(
        1 "100% at 50 deg"
        2 "100% at 60 deg"
        3 "100% at 70 deg"
    )
    local choice=$("${cmd[@]}" "${options[@]}" 2>&1 >/dev/tty)
    if [[ -n "$choice" ]]; then
        case "$choice" in
            1)
                python /opt/kintaro/start/json.py -v "PWM_FAN" -s "1"

                printMsgs "set PWM to 50 deg"
                ;;
            2)
                python /opt/kintaro/start/json.py -v "PWM_FAN" -s "2"
                printMsgs "set PWM to 60 deg"
                ;;
            3)
                python /opt/kintaro/start/json.py -v "PWM_FAN" -s "3"
                printMsgs "set PWM to 70 deg"
                ;;
        esac
    fi
}


function change_fan() {
    local cmd=(dialog --backtitle "$__backtitle" --menu "Choose an option." 22 86 16)
    local options=(
        1 "Activate and setup PWM-Fan"
        2 "Use default fan mode"
        3 "No fan at all"

    )
    local choice=$("${cmd[@]}" "${options[@]}" 2>&1 >/dev/tty)
    if [[ -n "$choice" ]]; then
        case "$choice" in
            1)
                pwm_menu

                ;;
            2)
                python /opt/kintaro/start/json.py -v "Fan" -s "True"
                python /opt/kintaro/start/json.py -v "PWM_FAN" -s "False"
                printMsgs "Using default I/O-Fan controll !"
                ;;

            3)
                python /opt/kintaro/start/json.py -v "PWM_FAN" -s "False"
                python /opt/kintaro/start/json.py -v "Fan" -s "False"
                printMsgs "No Fan !"
                ;;
        esac
    fi
}


function remove() {
    local cmd=(dialog --backtitle "$__backtitle" --menu "Choose an option." 22 86 16)
    local options=(
        1 "Abort"
        2 "Uninstall kintaro driver"

    )
    local choice=$("${cmd[@]}" "${options[@]}" 2>&1 >/dev/tty)
    if [[ -n "$choice" ]]; then
        case "$choice" in
            1)
                printMsgs "Aborted !"
                ;;
            2)
                printMsgs "Uninstalling !"
                sudo dpkg -u kintarosnes
                ;;
        esac
    fi
}

function pcb() {
    local cmd=(dialog --backtitle "$__backtitle" --menu "Choose an option." 22 86 16)
    local options=(
        1 "Buttons on"
        2 "Buttons off"
    )
    local choice=$("${cmd[@]}" "${options[@]}" 2>&1 >/dev/tty)
    if [[ -n "$choice" ]]; then
        case "$choice" in
            1)
                printMsgs "PCB on"
                python /opt/kintaro/start/json.py -v "PCB" -s "True"
                ;;
            2)
                printMsgs "PCB off"
                python /opt/kintaro/start/json.py -v "PCB" -s "False"
                ;;
        esac
    fi
}



function gui_kintaro() {
        while true; do
        local cmd=(dialog --backtitle "$__backtitle" --menu "Configure Kintaro Driver" 22 76 16)
        local options=(
            R "Fan-Options"
            X "PCB-Options"
            D "Start Options"
            U "Update the package"
            C "Remove Kintaro Driver"
        )

        local choice=$("${cmd[@]}" "${options[@]}" 2>&1 >/dev/tty)
        if [[ -n "$choice" ]]; then

            case "$choice" in
                R)
                    change_fan
                    ;;
                X)
                    pcb
                    ;;
                D)
                    display_active_and_registered_bluetooth
                    ;;
                U)
                    printMsgs "Updating Package !"
                    sudo apt-get update
                    sudo apt-get upgrade kintarosnes
                    ;;
                C)
                    remove
                    ;;
                M)
                    connect_mode_bluetooth
                    ;;
            esac
        else
            break
        fi
    done
}

