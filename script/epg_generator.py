import requests, json, re, os
from bs4 import BeautifulSoup
from datetime import datetime, timedelta

TIMEZONE = "-0300"
DAYS = 7

def extrair_programacao(url):
    r = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
    soup = BeautifulSoup(r.text, "html.parser")

    texto = soup.get_text("\n")
    linhas = texto.split("\n")

    padrao = re.compile(r"(\d{2}:\d{2})\s*[-–]\s*(.+)")

    programas = []
    for l in linhas:
        l = l.strip()
        m = padrao.match(l)
        if m:
            programas.append((m.group(1), m.group(2)))

    return programas

def gerar_epg():
    with open("data/channels.json") as f:
        data = json.load(f)

    xml = ['<?xml version="1.0" encoding="UTF-8"?>', '<tv>']

    for ch in data["channels"]:
        xml.append(f'<channel id="{ch["id"]}"><display-name>{ch["name"]}</display-name></channel>')

        programas = extrair_programacao(ch["source"])

        for d in range(DAYS):
            base = datetime.now() + timedelta(days=d)

            for i, (hora, titulo) in enumerate(programas):
                h, m = map(int, hora.split(":"))
                start = base.replace(hour=h, minute=m, second=0)

                if i < len(programas) - 1:
                    ph, pm = map(int, programas[i+1][0].split(":"))
                    stop = base.replace(hour=ph, minute=pm, second=0)
                else:
                    stop = start + timedelta(hours=1)

                xml.append(f'''
<programme start="{start.strftime("%Y%m%d%H%M%S")} {TIMEZONE}" stop="{stop.strftime("%Y%m%d%H%M%S")} {TIMEZONE}" channel="{ch["id"]}">
<title>{titulo}</title>
</programme>
''')

    xml.append('</tv>')

    os.makedirs("output", exist_ok=True)
    with open("output/epg.xml", "w", encoding="utf-8") as f:
        f.write("\n".join(xml))

if __name__ == "__main__":
    gerar_epg()