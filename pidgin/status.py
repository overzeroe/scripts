import sys
import dbus
import gobject

from dbus.mainloop.glib import DBusGMainLoop


STATUS_FILE="/tmp/.pidgin_status"
SET_STATUS_FILE="/tmp/.pidgin_status_post_interpolation"

# Update the status
def update_status(arg_list):
    " Update the status. This saves the status to a hidden file in your home dir, and then sets your Pidgin status to it."

    global STATUS_FILE
    status = arg_list[0]

    # Save the status in its original form, along with incomplete fields, in a file
    status_file = file(STATUS_FILE, "w")
    status_file.write(status)
    status_file.close()

    # Find number of fields
    num_fields = status.count("%s")
    fields = [""] * num_fields       # Got to admit, this is a nifty line
    
    # Set the fields to null and actually set the status
    update_fields(fields)

def update_fields(arg_list):
    " Change the fields in your Pidgin status."

    global STATUS_FILE
    
    # Read the status from the file
    status_file = file(STATUS_FILE, "r")
    status = "".join(status_file .readlines())
    status_file.close()

    # Fill in the fields
    complete_status = status % tuple(arg_list)

    # Finally actually set the status
    set_pidgin_status_message(complete_status)


# Make pidgin change status!
def set_pidgin_status_message(status_str):
    " Set the pidgin status message "

    # Get your status
    status = purple.PurpleSavedstatusGetCurrent()

    # Update which status was last set by this script
    set_last_set_status(status_str)

    # Set the status message of the current status
    purple.PurpleSavedstatusSetMessage(status, status_str)

    # Transformers, Activate!
    purple.PurpleSavedstatusActivate(status)


# Set the last post-interpolation-of-fields status
def set_last_set_status(stat):
    global SET_STATUS_FILE

    # Remember the actual last status (with fields interpolated)
    status_file = file(SET_STATUS_FILE, "w")
    status_file.write(stat)
    status_file.close()

# Get the last post-interpolation of fields status
def get_last_set_status():
    global SET_STATUS_FILE

    # Read the status from the file
    status_file = file(SET_STATUS_FILE, "r")
    last_set_status_message = "".join(status_file .readlines())
    status_file.close()
    
    return last_set_status_message




# Start D-Bus
purple=None
def setup_dbus():
    " Start the dbus connection"
    global purple

    dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)
    session_bus = dbus.SessionBus()
    bus_object = session_bus.get_object("im.pidgin.purple.PurpleService", "/im/pidgin/purple/PurpleObject")
    purple = dbus.Interface(bus_object, "im.pidgin.purple.PurpleInterface")
    
    # Start listening for Pidgin status change events
    if sys.argv[1] == "listen":
        listen(session_bus)

# Listen for status changes and update the local status
def listen(bus):
    # Update the local status
    def status_updated(purple_account, old_status, new_status):
        new_status_message = purple.PurpleSavedstatusGetMessage(purple.PurpleSavedstatusGetCurrent())

        if new_status_message != get_last_set_status():
            update_status([new_status_message])

    # Call status_updated whenever Pidgin changes the status
    bus.add_signal_receiver(status_updated, dbus_interface="im.pidgin.purple.PurpleInterface", signal_name="AccountStatusChanged")


# Listen continuously
def start_listen_loop():
    loop = gobject.MainLoop()
    loop.run()

# Make sure we have enough arguments to do something
if len(sys.argv) <= 1:
    print "Error: not enough arguments."
    sys.exit(0)

# Start D-Bus
setup_dbus()

# Either update the status or change fields, or start listening for status changes
if sys.argv[1] == "status":
    update_status(sys.argv[2:])
elif sys.argv[1] == "fields":
    update_fields(sys.argv[2:])
elif sys.argv[1] == "listen":
    start_listen_loop()
else:
    print "Error: unknown operation on status."
