#!/usr/bin/env python
"""
Script para actualizar la contraseña del usuario admin.
Ejecutar con: python actualizar_password.py
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'control_asistencia.settings')
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()

try:
    u = User.objects.get(username='admin')
    u.set_password('a')
    u.save()
    print('✓ Contraseña actualizada correctamente para el usuario: admin')
except User.DoesNotExist:
    print('✗ Error: El usuario admin no existe')
except Exception as e:
    print(f'✗ Error: {e}')
