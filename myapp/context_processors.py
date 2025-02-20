def agregar_grupos_usuario(request):
    if request.user.is_authenticated:
        return {'grupos_usuario': list(request.user.groups.values_list('name', flat=True))}
    return {'grupos_usuario': []}
