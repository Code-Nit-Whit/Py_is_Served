import gi
gi.require_version('AppIndicator3', '0.1')
from gi.repository import AppIndicator3 as appindicator
from gi.repository import Gtk

# Create the AppIndicator
indicator_id = "http.server.icon"
icon_name = "server-reg.png"
icon_path = "./icons/server-reg.png"
attention_icon_name = "derver-warn.png"
attention_icon_path = "./icons/server-warn.png"

try:
    indicator = appindicator.Indicator.new(
        indicator_id,
        icon_name,
        appindicator.IndicatorCategory.APPLICATION_STATUS
    )
    indicator.set_attention_icon_full(attention_icon_name, "Attention")
    indicator.set_status(appindicator.IndicatorStatus.ACTIVE)

    # Create the menu
    menu = Gtk.Menu()
    item_close_server = Gtk.MenuItem(label="Close Server")
    item_open_url = Gtk.MenuItem(label="Open URL")
    item_close_server.connect("activate", stop_server)
    item_open_url.connect("activate", open_url)
    menu.append(item_close_server)
    menu.append(item_open_url)
    indicator.set_menu(menu)

    # Set up GTK main loop
    import signal
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    import gi.repository.Gtk as Gtk
    Gtk.main()

except Exception as e:
    log_message("error", f"An unexpected error occurred in the GTK main loop: {e}")