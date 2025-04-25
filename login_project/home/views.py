from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Usuario
from .serializers import UsuarioSerializer
from .services import UsuarioService


class UsuarioViewSet(viewsets.ViewSet):
    serializer_class = UsuarioSerializer
    usuario_service = UsuarioService()

    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            usuario = self.usuario_service.criar_usuario(serializer.validated_data)
            return Response(self.serializer_class(usuario).data, status=201)
        return Response(serializer.errors, status=400)

    def list(self, request):
        usuarios = self.usuario_service.listar_usuarios()
        return Response(self.serializer_class(usuarios, many=True).data)

    def retrieve(self, request, pk=None):
        usuario = self.usuario_service.buscar_usuario(pk)
        return Response(self.serializer_class(usuario).data)

    def update(self, request, pk=None):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            usuario = self.usuario_service.atualizar_usuario(
                pk, serializer.validated_data
            )
            return Response(self.serializer_class(usuario).data)
        return Response(serializer.errors, status=400)

    def destroy(self, request, pk=None):
        self.usuario_service.deletar_usuario(pk)
        return Response(status=204)

    @action(detail=False, methods=["delete"])
    def deletar_todos(self, request):
        self.usuario_service.deletar_todos_usuarios(confirmacao=True)
        return Response(status=204)
