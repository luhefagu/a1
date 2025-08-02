import regex as re
from pyscript import document
from datetime import datetime
import unicodedata

def analizar_indicacion(event):
    input_text = document.querySelector("#indicacion")
    indicacion = input_text.value
    output_div = document.querySelector("#output")
    output_div.innerText = analizar_indicacion_medica(indicacion)

# --- Funciones de análisis y procesamiento ---
traducciones = {
    "aas": "acido acetilsalicilico",
    "tranexamico": "acido tranexamico",
    "antiespasmodico": "viadil",
    "unasyn": "ampicilina sulbactam",
    "ampi sulba": "ampicilina sulbactam",
    "ampi-sulba": "ampicilina sulbactam",
    "ampi/sulba": "ampicilina sulbactam",
    "ampicilina sulba": "ampicilina sulbactam",
    "ampicilina-sulba": "ampicilina sulbactam",
    "ampicilina/sulba": "ampicilina sulbactam",
    "ampi sulbactam": "ampicilina sulbactam",
    "ampi-sulbactam": "ampicilina sulbactam",
    "ampi/sulbactam": "ampicilina sulbactam",
    "ampicilina-sulbactam": "ampicilina sulbactam",
    "ampicilina/sulbactam": "ampicilina sulbactam",
    "butilescopolamina": "buscapina",
    "butil-escopolamina": "buscapina",
    "butil escopolamina": "buscapina",
    "escopolamina": "buscapina",
    "ferinject": "hierro carboximaltosa",
    "fierro carboximaltosa": "hierro carboximaltosa",
    "carboximaltosa fierro": "hierro carboximaltosa",
    "carboximaltosa hierro": "hierro carboximaltosa",
    "cefta avibactam": "ceftazidima avibactam",
    "cefta-avibactam": "ceftazidima avibactam",
    "cefta/avibactam": "ceftazidima avibactam",
    "cefta avi": "ceftazidima avibactam",
    "cefta-avi": "ceftazidima avibactam",
    "cefta/avi": "ceftazidima avibactam",
    "acantex": "ceftriaxona",
    "haldol": "haloperidol",
    "imipenem": "imipenem cilastatina",
    "imi cilastatina": "imipenem cilastatina",
    "imi-cilastatina": "imipenem cilastatina",
    "imi/cilastatina": "imipenem cilastatina",
    "imipenem-cilastatina": "imipenem cilastatina",
    "imipenem/cilastatina": "imipenem cilastatina",
    "KCl": "cloruro de potasio",
    "cloruro potasio": "cloruro de potasio",
    "precedex": "dexmedetomidina",
    "adrenalina": "epinefrina",
    "EPO": "eritropoyetina",
    "fentanilo": "fentanil",
    "fentanyl": "fentanil",
    "venofer": "hierro sacarato",
    "fierro sacarato": "hierro sacarato",
    "sacarato fierro": "hierro sacarato",
    "sacarato hierro": "hierro sacarato",
    "vitamina k": "fitoquinona",
    "vit k": "fitoquinona",
    "KH2PO4": "fosfato monopotasico",
    "monofosfato potasio": "fosfato monopotasico",
    "cedilanid": "lanatosido c",
    "lanatosido": "lanatosido c",
    "levosulpirida": "levosulpiride",
    "petidina": "meperidina",
    "sf": "suero fisiologico 0.9%",
    "acetaminofeno": "paracetamol",
    "acetaminofen": "paracetamol",
    'paracetamol': 'paracetamol',
    'noradrenalina': 'noradrenalina',
    'sg5%': 'suero glucosado 5%',
    'metamizol': 'metamizol',
    'heparina': 'heparina',
    'suero ringer lactato': 'suero ringer lactato',
    'labetalol': 'labetalol',
    'albumina 5%': 'albumina 5%',
    'kcl 10%': 'cloruro potasio 10%',
    'sulfato magnesio 20%': 'sulfato magnesio 20%',
    'sulfato magnesio 25%': 'sulfato magnesio 25%',
    'sg': 'suero glucosado',
    'agua bidestilada': 'agua bidestilada',
    'bicarbonato': 'bicarbonato sodio',
    'lidocaina': 'lidocaina',
    'aminoacidos 15%': 'aminoacidos 15%',
    'tiamina': 'tiamina',
    'oligoelementos': 'oligoelementos',
    'mvb 12': 'mvb 12',
    'aminoacidos 10%': 'aminoacidos 10%',
    'mvi': 'mvi 12',
    'fosfato de potasio': 'fosfato monopotasico',
    'mgso4': 'sulfato magnesio',
    'sg 10%': 'suero glucosado 10%',
    'aminoacidos 5%': 'aminoacidos 5%',
    'kh2po4': 'fosfato monopotasico',
    'lidocaina 2%': 'lidocaina 2%',
    'tramadol': 'tramadol',
    'ketorolaco': 'ketorolaco',
    'agua esteril': 'agua bidestilada',
    'bicarbonato 2/3 molar': 'bicarbonato 2/3 molar',
    'bicarbonato 2/3 m': 'bicarbonato 2/3 molar',
    'bicarbonato 2/3m': 'bicarbonato 2/3 molar',
    'lactulosa': 'lactulosa',
    'ac. tranexamico': 'acido tranexamico',
    'milrinona': 'milrinona',
    'furosemida': 'furosemida',
    'cefazolina': 'cefazolina',
    'entecavir': 'entecavir',
    'metadona': 'metadona',
    'eutirox': 'levotiroxina',
    'omeprazol': 'omeprazol',
    'quetiapina': 'quetiapina',
    'gabapentina': 'gabapentina',
    'haldol': 'haloperidol',
    'timolol 0.5%': 'timolol 0.5%',
    'phoslo': 'acetato calcio',
    'vitamina d': 'colecalciferol',
    'espironolactona': 'espironolactona',
    'acido ursodeoxicolico': 'acido ursodeoxicolico',
    'rifaximina': 'rifaximina',
    'elcal d 800/500': 'elcal d 800/500',
    'bonavid': 'colecalciferol',
    'esomeprazol': 'esomeprazol',
    'sf 0.9%': 'suero fisiológico 0.9%',
    'ampicilina/sulbactam': 'ampicilina sulbactam',
    'suero premezclado': 'suero premezclado',
    'melatonina': 'melatonina',
    'risperidona': 'risperidona',
    'sertralina': 'sertralina',
    'lorazepam': 'lorazepam',
    'clonazepam': 'clonazepam',
    'vancomicina': 'vancomicina',
    'tigeciclina': 'tigeciclina',
    'anidulafungina': 'anidulafungina',
    'cotrimoxazol forte': 'cotrimoxazol forte',
    'enoxaparina': 'enoxaparina',
    'ondansetron': 'ondansetron',
    'hidrocortisona': 'hidrocortisona',
    'losartan': 'losartan',
    'amlodipino': 'amlodipino',
    'carvedilol': 'carvedilol',
    'gluconato de calcio 10%': 'gluconato calcio 10%',
    'citrato de calcio': 'citrato calcio',
    'calcitriol': 'calcitriol',
    'bicarbonato de sodio': 'bicarbonato sodio',
    'spm': 'suero premezclado',
    'imipenem': 'imipenem cilastatina',
    'odanex': 'ondansetron',
    'amoxicilina': 'amoxicilina',
    'medicamento x': 'no existe',
    'fentanil': 'fentanil',
    'zopiclona': 'zopiclona',
    'ibuprofeno': 'ibuprofeno',
    'farmacoz': 'no existe',
    'farmacoa': 'no existe',
    'suero fisiologico 0.9%': 'suero fisiologico 0.9%',
    'vitamina c': 'vitamina c',
    'solucion nutritiva': 'no existe',
    'medicamento z': 'no existe',
    'nad': 'noradrenalina',
    }

### Importa diccionario personalizado de nombres de medicamentos
traducciones_uptodate = {}
traducciones_uptodate.update(traducciones)

def estandarizar_nombres (nombre_entrada, diccionario = traducciones_uptodate):
    try:
        return diccionario[nombre_entrada]
    except:
        return nombre_entrada
        
def revisar_nombres (resultado):
    resultado["solucion_base"]["nombre"] = estandarizar_nombres(resultado["solucion_base"]["nombre"])
    for aditivo in resultado["aditivos_info"]:
        aditivo["nombre"] = estandarizar_nombres(aditivo["nombre"])
    return resultado

def parse_fraction(s):
    """
    Convierte una cadena que representa una cantidad (ej. '1/2', '1/3', '1/4') a un número float
    Maneja enteros, floats, fracciones
    """
    # Revisa si es número --> lo devuelve directo
    if isinstance(s, (int, float)):
        return s
    # Calcular fracciones --> float
    s = str(s).lower().strip()
    if '/' in s:
        parts = s.split('/')
        if len(parts) == 2:
            try:
                num = float(parts[0].replace(',', '.'))
                den = float(parts[1].replace(',', '.'))
                if den != 0:
                    return num / den
            except ValueError:
                pass
    # Elimina los puntos de miles 
    # Revisa si después de un punto hay 2 digito(s) + 1 cero al final --> lo más probable es que sea de miles
    try:
        s = s.replace(" ", "")

        if ',' in s:
            s_processed = s.replace(".", "").replace(",", ".")
        else:
            num_periods = s.count('.')

            if num_periods == 0:
                s_processed = s
            elif num_periods == 1:
                if re.match(r'^\d+\.\d{2}[0]{1}$', s):
                    s_processed = s.replace(".", "")
                else:
                    s_processed = s
            else:
                parts = s.split('.')
                s_processed = "".join(parts[:-1]) + "." + parts[-1]
        
        return float(s_processed)

    except ValueError:
        pass

def parse_date_and_duration(text):
    """
    Parameters
    ----------
    text : str
        Texto que contiene fecha de inicio y/o duración

    Returns
    -------
    fi_date : datetime
        Cálcula fecha de inicio de fármaco.
    duration_days : int
        Cálcula los días de duración de un medicamento.

    """
    fi_date = None
    duration_days = None

    fi_match = re.search(r"fi(?:\s*:\s*|\s*)(\d{1,2}\/\d{1,2}(?:\/\d{2,4})?)", text, re.IGNORECASE)
    if fi_match:
        fi_raw = fi_match.group(1)
        # Permanece la cadena original si está malformada, como se solicitó
        try:
            # Intentar parsear para validar, pero mantener raw si falla
            if len(fi_raw.split('/')) == 2: # dd/mm
                fi_date = datetime.strptime(fi_raw + f"/{datetime.now().year}", "%d/%m/%Y")
                if fi_date > datetime.now(): # evita que se contabilice por error algo iniciado el año anterior
                    fi_date = datetime.strptime(fi_raw + f"/{datetime.now().year-1}", "%d/%m/%Y")
            else: # dd/mm/yyyy o dd/mm/yy
                fi_date = datetime.strptime(fi_raw, "%d/%m/%Y")
        except ValueError:
            fi_date = fi_raw # Mantener la cadena original malformada
    
    duration_match = re.search(r"por\s+(\d+)\s*(dias|dia|d|semanas|semana|sem|meses|mes|m)", text, re.IGNORECASE)
    if duration_match:
        value = int(duration_match.group(1))
        unit = duration_match.group(2).lower()
        if unit in ["dias", "dia", "d"]:
            duration_days = value
        elif unit in ["semanas", "semana", "sem"]:
            duration_days = value * 7
        elif unit in ["meses", "mes", "m"]:
            duration_days = value * 30 # Aproximación

    return fi_date, duration_days

def _normalize_dia_semana(dia_semana):
    """
    Normaliza los dias de la semana
    Parameters
    ----------
    dia_semana : srt
        srt que contiene dias de la semana, que requieren ser uniformados

    Returns
    -------
    dia_semana : srt
        Devuelve srt con dias estandarizadas

    """
    dia_semana = dia_semana.lower().strip()
    if dia_semana in ["lunes","lun", "lu", "l"]: return "lunes"
    if dia_semana in ["martes", "mar", "ma"]: return "martes"
    if dia_semana in ["miercoles", "mier", "mie", "mi"]: return "miercoles"
    if dia_semana in ["jueves", "jue", "ju", "j"]: return "jueves"
    if dia_semana in ["viernes", "vie", "vi", "v"]: return "viernes"
    if dia_semana in ["sabado", "sab", "sa", "s"]: return "sabado"
    if dia_semana in ["domingo", "dom", "do", "d"]: return "domingo"
    return dia_semana

def _normalize_unit(unit):
    """
    Normaliza las unidades de uso más frecuente para evitar confusiones
    Parameters
    ----------
    unit : str
        Texto que contiene unidad según analizador sintáctico, pero que requiere ser uniformada

    Returns
    -------
    unit : str
        Devuelve str con unidades estandarizadas

    """
    unit = unit.lower().strip()
    if unit in ["microgramos","microgramo", "gamas", "gama", "ug", "mcg"]: return "ug"
    if unit in ["miligramos", "miligramo", "mgrs", "mgr", "mg"]: return "mg"
    if unit in ["gramos", "gramo", "grs", "gr", "g"]: return "gr"
    if unit in ["mililitros", "mililitro", "ml", "mls", "ml.", "cc", "cm3"]: return "ml"
    if unit in ["litros", "litro", "l", "ls", "l.", "lts", "lt"]: return "lt"
    if unit in ["ui", "u", "unidades", "unidades internacionales"]: return "UI"
    if unit in ["comprimido", "comprimidos", "comps", "comp.", "comp", "cp"]: return "comprimido"
    if unit in ["capsula", "capsulas", "cap"]: return "capsula"
    if unit in ["tableta", "tabletas", "tab"]: return "tableta"
    if unit in ["gota", "gotas"]: return "gota"
    if unit in ["ampolla", "ampollas", "amp", "amp.", "amps", "amp/"]: return "ampolla"
    if unit in ["vial", "viales"]: return "vial"
    if unit in ["jeringa", "jeringas"]: return "jeringa"
    if unit in ["sachet", "sachets"]: return "sachet"
    if unit in ["puff", "puffs"]: return "puff"
    if unit in ["inhalacion", "inhalaciones", "inh"]: return "inhalacion"
    if unit in ["nebulizacion", "nebulizaciones"]: return "nebulizacion"
    if unit in ["supositorio", "supositorios"]: return "supositorio"
    if unit in ["ovulo", "ovulos"]: return "ovulo"
    if unit in ["aplicacion", "aplicaciones"]: return "aplicacion"    
    if unit in ["enema", "enemas"]: return "enema"
    if unit in ["hrs", "hr", "horas", "hora", "h" ]: return "hora"
    if unit in ["min", "min.", "mins", "minuto", "minutos"]: return "min"
    if unit in ["seg", "seg.", "segs", "segundo", "segundos" ]: return "seg"
    if unit in ["dia", "d", "dias"]: return "dia"
    if unit in ["sem", "semana", "semanas", "semanal"]: return "sem"
    if unit in ["mes", "meses", "mensual"]: return "mes"
    return unit

def _compatibilidad_unidades (unidad_1, unidad_2):
    if unidad_1 and unidad_2 in ["ug", "mg", "gr", "kg"]:
        return True, "gr"
    if unidad_1 and unidad_2 in ["ml", "lt"]:
        return True, "lt"
    if unidad_1 and unidad_2 in ["seg", "min", "hora", "dia", "semana", "mes"]:
        return True, "tiempo"
    if unidad_1 and unidad_2 in ["comprimido", "capsula", "tableta"]:
        return True, "comp-oral"
    return False, None

def _get_daily_frequency_multiplier(frequency_text):
    frequency_text = frequency_text.lower().strip()
    if "cada" in frequency_text:
        match = re.search(r"cada\s*(\d+)\s*(hrs|hr|horas|hora|h)", frequency_text)
        if match:
            hours = int(match.group(1))
            if hours > 0:
                return 24 / hours
        match = re.search(r"cada\s*(\d+)\s*(dias|dia|d)", frequency_text)
        if match:
            days = int(match.group(1))
            if days > 0:
                return 1 / days
    elif "vez al dia" in frequency_text or "qd" in frequency_text or "diario" in frequency_text:
        return 1
    elif "veces al dia" in frequency_text:
        match = re.search(r"(\d+)\s*veces al dia", frequency_text)
        if match:
            return int(match.group(1))
    elif "cada 12" in frequency_text: return 2
    elif "cada 8" in frequency_text: return 3
    elif "cada 6" in frequency_text: return 4
    elif "cada 4" in frequency_text: return 6
    elif "cada 24" in frequency_text: return 1
    elif "cada 48" in frequency_text: return 0.5
    # Añadir más patrones de frecuencia según sea necesario
    return None

def calculate_total_daily_dose_from_pauta(
    dosis_cantidad, dosis_unidad, frecuencia_tipo, frecuencia_valor, frecuencia_unidad_tiempo
):
    if not (dosis_cantidad and dosis_unidad and frecuencia_tipo and frecuencia_valor and frecuencia_unidad_tiempo):
        return None, None

    normalized_dosis_unidad = _normalize_unit(dosis_unidad)

    daily_multiplier = None
    if frecuencia_tipo == "cada":
        if frecuencia_unidad_tiempo == "hora" and frecuencia_valor > 0:
            daily_multiplier = 24 / frecuencia_valor
        elif frecuencia_unidad_tiempo == "dia" and frecuencia_valor > 0:
            daily_multiplier = 1 / frecuencia_valor
    elif frecuencia_tipo == "veces al dia":
        daily_multiplier = frecuencia_valor
    elif frecuencia_tipo == "diario":
        daily_multiplier = 1
    # Añadir más lógicas de frecuencia si es necesario

    if daily_multiplier is not None:
        total_daily_dose = dosis_cantidad * daily_multiplier
        return total_daily_dose, normalized_dosis_unidad
    return None, None

def remove_accents(input_str):
    if input_str is None:
        return None
    nfkd_form = unicodedata.normalize('NFKD', input_str)
    # nfkd_form.replace("n~", "ñ")
    return "".join([c for c in nfkd_form if not unicodedata.combining(c)])

def clean_and_normalize_text(text):
    """Limpia el texto, elimina múltiples espacios y espacios al inicio/final."""
    if text is None:
        return ""
    text = str(text).lower()
    text = re.sub(r'\s+', ' ', text).strip()
    return text

lista_nombres = []

def analizar_indicacion_medica(indicacion_medica):
    print (indicacion_medica)

    indicacion_original = indicacion_medica
    processed_indicacion = remove_accents(indicacion_medica.lower())
    temp_indicacion = processed_indicacion 

    resultados = {
        "solucion_base": {"nombre": None, "cantidad": None, "unidad": None},
        "aditivos_info": [],
        "frecuencia_tipo": None,
        "frecuencia_valor": None,
        "frecuencia_unidad_tiempo": None,
        "frecuencia_dia_semana": None,
        "via_administracion": None,
        "forma_administracion": None,
        "velocidad_infusion_cantidad": None,
        "velocidad_infusion_unidad_dosis": None,
        "velocidad_infusion_unidad_tiempo": None,
        "tiempo_infusion_cantidad": None,
        "tiempo_infusion_unidad": None,
        "condicion_administracion": None,
        "condicion_ma": None,
        "duracion_tratamiento_dias": None,
        "observaciones": None,
        "fecha_inicio_tratamiento": None
    }

    # 1. Extraer fecha de inicio y duración
    fi_date, duration_days = parse_date_and_duration(temp_indicacion)
    resultados["fecha_inicio_tratamiento"] = fi_date
    resultados["duracion_tratamiento_dias"] = duration_days
    if fi_date:
        temp_indicacion = re.sub(r"fi(?:\s*:\s*|\s*)" + re.escape(str(fi_date).lower()), " ", temp_indicacion, flags=re.IGNORECASE).strip()
    if duration_days:
        duration_match = re.search(r"por\s+(\d+)\s*(dias|dia|d|semanas|semana|sem|meses|m)", temp_indicacion, re.IGNORECASE)
        # if duration_match:
        #     temp_indicacion = re.sub(re.escape(duration_match.group(0)), " ", temp_indicacion, flags=re.IGNORECASE, count=1).strip()

    # 2. Extraer Aditivo y Solución Base Combinados (ej. "Noradrenalina 4 mg/250 mL SG5%")
    # Patrón: [medicamento] [dosis] / [volumen] [solución base]
    ADITIVO_DILUCION_SLASH_PATTERN = re.compile(
        r"(?:bic\s*de|bic\s+)?([a-zA-ZñÑ.\s]+?)\s*(\d+(?:[.,]\d+)?|\d+\/\d+|\½)\s*(mg|gr|g|ug|mcg|UI|unidades)\s*\/\s*"
        r"(\d+(?:[.,]\d+)?|\d+\/\d+|\½)\s*(ml|cc|L|litros)\s*([a-zA-ZñÑ\s\d%]+?)(?:[\s,.]|$)", 
        re.IGNORECASE
    )

    match_slash_dilution = ADITIVO_DILUCION_SLASH_PATTERN.search(temp_indicacion)
    if match_slash_dilution:
        try:
            aditivo_nombre = clean_and_normalize_text(match_slash_dilution.group(1))
            aditivo_cantidad = parse_fraction(match_slash_dilution.group(2))
            aditivo_unidad = _normalize_unit(match_slash_dilution.group(3))
            
            solucion_base_cantidad = parse_fraction(match_slash_dilution.group(4))
            solucion_base_unidad = _normalize_unit(match_slash_dilution.group(5))
            solucion_base_nombre = clean_and_normalize_text(match_slash_dilution.group(6))

            resultados["aditivos_info"].append({
                "nombre": aditivo_nombre,
                "dosis_cantidad": aditivo_cantidad,
                "dosis_unidad": aditivo_unidad,
            })
            resultados["solucion_base"] = {
                "nombre": solucion_base_nombre,
                "cantidad": solucion_base_cantidad,
                "unidad": solucion_base_unidad
            }
            """
            Agregar nombres al listado de nombres
            """
            lista_nombres.append(aditivo_nombre)
            lista_nombres.append(solucion_base_nombre)
            #########
            #########
            
            temp_indicacion = re.sub(re.escape(match_slash_dilution.group(0)), " ", temp_indicacion, flags=re.IGNORECASE, count=1).strip()
            temp_indicacion = re.sub(r'\s+', ' ', temp_indicacion).strip()
        except IndexError:
            pass # Fallback to other patterns if this one fails to parse groups

    # 3. Extraer velocidad de infusión (VI) - Incluye ug/Kg/hr
    VI_PATTERNS = [
        # Para ug/kg/hr - 4 grupos de captura
        r"(?:iniciar\s*a|iniciar|\ba\s*pasar\s*a|pasar\s*a|\ba)?\s*(\d+(?:[.,]\d+)?)\s*(ug|mcg)\s*\/\s*(kg|kgs)\s*\/\s*(hrs|hr|horas|hora|h|minuto|min)",
        # Existing: for simpler units
        r"(?:iniciar\s*a|iniciar|\ba\s*pasar\s*a|pasar\s*a|\ba)?\s*(\d+(?:[.,]\d+)?)\s*(mg|gr|g|ug|mcg|ml|cc|unidades|UI)\s*\/\s*(hrs|hr|horas|hora|h)",
        r"(?:iniciar\s*a|iniciar|\ba\s*pasar\s*a|pasar\s*a|\ba)?\s*(\d+(?:[.,]\d+)?)\s*(mg|gr|g|ug|mcg|ml|cc|unidades|UI)\s*(?:por)?\s*(min|mins|minuto|minutos)",
        r"(?:iniciar\s*a|iniciar|\ba\s*pasar\s*a|pasar\s*a|\ba)?\s*(\d+(?:[.,]\d+)?)\s*(ml|cc|gotas)\s*\/\s*(hrs|hr|horas|h|minutos|minuto|mins|min)"
    ]

    chosen_vi_match = None
    for pattern in VI_PATTERNS:
        match = re.search(pattern, temp_indicacion, re.IGNORECASE)
        if match:
            chosen_vi_match = match
            break

    if chosen_vi_match:
        resultados["velocidad_infusion_cantidad"] = parse_fraction(chosen_vi_match.group(1))
        # Logic for ug/kg/hr vs others
        # Check if it's the ug/kg/hr pattern by checking group count and content
        if len(chosen_vi_match.groups()) == 4 and chosen_vi_match.group(2).lower() in ['ug', 'mcg'] and chosen_vi_match.group(3).lower() == 'kg':
            resultados["velocidad_infusion_unidad_dosis"] = f"{_normalize_unit(chosen_vi_match.group(2))}/{chosen_vi_match.group(3).lower()}"
            resultados["velocidad_infusion_unidad_tiempo"] = _normalize_unit(chosen_vi_match.group(4))
        else:
            resultados["velocidad_infusion_unidad_dosis"] = _normalize_unit(chosen_vi_match.group(2))
            resultados["velocidad_infusion_unidad_tiempo"] = _normalize_unit(chosen_vi_match.group(3))
        
        try:
            temp_indicacion = re.sub(re.escape(" a pasar"+chosen_vi_match.group(0)), " ", temp_indicacion, flags=re.IGNORECASE, count=1).strip()
            temp_indicacion = re.sub(re.escape("pasar"+chosen_vi_match.group(0)), " ", temp_indicacion, flags=re.IGNORECASE, count=1).strip()
            temp_indicacion = re.sub(re.escape("iniciar"+chosen_vi_match.group(0)), " ", temp_indicacion, flags=re.IGNORECASE, count=1).strip()
            temp_indicacion = re.sub(re.escape(chosen_vi_match.group(0)), " ", temp_indicacion, flags=re.IGNORECASE, count=1).strip()
        except:
            None
        temp_indicacion = re.sub(r'\s+', ' ', temp_indicacion).strip() 

    # 3. Extraer tiempo de infusión 
    TIEMPO_PATTERNS = [
        r"\b(?:a\s*pasar\s*en|pasar\s*en|pasar|en)\s*(\d+(?:[.,]\d+)?)\s*(hrs|hr|horas|h|minutos|minuto|mins|min)"
    ]
    
    chosen_vi_match = None
    for pattern in TIEMPO_PATTERNS:
        match = re.search(pattern, temp_indicacion, re.IGNORECASE)
        if match:
            chosen_vi_match = match
            break
    
    if chosen_vi_match:
        # print(chosen_vi_match.group(0))
        resultados["tiempo_infusion_cantidad"] = parse_fraction(chosen_vi_match.group(1))
        resultados["tiempo_infusion_unidad"] = _normalize_unit(chosen_vi_match.group(2))
        try:
            temp_indicacion = re.sub(re.escape("a pasar en"+chosen_vi_match.group(0)), " ", temp_indicacion, flags=re.IGNORECASE, count=1).strip()
            temp_indicacion = re.sub(re.escape("pasar en"+chosen_vi_match.group(0)), " ", temp_indicacion, flags=re.IGNORECASE, count=1).strip()
            temp_indicacion = re.sub(re.escape("pasar"+chosen_vi_match.group(0)), " ", temp_indicacion, flags=re.IGNORECASE, count=1).strip()
            temp_indicacion = re.sub(re.escape("en"+chosen_vi_match.group(0)), " ", temp_indicacion, flags=re.IGNORECASE, count=1).strip()
            temp_indicacion = re.sub(re.escape(chosen_vi_match.group(0)), " ", temp_indicacion, flags=re.IGNORECASE, count=1).strip()
        except:
            None
        temp_indicacion = re.sub(r'\s+', ' ', temp_indicacion).strip() 

    # 4. Extraer vía y forma de administración
    #  vias_administracion ="vo|oral|sublingual|topica|tópica|intramuscular|im|intravenosa|iv|ev|endovenosa|intravenoso|endovenoso|subcutanea|sc|intradermica|id|rectal|vaginal|nasal|oftalmica|oftálmica|otopica|otópica|inhalatoria|nbz|nebulizada|nebulizado|intratecal|epidural|intraperitoneal|intraarticular|intraarticular|intracardiaca|intraosea|intraósea|uretral|enema" #"|vo|oral|ev|iv|sc|im|id|endovenosa|intravenoso|endovenoso|enjuague|enema|inhalatoria|nbz|nebulizada|nebulizado'
    VIA_ADMINISTRACION_PATTERNS = [
        r"\b(?:via|vía)\s*(vo|oral|ev|iv|sc|im|id|sl|endovenosa|intravenoso|endovenoso|enjuague|enema|inhalatoria|nbz|nebulizada|nebulizado)\b",
        r"\b(?:vo|oral|sublingual|sl|topica|tópica|intramuscular|im|intravenosa|iv|ev|endovenosa|intravenoso|endovenoso|subcutanea|sc|intradermica|id|rectal|intra\s*rectal|vaginal|nasal|oftalmica|oftálmica|otopica|otópica|inhalatoria|nbz|nebulizada|nebulizado|intratecal|epidural|intraperitoneal|intraarticular|intraarticular|intracardiaca|intraosea|intraósea|uretral|enema|en\s*enjuague|enjuague)\b",
    ]
    
    for pattern in VIA_ADMINISTRACION_PATTERNS:
        match = re.search(pattern, temp_indicacion, re.IGNORECASE)
        if match:
            via_raw = match.group(0).lower()
            if via_raw in ['vo', 'oral', 'via oral']: 
                resultados["via_administracion"] = "oral"
            elif via_raw in ['sl', 'sublingual']: 
                resultados["via_administracion"] = "sublingual"
            elif via_raw in ['enjuague', 'en enjuague']: 
                resultados["via_administracion"] = "enjuague"
            elif via_raw in ['im', 'intramuscular']: 
                resultados["via_administracion"] = "intramuscular"
            elif via_raw in ['iv', 'ev', 'intravenosa', 'endovenosa', 'intravenoso', 'endovenoso']: # Normalizar 'endovenosa'
                resultados["via_administracion"] = "endovenosa"
            elif via_raw in ['sc', 'subcutanea', "subcutaneo"]: 
                resultados["via_administracion"] = "subcutanea"
            elif via_raw in ['id', 'intradermica']: 
                resultados["via_administracion"] = "intradermica"
            elif via_raw in ['topica', 'topico', "topicas", "topicos"]: 
                resultados["via_administracion"] = "topica"
            elif via_raw in ['nbz', 'nebulizado', "nebulizada", "nebulizados", "nebulizadas", "nebulizacion", ]: 
                resultados["via_administracion"] = "nebulizada"
            elif via_raw in ['enema', 'rectal', "intrarectal", "intra rectal"]: 
                resultados["via_administracion"] = "rectal"
            else: resultados["via_administracion"] = via_raw
            temp_indicacion = re.sub(re.escape(match.group(0)), " ", temp_indicacion, flags=re.IGNORECASE, count=1).strip()
            temp_indicacion = re.sub(r'\s+', ' ', temp_indicacion).strip()
            break 

    # # 5. Extraer criterio de suspensión
    # CRITERIO_SUSPENSION_PATTERNS = [
    #     r"suspender\s*(?:si|con)?\s*(tension arterial|ta|frecuencia cardiaca|fc|saturacion|dolor|fiebre|glicemia|glucosa|disnea|tos|nauseas|vomitos|diarrea|cefalea|mareo|prurito|rash|hipotension|hipertension|bradicardia|taquicardia|hipoglicemia|hiperglicemia|neutropenia|trombocitopenia|anemia|insuficiencia renal|insuficiencia hepatica|creatinina|uresis|diuresis|oliguria|anuria|edema|shock|sepsis|convulsion|convulsiones|alteracion del estado de conciencia|inestabilidad hemodinamica|reaccion alergica|anafilaxia|sangrado|hemorragia|obstruccion|ileo|perforacion|sepsis|acidosis|alcalosis|desequilibrio hidroelectrolitico|hiponatremia|hipernatremia|hipocalemia|hipercalemia|hipocalcemia|hipercalcemia|hipomagnesemia|hipermagnesemia|hipofosfatemia|hiperfosfatemia)",
    #     r"no\s*administrar\s*si\s*(?:ta|tension arterial|fc|frecuencia cardiaca)\s*<",
    #     r"susp\s*si\s*(?:ta|tension arterial|fc|frecuencia cardiaca|saturacion|dolor|fiebre|glicemia|glucosa|disnea|tos|nauseas|vomitos|diarrea|cefalea|mareo|prurito|rash|hipotension|hipertension|bradicardia|taquicardia|hipoglicemia|hiperglicemia|neutropenia|trombocitopenia|anemia|insuficiencia renal|insuficiencia hepatica|creatinina|uresis|diuresis|oliguria|anuria|edema|shock|sepsis|convulsion|convulsiones|alteracion del estado de conciencia|inestabilidad hemodinamica|reaccion alergica|anafilaxia|sangrado|hemorragia|obstruccion|ileo|perforacion|sepsis|acidosis|alcalosis|desequilibrio hidroelectrolitico|hiponatremia|hipernatremia|hipocalemia|hipercalemia|hipocalcemia|hipercalcemia|hipomagnesemia|hipermagnesemia|hipofosfatemia|hiperfosfatemia)"
    # ]

    # for pattern in CRITERIO_SUSPENSION_PATTERNS:
    #     match = re.search(pattern, temp_indicacion, re.IGNORECASE)
    #     if match:
    #         resultados["criterio_suspension"] = clean_and_normalize_text(match.group(0))
    #         temp_indicacion = re.sub(re.escape(match.group(0)), " ", temp_indicacion, flags=re.IGNORECASE, count=1).strip()
    #         temp_indicacion = re.sub(r'\s+', ' ', temp_indicacion).strip()
    #         break

    
    # 5. Extraer máximos y condicion administración
    MAXIMO_PATTERNS = [
        r"(max|maximo)\s+([a-zA-ZñÑ0-9/\s]+)\s*(en\s*caso|si[\s+]|cuando)\s*([a-zA-ZñÑ0-9\-\+\/\s]+)",
        r"(en\s*caso|si|cuando)\s*([a-zA-ZñÑ0-9\-\+\/\s]+)\s*(max|maximo)\s+([a-zA-ZñÑ0-9\/\s]+)",
        r"(max|maximo)\s+([a-zA-ZñÑ0-9.\/\s]+)",
        # r"maximo\s*([a-zA-ZñÑ0-9/\s]+)",
        # r"en\s*caso\s*([a-zA-ZñÑ0-9/\s]+)"
    ]

    for pattern in MAXIMO_PATTERNS:
        match = re.search(pattern, temp_indicacion, re.IGNORECASE)
        if match:
            if len(match.groups()) == 2:
                resultados["condicion_ma"] = clean_and_normalize_text(match.group(0)) # Captura completo "maximo cada XXXXX"
                temp_indicacion = re.sub(re.escape(match.group(0)), " ", temp_indicacion, flags=re.IGNORECASE, count=1).strip()
                temp_indicacion = re.sub(r'\s+', ' ', temp_indicacion).strip()
                resultados["frecuencia_tipo"] = "SOS"
                # Clear other frequency fields if S.O. is the primary type
                resultados["frecuencia_valor"] = None
                resultados["frecuencia_unidad_tiempo"] = None
                break
            elif len(match.groups()) == 4:
                if "max" in match.group(1):
                    resultados["condicion_ma"] = clean_and_normalize_text(match.group(1)+" "+match.group(2)) # Captura completo "maximo cada XXXXX"
                    resultados["condicion_administracion"] = clean_and_normalize_text(match.group(3)+" "+match.group(4)) # Capture the full "si X" phrase
                else:
                    resultados["condicion_ma"] = clean_and_normalize_text(match.group(3)+" "+match.group(4)) # Captura completo "maximo cada XXXXX"
                    resultados["condicion_administracion"] = clean_and_normalize_text(match.group(1)+" "+match.group(2)) # Capture the full "si X" phrase
                temp_indicacion = re.sub(re.escape(match.group(0)), " ", temp_indicacion, flags=re.IGNORECASE, count=1).strip()
                temp_indicacion = re.sub(r'\s+', ' ', temp_indicacion).strip()
                resultados["frecuencia_tipo"] = "SOS"
                # Clear other frequency fields if S.O. is the primary type
                resultados["frecuencia_valor"] = None
                resultados["frecuencia_unidad_tiempo"] = None
                break

    
    
    # 6. Extraer condición de administración
    CONDICION_ADMINISTRACION_PATTERNS = [
        r"si[\s*]([a-zA-ZñÑ/\s]+)", # "si fiebre o dolor,"
        r"cuando\s*([a-zA-ZñÑ/\s]+)",
        r"en\s*caso\s*([a-zA-ZñÑ/\s]+)"
    ]

    for pattern in CONDICION_ADMINISTRACION_PATTERNS:
        match = re.search(pattern, temp_indicacion, re.IGNORECASE)
        if match:
            resultados["condicion_administracion"] = clean_and_normalize_text(match.group(0)) # Capture the full "si X" phrase
            temp_indicacion = re.sub(re.escape(match.group(0)), " ", temp_indicacion, flags=re.IGNORECASE, count=1).strip()
            temp_indicacion = re.sub(r'\s+', ' ', temp_indicacion).strip()
            resultados["frecuencia_tipo"] = "SOS"
            # Clear other frequency fields if S.O. is the primary type
            resultados["frecuencia_valor"] = None
            resultados["frecuencia_unidad_tiempo"] = None
            break

    # 7. Extraer frecuencia (Reordenado para priorizar S.O.S.)
    FRECUENCIA_PATTERNS = [
        r'\bs.o.s.\b|\bs.o.s\b|\bs.o.\b|\bsos\b|\bPRN\b', # Prioriza SOS
        r'dia\s*por\s*medio',
        r'(?:cada|c\/|q)\s*(\d+(?:[.,]\d+)?)\s*(hrs|hr|horas|hora|h)\.?', # cada X horas
        r'(\d+)\s*veces\s*\bal\s*dia', # X veces al día
        r'(?:cada|c\/|q)\s*(\d+(?:[.,]\d+)?)\s*(dias|dia|d)\.?', # cada X días
        r'(?:cada|c\/|q)\s*(\d+(?:[.,]\d+)?)\s*(semanas|semana|sem|s)\.?', # cada X semanas
        r'(\d+)\s*veces\s*(por|al|\/)\s*(?:semana|sem)',
        r'(\d+)\s*veces\s*\b(por|al|\/)\s*(?:dia|d)',
        r'(una|un)?\s*vez\s*al\s*(?:dia|diario|d)',
        r'(dos|2)?\s*veces\s*al\s*(?:dia|diario|d)',
        r'(tres|3)?\s*veces\s*al\s*(?:dia|diario|d)',
        r'(cuatro|4)?\s*veces\s*al\s*(?:dia|diario|d)',
        r'(cinco|5)?\s*veces\s*al\s*(?:dia|diario|d)',
        r'(seis|6)?\s*veces\s*al\s*(?:dia|diario|d)',
        r'(siete|7)?\s*veces\s*al\s*(?:dia|diario|d)',
        r'(ocho|8)?\s*veces\s*al\s*(?:dia|diario|d)',
        r'(?:manana|am)\s*(y|\-)\s*(?:noche|tarde|pm)',
        r'\bcada\s*dia|\/\s*dia|\bal\s*dia|\bdiario|\bdiaria|\bqd|\bnoche|\bdia\b', #la forma más sensible e inespecífica
        r'(cada|\/|a\s*la)?\s*(semanal|semana|sem)',
        r'c(?:ada)?\s*\d+\s*(?:horas|hora|hs|h)', # Already covered by cada X horas, but keep for robustness
        r'cada\s*(\d+)\s*minutos',
        r'por\s*(\d+)\s*vez|veces',
    ]

    for pattern in FRECUENCIA_PATTERNS:
        match = re.search(pattern, temp_indicacion, re.IGNORECASE)
        if match:
            frecuencia_str = match.group(0).lower()
            if "s.o." in frecuencia_str or "s.o.s." in frecuencia_str or "sos" in frecuencia_str or "prn" in frecuencia_str:
                resultados["frecuencia_tipo"] = "SOS"
                # Clear other frequency fields if S.O. is the primary type
                resultados["frecuencia_valor"] = None
                resultados["frecuencia_unidad_tiempo"] = None
            elif any(p in frecuencia_str for p in ["manana","am"] ) and any(q in frecuencia_str for q in ["noche","tarde","pm"]):
                resultados["frecuencia_tipo"] = "veces"
                resultados["frecuencia_valor"] = 2
                resultados["frecuencia_unidad_tiempo"] = "dia"
            elif "dia por medio" in frecuencia_str:
                resultados["frecuencia_tipo"] = "cada"
                resultados["frecuencia_valor"] = 2
                resultados["frecuencia_unidad_tiempo"] = "dia"
            elif ("cada" in frecuencia_str or "c/" in frecuencia_str or "c /" in frecuencia_str) and (re.search(r"(\d+)", frecuencia_str) != None):
                    resultados["frecuencia_tipo"] = "cada"
                    if ("hr" in frecuencia_str or "hrs" in frecuencia_str or "hora" in frecuencia_str or "horas" in frecuencia_str or "h" in frecuencia_str):
                        resultados["frecuencia_valor"] = int(re.search(r"(\d+)", frecuencia_str).group(1))
                        resultados["frecuencia_unidad_tiempo"] = "hora"
                    elif ("dia" in frecuencia_str or "diario" in frecuencia_str or "d" in frecuencia_str):
                        resultados["frecuencia_valor"] = int(re.search(r"(\d+)", frecuencia_str).group(1))
                        resultados["frecuencia_unidad_tiempo"] = "dia"
                    elif ("semana" in frecuencia_str or "sem" in frecuencia_str or "semanal" in frecuencia_str):
                        resultados["frecuencia_valor"] = int(re.search(r"(\d+)", frecuencia_str).group(1))
                        resultados["frecuencia_unidad_tiempo"] = "semana"
            elif ("veces" in frecuencia_str or "vez" in frecuencia_str) and (re.search(r"(\d+)", frecuencia_str) != None):
                resultados["frecuencia_tipo"] = "veces"
                if ("dia" in frecuencia_str or "diario" in frecuencia_str or "d" in frecuencia_str): 
                    resultados["frecuencia_valor"] = int(re.search(r"(\d+)", frecuencia_str).group(1))
                    resultados["frecuencia_unidad_tiempo"] = "dia"
                elif ("semana" in frecuencia_str or "sem" in frecuencia_str or "semanal" in frecuencia_str):
                    resultados["frecuencia_valor"] = int(re.search(r"(\d+)", frecuencia_str).group(1))
                    resultados["frecuencia_unidad_tiempo"] = "semana"
                elif (re.search(r"(\d+)", frecuencia_str) != None):
                    resultados["frecuencia_valor"] = int(re.search(r"(\d+)", frecuencia_str).group(1))
                    resultados["frecuencia_unidad_tiempo"] = "numero"
            elif "noche" in frecuencia_str:
                resultados["frecuencia_tipo"] = "veces"
                resultados["frecuencia_valor"] = 1
                resultados["frecuencia_unidad_tiempo"] = "noche"
            elif "cada dia" in frecuencia_str or "al dia" in frecuencia_str or "/dia" in frecuencia_str or "/ dia" in frecuencia_str or "diario" in frecuencia_str or "qd" in frecuencia_str or "vez al dia" in frecuencia_str or "dia" in frecuencia_str or "manana" in frecuencia_str:
                resultados["frecuencia_tipo"] = "veces"
                resultados["frecuencia_valor"] = 1
                resultados["frecuencia_unidad_tiempo"] = "dia"
            elif "semanal" in frecuencia_str or "semana" in frecuencia_str:
                resultados["frecuencia_tipo"] = "veces"
                resultados["frecuencia_valor"] = 1
                resultados["frecuencia_unidad_tiempo"] = "semana"
            else: 
                 # General frequency for patterns with value and unit
                 if len(match.groups()) >= 2 and match.group(1) and match.group(2):
                    if match.group(1).isdigit(): 
                        resultados["frecuencia_valor"] = int(match.group(1))
                        resultados["frecuencia_unidad_tiempo"] = _normalize_unit(match.group(2))
                        resultados["frecuencia_tipo"] = "cada" if "cada" in frecuencia_str else "varios"
        
            temp_indicacion = re.sub(re.escape(match.group(0)), " ", temp_indicacion, flags=re.IGNORECASE, count=1).strip()
            temp_indicacion = re.sub(r'\s+', ' ', temp_indicacion).strip()
            break # Break after first frequency match

    # 8. Extraer patrón de dilución inline (aditivos) - la original, si la nueva slash pattern no coincidió
    tipos_soluciones = "(suero\s*fisiologico\s*0.9%|fisiologico\s*0.9%|spm|sg5%|sg\s*5%|sg10%|sg\s*10%|sf\s*0.9%|sf0.9%|sf|sg|albumina\s*5%|albumina\s*20%|suero\s*ringer\s*lactato|ringer\s*lactato|dextrosa|cloruro\s+de\s+sodio|agua\s+destilada|agua\s+bidestilada|agua\s+esteril|solucion\s+fisiologica|suero\s+glucosado|solucion\s+glucosada|suero\s+premezclado)"
    SOLUCION_BASE_PATTERNS = [
        r"(?:en|en\s+solucion\s+de|con|diluido\s+en)?\s*"+tipos_soluciones+"\s*(\d+(?:[.,]\d+)?)\s*(ml|cc|l|litros)",
        r"(?:en|en\s+solucion\s+de|con|diluido\s+en)?\s*(\d+(?:[.,]\d+)?)\s*(ml|cc|l|litros)\s*"+tipos_soluciones,
        r"(?:en|en\s+solucion\s+de|con|diluido\s+en)?\s*(\d+(?:[.,]\d+)?)\s*(ml|cc|l|litros)\s*(de|\s*)\s*"+tipos_soluciones,
        r""+tipos_soluciones+"\s*(\d+(?:[.,]\d+)?)\s*(ml|cc|l|litros)(?!\s*de)", 
        r""+tipos_soluciones+"(?:[\s,.]|$)" 
     ]
    
    match_general_base = None
    if not resultados["solucion_base"]["nombre"]: 
        for pattern in SOLUCION_BASE_PATTERNS:
            match = re.search(pattern, temp_indicacion, re.IGNORECASE)
            if match:
                match_general_base = match
                break
        
        if match_general_base:
            if len(match_general_base.groups()) == 3: 
                if parse_fraction(match_general_base.group(1)) == None: # Revisa si primer dato no es número (dosis) 
                    resultados["solucion_base"]["nombre"] = clean_and_normalize_text(match_general_base.group(1))
                    resultados["solucion_base"]["cantidad"] = parse_fraction(match_general_base.group(2))
                    resultados["solucion_base"]["unidad"] = _normalize_unit(match_general_base.group(3))
                else:
                    resultados["solucion_base"]["nombre"] = clean_and_normalize_text(match_general_base.group(3))
                    resultados["solucion_base"]["cantidad"] = parse_fraction(match_general_base.group(1))
                    resultados["solucion_base"]["unidad"] = _normalize_unit(match_general_base.group(2))
            elif len(match_general_base.groups()) == 4:
                resultados["solucion_base"]["nombre"] = clean_and_normalize_text(match_general_base.group(4))
                resultados["solucion_base"]["cantidad"] = parse_fraction(match_general_base.group(1))
                resultados["solucion_base"]["unidad"] = _normalize_unit(match_general_base.group(2))
            elif len(match_general_base.groups()) == 1: 
                resultados["solucion_base"]["nombre"] = clean_and_normalize_text(match_general_base.group(1))
            """
            Agregar nombres al listado de nombres
            """
            lista_nombres.append(resultados["solucion_base"]["nombre"])
            ##########
            
            temp_indicacion = re.sub(re.escape(match_general_base.group(0)), " ############## ", temp_indicacion, flags=re.IGNORECASE, count=1).strip()
            temp_indicacion = re.sub(r'\s+', ' ', temp_indicacion).strip()


    # 9. Extraer aditivos simples (solo si no se extrajeron antes con patrones complejos)
    ADITIVO_SIMPLE_PATTERNS = [
        r"(?:bic\s*de|bic\s+)?\b([a-zA-ZñÑ./\s]+)\s+(\d*(?:[.,]\d+)?[%]|\d+[/]\d+)\s*(?:diluir|[(][a-z0-9/.,\s*]+[)])?\s+(\d+(?:[.,]\d+)?|\d+\/\d+)\s*(gotas|gota|gramos|gramo|mg|gr|g|ug|mcg|unidades|UI|U|ml|cc|L|litros|comprimidos|comprimido|comp|tableta|capsula|amp.|amp|ampolla|ampollas|vial|set|puffs|puff)[am]\s*[\-]\s*(\d+(?:[.,]\d+)?|\d+\/\d+)\s*(gotas|gota|gramos|gramo|mg|gr|g|ug|mcg|unidades|UI|U|ml|cc|L|litros|comprimidos|comprimido|comp|tableta|capsula|amp.|amp|ampolla|ampollas|vial|set|puffs|puff|inhalaciones|inhalacion|inh)[pm](?:[\s,.]|$)",
        r"(?:bic\s*de|bic\s+)?\b([a-zA-ZñÑ./\s]+)\s+(\d+(?:[.,]\d+)?|\d+\/\d+)\s*(gotas|gota|gramos|gramo|mg|gr|g|ug|mcg|unidades|UI|U|ml|cc|L|litros|comprimidos|comprimido|comp|tableta|capsula|amp.|amp|ampolla|ampollas|vial|set|puffs|puff)\s*(?:am|manana)\s*(?:\s+y\s+|\-)\s*(\d+(?:[.,]\d+)?|\d+\/\d+)\s*(gotas|gota|gramos|gramo|mg|gr|g|ug|mcg|unidades|UI|U|ml|cc|L|litros|comprimidos|comprimido|comp|tableta|capsula|amp.|amp|ampolla|ampollas|vial|set|puffs|puff|inhalaciones|inhalacion|inh)\s*(?:pm|tarde|noche)\s*(?:[\s,.]|$)",
        r"(?:bic\s*de|bic\s+)?(\b[a-zA-ZñÑ./\s]+)\s+(\d*(?:[.,]\d+)?[%]|\d+[/]\d+)\s*(?:diluir|[(][a-z0-9/.,\s*]+[)])?\s+([0-9\.\,\-\s]+)\s*(gotas|gota|gramos|gramo|mg|gr|g|ug|mcg|unidades|UI|U|ml|cc|L|litros|comprimidos|comprimido|comp|tableta|capsula|amp.|amp|ampolla|ampollas|vial|set|puffs|puff|inhalaciones|inhalacion|inh)(?:[\s,.]|$)",
        r"(?:bic\s*de|bic\s+)?\b([a-zA-ZñÑ./\s]+)\s+(\d*(?:[.,]\d+)?[%]|\d+[/]\d+)\s*(?:diluir|[(][a-z0-9/.,\s*]+[)])?\s+([0-9\.\,\-\s]+)\s*(gotas|gota|gramos|gramo|mg|gr|g|ug|mcg|unidades|UI|U|ml|cc|L|litros|comprimidos|comprimido|comp|tableta|capsula|amp.|amp|ampolla|ampollas|vial|set|puffs|puff|inhalaciones|inhalacion|inh)(?:[\s,.]|$)",
        r"(?:bic\s*de|bic\s+)?\b([a-zA-ZñÑ./\s]+)\s+(\d*(?:[.,]\d+)?[%]|\d+[/]\d+)\s*(?:diluir|[(][a-z0-9/.,\s*]+[)])?\s+(\d+(?:[.,]\d+)?|\d+\/\d+)\s*(gotas|gota|gramos|gramo|mg|gr|g|ug|mcg|unidades|UI|U|ml|cc|L|litros|comprimidos|comprimido|comp|tableta|capsula|amp.|amp|ampolla|ampollas|vial|set|puffs|puff|inhalaciones|inhalacion|inh)(?:[\s,.]|$)" ,
        r"(?:[\s,.])(\d+(?:[.,]\d+)?|\d+\/\d+)\s*(gotas|gota|gramos|gramo|mg|gr|g|ug|mcg|unidades|UI|U|ml|cc|L|litros|comprimidos|comprimido|comp|tableta|capsula|amp.|amp|ampolla|ampollas|vial|set|puffs|puff|inhalaciones|inhalacion|inh)(?:\s+de)?\s+([a-zA-ZñÑ0-9./%\s]+?)\s*(\d+(?:[.,]\d+)?[%]|\d+[/]\d+)",
        r"(?:bic\s*de|bic\s+)?([a-zA-ZñÑ./\s]+)\s+(\d+(?:[/]\d+)?\s*m|\d+(?:[/]\d+)?\s*molar)\s*(?:diluir|[(][a-z0-9/.,\s*]+[)])?\s+(\d+(?:[.,]\d+)?|\d+\/\d+)\s*(gotas|gota|gramos|gramo|mg|gr|g|ug|mcg|unidades|UI|U|ml|cc|L|litros|comprimidos|comprimido|comp|tableta|capsula|amp.|amp|ampolla|ampollas|vial|set|puffs|puff|inhalaciones|inhalacion|inh)(?:[\s,.]|$)" ,
        r"(?:[\s,.])(\d+(?:[.,]\d+)?|\d+\/\d+)\s*(gotas|gota|gramos|gramo|mg|gr|g|ug|mcg|unidades|UI|U|ml|cc|L|litros|comprimidos|comprimido|comp|tableta|capsula|amp.|amp|ampolla|ampollas|vial|set|puffs|puff|inhalaciones|inhalacion|inh)(?:\s+de)?\s+([a-zA-ZñÑ0-9./%\s]+?)(?:[\s,.])\s*(\d+(?:[/]\d+)?\s*M|Molar)",                
        r"(?:bic\s*de|bic\s+)?\b([a-zA-ZñÑ0-9.,/\s]+)\s*(?:diluir|[(][a-z0-9/.,\s*]+[)])?\s+(\d+(?:[.,]\d+)?|\d+\/\d+)\s*(gotas|gota|gramos|gramo|mg|gr|g|ug|mcg|unidades|UI|U|ml|cc|L|litros|comprimidos|comprimido|comp|tableta|capsula|amp.|amp|ampolla|ampollas|vial|set|puffs|puff|inhalaciones|inhalacion|inh)(?:[\s,.]|$)" ,
        r"(?:bic\s*de|bic\s+)?(\b[a-zA-ZñÑ./\s]+)\s+([0-9\.\,\-\s]+)\s*(gotas|gota|gramos|gramo|mg|gr|g|ug|mcg|unidades|UI|U|ml|cc|L|litros|comprimidos|comprimido|comp|tableta|capsula|amp.|amp|ampolla|ampollas|vial|set|puffs|puff|inhalaciones|inhalacion|inh)(?:[\s,.]|$)",

        # r"(\d+(?:[.,\s]\d+)?|\d+\/\d+|\½)\s*(mg|gr|g|ug|mcg|UI|unidades|ml|cc|L|litros|comp|tableta|capsula|amp|ampolla|vial)(?:\s+de)?\s+([a-zA-ZñÑ\s]+?)(?:[\s,.]|$)", 

        # r"(\d+(?:[.,\s]\d+)?|\d+\/\d+)\s*(mg|gr|g|ug|mcg|UI|unidades|ml|cc|L|litros|comprimidos|comprimido|comp|tableta|capsula|amp.|amp|ampolla|ampollas|vial|set)(?:\s+de)?\s+([a-zA-ZñÑ.\s]+?)",        
        r"(\d+(?:[.,]\d+)?|\d+\/\d+)\s*(gotas|gota|gramos|gramo|mg|gr|g|ug|mcg|unidades|UI|U|ml|cc|L|litros|comprimidos|comprimido|comp|tableta|capsula|amp.|amp|ampolla|ampollas|vial|set|puffs|puff)(?:\s+de)?\s+([a-zA-ZñÑ0-9./\s]*)",
        r"(\d+(?:[.,\-\s*]\d+)?|\d+\/\d+)\s*(gotas|gota|gramos|gramo|mg|gr|g|ug|mcg|unidades|UI|U|ml|cc|L|litros|comprimidos|comprimido|comp|tableta|capsula|amp.|amp|ampolla|ampollas|vial|set|puffs|puff)(?:\s+de)?\s+([a-zA-ZñÑ0-9./\s]*)",
        ]
    if not resultados["aditivos_info"]: # Solo intentar si no se llenaron con el patrón slash
        for pattern in ADITIVO_SIMPLE_PATTERNS:
            for match in list(re.finditer(pattern, temp_indicacion, re.IGNORECASE)):
                if "+" not in temp_indicacion and len(resultados["aditivos_info"]) == 1: #en caso de que sea 1 sólo medicamento (sin signo + en indicación) y ya lo haya agregado --> Se detiene
                    break
                else:
                    try:
                        # print(match)
                        dosis_cantidad = None
                        dosis_unidad = None
                        nombre_aditivo = None
                        if len(match.groups()) == 3: # Asegurarse de que haya 3 grupos capturados
                            # Determinar si es patrón cantidad-unidad-nombre o nombre-cantidad-unidad
                            # Heurística: si el primer grupo es un número, es cantidad-unidad-nombre
                            if parse_fraction(match.group(1)) is not None: 
                                dosis_cantidad = parse_fraction(match.group(1))
                                dosis_unidad = _normalize_unit(match.group(2))
                                nombre_aditivo = clean_and_normalize_text(match.group(3))
                            elif "-" not in match.group(2): # Asumir nombre-cantidad-unidad y revisar que no sea prescripción variable (con "-")
                                nombre_aditivo = clean_and_normalize_text(match.group(1))
                                dosis_cantidad = parse_fraction(match.group(2))
                                dosis_unidad = _normalize_unit(match.group(3))
                            elif "-" in match.group(2):
                                nombre_aditivo = clean_and_normalize_text(match.group(1))
                                dosis_cantidad_temp = match.group(2).split("-")
                                dosis_cantidad = []
                                for n in dosis_cantidad_temp:
                                    dosis_cantidad.append(parse_fraction(n))
                                dosis_unidad = _normalize_unit(match.group(3))
                                resultados["frecuencia_tipo"] = "veces-var"
                                resultados["frecuencia_valor"] = len(dosis_cantidad)
                                resultados["frecuencia_unidad_tiempo"] = "dia"
                        elif len(match.groups()) == 4: # Asegurarse de que haya 4 grupos capturados en casos con %
                            # Determinar si es patrón cantidad-unidad-nombre o nombre-cantidad-unidad
                            # Heurística: si el primer grupo es un número, es cantidad-unidad-nombre
                            if parse_fraction(match.group(1)) is not None: 
                                dosis_cantidad = parse_fraction(match.group(1))
                                dosis_unidad = _normalize_unit(match.group(2))
                                nombre_aditivo = clean_and_normalize_text(match.group(3)+" "+match.group(4))
                            elif "-" not in match.group(3):  # Asumir nombre-cantidad-unidad y revisar que no sea prescripción variable (con "-")
                                nombre_aditivo = clean_and_normalize_text(match.group(1)+" "+match.group(2))
                                dosis_cantidad = parse_fraction(match.group(3))
                                dosis_unidad = _normalize_unit(match.group(4))                        
                            elif "-" in match.group(3):
                                nombre_aditivo = clean_and_normalize_text(match.group(1)+" "+match.group(2))
                                dosis_cantidad_temp = match.group(3).split("-")
                                dosis_cantidad = []
                                for n in dosis_cantidad_temp:
                                    dosis_cantidad.append(parse_fraction(n))
                                dosis_unidad = _normalize_unit(match.group(4))
                                resultados["frecuencia_tipo"] = "veces-var"
                                resultados["frecuencia_valor"] = len(dosis_cantidad)
                                resultados["frecuencia_unidad_tiempo"] = "dia"
                        elif len(match.groups()) == 5: # Asegurarse de que haya 5 grupos capturados en casos con AM - PM
                            nombre_aditivo = clean_and_normalize_text(match.group(1))
                            dosis_cantidad = []
                            dosis_cantidad.append(match.group(2))
                            dosis_cantidad.append(match.group(4))
                            dosis_unidad = []
                            dosis_unidad.append(_normalize_unit(match.group(3)))
                            dosis_unidad.append(_normalize_unit(match.group(5)))
                            resultados["frecuencia_tipo"] = "veces-var"
                            resultados["frecuencia_valor"] = len(dosis_cantidad)
                            resultados["frecuencia_unidad_tiempo"] = "dia"
                        
                        else:
                            continue # No coincide con el número esperado de grupos
    
                        if nombre_aditivo is None or dosis_cantidad is None or dosis_unidad is None:
                            continue
    
                        # CORRECCIÓN: Excluir "sos", "s.o.", "max" de ser identificados como nombres de aditivos
                        if any(keyword == nombre_aditivo for keyword in ["bolo", "gotas", "nebulizacion", "sos", "s.o.s", "prn", "bic", "dar", "max", "maximo", "en", "con", "para", "pasar"]): 
                            continue
    
                        if len(nombre_aditivo) < 3 and nombre_aditivo not in ["sf", "sg", "g", "ml", "mg"]: # Mejorar el filtro de nombres cortos  
                            continue
    
                        resultados["aditivos_info"].append({
                            "nombre": nombre_aditivo,
                            "dosis_cantidad": dosis_cantidad,
                            "dosis_unidad": dosis_unidad,
                        })
                        """
                        Agregar nombres al listado de nombres
                        """
                        lista_nombres.append(nombre_aditivo)
                        ##########
                        temp_indicacion = re.sub(re.escape(match.group(0)), " ", temp_indicacion, flags=re.IGNORECASE, count=1).strip()
                        temp_indicacion = re.sub(r'\s+', ' ', temp_indicacion).strip()
                      
                    except IndexError:
                        continue 
                    
                

    # Extraer forma de administración
    FORMA_ADMINISTRACION_PATTERNS = [
        r'\b(?:bolo|bic|bic de|gotas|nebulizacion|nebulizaciones|sachets|puff|comp|comprimido|comprimidos|capsula|capsulas|jeringa|solucion|suspension|jarabe|crema|unguento|pomada|gel|supositorio|ovulo|inhalador|spray|parche|ampolla|vial)\b'
    ]


    for pattern in FORMA_ADMINISTRACION_PATTERNS:
        match = re.search(pattern, temp_indicacion, re.IGNORECASE)
        if match:
            resultados["forma_administracion"] = clean_and_normalize_text(match.group(0))
            # temp_indicacion = re.sub(re.escape(match.group(0)), " ", temp_indicacion, flags=re.IGNORECASE, count=1).strip()
            # temp_indicacion = re.sub(r'\s+', ' ', temp_indicacion).strip()
            break 

    # Extraer dia semana
    DIA_SEMANA_PATTERNS = [
        r'\b(de)\s+(lunes|martes|miercoles|jueves|viernes|sabado|domingo|lun|lu|l|mar|ma|mier|mie|mi|jue|ju|j|vie|vi|v|sab|sa|s|dom|do|d)\s+(a)\s+(lunes|martes|miercoles|jueves|viernes|sabado|domingo|lun|lu|l|mar|ma|mier|mie|mi|jue|ju|j|vie|vi|v|sab|sa|s|dom|do|d)\b',
        r'\b(?:lunes|martes|miercoles|jueves|viernes|sabado|domingo|lun|lu|l|mar|ma|mier|mie|mi|jue|ju|j|vie|vi|v|sab|sa|s|dom|do|d)\s*(\-)\s*(?:lunes|martes|miercoles|jueves|viernes|sabado|domingo|lun|lu|l|mar|ma|mier|mie|mi|jue|ju|j|vie|vi|v|sab|sa|s|dom|do|d)\s*(?:\-)?\s*(?:lunes|martes|miercoles|jueves|viernes|sabado|domingo|lun|lu|l|mar|ma|mier|mie|mi|jue|ju|j|vie|vi|v|sab|sa|s|dom|do|d)?\s*(?:\-)?\s*(?:lunes|martes|miercoles|jueves|viernes|sabado|domingo|lun|lu|l|mar|ma|mier|mie|mi|jue|ju|j|vie|vi|v|sab|sa|s|dom|do|d)?\s*(?:\-)?\s*(?:lunes|martes|miercoles|jueves|viernes|sabado|domingo|lun|lu|l|mar|ma|mier|mie|mi|jue|ju|j|vie|vi|v|sab|sa|s|dom|do|d)?\s*(?:\-)?\s*(?:lunes|martes|miercoles|jueves|viernes|sabado|domingo|lun|lu|l|mar|ma|mier|mie|mi|jue|ju|j|vie|vi|v|sab|sa|s|dom|do|d)?\b',
        r'\b(?:lunes|martes|miercoles|jueves|viernes|sabado|domingo|lun|lu|l|mar|ma|mier|mie|mi|jue|ju|j|vie|vi|v|sab|sa|s|dom|do|d)\b'
    ]


    for pattern in DIA_SEMANA_PATTERNS:
        match = re.search(pattern, temp_indicacion, re.IGNORECASE)
        if match:
            lista_dia_semana_normalizada = []
            try:
                if match.group(1) == "de":
                    lista_ampliada_semana = ["lunes","martes","miercoles","jueves","viernes","sabado","domingo","lunes","martes","miercoles","jueves","viernes","sabado","domingo"]
                    indice_inicio = lista_ampliada_semana.index(_normalize_dia_semana(match.group(2)))
                    indice_final = lista_ampliada_semana.index(_normalize_dia_semana(match.group(4)), indice_inicio+1) + 1
                    lista_dia_semana_normalizada = lista_ampliada_semana[indice_inicio:indice_final]
            except:
                None
            if lista_dia_semana_normalizada == []:
                lista_dia_semana = clean_and_normalize_text(match.group(0)).split("-")
                for dia_semana in lista_dia_semana:
                    dia_semana_normalizado = _normalize_dia_semana(dia_semana)
                    lista_dia_semana_normalizada.append(dia_semana_normalizado)
            resultados["frecuencia_dia_semana"] = lista_dia_semana_normalizada
            temp_indicacion = re.sub(re.escape(match.group(0)), " ", temp_indicacion, flags=re.IGNORECASE, count=1).strip()
            temp_indicacion = re.sub(r'\s+', ' ', temp_indicacion).strip()
    
    # # Limpieza de elementos comunes que podrían haber quedado y no son relevantes para observaciones
    # temp_indicacion = re.sub(r'\b(?:via|vía|oral|enjuague|sublingual|topica|tópica|intramuscular|im|intravenosa|iv|ev|endovenosa|intravenoso|endovenoso|subcutanea|sc|intradermica|id|rectal|vaginal|nasal|oftalmica|oftálmica|otopica|otópica|inhalatoria|intratecal|epidural|intraperitoneal|intraarticular|intraarticular|intracardiaca|intraosea|intraósea|uretral)\b', ' ', temp_indicacion, flags=re.IGNORECASE).strip()
    # temp_indicacion = re.sub(r'\b(?:bolo|bic|gotas|nebulizacion|nebulizaciones|sachets|puff|comp|comprimido|comprimidos|capsula|capsulas|jeringa|solucion|suspension|jarabe|crema|unguento|pomada|gel|supositorio|ovulo|inhalador|spray|parche|ampolla|vial)\b', ' ', temp_indicacion, flags=re.IGNORECASE).strip()
    temp_indicacion = re.sub(r'\b(?:iniciar a|iniciar|diluir en|en)\b', ' ', temp_indicacion, flags=re.IGNORECASE).strip()
    # temp_indicacion = re.sub(r'\b(?:por)\b', ' ', temp_indicacion, flags=re.IGNORECASE).strip() 
    # temp_indicacion = re.sub(r'\s+', ' ', temp_indicacion).strip()

    # 10. Asignar el texto restante a "observaciones"
    extracted_elements_to_remove = []

    # # Añadir términos generales que podrían quedar y son parte de conceptos ya extraídos
    # extracted_elements_to_remove.extend(["s.o.", "sos", "PRN", "segun orden medica"]) # Asegurar remoción de términos SOS
    # if resultados["condicion_administracion"]:
    #     # Quitar "si" del inicio si existe para la remoción más genérica
    #     cleaned_cond = re.sub(r'^(si|cuando|en caso de)\s*', '', resultados["condicion_administracion"], flags=re.IGNORECASE).strip()
    #     extracted_elements_to_remove.append(resultados["condicion_administracion"])
    #     if cleaned_cond: # Añadir la condición sin la palabra clave inicial para una remoción más flexible
    #         extracted_elements_to_remove.append(cleaned_cond) 

    # if resultados["via_administracion"]:
    #     extracted_elements_to_remove.append(resultados["via_administracion"])
    # if resultados["forma_administracion"]:
    #     extracted_elements_to_remove.append(resultados["forma_administracion"])
    
    # # No añadir la frecuencia fija a la remoción si 's.o.' es el tipo,
    # # ya que 'max cada 8 hrs' es una observación en este caso.
    # if resultados["frecuencia_tipo"] and resultados["frecuencia_tipo"] != "s.o." and resultados["frecuencia_valor"] and resultados["frecuencia_unidad_tiempo"]:
    #     extracted_elements_to_remove.append(f"{resultados['frecuencia_tipo']} {resultados['frecuencia_valor']} {resultados['frecuencia_unidad_tiempo']}")
    
    # for aditivo in resultados["aditivos_info"]:
    #     # Añadir la cadena completa del aditivo (ej. "metamizol 1 g")
    #     extracted_elements_to_remove.append(f"{aditivo['nombre']} {aditivo['dosis_cantidad']} {aditivo['dosis_unidad']}")
    #     # Añadir solo el nombre del aditivo (ej. "metamizol") para removerlo si persiste solo
    #     extracted_elements_to_remove.append(aditivo['nombre']) 

    # if resultados["solucion_base"]["nombre"]:
    #     base_name = resultados["solucion_base"]["nombre"]
    #     base_qty = resultados["solucion_base"]["cantidad"]
    #     base_unit = resultados["solucion_base"]["unidad"]
    #     if base_name and base_qty and base_unit:
    #         extracted_elements_to_remove.append(f"{base_name} {base_qty} {base_unit}")
    #     extracted_elements_to_remove.append(base_name)

    # # Ordenar por longitud descendente para eliminar coincidencias más largas primero
    # extracted_elements_to_remove.sort(key=len, reverse=True)

    current_observaciones = clean_and_normalize_text(temp_indicacion)
    
    # # Limpiar current_observaciones de los elementos ya extraídos
    # for elem in extracted_elements_to_remove:
    #     # Usar límites de palabra para una remoción más precisa de nombres/frases
    #     # Esto previene eliminar partes de palabras (ej. "dolor" de "dolores")
    #     pattern_to_remove_word_boundary = r'\b' + re.escape(elem.lower().replace(" ", r'\s*')) + r'\b'
    #     current_observaciones = re.sub(pattern_to_remove_word_boundary, ' ', current_observaciones, flags=re.IGNORECASE).strip()
        
    #     # También remover sin límites de palabra para frases que podrían no tenerlos
    #     # (ej. al inicio/final de la cadena o si están pegadas a puntuación)
    #     pattern_to_remove_no_boundary = re.escape(elem.lower().replace(" ", r'\s*'))
    #     current_observaciones = re.sub(pattern_to_remove_no_boundary, ' ', current_observaciones, flags=re.IGNORECASE).strip()


    # Limpieza final de observaciones
    current_observaciones = re.sub(r'\s+', ' ', current_observaciones).strip()
    current_observaciones = re.sub(r'[;,.]+$', '', current_observaciones).strip() # Elimina puntuación al final
    current_observaciones = re.sub(r'^\W+|\W+$', '', current_observaciones).strip() # Elimina cualquier carácter no alfanumérico al inicio/final
    # current_observaciones = re.sub(r'\s*\W+\s*', ' ', current_observaciones).strip() # Reemplaza múltiples signos de puntuación/espacios con un solo espacio


    if len(current_observaciones) > 0 and len(current_observaciones) <= 2 and not re.search(r'[a-z0-9]', current_observaciones):
        current_observaciones = ""
    
    if current_observaciones:
        resultados["observaciones"] = current_observaciones
    else:
        resultados["observaciones"] = None
    
    resultados = revisar_nombres(resultados)
    
    return resultados

# print(lista_nombres)