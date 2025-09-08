from fastapi import FastAPI
import pandas as pd

app = FastAPI()

# Parametri IVA e regole fiscali
ALIQUOTA_IVA = 0.22

regole = {
    "materie_prime": {"deducibilita": 1.0, "detraibilita_iva": 1.0},
    "telefonia": {"deducibilita": 0.8, "detraibilita_iva": 0.5},
    "vitto_alloggio": {"deducibilita": 0.75, "detraibilita_iva": 0.0}
}

@app.get("/confronto")
def confronto_regimi(
    incassi_lordi: float,
    materie_prime: float,
    telefonia: float,
    vitto_alloggio: float,
    codice_ateco: str = "56.10.30",  # default gelaterie
    imposta_sostitutiva: float = 0.15
):
    # coeff redditività ATECO demo
    coeff_ateco = 0.40 if codice_ateco == "56.10.30" else 0.67

    # --- FORFETTARIO ---
    reddito_forf = incassi_lordi * coeff_ateco
    imposte_forf = reddito_forf * imposta_sostitutiva
    netto_forf = incassi_lordi - imposte_forf

    # --- ORDINARIO ---
    ricavi_ord = incassi_lordi / (1 + ALIQUOTA_IVA)

    # Calcolo costi deducibili
    costi_input = {
        "materie_prime": materie_prime,
        "telefonia": telefonia,
        "vitto_alloggio": vitto_alloggio
    }

    costi_deducibili = 0
    iva_detraibile = 0

    for categoria, costo_lordo in costi_input.items():
        imponibile = costo_lordo / (1 + ALIQUOTA_IVA)
        iva = costo_lordo - imponibile

        ded = imponibile * regole[categoria]["deducibilita"]
        iva_det = iva * regole[categoria]["detraibilita_iva"]

        costi_deducibili += ded
        iva_detraibile += iva_det

    reddito_ord = ricavi_ord - costi_deducibili
    imposte_ord = reddito_ord * 0.23 if reddito_ord > 0 else 0
    netto_ord = incassi_lordi - imposte_ord

    # --- Tabella di confronto ---
    df = pd.DataFrame({
        "Voce": [
            "Incassi lordi",
            "Ricavi netti (scorporati IVA)",
            "Costi deducibili",
            "IVA detraibile",
            "Reddito imponibile",
            "Imposte",
            "Utile netto"
        ],
        "Forfettario (€)": [
            incassi_lordi,
            incassi_lordi,
            0,
            0,
            reddito_forf,
            imposte_forf,
            netto_forf
        ],
        "Ordinario (€)": [
            incassi_lordi,
            ricavi_ord,
            costi_deducibili,
            iva_detraibile,
            reddito_ord,
            imposte_ord,
            netto_ord
        ]
    })

    return df.to_dict(orient="records")
