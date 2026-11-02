"""Ingeniería Económica — Grupo 13. Calculadoras fieles al Taller 3 (8 hojas)."""
from decimal import Decimal, ROUND_HALF_UP
from pathlib import Path

from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, ConfigDict, Field

BASE_DIR = Path(__file__).resolve().parent
app = FastAPI(title="Ingeniería Económica — Grupo 13", version="1.0.1")
app.mount("/static", StaticFiles(directory=BASE_DIR / "static"), name="static")


@app.get("/", include_in_schema=False)
def inicio():
    return FileResponse(BASE_DIR / "templates" / "index.html")


@app.get("/health", tags=["Sistema"])
def salud():
    return {"estado": "ok", "asignatura": "Ingeniería Económica", "ejercicios": 8}


class Entrada(BaseModel):
    model_config = ConfigDict(extra="forbid", allow_inf_nan=False)


def centavos(numero: float) -> float:
    """Equivalente a ROUND(..., 2) de Excel para moneda."""
    return float(Decimal(str(numero)).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP))


def numero_es(numero: float, decimales: int = 2, *, fijo: bool = False) -> str:
    """Formato español: miles con punto, decimales con coma.

    En cantidades generales elimina ceros finales innecesarios.
    En importes monetarios conserva exactamente dos decimales.
    """
    cadena = f"{numero:,.{decimales}f}"
    entero, separador, fraccion = cadena.partition(".")
    entero = entero.replace(",", ".")
    if separador:
        if not fijo:
            fraccion = fraccion.rstrip("0")
        if fraccion:
            return entero + "," + fraccion
    return entero


def usd(numero: float) -> str:
    return "$" + numero_es(numero, 2, fijo=True)


def porcentaje(numero: float) -> str:
    return numero_es(numero, 4) + " %"


def tiempo_legible(anios: float) -> str:
    """Convierte años a años/meses cuando hay meses enteros exactos.

    Si hay meses fraccionarios, mantiene el tiempo decimal sin inventar
    meses enteros a partir de un redondeo.
    """
    meses = anios * 12
    if abs(meses - round(meses)) < 1e-8:
        anios_enteros, meses_restantes = divmod(round(meses), 12)
        if anios_enteros and meses_restantes:
            return f"{anios_enteros} años y {meses_restantes} meses"
        if anios_enteros:
            return f"{anios_enteros} " + ("año" if anios_enteros == 1 else "años")
        return f"{meses_restantes} " + ("mes" if meses_restantes == 1 else "meses")
    return numero_es(anios, 6) + " años"


def respuesta(titulo: str, resultado: str, pasos: list[str], secundarios=None, nota="", tabla=None):
    return {
        "titulo": titulo,
        "resultado": resultado,
        "pasos": pasos,
        "secundarios": secundarios or [],
        "nota": nota,
        "tabla": tabla or [],
    }


# 1 — Interés simple: calcular la tasa anual
class E1(Entrada):
    capital: float = Field(gt=0)
    interes: float = Field(ge=0)
    anios: int = Field(ge=0, le=200)
    meses: int = Field(ge=0, le=11)


@app.post("/api/ejercicios/1", tags=["Interés simple"])
def ejercicio_1(d: E1):
    t = d.anios + d.meses / 12
    if t <= 0:
        raise HTTPException(422, "El tiempo debe ser mayor que cero.")
    tasa = d.interes / (d.capital * t) * 100
    return respuesta("Tasa de interés simple anual", porcentaje(tasa) + " anual", [
        "Fórmula: i = I / (C × n)",
        f"Tiempo en años: n = {d.anios} + {d.meses}/12 = {numero_es(t, 6)}",
        f"Sustitución: i = {usd(d.interes)} / ({usd(d.capital)} × {numero_es(t, 6)}) × 100",
        f"Tasa anual: i = {porcentaje(tasa)}",
    ])


@app.get("/api/ejercicios/1", tags=["Interés simple"])
def ejercicio_1_compatibilidad(capital: float = Query(gt=0), interes: float = Query(ge=0),
                             anios: int = Query(ge=0, le=200), meses: int = Query(ge=0, le=11)):
    """Conserva la prueba GET que se creó antes de montar la interfaz."""
    t = anios + meses / 12
    if t <= 0:
        raise HTTPException(422, "El tiempo debe ser mayor que cero.")
    return {"capital": capital, "interes": interes, "tiempo_anios": round(t, 6),
            "tasa_anual": round(interes / (capital * t) * 100, 4)}


# 2 — Interés simple: calcular plazo
class E2(Entrada):
    capital: float = Field(gt=0)
    interes: float = Field(ge=0)
    tasa_anual: float = Field(gt=0, le=10000)


@app.post("/api/ejercicios/2", tags=["Interés simple"])
def ejercicio_2(d: E2):
    n = d.interes / (d.capital * (d.tasa_anual / 100))
    meses = numero_es(n * 12, 6) + " meses"
    return respuesta("Tiempo de inversión", tiempo_legible(n), [
        "Fórmula: n = I / (C × i)",
        f"Tasa decimal: i = {numero_es(d.tasa_anual, 4)} / 100 = {numero_es(d.tasa_anual / 100, 6)}",
        f"Sustitución: n = {usd(d.interes)} / ({usd(d.capital)} × {numero_es(d.tasa_anual / 100, 6)})",
        f"Tiempo: n = {tiempo_legible(n)} (equivalente a {meses})",
    ], secundarios=[{"etiqueta": "Equivalente en meses", "valor": meses}])


# 3 — Interés simple: valor presente
class E3(Entrada):
    monto_futuro: float = Field(gt=0)
    tasa_anual: float = Field(ge=0, le=10000)
    meses: float = Field(gt=0, le=2400)


@app.post("/api/ejercicios/3", tags=["Interés simple"])
def ejercicio_3(d: E3):
    n = d.meses / 12
    factor = 1 + d.tasa_anual / 100 * n
    valor = d.monto_futuro / factor
    return respuesta("Capital inicial o valor presente", usd(centavos(valor)), [
        "Fórmula: C = M / (1 + i × n)",
        f"Tiempo: n = {numero_es(d.meses, 2)} / 12 = {numero_es(n, 6)} años",
        f"Factor simple: 1 + ({numero_es(d.tasa_anual, 4)} / 100 × {numero_es(n, 6)}) = {numero_es(factor, 6)}",
        f"Valor presente: C = {usd(d.monto_futuro)} / {numero_es(factor, 6)} = {usd(centavos(valor))}",
    ])


# 4 — Fecha focal: valor presente de tres pagos futuros
class E4(Entrada):
    tasa_anual: float = Field(ge=0, le=10000)
    base_dias: int = Field(gt=0, le=366)
    monto_1: float = Field(ge=0)
    dias_1: int = Field(ge=0, le=30000)
    monto_2: float = Field(ge=0)
    dias_2: int = Field(ge=0, le=30000)
    monto_3: float = Field(ge=0)
    dias_3: int = Field(ge=0, le=30000)


@app.post("/api/ejercicios/4", tags=["Fecha focal"])
def ejercicio_4(d: E4):
    flujos = [("9 de mayo", d.monto_1, d.dias_1),
             ("20 de junio", d.monto_2, d.dias_2),
             ("23 de diciembre", d.monto_3, d.dias_3)]
    tasa = d.tasa_anual / 100
    tabla = []
    valores = []
    pasos = ["Fórmula de cada pago: C = M / (1 + i × días / base)"]
    acumulado = Decimal("0")
    for idx, (fecha, monto, dias) in enumerate(flujos, 1):
        vp = centavos(monto / (1 + tasa * dias / d.base_dias))
        acumulado += Decimal(str(vp))
        valores.append(vp)
        tabla.append({"concepto": f"Pago {idx} · {fecha}", "dato": f"{dias} días", "resultado": usd(vp)})
        pasos.append(f"Pago {idx}: {usd(monto)} / (1 + {numero_es(tasa, 6)} × {dias}/{d.base_dias}) = {usd(vp)}")
    total = float(acumulado)
    pasos.append(f"Inversión inicial requerida = {usd(valores[0])} + {usd(valores[1])} + {usd(valores[2])} = {usd(total)}")
    return respuesta("Inversión requerida el 15 de febrero", usd(total), pasos, tabla=tabla,
                     nota="Se usan los días del taller y año comercial. Cada valor presente se redondea a centavos antes de sumarlo, igual que en Excel.")



# 5 — Fecha focal: dos depósitos y un retiro
class E5(Entrada):
    tasa_anual: float = Field(ge=0, le=10000)
    base_dias: int = Field(gt=0, le=366)
    deposito_1: float = Field(ge=0)
    dias_1: int = Field(ge=0, le=30000)
    deposito_2: float = Field(ge=0)
    dias_2: int = Field(ge=0, le=30000)
    retiro: float = Field(ge=0)
    dias_retiro: int = Field(ge=0, le=30000)


@app.post("/api/ejercicios/5", tags=["Fecha focal"])
def ejercicio_5(d: E5):
    tasa = d.tasa_anual / 100
    flujos = [("Depósito · 15 de diciembre", d.deposito_1, d.dias_1),
             ("Depósito · 11 de marzo", d.deposito_2, d.dias_2),
             ("Retiro · 28 de enero", -d.retiro, d.dias_retiro)]
    tabla = []
    valores = []
    pasos = ["Fórmula de valor focal: M = C × (1 + i × días / base)",
             "Los depósitos se suman; el retiro se resta."]
    for fecha, flujo, dias in flujos:
        valor = centavos(flujo * (1 + tasa * dias / d.base_dias))
        valores.append(Decimal(str(valor)))
        tabla.append({"concepto": fecha, "dato": f"{dias} días", "resultado": usd(valor)})
        pasos.append(f"{fecha}: {usd(flujo)} × (1 + {numero_es(tasa, 6)} × {dias}/{d.base_dias}) = {usd(valor)}")
    total = float(sum(valores))
    neto = centavos(total - (d.deposito_1 + d.deposito_2 - d.retiro))
    pasos.append(f"Saldo al 9 de mayo: {usd(float(valores[0]))} + {usd(float(valores[1]))} − {usd(abs(float(valores[2])))} = {usd(total)}")
    return respuesta("Saldo en la fecha focal: 9 de mayo", usd(total), pasos,
                     secundarios=[{"etiqueta": "Interés neto generado", "valor": usd(neto)}], tabla=tabla,
                     nota="Se mantienen los plazos en días utilizados en el Excel, con base de 360 días. El retiro se considera un flujo negativo.")


# 6 — Fecha focal: sustitución de deudas
class E6(Entrada):
    prestamo_1: float = Field(ge=0)
    tasa_prestamo: float = Field(ge=0, le=10000)
    plazo_contrato_anios: float = Field(ge=0, le=200)
    deuda_2: float = Field(ge=0)
    tasa_equivalencia: float = Field(ge=0, le=10000)
    pago_hoy: float = Field(ge=0)
    vencimiento_1_meses: float = Field(ge=0, le=2400)
    vencimiento_2_meses: float = Field(ge=0, le=2400)
    focal_meses: float = Field(gt=0, le=2400)


@app.post("/api/ejercicios/6", tags=["Fecha focal"])
def ejercicio_6(d: E6):
    if d.focal_meses < max(d.vencimiento_1_meses, d.vencimiento_2_meses):
        raise HTTPException(422, "Este ejercicio se plantea con fecha focal igual o posterior a ambos vencimientos.")
    i = d.tasa_equivalencia / 100
    vencimiento = d.prestamo_1 * (1 + d.tasa_prestamo / 100 * d.plazo_contrato_anios)
    deuda1 = vencimiento * (1 + i * (d.focal_meses - d.vencimiento_1_meses) / 12)
    deuda2 = d.deuda_2 * (1 + i * (d.focal_meses - d.vencimiento_2_meses) / 12)
    pago_focal = d.pago_hoy * (1 + i * d.focal_meses / 12)
    x = deuda1 + deuda2 - pago_focal
    return respuesta("Pago X en la fecha focal", usd(centavos(x)), [
        "Ecuación de valor en la fecha focal: deudas = pago hoy capitalizado + X",
        f"Deuda 1 al vencimiento: {usd(d.prestamo_1)} × (1 + {numero_es(d.tasa_prestamo / 100, 6)} × {numero_es(d.plazo_contrato_anios, 4)}) = {usd(centavos(vencimiento))}",
        f"Deuda 1 en fecha focal: {usd(centavos(vencimiento))} × (1 + {numero_es(i, 6)} × ({numero_es(d.focal_meses, 2)} − {numero_es(d.vencimiento_1_meses, 2)})/12) = {usd(centavos(deuda1))}",
        f"Deuda 2 en fecha focal: {usd(d.deuda_2)} × (1 + {numero_es(i, 6)} × ({numero_es(d.focal_meses, 2)} − {numero_es(d.vencimiento_2_meses, 2)})/12) = {usd(centavos(deuda2))}",
        f"Pago de hoy en fecha focal: {usd(d.pago_hoy)} × (1 + {numero_es(i, 6)} × {numero_es(d.focal_meses, 2)}/12) = {usd(centavos(pago_focal))}",
        f"X = {usd(centavos(deuda1))} + {usd(centavos(deuda2))} − {usd(centavos(pago_focal))} = {usd(centavos(x))}",
    ], secundarios=[{"etiqueta": "Deuda 1 al vencimiento", "valor": usd(centavos(vencimiento))}],
    nota="La fecha focal debe ser igual o posterior a los vencimientos para mantener el planteamiento original del taller.")


# 7 — Descuento simple comercial por anticipado
class E7(Entrada):
    nominal: float = Field(gt=0)
    tasa_descuento: float = Field(ge=0, le=10000)
    meses: float = Field(gt=0, le=2400)


@app.post("/api/ejercicios/7", tags=["Descuento simple"])
def ejercicio_7(d: E7):
    n = d.meses / 12
    factor = d.tasa_descuento / 100 * n
    if factor >= 1:
        raise HTTPException(422, "El descuento igualaría o superaría el valor nominal; reduce la tasa o el plazo.")
    descuento = d.nominal * factor
    liquido = d.nominal - descuento
    return respuesta("Capital líquido recibido", usd(centavos(liquido)), [
        "Fórmulas: D = F × d × n;  P = F − D",
        f"Tiempo: n = {numero_es(d.meses, 2)}/12 = {numero_es(n, 6)} años",
        f"Descuento: D = {usd(d.nominal)} × {numero_es(d.tasa_descuento / 100, 6)} × {numero_es(n, 6)} = {usd(centavos(descuento))}",
        f"Capital líquido: P = {usd(d.nominal)} − {usd(centavos(descuento))} = {usd(centavos(liquido))}",
    ], secundarios=[{"etiqueta": "Descuento aplicado", "valor": usd(centavos(descuento))}])


# 8 — Tasa simple real equivalente al descuento anticipado
class E8(Entrada):
    nominal: float = Field(gt=0)
    recibido: float = Field(gt=0)
    meses: float = Field(gt=0, le=2400)
    tasa_descuento: float = Field(ge=0, le=10000)


@app.post("/api/ejercicios/8", tags=["Tasa equivalente"])
def ejercicio_8(d: E8):
    if d.recibido > d.nominal:
        raise HTTPException(422, "El capital recibido no puede superar al valor nominal de este descuento anticipado.")
    n = d.meses / 12
    descuento = d.nominal - d.recibido
    real = descuento / (d.recibido * n) * 100
    d_original = d.tasa_descuento / 100
    if d_original * n >= 1:
        raise HTTPException(422, "La tasa de descuento ingresada no permite un capital líquido positivo para ese plazo.")
    equivalente_tasa_d = d_original / (1 - d_original * n) * 100
    tasa_implicita = descuento / (d.nominal * n) * 100
    coincide = abs(real - equivalente_tasa_d) < 0.00001
    nota = ("La comprobación coincide: la tasa de descuento y el capital recibido son coherentes."
            if coincide else "Atención: al cambiar los datos, el nominal, el recibido y la tasa de descuento ya no son coherentes entre sí. La tasa real principal se calcula con el dinero efectivamente recibido; la otra tasa corresponde al descuento indicado.")
    return respuesta("Tasa simple real equivalente", porcentaje(real) + " anual", [
        "Fórmula principal: i = (F − P) / (P × n)",
        f"Costo financiero: I = {usd(d.nominal)} − {usd(d.recibido)} = {usd(descuento)}",
        f"Plazo: n = {numero_es(d.meses, 2)}/12 = {numero_es(n, 6)} años",
        f"Tasa real: i = {usd(descuento)} / ({usd(d.recibido)} × {numero_es(n, 6)}) × 100 = {porcentaje(real)}",
        f"Comprobación desde d: i = d / (1 − d × n) = {porcentaje(equivalente_tasa_d)}",
    ], secundarios=[
        {"etiqueta": "Tasa por fórmula de descuento", "valor": porcentaje(equivalente_tasa_d) + " anual"},
        {"etiqueta": "Descuento implícito de los flujos", "valor": porcentaje(tasa_implicita) + " anual"},
    ], nota=nota)
