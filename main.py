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
    # Ottenere il coefficiente di redditività dal codice ATECO
    coeff_ateco = get_coefficiente_by_ateco(codice_ateco)
    descrizione_attivita = get_descrizione_by_ateco(codice_ateco)
    
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
        ded = imponibile * regole[categoria]["deducibilfrom fastapi import FastAPI
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

# Endpoint aggiuntivo per cercare codici ATECO
@app.get("/cerca-ateco")
def cerca_codici_ateco(query: str = ""):
    """
    Cerca codici ATECO per parola chiave nella descrizione
    """
    if not query:
        return {"errore": "Inserisci una parola chiave per la ricerca"}
    
    query_lower = query.lower()
    risultati = []
    
    for codice, info in CODICI_ATECO.items():
        if query_lower in info["descrizione"].lower():
            risultati.append({
                "codice": codice,
                "descrizione": info["descrizione"],
                "coefficiente": f"{info['coefficiente'] * 100}%"
            })
    
    return {
        "query": query,
        "risultati_trovati": len(risultati),
        "codici_ateco": risultati[:20]  # Limitiamo a 20 risultati
    }

# Endpoint per ottenere tutti i settori e coefficienti
@app.get("/settori-coefficienti")
def settori_coefficienti():
    """
    Restituisce un riepilogo dei settori con i rispettivi coefficienti
    """
    settori = {
        "Industrie alimentari e delle bevande": {
            "coefficiente": "40%",
            "codici_esempio": ["10.11.00", "10.52.00", "11.05.00"],
            "descrizione": "Produzione, lavorazione e conservazione di alimenti e bevande"
        },
        "Commercio all'ingrosso e al dettaglio": {
            "coefficiente": "40%",
            "codici_esempio": ["45.11.00", "47.11.00", "47.24.00"],
            "descrizione": "Vendita di beni al dettaglio e all'ingrosso, inclusi autoveicoli"
        },
        "Commercio ambulante alimentare": {
            "coefficiente": "40%",
            "codici_esempio": ["47.81.00", "47.82.00"],
            "descrizione": "Commercio su aree pubbliche di prodotti alimentari e bevande"
        },
        "Commercio ambulante non alimentare": {
            "coefficiente": "54%",
            "codici_esempio": ["47.89.00", "47.99.00"],
            "descrizione": "Commercio su aree pubbliche di altri prodotti"
        },
        "Intermediari del commercio": {
            "coefficiente": "62%",
            "codici_esempio": ["46.11.00", "46.17.00", "46.19.00"],
            "descrizione": "Intermediazione commerciale per conto terzi"
        },
        "Costruzioni e attività immobiliari": {
            "coefficiente": "86%",
            "codici_esempio": ["41.20.00", "43.21.00", "68.31.00"],
            "descrizione": "Costruzioni, installazioni e servizi immobiliari"
        },
        "Servizi di alloggio e ristorazione": {
            "coefficiente": "40%",
            "codici_esempio": ["55.10.00", "56.10.11", "56.30.00"],
            "descrizione": "Hotel, ristoranti, bar e servizi di ristorazione"
        },
        "Attività professionali e consulenze": {
            "coefficiente": "78%",
            "codici_esempio": ["69.10.00", "69.20.00", "74.10.00"],
            "descrizione": "Servizi legali, contabili, consulenze e attività professionali"
        },
        "Attività sanitarie e assistenziali": {
            "coefficiente": "78%",
            "codici_esempio": ["86.22.00", "86.90.30", "87.10.00"],
            "descrizione": "Servizi medici, sanitari e di assistenza sociale"
        },
        "Istruzione e formazione": {
            "coefficiente": "78%",
            "codici_esempio": ["85.20.00", "85.52.00", "85.53.00"],
            "descrizione": "Servizi di istruzione, formazione e corsi"
        },
        "Attività finanziarie e assicurative": {
            "coefficiente": "78%",
            "codici_esempio": ["64.92.00", "65.12.00", "66.22.00"],
            "descrizione": "Servizi finanziari, assicurativi e di intermediazione"
        },
        "Altre attività economiche": {
            "coefficiente": "67%",
            "codici_esempio": ["Codici non classificati sopra"],
            "descrizione": "Tutte le altre attività non rientranti nelle categorie precedenti"
        }
    }
    
    return settori

# Endpoint per ottenere informazioni su un codice ATECO specifico
@app.get("/info-ateco/{codice}")
def info_codice_ateco(codice: str):
    """
    Restituisce informazioni dettagliate su un codice ATECO specifico
    """
    if codice in CODICI_ATECO:
        return {
            "codice": codice,
            "descrizione": CODICI_ATECO[codice]["descrizione"],
            "coefficiente_redditivita": f"{CODICI_ATECO[codice]['coefficiente'] * 100}%",
            "valido": True
        }
    else:
        return {
            "codice": codice,
            "descrizione": "Codice ATECO non trovato nel database",
            "coefficiente_redditivita": "67% (coefficiente generico)",
            "valido": False,
            "note": "Verrà applicato il coefficiente generico del 67% per attività non classificate"
        }
