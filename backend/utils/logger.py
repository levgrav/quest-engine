def log(message):
    with open("backend/utils/log.txt", 'a') as f:
        f.write(message + "\n")