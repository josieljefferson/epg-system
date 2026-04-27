import json, os

def gerar_m3u():
    with open("data/channels.json") as f:
        data = json.load(f)

    linhas = ["#EXTM3U"]

    for ch in data["channels"]:
        linhas.append(
            f'#EXTINF:-1 tvg-id="{ch["id"]}" tvg-name="{ch["name"]}" tvg-logo="{ch["logo"]}" group-title="Brasil",{ch["name"]}'
        )
        linhas.append(ch["stream"])

    os.makedirs("output", exist_ok=True)
    with open("output/playlist.m3u", "w", encoding="utf-8") as f:
        f.write("\n".join(linhas))

if __name__ == "__main__":
    gerar_m3u()