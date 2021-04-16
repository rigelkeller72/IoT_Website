import pyttsx3

engine = pyttsx3.init()

engine.say('Intruder Alert!')

# voices = engine.getProperty('voices')
# voice = voices[1]
# engine.setProperty('voice', voice.id)
#
# engine.say('U k Hazel says Cary Grant')
#
# rate = engine.getProperty('rate')
# engine.setProperty('rate', rate-25)
#
# engine.say('U k Hazel says Cary Grant')
#
# for voice in voices:
#    engine.setProperty('voice', voice.id)
#    #print(voice.id)
#    engine.say('The quick brown fox jumped over the lazy dog.')
engine.runAndWait()

