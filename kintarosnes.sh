#!/usr/bin/env bash



rp_module_id="kintarosnes"
rp_module_desc="Snes PCB Driver"
rp_module_section="driver"
rp_module_flags="noinstclean"
rp_module_help="Keep in mind that ..."

function update_kintaro() {
    # install from there to system folders
    sudo apt-get update
    sudo apt-get upgrade kintarosnes
}

function gui_kintaro() {
    local cmd=(dialog --backtitle "$__backtitle" --menu "Choose an option." 22 86 16)
    local options=(
        1 "Enable PowerBlock driver"
        2 "Disable PowerBlock driver"

    )
    local choice=$("${cmd[@]}" "${options[@]}" 2>&1 >/dev/tty)
    if [[ -n "$choice" ]]; then
        case "$choice" in
            1)
                make -C "$md_inst/build" installservice
                printMsgs "dialog" "Enabled PowerBlock driver."
                ;;
            2)
                make -C "$md_inst/build" uninstallservice
                printMsgs "dialog" "Disabled PowerBlock driver."
                ;;
        esac
    fi
}

function remove_kintaro() {
    sudo ./opt/kintaro/remove.sh
}
