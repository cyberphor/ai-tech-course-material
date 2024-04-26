class LoginRouter:
    """
    A router to control all database operations.
    """

    def db_for_write(self, model, **hints):
        """
        Write requests will be routed to the "default" database (as defined in "settings.py").
        """
        return "default"

    def db_for_read(self, model, **hints):
        """
        Read requests will be routed to the "read" database (as defined in "settings.py").
        """
        return "read"
