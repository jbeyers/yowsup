## Notes on broadcasting media

If you compare this branch with master, you should see the following:

 * I have added a broadcast option (with the -b parameter) to yowsup-cli. This worked at some point, but the broadcast demo app changed too much, so it is not currently working.
 * I have added a run.py script that should be able to take some hardcoded parameters (open up the file and you will see). You can add a path to an image and a list of numbers, and it will send a message.
 * The message currently only sends to the first person in the list. I think that it is sending both a 'to' stanza and a 'broadcast' stanza, and only the 'to' stanza is used.

After cloning the repository, cd'ing into it, and editing run.py to include some working parameters, The following should get you going:

`virtualenv ve --python=python3`
`./ve/bin/pip install -r requirements.txt`
`./ve/bin/python run.py`

Note that as written, the first time you upload the image, you will get an upload failed error, but the image will have uploaded, and on subsequent runs it will work.

At this point, because the message is initially constructed as a single media message, and I change the class later (a pattern that is used a lot in this codebase), the message is probably interpreted as a normal mediamessage by the lower layers, even if it has the extra broadcast stanza. Since I tried so many things, this might require just a little bit of fiddling to make work. Or not. I'm not spending more time on figuring that out.

Odds are that the broadcastmediamessage class and the layer needs to be built out from the ground up instead of trying to shoehorn and reuse functionality from other classes.

Hope this helps anyone who wants to take this further.
