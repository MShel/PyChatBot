Start PyChatBot

export facebook_token="tall nerd jumped under fox" &&
export page_token="EAAJRb4ZBZBzHQBALZBfkg1kFJcZBN2PK8KNCnIaVs3lykOUTwfouZAT0Vw0qKGyhuqorr3ajxEM3tuJ72UKKG8uelGtupO61uk9JkJ8ULnKUMSV3f5M6x2RRax4wIfZCs7o2DLoFydJMUVtAmiNpZAX2slyy08jNg0SZB28BjlxQzQZDZD" &&
kill `pidof uwsgi` &&
celery -A storage.Celery worker -l info &&
uwsgi --ini pychatbot_uwsgi.ini>log.txt  & &&


