"""Aplica uma passada conservadora de humanização nos três apkgs.

As substituições são exatas e não traduzem termos em inglês nem nomes de
serviços, recursos ou conceitos da área. Nenhum cartão é criado ou removido:
apenas os campos de texto são reescritos, mantendo GUIDs, IDs e estrutura.
"""

import sqlite3
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

ASPAS_RETAS = [
    ("\u201c", '"'),
    ("\u201d", '"'),
    ("\u2018", "'"),
    ("\u2019", "'"),
]

SUBSTITUICOES = {
    "07-Cloud-Engineer-Final.apkg": [
        ("o provedor possui a infraestrutura", "o provedor é dono da infraestrutura"),
        ("Cada VM possui kernel", "Cada VM tem kernel"),
        ("OSI possui 7 camadas", "OSI tem 7 camadas"),
        ("o ICMPv6 é essencial para funcionamento e diagnóstico",
         "o ICMPv6 precisa estar liberado para a rede funcionar e poder ser diagnosticada"),
        ("cada região possui serviços, preços e requisitos de conformidade próprios",
         "cada região tem serviços, preços e requisitos de conformidade próprios"),
        ("Subnet pública possui rota para um Internet Gateway",
         "Subnet pública tem rota para um Internet Gateway"),
        ("toda VPC possui uma rota local", "toda VPC tem uma rota local"),
        ("cada task ECS possui uma log stream", "cada task ECS tem uma log stream"),
        ("identificar a causa fundamental do incidente",
         "identificar a causa raiz do incidente"),
        ("<b>funcionalidade essencial</b>", "<b>funcionalidade crítica</b>"),
        ("disparam substituição ou desvio de tráfego de forma automática",
         "disparam substituição ou desvio de tráfego automaticamente"),
        ("Serve como primeiro passo", "É o primeiro passo"),
        ("cria tudo de forma automática e repetível",
         "cria os recursos automaticamente e permite repetir o processo"),
        ("Move dados entre armazenamento on-premises e AWS de forma acelerada e agendada.",
         "Move dados entre armazenamento on-premises e AWS com transferência acelerada e agendada."),
    ],
    # Os cards do 08 já são gerados com aspas retas e com o texto final das
    # correções pedagógicas (cartão 39 incluído), então só as aspas se aplicam.
    "08-Soft-Skills.apkg": ASPAS_RETAS,
    "09-Prompt-Engineering.apkg": [],
}


def reescrever(caminho, substituicoes):
    with zipfile.ZipFile(caminho) as arquivo:
        dados = arquivo.read("collection.anki2")
        outros = {
            nome: arquivo.read(nome)
            for nome in arquivo.namelist()
            if nome != "collection.anki2"
        }

    con = sqlite3.connect(":memory:")
    con.deserialize(dados)
    notas = list(con.execute("select id, flds from notes"))
    contagens = {antigo: 0 for antigo, _ in substituicoes}
    alterados = 0

    for nota_id, flds in notas:
        campos = flds.split("\x1f")
        novo = []
        for campo in campos:
            for antigo, texto_novo in substituicoes:
                if antigo in campo:
                    contagens[antigo] += campo.count(antigo)
                    campo = campo.replace(antigo, texto_novo)
            novo.append(campo)
        novo_flds = "\x1f".join(novo)
        if novo_flds != flds:
            con.execute("update notes set flds=? where id=?", (novo_flds, nota_id))
            alterados += 1

    con.commit()
    colecao_nova = con.serialize()
    con.close()

    with zipfile.ZipFile(caminho, "w", zipfile.ZIP_DEFLATED) as arquivo:
        arquivo.writestr("collection.anki2", colecao_nova)
        for nome, dados_member in outros.items():
            arquivo.writestr(nome, dados_member)

    return alterados, contagens


def main():
    for relativo, substituicoes in SUBSTITUICOES.items():
        caminho = ROOT / relativo
        alterados, contagens = reescrever(caminho, substituicoes)
        nao_usadas = [antigo for antigo, n in contagens.items() if n == 0]
        print("%s: %d notas alteradas" % (caminho.name, alterados))
        if nao_usadas:
            print("  regras sem ocorrência:", nao_usadas)


if __name__ == "__main__":
    main()
