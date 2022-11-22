

def calculate_player_speed(current_heart, base_heart):
    
    temp_ratio = abs(((current_heart - base_heart)/base_heart)*5)

    speed = 5 - (5*temp_ratio)
    if speed < 0:
        speed = 0
    
    return speed

def tens_time():

    time = 1

    return time #seconds

def erm_pwm():
    pwm = 500

    return pwm

def erm_decay_time():
    time = 1000

    return time #milliseconds