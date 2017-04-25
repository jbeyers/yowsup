import sys
from yowsup.demos import broadcastclient


def get_config(path):
    """Partially taken from the cli demo"""
    with open(path) as f:
        config = {}
        for l in f:
            line = l.strip()
            if len(line) and line[0] not in ('#',';'):
                prep = line.split('#', 1)[0].split(';', 1)[0].split('=', 1)
                varname = prep[0].strip()
                val = prep[1].strip()
                config[varname.replace('-', '_')] = val
    return config


if __name__ == "__main__":
    #replace with image path
    image_path = "/path/to/image.jpg"
    # Caption for the image
    caption = "This is my image"
    # List of numbers to broadcast to.
    numbers = ['27821111111'] 
    config = get_config('yowsup.conf')
    credentials = (config['phone'], config['password'])
    try:
        stack = broadcastclient.YowsupBroadcastStack(
                credentials,
                (numbers, image_path, caption)
                )
        stack.start()
    except KeyboardInterrupt:
        print("\nGoing down....")
        sys.exit(0)
