class WorkspaceError(Exception):
    """Base workspace exception."""


class WorkspaceExistsError(WorkspaceError):
    """Workspace already exists."""


class InvalidWorkspaceError(WorkspaceError):
    """Folder is not a valid Athena workspace."""