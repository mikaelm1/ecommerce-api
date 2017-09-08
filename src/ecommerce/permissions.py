from rest_framework import permissions


class EmailConfirmed(permissions.BasePermission):
    """
    Allows access only to users that have confirmed emails.
    """
    message = 'You have not verified your email address yet.'

    def has_permission(self, req, view):
        return req.user and req.user.email_verified
