import os
import django
import random

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'portal_django.settings')
django.setup()

from core.models import EstatisticaViolencia

def populate():
    EstatisticaViolencia.objects.all().delete()
    
    municipios = ['Cuiabá', 'Várzea Grande', 'Rondonópolis', 'Sinop', 'Tangará da Serra', 'Sorriso']
    tipos_crime = ['Feminicídio', 'Agressão Física', 'Ameaça', 'Violência Psicológica', 'Estupro']
    anos = [2022, 2023, 2024]
    idades = ['18-25', '26-35', '36-45', '46-55', '56+']
    racas = ['Branca', 'Preta', 'Parda', 'Indígena', 'Amarela', 'Não Informada']
    
    records = []
    
    for ano in anos:
        for mes in range(1, 13):
            for municipio in municipios:
                for crime in tipos_crime:
                    # Weight probabilities for realism
                    base_qtd = random.randint(10, 50)
                    if crime == 'Feminicídio':
                        base_qtd = random.randint(0, 3)
                    elif crime == 'Ameaça':
                        base_qtd = random.randint(30, 100)
                        
                    if municipio == 'Cuiabá':
                        base_qtd = int(base_qtd * 1.5)
                        
                    # Create multiple records to have diverse profiles
                    for _ in range(3):
                        qtd = base_qtd // 3 + random.randint(0, 5)
                        if qtd > 0:
                            records.append(EstatisticaViolencia(
                                municipio=municipio,
                                tipo_crime=crime,
                                ano=ano,
                                mes=mes,
                                quantidade=qtd,
                                perfil_vitima_idade=random.choice(idades),
                                perfil_vitima_raca=random.choice(racas)
                            ))
                            
    EstatisticaViolencia.objects.bulk_create(records)
    print(f"Populated {len(records)} records successfully.")

if __name__ == '__main__':
    populate()
