from num2words import num2words

hour = 1

while hour <= 12:
    print 'Alarm set for ' + str(hour) + ' [2-second pause]'

    minute = 1

    while minute < 60:
        if minute < 10:
            oh = '0'
        else:
            oh = ''

        print 'Alarm set for ' + str(hour) + ':' + oh + str(minute) + ' [2-second pause]'
        minute = minute + 1

    hour = hour + 1

exit()

"""print num2words(154223423)
exit()

while hour <= 12:
    print 'Your alarm is set for ' + num2words(hour) + ' [2-second pause]'

    minute = 1

    while minute < 60:
        if minute < 10:
            oh = ' oh '
        else:
            oh = ' '

        print 'Alarm set for ' + num2words(hour) + oh + num2words(minute) + ' [2-second pause]'
        minute = minute + 1

    hour = hour + 1"""

sleep_sounds = [
    'Ocean Waves',
    'Horizon',
    'Nocturne',
    'Morpheus',
    'Aura',
    'Brown Noise',
    'Cosmos',
    'Autumn Wind',
    'Fireside',
    'Rainfall',
    'White Noise',
    'Forest Creek'
]

for sleep_sound in sleep_sounds:
    print 'Sense will play ' + sleep_sound + ' in [2-second pause]'

minutes = 1

while minutes < 60:
    if minutes == 1:
        print num2words(minutes) + ' minute [2-second pause]'
    else:
        print num2words(minutes) + ' minutes [2-second pause]'

    minutes = minutes + 1

hours = 1

while hours < 4:
    if hours == 1:
        print 'in an hour'
    else:
        print 'in ' + num2words(hours) + ' hours'

    hours = hours + 1

room_conditions = [
    'Temperature',
    'Humidity',
    'Air Quality',
    'Light Level',
    'Noise Level',
    'Sound Level'
]

humidity = 0

while humidity <= 100:
    print 'The humidity in your room is ' + num2words(humidity) + ' percent [2-second pause]'
    humidity = humidity + 1

temperature = 0

while temperature <= 200:
    print 'The temperature in your room is ' + num2words(temperature) + ' degrees [2-second pause]'
    temperature = temperature + 1
