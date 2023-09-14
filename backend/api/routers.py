import gitpm.viewsets as Viewsets
from rest_framework import routers

router = routers.DefaultRouter()

router.register(r'users', Viewsets.UserViewSet)
router.register(r'repositories/external', Viewsets.GitRepositoryViewSet)
router.register(r'eventlog', Viewsets.EventLogViewSet)
router.register(r'process', Viewsets.ProcessModelViewSet)
