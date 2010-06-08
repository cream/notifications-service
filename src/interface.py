import gobject
import gtk
import cairo
import webkit
import javascriptcore as jscore

class NotificationWindow(gobject.GObject):

    __gtype_name__ = 'NotificationWindow'
    __gsignals__ = {
        'closed': (gobject.SIGNAL_RUN_LAST, gobject.TYPE_PYOBJECT, ())
        }

    def __init__(self, summary, body, icon):

        gobject.GObject.__init__(self)

        self.summary = summary
        self.body = body
        self.icon = icon

        self.window = gtk.Window()
        self.window.set_keep_above(True)
        self.window.set_app_paintable(True)
        self.window.connect('expose-event', self.expose_cb)
        self.window.set_colormap(self.window.get_screen().get_rgba_colormap())
        self.window.set_decorated(False)

        self.view = webkit.WebView()
        self.view.set_transparent(True)
        self.view.connect('expose-event', self.resize_cb)

        self.view.open('file://./interface/notification.html')

        self.window.add(self.view)
        self.window.show_all()

        self.js_context = jscore.JSContext(self.view.get_main_frame().get_global_context()).globalObject
        self.js_context.get_data = self.get_data
        self.js_context.hide = self.hide

        self.window.present()


    def resize_cb(self, widget, event, *args):

        body = self.js_context.document.body

        if body:
            width = int(body.offsetWidth)
            height = int(body.offsetHeight)
            try:
                if not self._size == (width, height):
                    self._size = (width, height)
                    self.window.set_size_request(width, height)
                    self.window.resize(width, height)
            except AttributeError:
                self._size = (width, height)
                self.window.set_size_request(width, height)
                self.window.resize(width, height)

    def get_data(self):

        return {
            'summary': self.summary,
            'body': self.body,
            'icon': self.icon
            }


    def hide(self):
        print 'YAAAY'
        self.window.destroy()
        self.emit('closed')


    def expose_cb(self, window, event):

        ctx = self.window.window.cairo_create()
        ctx.set_operator(cairo.OPERATOR_SOURCE)
        ctx.set_source_rgba(0, 0, 0, 0)
        ctx.fill()

#notif = NotificationWindow('Notification', """Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua.""", 'fd')
#gtk.main()i
