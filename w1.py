#!/usr/bin/env python3

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk
import cairo


supports_alpha = False


def screen_changed(widget, old_screen, userdata=None):
    global supports_alpha

    screen = widget.get_screen()
    visual = screen.get_rgba_visual()

    if visual is None:
        print("Your screen does not support alpha channels!")
        visual = screen.get_system_visual()
        supports_alpha = False
    else:
        print("Your screen supports alpha channels!")
        supports_alpha = True

    widget.set_visual(visual)


def expose_draw(widget, event, userdata=None):
    global supports_alpha

    cr = widget.get_window().cairo_create()

    if supports_alpha:
        # print("setting transparent window")
        cr.set_source_rgba(1.0, 1.0, 1.0, 0.0) 
    else:
        # print("setting opaque window")
        cr.set_source_rgb(1.0, 1.0, 1.0)

    cr.set_operator(cairo.OPERATOR_SOURCE)
    cr.paint()

    return False

def clicked(window, event, userdata=None):
    # toggle window manager frames
    window.set_decorated(not window.get_decorated())


if __name__ == "__main__":
    window = Gtk.Window()
    window.set_position(Gtk.WindowPosition.MOUSE)
    window.set_gravity(Gdk.Gravity.SOUTH_WEST)
    window.set_default_size(400, 100)
    window.move(350,1700)
    
    window.set_title("Alpha Demo")
    window.connect("delete-event", Gtk.main_quit)

    window.set_app_paintable(True)

    window.connect("draw", expose_draw)
    window.connect("screen-changed", screen_changed)

    window.set_decorated(False)
    window.add_events(Gdk.EventMask.BUTTON_PRESS_MASK)
    window.connect("button-press-event", clicked)

    box = Gtk.Box(spacing=6,homogeneous=False)
    window.add(box)
    button = Gtk.Button.new_with_label("button1")
    button.set_size_request(50, 50)
    label = Gtk.Label(
            label="Dear God! Thank you for everything."
        )
    label.set_line_wrap(True)
    # label.set_max_width_chars(256)
    
    # box.pack_start(button,True,True,0)
    box.pack_start(label,True,True,0)

    screen_changed(window, None, None)

    window.show_all()
    Gtk.main()
