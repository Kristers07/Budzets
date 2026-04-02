from __future__ import annotations

import csv
from datetime import datetime
from pathlib import Path

from flask import Flask, flash, redirect, render_template, request, send_from_directory, url_for

app = Flask(__name__, template_folder=".")
app.secret_key = "budzets-secret-key"

# CSV fails, kur tiek glabāti visi budžeta ieraksti.
DATA_FILE = Path("dati.csv")
IERAKSTU_TIPI = ("Ienakums", "Izdevums")
dati: list[dict] = []


def ieladet_datus() -> None:
    # Ielādē ierakstus no CSV faila programmas palaišanas brīdī.
    dati.clear()
    if not DATA_FILE.exists():
        return

    with DATA_FILE.open("r", newline="", encoding="utf-8") as fails:
        lasitajs = csv.DictReader(fails)
        for rinda in lasitajs:
            try:
                dati.append(
                    {
                        "tips": rinda["tips"],
                        "summa": float(rinda["summa"]),
                        "apraksts": rinda["apraksts"],
                        "datums": rinda["datums"],
                    }
                )
            except (KeyError, TypeError, ValueError):
                continue


def saglabat_datus() -> None:
    # Saglabā pašreizējos ierakstus atpakaļ CSV failā.
    with DATA_FILE.open("w", newline="", encoding="utf-8") as fails:
        lauki = ["tips", "summa", "apraksts", "datums"]
        rakstitajs = csv.DictWriter(fails, fieldnames=lauki)
        rakstitajs.writeheader()
        rakstitajs.writerows(dati)


def kopsavilkums(ieraksti: list[dict]) -> dict:
    # Aprēķina kopējos ienākumus, izdevumus un bilanci izvēlētajiem ierakstiem.
    ienakumi = sum(ier["summa"] for ier in ieraksti if ier["tips"] == "Ienakums")
    izdevumi = sum(ier["summa"] for ier in ieraksti if ier["tips"] == "Izdevums")
    return {
        "ienakumi": ienakumi,
        "izdevumi": izdevumi,
        "bilance": ienakumi - izdevumi,
    }


def filtreti_ieraksti(tips: str, datums_no: str, datums_lidz: str) -> list[dict]:
    # Atlasa ierakstus pēc tipa un datuma intervāla, un pievieno ID dzēšanai.
    atlasitie = list(enumerate(dati))

    if tips in IERAKSTU_TIPI:
        atlasitie = [ier for ier in atlasitie if ier[1]["tips"] == tips]

    if datums_no:
        atlasitie = [ier for ier in atlasitie if ier[1]["datums"] >= datums_no]

    if datums_lidz:
        atlasitie = [ier for ier in atlasitie if ier[1]["datums"] <= datums_lidz]

    atlasitie.reverse()
    return [{"id": indekss, **ieraksts} for indekss, ieraksts in atlasitie]


@app.template_filter("nauda")
def nauda(summa: float) -> str:
    # Pārvērš skaitli ērtā naudas formātā attēlošanai lapā.
    return f"{summa:.2f} EUR"


@app.route("/style.css")
def stils():
    return send_from_directory(".", "style.css")


@app.route("/")
def index():
    # Parāda galveno lapu ar filtriem, ierakstiem un kopsavilkumu.
    tips = request.args.get("tips", "Visi")
    datums_no = request.args.get("datums_no", "")
    datums_lidz = request.args.get("datums_lidz", "")

    ieraksti = filtreti_ieraksti(tips, datums_no, datums_lidz)
    atlasitais_kopsavilkums = kopsavilkums(ieraksti)

    return render_template(
        "index.html",
        dati=ieraksti,
        tips=tips,
        datums_no=datums_no,
        datums_lidz=datums_lidz,
        kopsavilkums=atlasitais_kopsavilkums,
        visi=kopsavilkums(dati),
        sodien=datetime.now().strftime("%Y-%m-%d"),
    )


@app.route("/pievienot", methods=["POST"])
def pievienot():
    # Nolasa formas datus, pārbauda tos un pievieno jaunu ierakstu.
    tips = request.form.get("tips", "").strip()
    summa_teksts = request.form.get("summa", "").replace(",", ".").strip()
    apraksts = request.form.get("apraksts", "").strip()
    datums = request.form.get("datums", "").strip()

    if tips not in IERAKSTU_TIPI:
        flash("Izvelies derigu ieraksta tipu.", "error")
        return redirect(url_for("index"))

    if not apraksts:
        flash("Apraksts nedrikst but tukss.", "error")
        return redirect(url_for("index"))

    try:
        summa = float(summa_teksts)
    except ValueError:
        flash("Summai jabut skaitlim.", "error")
        return redirect(url_for("index"))

    if summa <= 0:
        flash("Summai jabut lielakai par nulli.", "error")
        return redirect(url_for("index"))

    if not datums:
        datums = datetime.now().strftime("%Y-%m-%d")

    dati.append(
        {
            "tips": tips,
            "summa": summa,
            "apraksts": apraksts,
            "datums": datums,
        }
    )
    saglabat_datus()
    flash("Ieraksts veiksmigi pievienots.", "success")
    return redirect(url_for("index"))


@app.route("/dzest/<int:ieraksta_id>", methods=["POST"])
def dzest(ieraksta_id: int):
    # Izdzēš ierakstu pēc tā saraksta indeksa.
    if 0 <= ieraksta_id < len(dati):
        dati.pop(ieraksta_id)
        saglabat_datus()
        flash("Ieraksts izdzests.", "success")
    else:
        flash("Ieraksts nav atrasts.", "error")
    return redirect(url_for("index"))

# Ielādē datus uzreiz, lai tie būtu pieejami pirms pirmā pieprasījuma.
ieladet_datus()

if __name__ == "__main__":
    app.run(debug=True)
