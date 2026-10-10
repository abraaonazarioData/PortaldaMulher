import os
import django
from django.utils.text import slugify

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'portal_django.settings')
django.setup()

from core.models import Tema, PageContent

def populate_documentos():
    # Temas
    tema_leg, _ = Tema.objects.get_or_create(slug='legislacao', defaults={'nome': 'Legislação', 'ordem': 5})
    tema_rel, _ = Tema.objects.get_or_create(slug='relatorios', defaults={'nome': 'Relatórios', 'ordem': 6})
    tema_estudos, _ = Tema.objects.get_or_create(slug='estudos', defaults={'nome': 'Estudos', 'ordem': 7})

    dados = [
        # Legislação
        (tema_leg, "Lei Complementar Estadual 837/2026", "Institui o Gabinete de Enfrentamento à Violência de Gênero contra a Mulher (GEVM) no âmbito de Mato Grosso.", "https://www.sefaz.mt.gov.br/legislacao/pesquisa-normas"),
        (tema_leg, "Lei Federal 15.410/2026 (Lei Bárbara Penna)", "Reforça a proteção de mulheres vítimas de violência, prevendo o crime de tortura pela submissão reiterada da mulher a intenso sofrimento doméstico e endurecendo punições a agressores.", "https://www.planalto.gov.br/ccivil_03/_ato2023-2026/2026/lei/l15410.htm"),
        (tema_leg, "Lei Federal 15.409/2026", "Cria o Cadastro Nacional de Pessoas Condenadas por Violência contra a Mulher (CNVM) para integrar os sistemas de segurança pública.", "https://www.planalto.gov.br/ccivil_03/_ato2023-2026/2026/lei/l15409.htm"),
        (tema_leg, "Lei Federal 15.438/2026 (Art. 3º)", "Legislação Federal em defesa da mulher.", "https://www.planalto.gov.br/ccivil_03/_ato2023-2026/2026/lei/l15438.htm#art3"),
        (tema_leg, "Portaria INSS nº 1.961/2026", "Garantias previdenciárias e assistência institucional.", "https://in.gov.br/web/dou/-/portaria-pres/inss-n-1.961-de-28-de-maio-de-2026-709128702"),
        (tema_leg, "Decreto Estadual 2003/2026", "Altera e acrescenta dispositivos ao Decreto nº 1.708.", "/static/Documentos e Legislação/Decreto Estadual n° 2003 de 23 04 2026.pdf"),
        (tema_leg, "Decreto Estadual 2002/2026", "Institui o Programa Meninas que Transformam.", "/static/Documentos e Legislação/Decreto n. 2002 de 23 04 2026.pdf"),
        (tema_leg, "Decreto Estadual 2001/2026", "Institui o Portal Mulher MT.", "/static/Documentos e Legislação/Decreto n. 2001 de 23 04 2026.pdf"),
        (tema_leg, "Decreto 1708/2025 (Plano Estadual de Metas)", "Institui a Rede Estadual de Enfrentamento da Violência contra a Mulher e aprova o Plano Estadual de Metas", "/static/Documentos e Legislação/Decreto Estadual n° 1708 23 10 2025.pdf"),
        (tema_leg, "Lei Federal 15.116/2025", "Legislação Federal de proteção e garantia de direitos da mulher.", "https://www.planalto.gov.br/ccivil_03/_ato2023-2026/2025/lei/l15116.htm"),
        (tema_leg, "Lei Federal 14.994/2024", "Pacote Antifeminicídio: Endurece penas para crimes praticados contra a mulher em contexto doméstico ou familiar.", "http://www.planalto.gov.br/ccivil_03/_Ato2023-2026/2024/Lei/L14994.htm"),
        (tema_leg, "Lei Federal 14.899/2024", "Dispõe sobre planos de metas para o enfrentamento integrado da violência doméstica e familiar contra a mulher.", "https://www.planalto.gov.br/ccivil_03/_ato2023-2026/2024/lei/l14899.htm"),
        (tema_leg, "Lei Federal 14.786/2023 (Protocolo \"Não é Não\")", "Institui o protocolo para prevenção do constrangimento e violência contra a mulher em ambientes de shows, casas noturnas e locais onde se vendem bebidas alcoólicas.", "https://www.planalto.gov.br/ccivil_03/_ato2023-2026/2023/lei/l14786.htm"),
        (tema_leg, "Lei Federal 14.717/2023", "Institui pensão especial aos filhos e dependentes de vítimas de feminicídio.", "https://www.planalto.gov.br/ccivil_03/_ato2023-2026/2023/lei/l14717.htm"),
        (tema_leg, "Lei Federal 14.310/2022", "(Lei Maria da Penha), para determinar o registro imediato, pela autoridade judicial, das medidas protetivas de urgência deferidas em favor da mulher em situação de violência doméstica e familiar, ou de seus dependentes.", "https://www.planalto.gov.br/ccivil_03/_ato2019-2022/2022/lei/l14310.htm#:~:text=LEI%20N%C2%BA%2014.310%2C%20DE%208%20DE%20MAR%C3%87O%20DE%202022&text=Altera%20a%20Lei%20n%C2%BA%2011.340,familiar%2C%20ou%20de%20seus%20dependentes"),
        (tema_leg, "Lei Federal 14.192/2021", "Estabelece normas para prevenir, reprimir e combater a violência política contra a mulher nos espaços de poder e decisão.", "https://www.planalto.gov.br/ccivil_03/_ato2019-2022/2021/lei/l14192.htm"),
        (tema_leg, "Resolução AGER nº 002/2017", "Institui a \"Parada Segura\" para usuárias do sexo feminino no transporte coletivo intermunicipal de passageiros de característica urbana, no âmbito do município de Cuiabá.", "/static/Documentos e Legislação/Resolução AGER.pdf"),
        (tema_leg, "Lei Federal 13.104/2015", "Código Penal, para prever o feminicídio como circunstância qualificadora do crime de homicídio", "https://www.planalto.gov.br/ccivil_03/_ato2015-2018/2015/lei/l13104.htm"),
        (tema_leg, "Lei Federal 12.845/2013 (Lei do Minuto Seguinte)", "Dispõe sobre o atendimento obrigatório, integral, imediato e gratuito em hospitais a pessoas em situação de violência sexual.", "https://www.planalto.gov.br/ccivil_03/_ato2011-2014/2013/lei/l12845.htm"),
        (tema_leg, "Lei Federal 12.737/2012 (Lei Carolina Dieckmann)", "Dispõe sobre a tipificação criminal de delitos informáticos (invasão de dispositivo informático alheio).", "https://www.planalto.gov.br/ccivil_03/_ato2011-2014/2012/lei/l12737.htm"),
        (tema_leg, "Lei Federal 12.650/2012 (Lei Joanna Maranhão)", "Altera as regras de contagem de prescrição nos crimes contra a dignidade sexual de crianças e adolescentes, iniciando o prazo apenas a partir da maioridade (18 anos) da vítima.", "https://www.planalto.gov.br/ccivil_03/_ato2011-2014/2012/lei/l12650.htm"),
        (tema_leg, "Lei Federal 11.340/2006", "Dispõe mecanismos para coibir a violência doméstica e familiar contra a mulher", "https://www.planalto.gov.br/ccivil_03/_ato2004-2006/2006/lei/l11340.htm"),
        (tema_leg, "Lei Federal 10.778/2003", "Estabelece a notificação compulsória, em todo o território nacional, dos casos de violência contra a mulher que for atendida em serviços de saúde públicos ou privados.", "https://www.planalto.gov.br/ccivil_03/leis/2003/l10.778.htm"),

        # Relatórios
        (tema_rel, "Anuário de Violência contra a Mulher 2024", "Estatísticas, análises oficiais e indicadores detalhados da violência contra a mulher no estado em 2024.", "https://dados.mt.gov.br/"),
        (tema_rel, "Anuário de Violência contra a Mulher 2023", "Dados consolidados, séries históricas de ocorrências e acolhimento de mulheres vítimas de violência em 2023.", "https://dados.mt.gov.br/"),
    ]

    for tema, title, text, link in dados:
        slug = slugify(title)[:50] # limits length to avoid slug issues
        PageContent.objects.update_or_create(
            title=title,
            defaults={
                'tema': tema,
                'slug': slug,
                'text': text,
                'link_url': link
            }
        )
    print("Dados inseridos com sucesso!")

if __name__ == '__main__':
    populate_documentos()
