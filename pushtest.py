from pushbullet import Pushbullet

API_KEY = "o.QCdVDvNwBIEaJxVsaUmDe50lm5KaQ8f9"
filename = 'resolution.txt'

with open(filename, mode='r') as f:
    text = f.read()

pb = Pushbullet(API_KEY)
push = pb.push_note("This is the title", text)
