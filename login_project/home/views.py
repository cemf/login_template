from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from .permissions import IsAdminUser
from .services import UsuarioService
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import status
from .serializers import LoginSerializer, UsuarioRegistroSerializer
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator


class UsuarioViewSet(viewsets.ViewSet):
    usuario_service = UsuarioService()

    def get_permissions(self):
        if self.action in ['login_page', 'registro', 'login', 'create']:
            return [AllowAny()]
        elif self.action in ['list', 'retrieve', 'deletar_todos']:
            return [IsAdminUser()]
        return [IsAuthenticated()]

    @action(detail=False, methods=['get', 'post'], url_path='login-page', permission_classes=[AllowAny])
    def login_page(self, request):
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request, username=username, password=password)
            
            if user is not None:
                auth_login(request, user)
                return redirect('usuario-area-logada')
            else:
                return render(request, 'home/login.html', {'error': 'Usuário ou senha inválidos'})
        
        return render(request, 'home/login.html')

    @action(detail=False, methods=['get'])
    @method_decorator(login_required)
    def area_logada(self, request):
        return render(request, 'home/area_logada.html')

    @action(detail=False, methods=['get'], url_path='logout')
    def logout(self, request):
        auth_logout(request)
        return redirect('usuario-login-page')

    @action(detail=False, methods=["post"])
    def registro(self, request):
        usuario = self.usuario_service.registrar_usuario(request.data)
        return Response(
            {"message": "Usuário registrado com sucesso", "id": usuario.id},
            status=status.HTTP_201_CREATED,
        )

    @action(detail=False, methods=["post"])
    def login(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        result = self.usuario_service.login_usuario(
            serializer.validated_data["username"], serializer.validated_data["password"]
        )
        return Response(result)

    def list(self, request):
        usuarios = self.usuario_service.listar_usuarios()
        serializer = UsuarioRegistroSerializer(usuarios, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        usuario = self.usuario_service.buscar_usuario(pk)
        serializer = UsuarioRegistroSerializer(usuario)
        return Response(serializer.data)

    def create(self, request):
        try:
            usuario = self.usuario_service.registrar_usuario(request.data)
            return Response({'message': 'Usuário criado com sucesso', 'id': usuario.id})
        except Exception as e:
            return Response({'error': str(e)}, status=400)

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

    @action(detail=False, methods=['get'])
    def me(self, request):
        serializer = UsuarioRegistroSerializer(request.user)
        return Response(serializer.data)

    @action(detail=False, methods=['delete'])
    def deletar_todos(self, request):
        self.usuario_service.deletar_todos_usuarios(confirmacao=True)
        return Response({'message': 'Todos os usuários foram deletados'})
