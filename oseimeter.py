import aiy.audio
import aiy.cloudspeech
import aiy.voicehat
import aiy.i18n
from aiy.toneplayer import TonePlayer
from time import sleep
import queue
import signal
import threading



aiy.i18n.set_language_code("es-ES")

TO_RECOGNIZE = ["osea","o sea","sea"]
REPORT_COUNT_EVERY = 3

def setup():
  recognizer = aiy.cloudspeech.get_recognizer()
  player = Player(gpio=22, bpm=10)

  for recognize in TO_RECOGNIZE:
    recognizer.expect_phrase(recognize)

  return recognizer,player

class Service(object):

    def __init__(self):
        self._requests = queue.Queue()
        self._thread = threading.Thread(target=self._run)
        self._thread.start()

    def _run(self):
        while True:
            request = self._requests.get()
            if request is None:
                break
            self.process(request)
            self._requests.task_done()

    def join(self):
        self._thread.join()

    def stop(self):
        self._requests.put(None)

    def process(self, request):
        pass

    def submit(self, request):
        self._requests.put(request)



class Player(Service):
    """Controls buzzer."""

    def __init__(self, gpio, bpm):
        super().__init__()
        self._toneplayer = TonePlayer(gpio, bpm)
        self.JOY_SOUND = ('C5q', 'E5q', 'C6q')
        self.SAD_SOUND = ('C6q', 'E5q', 'C5q')
        self.MODEL_LOAD_SOUND = ('C6w', 'c6w', 'C6w')
        self.BEEP_SOUND = ('E6q', 'C6q')


    def process(self, sound):
        self._toneplayer.play(*sound)

    def play(self, sound):
        self.submit(sound)


def main():
  counter = 0
  recognizer,player = setup()

  button = aiy.voicehat.get_button()
  led = aiy.voicehat.get_led()
  aiy.audio.get_recorder().start()
  
  print("Oseimeter started")
  while True:
    text = recognizer.recognize()
    print(text)

    if text is None:
      continue

    text = text.lower()
    
    if any(test in text for test in TO_RECOGNIZE):
      counter += 1
      print(str(counter))
      player.play(player.SAD_SOUND)

      if counter%REPORT_COUNT_EVERY == 0:
        aiy.audio.say(str(counter))


  
            
if __name__ == "__main__":
  main()
