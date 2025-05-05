from .base import router as base_router
from .ml import router as ml_router
from .github_content import router as github_router

__all__ = ["base_router", "ml_router", "github_router"]
