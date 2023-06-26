from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings
from rest_framework import (
    views,
    authentication,
    permissions,
    response,
    status,
)
from . serializers import SignupSerializer


class LoginAPIView(ObtainAuthToken):
    """ Create a new auth token for users  """
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES


class LogoutAPIView(views.APIView):
    """ Delete a auth token of user """
    authentication_classes = (authentication.TokenAuthentication, )
    permission_classes = (permissions.IsAuthenticated, permissions.IsAdminUser)

    def get(self, request):
        request.user.auth_token.delete()
        return response.Response(status=status.HTTP_200_OK)


class SignupAPIView(views.APIView):
    serializer_class = SignupSerializer

    def post(self, request):
        serilaizer = self.serializer_class(data=request.data)
        if serilaizer.is_valid():
            serilaizer.save()
            return response.Response(
                serilaizer.data,
            )
        return response.Response(
            serilaizer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )
