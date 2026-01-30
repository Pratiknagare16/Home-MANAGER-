"""Role-based permissions. Owner / Member / Guest matrix."""
from models.user import ROLE_OWNER, ROLE_MEMBER, ROLE_GUEST


def can_manage_expenses(user):
    """Full: add / edit / delete expenses."""
    return user.role in (ROLE_OWNER, ROLE_MEMBER)


def can_view_expenses(user):
    return True  # all roles can view


def can_manage_tasks(user):
    """Full: add / edit / delete / assign tasks."""
    return user.role in (ROLE_OWNER, ROLE_MEMBER)


def can_view_tasks(user):
    return True


def can_manage_settings(user):
    """Home settings, invite, roles – owner only."""
    return user.role == ROLE_OWNER


def can_edit_expense(user, expense):
    """Edit/delete if owner/member, or if they paid it (optional)."""
    if user.role == ROLE_GUEST:
        return False
    return True


def can_edit_task(user, task):
    if user.role == ROLE_GUEST:
        return False
    return True
