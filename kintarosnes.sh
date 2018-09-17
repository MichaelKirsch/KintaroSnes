#!/usr/bin/env bash



rp_module_id="powerblock"
rp_module_desc="PowerBlock Driver"
rp_module_section="driver"
rp_module_flags="noinstclean"
rp_module_help="Please note that you need to manually enable or disable the PowerBlock Service in the Configuration section. IMPORTANT: If the service is enabled and the power switch functionality is enabled (which is the default setting) in the config file, you need to have a switch connected to the PowerBlock."

function depends_kintaro() {
    local depends=(cmake doxygen)
    isPlatform "rpi" && depends+=(libraspberrypi-dev)

    getDepends "${depends[@]}"
}

function sources_kintaro() {
    gitPullOrClone "$md_inst" https://github.com/petrockblog/PowerBlock.git
}

function build_kintaro() {
    cd "$md_inst"
    rm -rf "build"
    mkdir build
    cd build
    cmake ..
    make
    md_ret_require="$md_inst/build/powerblock"
}

function update_kintaro() {
    # install from there to system folders
    cd "$md_inst/build"
    make install
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
    make -C "$md_inst/build" uninstallservice
    make -C "$md_inst/build" uninstall
}
