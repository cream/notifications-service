import gobject
import gtk
import cairo
import webkit
import javascriptcore as jscore

import cream.gui

class NotificationWindow(gobject.GObject):

    __gtype_name__ = 'NotificationWindow'
    __gsignals__ = {
        'closed': (gobject.SIGNAL_RUN_LAST, gobject.TYPE_PYOBJECT, ()),
        'size-changed': (gobject.SIGNAL_RUN_LAST, gobject.TYPE_PYOBJECT, (gobject.TYPE_INT, gobject.TYPE_INT))
        }

    def __init__(self, summary, body, icon):

        gobject.GObject.__init__(self)

        self.summary = summary
        self.body = body
        self.icon = icon

        self.window = gtk.Window()
        self.window.set_skip_pager_hint(True)
        self.window.set_skip_taskbar_hint(True)
        self.window.set_size_request(355, -1)
        self.window.set_keep_above(True)
        self.window.set_app_paintable(True)
        self.window.connect('expose-event', self.expose_cb)
        self.window.set_colormap(self.window.get_screen().get_rgba_colormap())
        self.window.set_decorated(False)

        self.view = webkit.WebView()
        self.view.set_transparent(True)
        self.view.connect('expose-event', self.resize_cb)

        settings = self.view.get_settings()
        settings.set_property('enable-universal-access-from-file-uris', True)
        self.view.set_settings(settings)

        self.view.open('file://./interface/notification.html')

        self.window.add(self.view)

        self.js_context = jscore.JSContext(self.view.get_main_frame().get_global_context()).globalObject
        self.js_context.get_data = self.get_data
        self.js_context.hide = self.hide


    def show(self):
        self.window.show_all()


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
            self.emit('size-changed', width, height)


    def set_position(self, x, y):
        self.window.move(x, y)


    def get_position(self):
        return self.window.get_position()


    def get_size(self):
        return self.window.get_size()

    def move(self, x, y):

        def update(timeline, state):
            self.set_position((x - start_x) * state + start_x, (y - start_y) * state + start_y)

        start_x, start_y = self.get_position()

        t = cream.gui.Timeline(300, cream.gui.CURVE_SINE)
        t.connect('update', update)
        t.run()


    def get_data(self):

        return {
            'summary': self.summary,
            'body': self.body,
            'icon': self.icon
            }


    def destroy(self):
        self.window.destroy()


    def hide(self):
        self.destroy()
        self.emit('closed')

    def expose_cb(self, window, event):

        ctx = self.window.window.cairo_create()
        ctx.set_operator(cairo.OPERATOR_SOURCE)
        ctx.set_source_rgba(0, 0, 0, 0)
        ctx.fill()

#notif = NotificationWindow('Notification', """Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua.""", 'fd')
#gtk.main()i
