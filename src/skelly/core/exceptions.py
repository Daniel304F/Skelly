class SkellyError(Exception):
    """Base exception for all Skelly errors."""


class DependencyInstallError(SkellyError):
    """Raised when dependency installation fails."""


class TemplateRenderError(SkellyError):
    """Raised when template rendering fails."""


class BuildError(SkellyError):
    """Raised when project build fails."""
