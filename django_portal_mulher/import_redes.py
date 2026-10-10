import sys
import os

sys.path.append(r'c:\Users\Administrator\Desktop\Portal Mulher\new\Portal Mulher\Portal Mulher')
from app import REDES_DATA
from core.models import RedeProtecao

print("Iniciando importação de delegacias...")
for item in REDES_DATA:
    if not RedeProtecao.objects.filter(nome=item.get('nome'), cidade=item.get('cidade')).exists():
        RedeProtecao.objects.create(
            nome=item.get('nome', ''),
            tipo=item.get('tipo', ''),
            cidade=item.get('cidade', ''),
            endereco=item.get('endereco', ''),
            telefone=item.get('telefone', ''),
            email=item.get('email', ''),
            horario=item.get('horario', ''),
            latitude=item.get('latitude', None),
            longitude=item.get('longitude', None)
        )
print(f"Importação concluída. Total no DB: {RedeProtecao.objects.count()}")
