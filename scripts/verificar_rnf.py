"""Verifica los tres RNF y guarda la evidencia en evidencias/rnf/ (T29).

Uso, desde la raíz del repositorio:
    python scripts/verificar_rnf.py
"""
import subprocess
import sys
from datetime import datetime
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
SALIDA = RAIZ / "evidencias" / "rnf"


def ejecutar(comando):
    r = subprocess.run(comando, cwd=RAIZ, capture_output=True, text=True, encoding="utf-8", errors="replace")
    return r.returncode, (r.stdout + r.stderr).strip()


def guardar(nombre, titulo, cuerpo, aprobado):
    texto = (f"{titulo}\nFecha: {datetime.now():%Y-%m-%d %H:%M}\n"
             f"Resultado: {'CUMPLE' if aprobado else 'NO CUMPLE'}\n\n{cuerpo}\n")
    (SALIDA / nombre).write_text(texto, encoding="utf-8")
    print(f"{nombre}: {'CUMPLE' if aprobado else 'NO CUMPLE'}")
    return aprobado


def rnf01():
    titulo = "RNF01 - Agregar una historia requiere 0 líneas cambiadas en src/"
    _, commits = ejecutar(["git", "log", "--format=%h %an %s", "--diff-filter=A", "--", "data/segunda_historia.json"])
    if not commits:
        return guardar("rnf01_resultado.txt", titulo, "No existe un commit que agregue data/segunda_historia.json.", False)
    commit = commits.splitlines()[-1].split()[0]
    _, archivos = ejecutar(["git", "show", "--stat", "--format=%h %an %ad %s", commit])
    toca_src = any(linea.strip().startswith("src/") for linea in archivos.splitlines())
    _, prueba = ejecutar([sys.executable, "-m", "pytest", "tests/test_integracion.py", "-k", "I2", "-q", "-p", "no:cacheprovider"])
    aprobado = (not toca_src) and "1 passed" in prueba
    cuerpo = (f"Commit que agrega la segunda historia:\n{archivos}\n\n"
              f"Archivos de src/ modificados en ese commit: {'SÍ' if toca_src else 'NINGUNO'}\n\n"
              f"Prueba de integración con la segunda historia:\n{prueba}")
    return guardar("rnf01_resultado.txt", titulo, cuerpo, aprobado)


def rnf_pytest(nombre, filtro, titulo, minimo):
    _, salida = ejecutar([sys.executable, "-m", "pytest", "tests/test_rnf.py", "-k", filtro, "-v", "-p", "no:cacheprovider"])
    aprobados = salida.count(" PASSED")
    aprobado = aprobados >= minimo and "failed" not in salida.lower().split("=")[-1]
    return guardar(nombre, titulo, f"Casos aprobados: {aprobados} (mínimo esperado {minimo})\n\n{salida}", aprobado)


if __name__ == "__main__":
    SALIDA.mkdir(parents=True, exist_ok=True)
    resultados = [
        rnf01(),
        rnf_pytest("rnf02_resultado.txt", "RNF02",
                   "RNF02 - 9/9 archivos inválidos con código, causa e ID identificable", 10),
        rnf_pytest("rnf03_resultado.txt", "RNF03",
                   "RNF03 - 1000 entradas inválidas: 0 excepciones y estado idéntico", 1),
    ]
    sys.exit(0 if all(resultados) else 1)
