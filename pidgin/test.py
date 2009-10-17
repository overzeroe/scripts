We are hackers. At least, that's what we liked to call ourselves before the term got overpopularized, dramatized, and turned into a romantic notion of a person who breaks into computer systems. And by we, I mean the type of person who I would have been had I been born 20 or 30 years earlier - I'm past the real generation of hackers. But Hacker News lives on! Great news slash social discussion site.

Anyway, being the type of person that I am I have always had the urge to automate everything away. Just turn everything into a neat little script. So today, I've decided to finally figure out how to script Pidgin (the Swiss Army Knife of Instant Messengers) with Python. And write about it in a blog.

First of all, be informed: the best way to control Pidgin is with something called D-Bus. D-Bus is a method for applications to communicate between themselves without invoking direct socket-to-socket relations and protocols. It looks pretty nice. If you aren't familiar with D-Bus or the idea of message busses in general, here is the freedesktop.org Description and Introduction to D-Bus. And here's an intro on how to use D-Bus with Pidgin.

You know, I don't actually know what I'm doing. I'm more or less just writing out what I'm doing as I'm doing it - so if you started out new to this topic, by the time you read this, you'll know as much as I did when I was writing it. Wow, a mouthful.

So in case you don't feel like reading, here are the two ways of communicating with Pidgin that we now have - we can a) tell it to do things (call methods) and get responses (return values), and b) listen to its birdy cries (listen in on events) and respond appropriately. These are pretty standard methods of inter-module communication, nothin' special.

Whoa. There are a lot of signals. This seems like a pretty powerful scripting method. Here's a list.

Except with signals, we can't actually tell Pidgin to do anything. For that, we have methods. But, oh dear, the documentation for the available methods is slightly worse. According to the Pidgin How-To, "the only reference for the available functions is the documentation for the header files". Ack!



And now, onto coding! Let's use the Python D-Bus interface, since I like Python and it's what the Pidgin dev's seem to like having examples in.

First, as said in the D-Bus How-To, we get access to the interface:

[ccesN_python nowrap="false"]
import dbus

purple=None
def start_dbus():
" Start the python D-bus interface and connect to Pidgin "

# Store the connection in a global variable so we can use it later
global purple

# Open the session bus, get the pidgin purple service object, and get the interface for it
session_bus = dbus.SessionBus()
bus_object = session_bus.get_object("im.pidgin.purple.PurpleService", "/im/pidgin/purple/PurpleObject")
purple = dbus.Interface(bus_object, "im.pidgin.purple.PurpleInterface")
[/ccesN_python]

Next, let's decide what we want to try to do. Heh, unusual order of operations, but hey, whatever.

Hmm.

Let's just try basics. Updating your status from the command-line. But let's add in a special feature: the status will allow fields, using something similar to printf notation. So, for example, you might have the following commands:

[cceN_bash]
python status-update.py set-status "I am currently listening to %s by the artist %s. This status is updated through D-bus!";
python status-update.py set-fields "Fundamentum" "Lesiem";
[/cceN_bash]

The idea is that the viewers of your status won't even see the field notation. So let's get started.

So, how are we going to do this? Here's what I would do: store a status in a temporary file with the %s and all, and integrate the fields into it as necessary. Let's!

[ccesN_python]
# Let's store our status in a temp. file somewhere
STATUS_FILE="/tmp/pidgin-status"
[/ccesN_python]

[ccesN_python nowrap="false"]
# Update status will be passed all the command line arguments except the very first one
def update_status(arg_list):
" Update the Pidgin status; by default, set fields to blank "
global STATUS_FILE
status = arg_list[0]

# Save the status in its original form, along with incomplete fields, in a file
status_file = file(STATUS_FILE, "w")
status_file.write(status)
status_file.close()

# Find number of fields
num_fields = status.count("%s")
fields = [""] * num_fields # Got to admit, this is a nifty line

# Set the fields to null and actually set the status
update_fields(fields) # Instead of changing the status ourselves with d-bus, let's just let the update_fields method do it, since it will be doing it anyway
[/ccesN_python]

Well, next, we need to update fields. The fields will all be of the form of %s, and each subsequent field will be an additional command-line argument.

[ccesN_python nowrap="false"]
def update_fields(arg_list):
" Change the fields in your Pidgin status."

# We'll be reading from here.
global STATUS_FILE

# Read the status from the file
status_file = file(STATUS_FILE, "r")
status = "".join(status_file .readlines()) # This will just read in the contents of the file as a string
status_file.close()

# Fill in the fields by taking the command-line arguments, putting them in a tuple, and then integrating them into the status
complete_status = status % tuple(arg_list)

# Finally actually set the status
set_pidgin_status_message(complete_status) # Yes, once more, we're delegating it to a helper method which will deal with d-bus
[/ccesN_python]

Note how we have barely done anything with D-Bus at the moment - this is because this use of it is so simple that it barely requires communication with pidgin. Any more serious app would probably be using d-bus throughout. Anyway, let's finish off the application code by writing that helper method:

[ccesN_python nowrap="false"]
# Make pidgin change status!
def set_pidgin_status_message(status_str):
" Set the pidgin status message "

# Get your current status
status = purple.PurpleSavedstatusGetCurrent()

# Set the status message of the current status
purple.PurpleSavedstatusSetMessage(status, status_str)

# Transformers, Activate! (Update the status)
purple.PurpleSavedstatusActivate(status)
[/ccesN_python]

Wallah! We're essentially done. The last thing we have to do is create the application runner code itself, and that's simple:
[ccesN_python nowrap="false"]
import sys

# Make sure we have enough arguments to do something
if len(sys.argv) <= 1: print "Error: not enough arguments." sys.exit(0) # Start D-Bus setup_dbus() # Either update the status or change fields if sys.argv[1] == "status": update_status(sys.argv[2:]) elif sys.argv[1] == "fields": update_fields(sys.argv[2:]) else: print "Error: unknown operation on status." [/ccesN_python] That's it. Cool. Try it out, it should work. If you want to download the entire file, here it is: status.py

Questions? Comments? Answers? Do talk to me. I like being talked to!
