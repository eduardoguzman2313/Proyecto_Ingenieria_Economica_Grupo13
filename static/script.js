/* Catálogo de los ocho ejercicios originales. Cada uno mantiene su fórmula propia en FastAPI. */
const ejercicios = [
  {
    numero: 1, contenedor: 'lista-interes', titulo: 'Tasa de interés anual', tipo: 'Calcular tasa',
    enunciado: '¿Cuál es la tasa de interés a la que estuvo invertido un capital de $110.000 durante 2 años y 5 meses si produjo $39.875 de interés?',
    original: '15 % anual',
    campos: [
      ['capital', 'Capital inicial ($)', 110000, 0.01, 'any'],
      ['interes', 'Interés generado ($)', 39875, 0, 'any'],
      ['anios', 'Años enteros', 2, 0, 1, 200],
      ['meses', 'Meses adicionales', 5, 0, 1, 11]
    ]
  },
  {
    numero: 2, contenedor: 'lista-interes', titulo: 'Tiempo de inversión', tipo: 'Calcular tiempo',
    enunciado: '¿Qué tiempo estuvo invertido un capital de $85.000 que produjo $35.700 de interés a una tasa simple anual del 21 %?',
    original: '2 años · 24 meses',
    campos: [
      ['capital', 'Capital ($)', 85000, 0.01, 'any'],
      ['interes', 'Interés generado ($)', 35700, 0, 'any'],
      ['tasa_anual', 'Tasa de interés anual (%)', 21, 0.000001, 'any']
    ]
  },
  {
    numero: 3, contenedor: 'lista-interes', titulo: 'Capital inicial o valor presente', tipo: 'Calcular capital',
    enunciado: 'Encontrar el valor presente, al 6 % de interés simple anual, de $1.500 con vencimiento en 9 meses.',
    original: '$1.435,41',
    campos: [
      ['monto_futuro', 'Monto futuro ($)', 1500, 0.01, 'any'],
      ['tasa_anual', 'Tasa simple anual (%)', 6, 0, 'any'],
      ['meses', 'Tiempo (meses)', 9, 0.000001, 'any']
    ]
  },
  {
    numero: 4, contenedor: 'lista-focal', titulo: 'Inversión para tres pagos futuros', tipo: 'Valor presente',
    enunciado: 'Invertir el 15 de febrero al 5,1 % simple anual para disponer de $7.000 el 9 de mayo, $15.500 el 20 de junio y $10.000 el 23 de diciembre. Usar año de 360 días.',
    original: '$31.726,96',
    campos: [
      ['tasa_anual', 'Tasa simple anual (%)', 5.1, 0, 'any'],
      ['base_dias', 'Días del año comercial', 360, 1, 1, 366],
      ['monto_1', 'Pago 1 · 9 de mayo ($)', 7000, 0, 'any'],
      ['dias_1', 'Días hasta el pago 1', 83, 0, 1, 30000],
      ['monto_2', 'Pago 2 · 20 de junio ($)', 15500, 0, 'any'],
      ['dias_2', 'Días hasta el pago 2', 125, 0, 1, 30000],
      ['monto_3', 'Pago 3 · 23 de diciembre ($)', 10000, 0, 'any'],
      ['dias_3', 'Días hasta el pago 3', 311, 0, 1, 30000]
    ]
  },
  {
    numero: 5, contenedor: 'lista-focal', titulo: 'Depósitos y retiro en fecha focal', tipo: 'Saldo focal',
    enunciado: 'Adriana deposita $15.000 el 15 de diciembre y $10.000 el 11 de marzo; retira $9.500 el 28 de enero. Valorar todo al 9 de mayo con i = 12,48 % simple anual.',
    original: '$16.125,90',
    campos: [
      ['tasa_anual', 'Tasa simple anual (%)', 12.48, 0, 'any'],
      ['base_dias', 'Días del año comercial', 360, 1, 1, 366],
      ['deposito_1', 'Depósito · 15 de diciembre ($)', 15000, 0, 'any'],
      ['dias_1', 'Días hasta fecha focal (depósito 1)', 145, 0, 1, 30000],
      ['deposito_2', 'Depósito · 11 de marzo ($)', 10000, 0, 'any'],
      ['dias_2', 'Días hasta fecha focal (depósito 2)', 59, 0, 1, 30000],
      ['retiro', 'Retiro · 28 de enero ($)', 9500, 0, 'any'],
      ['dias_retiro', 'Días hasta fecha focal (retiro)', 101, 0, 1, 30000]
    ]
  },
  {
    numero: 6, contenedor: 'lista-focal', titulo: 'Sustitución de deudas', tipo: 'Calcular pago X',
    enunciado: 'Deuda de $1.000 con vencimiento en 6 meses, originada a 1,5 años al 4 %; otra de $2.500 vence en 9 meses sin intereses. Se pagan $2.000 hoy y X al año. Tasa de equivalencia: 5 %; fecha focal: 12 meses.',
    original: '$1.517,75',
    campos: [
      ['prestamo_1', 'Primera deuda, principal ($)', 1000, 0, 'any'],
      ['tasa_prestamo', 'Interés anual de primera deuda (%)', 4, 0, 'any'],
      ['plazo_contrato_anios', 'Plazo contractual (años)', 1.5, 0, 'any'],
      ['deuda_2', 'Segunda deuda ($)', 2500, 0, 'any'],
      ['tasa_equivalencia', 'Tasa simple de equivalencia (%)', 5, 0, 'any'],
      ['pago_hoy', 'Pago inmediato ($)', 2000, 0, 'any'],
      ['vencimiento_1_meses', 'Vence deuda 1 (meses desde hoy)', 6, 0, 'any'],
      ['vencimiento_2_meses', 'Vence deuda 2 (meses desde hoy)', 9, 0, 'any'],
      ['focal_meses', 'Fecha focal (meses desde hoy)', 12, 0.000001, 'any']
    ]
  },
  {
    numero: 7, contenedor: 'lista-descuento', titulo: 'Descuento por anticipado', tipo: 'Descuento comercial',
    enunciado: 'Un préstamo nominal de $30.000 por 8 meses se descuenta al 35 % anual por anticipado. Calcular (a) descuento y (b) capital líquido recibido.',
    original: '$23.000,00 de capital líquido · $7.000,00 de descuento',
    campos: [
      ['nominal', 'Valor nominal ($)', 30000, 0.01, 'any'],
      ['tasa_descuento', 'Tasa de descuento anual (%)', 35, 0, 'any'],
      ['meses', 'Plazo (meses)', 8, 0.000001, 'any']
    ]
  },
  {
    numero: 8, contenedor: 'lista-equivalente', titulo: 'Tasa de interés real equivalente', tipo: 'Tasa real',
    enunciado: 'Para el préstamo nominal de $30.000 con descuento anticipado de $7.000 y capital líquido de $23.000, determinar la tasa simple anual equivalente durante 8 meses.',
    original: '45,6522 % anual',
    campos: [
      ['nominal', 'Valor nominal ($)', 30000, 0.01, 'any'],
      ['recibido', 'Capital líquido recibido ($)', 23000, 0.01, 'any'],
      ['meses', 'Plazo (meses)', 8, 0.000001, 'any'],
      ['tasa_descuento', 'Tasa de descuento anual para comprobar (%)', 35, 0, 'any']
    ]
  }
];

function texto(etiqueta, contenido, clase) {
  const e = document.createElement(etiqueta);
  if (clase) e.className = clase;
  e.textContent = contenido;
  return e;
}

function renderizarRespuesta(caja, data) {
  caja.replaceChildren();
  caja.appendChild(texto('h4', data.titulo || 'Resultado'));
  caja.appendChild(texto('strong', data.resultado, 'resultado-principal'));
  if (data.secundarios && data.secundarios.length) {
    const fila = document.createElement('div');
    fila.className = 'resultado-secundarios';
    data.secundarios.forEach(item => fila.appendChild(texto('span', `${item.etiqueta}: ${item.valor}`)));
    caja.appendChild(fila);
  }
  if (data.tabla && data.tabla.length) {
    const bloque = document.createElement('div');
    bloque.className = 'resultado-tabla';
    const tabla = document.createElement('table');
    const thead = document.createElement('thead');
    const filaCab = document.createElement('tr');
    ['Operación', 'Tiempo', 'Valor focal / presente'].forEach(h => filaCab.appendChild(texto('th', h)));
    thead.appendChild(filaCab); tabla.appendChild(thead);
    const tbody = document.createElement('tbody');
    data.tabla.forEach(item => {
      const fila = document.createElement('tr');
      [item.concepto, item.dato, item.resultado].forEach(v => fila.appendChild(texto('td', v)));
      tbody.appendChild(fila);
    });
    tabla.appendChild(tbody); bloque.appendChild(tabla); caja.appendChild(bloque);
  }
  caja.appendChild(texto('h4', 'Procedimiento matemático'));
  const pasos = document.createElement('ol');
  pasos.className = 'resultado-pasos';
  (data.pasos || []).forEach(paso => pasos.appendChild(texto('li', paso)));
  caja.appendChild(pasos);
  if (data.nota) caja.appendChild(texto('p', data.nota, 'resultado-nota'));
  caja.hidden = false;
}

function crearEjercicio(ejercicio) {
  const articulo = document.createElement('article');
  articulo.className = 'ejercicio';
  articulo.id = `ejercicio-${ejercicio.numero}`;

  const encabezado = document.createElement('div');
  encabezado.className = 'ejercicio-head';
  const titulos = document.createElement('div');
  titulos.appendChild(texto('span', `EJERCICIO ${ejercicio.numero}`, 'numero-ejercicio'));
  titulos.appendChild(texto('h3', ejercicio.titulo));
  encabezado.appendChild(titulos);
  encabezado.appendChild(texto('span', ejercicio.tipo, 'tipo-ejercicio'));
  articulo.appendChild(encabezado);
  articulo.appendChild(texto('p', ejercicio.enunciado, 'enunciado'));
  articulo.appendChild(texto('p', 'DATOS EDITABLES', 'etiqueta-datos'));

  const formulario = document.createElement('form');
  formulario.id = `form-${ejercicio.numero}`;
  const campos = document.createElement('div');
  campos.className = 'campos';
  ejercicio.campos.forEach(([clave, titulo, valor, minimo, paso, maximo]) => {
    const contenedor = document.createElement('div');
    contenedor.className = 'campo';
    const id = `e${ejercicio.numero}-${clave}`;
    const label = document.createElement('label');
    label.htmlFor = id;
    label.textContent = titulo;
    const input = document.createElement('input');
    input.type = 'number';
    input.name = clave;
    input.id = id;
    input.value = String(valor);
    input.defaultValue = String(valor);
    input.min = String(minimo);
    input.step = String(paso);
    if (maximo !== undefined) input.max = String(maximo);
    input.required = true;
    contenedor.append(label, input);
    campos.appendChild(contenedor);
  });
  formulario.appendChild(campos);
  const acciones = document.createElement('div');
  acciones.className = 'acciones';
  const boton = texto('button', 'Calcular y ver procedimiento', 'btn-calcular');
  boton.type = 'submit';
  acciones.appendChild(boton);
  acciones.appendChild(texto('span', `Resultado original: ${ejercicio.original}`, 'resultado-original'));
  formulario.appendChild(acciones);
  articulo.appendChild(formulario);

  const error = document.createElement('p');
  error.className = 'resultado-error';
  error.setAttribute('role', 'alert');
  error.hidden = true;
  articulo.appendChild(error);
  const resultado = document.createElement('div');
  resultado.className = 'resultado';
  resultado.setAttribute('aria-live', 'polite');
  resultado.hidden = true;
  articulo.appendChild(resultado);
  const ocultar = () => { resultado.hidden = true; error.hidden = true; };
  formulario.addEventListener('input', ocultar);
  formulario.addEventListener('reset', ocultar);
  formulario.addEventListener('submit', async evento => {
    evento.preventDefault();
    if (!formulario.reportValidity()) return;
    const valores = {};
    new FormData(formulario).forEach((v, k) => { valores[k] = Number(v); });
    boton.disabled = true;
    boton.textContent = 'Calculando…';
    ocultar();
    try {
      const respuesta = await fetch(`/api/ejercicios/${ejercicio.numero}`, {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify(valores)
      });
      const datos = await respuesta.json();
      if (!respuesta.ok) {
        const detalle = datos.detail;
        const mensaje = typeof detalle === 'string' ? detalle :
          (Array.isArray(detalle) && detalle.length ? detalle[0].msg : 'Verifica los datos ingresados.');
        throw new Error(mensaje);
      }
      renderizarRespuesta(resultado, datos);
    } catch (err) {
      error.textContent = `No se pudo calcular: ${err.message}`;
      error.hidden = false;
    } finally {
      boton.disabled = false;
      boton.textContent = 'Calcular y ver procedimiento';
    }
  });
  return articulo;
}

for (const ejercicio of ejercicios) {
  const seccion = document.getElementById(ejercicio.contenedor);
  if (seccion) seccion.appendChild(crearEjercicio(ejercicio));
}

/* Mantener los enlaces al ejercicio visible incluso al entrar con un # desde otra pestaña. */
if (location.hash && /^#ejercicio-[1-8]$/.test(location.hash)) {
  requestAnimationFrame(() => document.querySelector(location.hash)?.scrollIntoView());
}
