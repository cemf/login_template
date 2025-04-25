from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.exceptions import AuthenticationFailed, ValidationError
from .models import Usuario
from .serializers import UsuarioRegistroSerializer
class UsuarioService:
    def registrar_usuario(self, data):
        serializer = UsuarioRegistroSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        usuario = serializer.save()
        return usuario

    def login_usuario(self, username, password):
        usuario = authenticate(username=username, password=password)
        if not usuario:
            raise AuthenticationFailed('Credenciais inválidas')
        
        refresh = RefreshToken.for_user(usuario)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'user': {
                'id': usuario.id,
                'username': usuario.username,
                'email': usuario.email,
            }
        }

    def get_usuario_by_token(self, token):
        try:
            return Usuario.objects.get(id=token['user_id'])
        except Usuario.DoesNotExist:
            raise AuthenticationFailed('Usuário não encontrado')

    def listar_usuarios(self):
        return Usuario.objects.all()

    def atualizar_usuario(self, usuario_id, data):
        usuario = self.buscar_usuario(usuario_id)
        for attr, value in data.items():
            setattr(usuario, attr, value)
        try:
            usuario.save()
            return usuario
        except Exception as e:
            raise ValidationError(f"Erro ao atualizar usuário: {str(e)}")

    def deletar_usuario(self, usuario_id):
        usuario = self.buscar_usuario(usuario_id)
        usuario.delete()

    def deletar_todos_usuarios(self, confirmacao=False):
        if not confirmacao:
            raise ValidationError("É necessário confirmar a operação de deleção em massa")
        Usuario.objects.filter(is_superuser=False, is_staff=False).delete()