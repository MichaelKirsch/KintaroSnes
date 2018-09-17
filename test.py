def pwm_fancontrol(hysteresis, starttemp, temp):
    perc = 100.0 * ((temp - (starttemp-hysteresis)) / (starttemp - (starttemp-hysteresis)))

    perc = min(max(perc, 0.0), 100.0)
    print(float(perc))
pwm_fancontrol(10,60,40
               )