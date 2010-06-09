import gtk

import cream
from cream.util.dicts import ordereddict
from cream.contrib.notifications import Frontend

from interface import NotificationWindow

NAME = 'org.cream.notifications.Frontend'
OBJECT = '/org/cream/notifications/Frontend'
CAPABILITIES = ()

class Service(Frontend, cream.Module):
    def __init__(self):
        cream.Module.__init__(self)
        Frontend.__init__(self, NAME, OBJECT, CAPABILITIES)

        self.screen_width = gtk.gdk.screen_width()
        self.windows = []
        self.connect('show-notification', self.sig_show_notification)
        self.connect('hide-notification', self.sig_hide_notification)

    def sig_size_changed(self, window, width, height):
        self.rearrange()

    def rearrange(self, unanimated=[]):
        y = 0
        for window in self.windows:
            window_width, window_height = window.get_size()
            if window not in unanimated:
                window.move(self.screen_width - window_width, y)
            else:
                window.set_position(self.screen_width - window_width, y)
            y += window_height

    def sig_show_notification(self, frontend, n):
        window = NotificationWindow(n.summary, n.body, 'fd')
        window.notification = n
        window.connect('closed', lambda window: self.delete_notification(n))
        self.windows.append(window)
        self.rearrange([window])
        window.show()

    def get_window_by_notification(self, n):
        for window in self.windows:
            if window.notification == n:
                return window
        raise IndexError(n)

    def sig_hide_notification(self, frontend, n):
        window = self.get_window_by_notification(n)
        window.destroy()
        self.delete_notification(n)

    def delete_notification(self, n):
        window = self.get_window_by_notification(n)
        self.windows.remove(window)
        self.rearrange()

if __name__ == '__main__':
    service = Service()
    service.main()
