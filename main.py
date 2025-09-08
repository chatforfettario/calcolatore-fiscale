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
    imposta_sostitutiva_15: float = 0.15,
    imposta_sostitutiva_5: float = 0.05
):
    # Coefficiente redditività ATECO (demo)
    coeff_ateco = 0.40 if codice_ateco == "56.10.30" else 0.67
    
    # --- FORFETTARIO 15% ---
    reddito_forf_15 = incassi_lordi * coeff_ateco
    imposte_forf_15 = reddito_forf_15 * imposta_sostitutiva_15
    netto_forf_15 = incassi_lordi - imposte_forf_15
    
    # --- FORFETTARIO AGEVOLATO 5% ---
    reddito_forf_5 = incassi_lordi * coeff_ateco
    imposte_forf_5 = reddito_forf_5 * imposta_sostitutiva_5
    netto_forf_5 = incassi_lordi - imposte_forf_5
    
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
        "Forfettario 15% (€)": [
            incassi_lordi,
            incassi_lordi,
            0,
            0,
            reddito_forf_15,
            imposte_forf_15,
            netto_forf_15
        ],
        "Forfettario 5% (€)": [
            incassi_lordi,
            incassi_lordi,
            0,
            0,
            reddito_forf_5,
            imposte_forf_5,
            netto_forf_5
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
    
    # Calcolo del risparmio fiscale
    risparmio_5_vs_15 = netto_forf_5 - netto_forf_15
    risparmio_5_vs_ord = netto_forf_5 - netto_ord
    risparmio_15_vs_ord = netto_forf_15 - netto_ord
    
    risultato = {
        "tabella_confronto": df.to_dict(orient="records"),
        "analisi_risparmio": {
            "forfettario_5_vs_15": {
                "risparmio_euro": risparmio_5_vs_15,
                "risparmio_percentuale": (risparmio_5_vs_15 / netto_forf_15 * 100) if netto_forf_15 > 0 else 0
            },
            "forfettario_5_vs_ordinario": {
                "risparmio_euro": risparmio_5_vs_ord,
                "risparmio_percentuale": (risparmio_5_vs_ord / netto_ord * 100) if netto_ord > 0 else 0
            },
            "forfettario_15_vs_ordinario": {
                "risparmio_euro": risparmio_15_vs_ord,
                "risparmio_percentuale": (risparmio_15_vs_ord / netto_ord * 100) if netto_ord > 0 else 0
            }
        },
        "regime_piu_conveniente": max(
            [("Forfettario 5%", netto_forf_5), 
             ("Forfettario 15%", netto_forf_15), 
             ("Ordinario", netto_ord)],
            key=lambda x: x[1]
        )[0]
    }
    
    return risultato

# Endpoint aggiuntivo per info sui regimi forfettari
@app.get("/info-forfettari")
def info_regimi_forfettari():
    return {
        "forfettario_15": {
            "aliquota": "15%",
            "limite_ricavi": 65000,
            "esenzione_iva": True,
            "contabilita_semplificata": True,
            "note": "Regime standard forfettario"
        },
        "forfettario_5": {
            "aliquota": "5%",
            "limite_ricavi": 65000,
            "durata_agevolazione": "5 anni",
            "requisiti": [
                "Nuova attività (non esercitata nei 3 anni precedenti)",
                "Non essere stati dipendenti/collaboratori negli ultimi 3 anni nel settore di attività",
                "Attività non costituisca prosecuzione di altra precedentemente esercitata"
            ],
            "esenzione_iva": True,
            "contabilita_semplificata": True,
            "note": "Regime agevolato per startup"
        }
    }
