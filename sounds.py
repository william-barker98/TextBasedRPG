from pygame import mixer
mixer.init()


def PlaySound(path, volume):
    sound = mixer.Sound(path)
    sound.set_volume(volume)
    sound.play()
