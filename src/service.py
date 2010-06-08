import cream

from cream.contrib.notifications import Frontend

from interface import NotificationWindow

NAME = 'org.cream.notifications.Frontend'
OBJECT = '/org/cream/notifications/Frontend'
CAPABILITIES = ()

class Service(Frontend, cream.Module):
    def __init__(self):
        cream.Module.__init__(self)
        Frontend.__init__(self, NAME, OBJECT, CAPABILITIES)

        self.windows = {}
        self.connect('show-notification', self.sig_show_notification)
        self.connect('hide-notification', self.sig_hide_notification)

    def sig_show_notification(self, frontend, n):
        window = NotificationWindow(n.summary, n.body, 'fd')
        window.connect('closed', lambda window: self.delete_notification(n))
        self.windows[n] = window

    def sig_hide_notification(self, frontend, n):
        self.windows[n].hide()
        self.delete_notifiation()

    def delete_notification(self, n):
        del self.windows[n]

if __name__ == '__main__':
    service = Service()
    service.main()
