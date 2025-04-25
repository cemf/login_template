from django.core.exceptions import ObjectDoesNotExist
from rest_framework.exceptions import NotFound, ValidationError
from .models import Usuario

class UsuarioService:
    def criar_usuario(self, data):
        try:
            return Usuario.objects.create(**data)
        except Exception as e:
            raise ValidationError(f"Erro ao criar usuário: {str(e)}")

    def listar_usuarios(self):
        return Usuario.objects.all()

    def buscar_usuario(self, usuario_id):
        try:
            return Usuario.objects.get(id=usuario_id)
        except ObjectDoesNotExist:
            raise NotFound(f"Usuário com ID {usuario_id} não encontrado")

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
        Usuario.objects.all().delete()