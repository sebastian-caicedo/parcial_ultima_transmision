#!/usr/bin/env bash
# Crea el tablero del parcial desde cero.
#  - Crea una issue por tarea de docs/backlog.md con título descriptivo, etiquetas y responsable
#  - Crea un tablero nuevo en GitHub Projects, lo vincula al repo y agrega las issues
#  - Estado inicial: T01 en Done, T02 en In Progress, el resto en Todo
#
# Funciona en Linux/macOS y en Windows con Git Bash. Solo necesita gh (no jq).
#
# Requisitos (una sola vez):
#   gh auth login
#   gh auth refresh -s project
#   Javier debe haber ACEPTADO la invitación de colaborador al repo (si no, no se le puede asignar).
#
# Uso, desde la raíz del repo:
#   bash scripts/crear_tablero.sh

set -euo pipefail

REPO="sebastian-caicedo/parcial_ultima_transmision"
OWNER="sebastian-caicedo"
USR_SC="sebastian-caicedo"
USR_JC="jxviercarta-a11y"
TITULO_TABLERO="Tablero - Parcial IS La última transmisión"

: > docs/mapa_issues.txt

# ---------- 1. Etiquetas ----------
echo "Creando etiquetas..."
etq() { gh label create "$1" --color "$2" --repo "$REPO" --force >/dev/null; }
etq "prioridad:A" "d73a4a"; etq "prioridad:M" "fbca04"; etq "prioridad:B" "0e8a16"
for u in 1 2 3 4 5 6 7; do etq "unidad-$u" "1d76db"; done
etq "cambio" "5319e7"; etq "entrega" "c5def5"

# ---------- 2. Tablero ----------
echo "Creando tablero..."
PROJ_NUM="$(gh project create --owner "$OWNER" --title "$TITULO_TABLERO" --format json --jq .number)"
PROJ_ID="$(gh project view "$PROJ_NUM" --owner "$OWNER" --format json --jq .id)"
gh project link "$PROJ_NUM" --owner "$OWNER" --repo "$REPO" >/dev/null || true

STATUS_ID="$(gh project field-list "$PROJ_NUM" --owner "$OWNER" --format json --jq '.fields[]|select(.name=="Status")|.id')"
opt() { gh project field-list "$PROJ_NUM" --owner "$OWNER" --format json --jq ".fields[]|select(.name==\"Status\")|.options[]|select(.name==\"$1\")|.id"; }
OPT_TODO="$(opt Todo)"; OPT_PROG="$(opt "In Progress")"; OPT_DONE="$(opt Done)"

# ---------- 3. Issues ----------

grep -E '^\| T[0-9]+' docs/backlog.md | while IFS='|' read -r _ id tarea unidad prio resp _; do
  id="$(xargs <<<"$id")"; tarea="$(xargs <<<"$tarea")"; unidad="$(xargs <<<"$unidad")"
  prio="$(xargs <<<"$prio")"; resp="$(xargs <<<"$resp")"

  etiquetas="prioridad:$prio"
  [[ "$unidad" =~ ^[1-7]$ ]] && etiquetas="$etiquetas,unidad-$unidad"
  [[ "$tarea" =~ [Cc]ambio ]] && etiquetas="$etiquetas,cambio"
  [[ "$tarea" =~ (ZIP|Video|Informe|README|[Cc]aptura) ]] && etiquetas="$etiquetas,entrega"

  asignar=()
  [[ "$resp" == *SC* ]] && asignar+=(--add-assignee "$USR_SC")
  [[ "$resp" == *JC* ]] && asignar+=(--add-assignee "$USR_JC")

  cuerpo="Tarea $id del backlog (docs/backlog.md). Unidad: $unidad. Prioridad: $prio. Responsable: $resp.
Ver definición de terminado en docs/plan_trabajo.md."

  url="$(gh issue create --repo "$REPO" --title "$id - $tarea" --body "$cuerpo" --label "$etiquetas" "${asignar[@]}")"

  item="$(gh project item-add "$PROJ_NUM" --owner "$OWNER" --url "$url" --format json --jq .id)"
  case "$id" in
    T01) estado="$OPT_DONE" ;;
    T02) estado="$OPT_PROG" ;;
    *)   estado="$OPT_TODO" ;;
  esac
  gh project item-edit --id "$item" --project-id "$PROJ_ID" --field-id "$STATUS_ID" --single-select-option-id "$estado" >/dev/null
  if [[ "$id" == "T01" ]]; then gh issue close "$url" --reason completed >/dev/null; fi
  echo "$id -> #${url##*/} ($resp)" | tee -a docs/mapa_issues.txt
done

echo
echo "Listo: https://github.com/users/$OWNER/projects/$PROJ_NUM"
echo "Correspondencia tarea -> issue guardada en docs/mapa_issues.txt (súbela al repo)."
echo "En la vista Board activa View > Fields > Assignees y Labels antes de la captura."
