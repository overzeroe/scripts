#!/usr/bin/python

import sys
import dbus
import gobject

from dbus.mainloop.glib import DBusGMainLoop

# Start D-Bus
purple=None
def setup_dbus():
    " Start the dbus connection"
    global purple

    print "Initializing dbus..."
    dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)
    session_bus = dbus.SessionBus()
    bus_object = session_bus.get_object("im.pidgin.purple.PurpleService", "/im/pidgin/purple/PurpleObject")
    purple = dbus.Interface(bus_object, "im.pidgin.purple.PurpleInterface")

    listen(session_bus)

# Listen for status changes and update the local status
def listen(bus):
    print "Listening for status changes..."
     
    # Update the local status
    def status_updated(buddy, old_status, status):
        print "Signal received...", buddy
        status_type = purple.PurpleStatusGetType(status)
        print purple.PurpleStatusTypeGetName(status_type), 
        print purple.PurpleStatusTypeGetAttrs(status_type)
        print
        print 

    # Call status_updated whenever Pidgin changes the status
    bus.add_signal_receiver(status_updated, dbus_interface="im.pidgin.purple.PurpleInterface", signal_name="BuddyStatusChanged")


# Listen continuously
def start_listen_loop():
    loop = gobject.MainLoop()
    loop.run()

# Start D-Bus
setup_dbus()
start_listen_loop()
