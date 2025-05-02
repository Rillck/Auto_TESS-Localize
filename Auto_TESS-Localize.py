import os
import pandas as pd
import numpy as np
import lightkurve as lk
import astropy.units as u
import matplotlib.pyplot as plt
import TESS_Localize as tl  # módulo Localize
from astroquery.vizier import Vizier
from astroquery.mast import Catalogs
from astropy.coordinates import SkyCoord
import inquirer
import warnings

plt.rcParams['font.family'] = 'Times New Roman'

# Ocultar warnings de sqrt inválido
warnings.filterwarnings("ignore", message=".*invalid value encountered in sqrt.*")

# Criar pasta
pasta_imagens = "TESS-Localize images"
os.makedirs(pasta_imagens, exist_ok=True)

# Função para obter o Gaia DR3 source_id de um TIC
def obter_gaia_dr3_source_do_tic(tic_id, radius_arcsec=5):
    try:
        mast_result = Catalogs.query_object(f'TIC {tic_id}', catalog='TIC')
        if len(mast_result) == 0:
            return None

        ra = mast_result[0]['ra']
        dec = mast_result[0]['dec']
        coord = SkyCoord(ra=ra * u.deg, dec=dec * u.deg)

        Vizier.ROW_LIMIT = 10
        catalog_id = "I/355/gaiadr3"
        result = Vizier.query_region(coord, radius=radius_arcsec * u.arcsec, catalog=catalog_id)

        if result and len(result[catalog_id]) > 0:
            return str(result[catalog_id][0]['Source'])
        else:
            return None
    except Exception as e:
        print(f"Erro ao consultar Gaia DR3 para TIC {tic_id}: {e}")
        return None

# Função principal
def verificar_alvo(lista_tics_periodos):
    total = len(lista_tics_periodos)
    resultados = []

    for idx, (tic, setor, period) in enumerate(lista_tics_periodos, 1):
        progresso = int((idx / total) * 100)
        print(f'\n🔍 Analyzing TIC {tic} - Sector {setor} - Period {period:.4f} days')

        try:
            search = lk.search_targetpixelfile(f'TIC {tic}', mission='TESS', sector=setor, exptime=120)
            tpf = search.download()
            if tpf is None:
                print("⚠️ TPF not found.")
                continue

            frequency = 1 / period
            localizador = tl.Localize(tpf, frequencies=[frequency], frequnit=u.day**-1)
            gaia_source_tic = obter_gaia_dr3_source_do_tic(tic)

            if hasattr(localizador, 'starfit') and localizador.starfit is not None and not localizador.starfit.empty:
                melhor_source = str(localizador.starfit.iloc[0]['source'])
                match = melhor_source == str(gaia_source_tic)
                print(f"✅ Best Gaia Source: {melhor_source} | TIC-associated Source: {gaia_source_tic} | Match: {'Yes' if match else 'No'}")
            else:
                melhor_source = None
                match = False
                print("⚠️ No Gaia match found.")

            nome_base = f"{tic}_{setor}"
            path_snr = os.path.join(pasta_imagens, f"{nome_base}_SNR.png")
            path_lc = os.path.join(pasta_imagens, f"{nome_base}_LCfit.png")

            # SNR Image
            plt.figure(figsize=(6, 6))
            plt.imshow(localizador.heatmap, origin='lower', cmap='viridis')
            if localizador.gaiadata is not None:
                cores = ['red' if str(s) == str(gaia_source_tic) else 'white' for s in localizador.gaiadata['source']]
                plt.scatter(localizador.gaiadata['x'], localizador.gaiadata['y'],
                            s=localizador.gaiadata['size'] * 5, c=cores, alpha=0.6, edgecolors='k')
            plt.scatter(localizador.location[0], localizador.location[1], marker='X', c='black', s=70)
            plt.title('SNR')
            plt.xlim(-0.5, localizador.aperture.shape[1] - 0.5)
            plt.ylim(-0.5, localizador.aperture.shape[0] - 0.5)
            plt.savefig(path_snr, bbox_inches='tight',dpi=300)
            plt.close()

            # Light Curve Fit
            localizador.plot_lc(save=path_lc)

            p_value = None
            rel_likelihood = None
            if localizador.starfit is not None and not localizador.starfit.empty and match:
                linha = localizador.starfit[localizador.starfit['source'] == melhor_source]
                if not linha.empty:
                    p_value = linha.iloc[0]['pvalue']
                    rel_likelihood = linha.iloc[0]['relative likelihood']

            resultados.append({
                'TIC': tic,
                'Sector': setor,
                'Period (day)': period,
                'Frequency (1/day)': frequency,
                'Source Gaia DR3 (TIC)': gaia_source_tic,
                'Best Gaia Source (Localize)': melhor_source,
                'p-value': p_value,
                'Relative Likelihood': rel_likelihood,
                'Match?': 'Yes' if match else 'No'
            })

        except Exception as e:
            print(f'❌ Error processing TIC {tic}: {e}')
            resultados.append({
                'TIC': tic,
                'Sector': setor,
                'Period (days)': period,
                'Error': str(e)
            })

    return pd.DataFrame(resultados)

# Entrada por prompt (seleção do arquivo .txt)
if __name__ == "__main__":
    arquivos_disponiveis = [f for f in os.listdir() if f.endswith('.txt')]
    pergunta = [
        inquirer.List('arquivo', message="Select a target file (.txt)", choices=arquivos_disponiveis)
    ]
    resposta = inquirer.prompt(pergunta)

    if resposta is None:
        print("❌ No file selected. Exiting.")
        exit()

    arquivo_escolhido = resposta['arquivo']
    df_targets = pd.read_csv(arquivo_escolhido)
    lista = list(zip(df_targets['TIC'], df_targets['Sector'], df_targets['Period']))
    df_resultados = verificar_alvo(lista)
    df_resultados.to_csv("result Auto TESS_Localize.csv", index=False)

