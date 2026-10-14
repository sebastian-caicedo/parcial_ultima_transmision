# Crea el tablero del parcial desde cero (versión para Windows / PowerShell).
#  - Crea una issue por tarea de docs\backlog.md con título, etiquetas y responsable
#  - Crea un tablero en GitHub Projects, lo vincula al repo y agrega las issues
#  - Estado inicial: T01 en Done (cerrada), T02 en In Progress, el resto en Todo
#
# Requisitos (una sola vez):
#   gh auth login
#   gh auth refresh -s project
#   Javier debe haber ACEPTADO la invitación de colaborador al repo.
#
# Uso, desde la raíz del repo (CMD o PowerShell):
#   powershell -ExecutionPolicy Bypass -File scripts\crear_tablero.ps1

$ErrorActionPreference = 'Stop'
[Console]::OutputEncoding = [Text.Encoding]::UTF8

$REPO   = 'sebastian-caicedo/parcial_ultima_transmision'
$OWNER  = 'sebastian-caicedo'
$USR_SC = 'sebastian-caicedo'
$USR_JC = 'jxviercarta-a11y'
$TITULO = 'Tablero - Parcial IS La última transmisión'
$MAPA   = Join-Path (Get-Location) 'docs\mapa_issues.txt'
$utf8   = New-Object System.Text.UTF8Encoding($false)

function Gh {
    $salida = & gh @args
    if ($LASTEXITCODE -ne 0) { throw "Falló: gh $($args -join ' ')" }
    return $salida
}

[IO.File]::WriteAllText($MAPA, '', $utf8)

# ---------- 1. Etiquetas ----------
Write-Host 'Creando etiquetas...'
$etiquetas = @{
    'prioridad:A' = 'd73a4a'; 'prioridad:M' = 'fbca04'; 'prioridad:B' = '0e8a16'
    'cambio' = '5319e7'; 'entrega' = 'c5def5'
}
1..7 | ForEach-Object { $etiquetas["unidad-$_"] = '1d76db' }
foreach ($e in $etiquetas.Keys) { Gh label create $e --color $etiquetas[$e] --repo $REPO --force | Out-Null }

# ---------- 2. Tablero ----------
Write-Host 'Creando tablero...'
$projNum = (Gh project create --owner $OWNER --title $TITULO --format json --jq .number | Select-Object -Last 1).Trim()
$projId  = (Gh project view $projNum --owner $OWNER --format json --jq .id | Select-Object -Last 1).Trim()
& gh project link $projNum --owner $OWNER --repo $REPO | Out-Null

$campos = (Gh project field-list $projNum --owner $OWNER --format json | Out-String) | ConvertFrom-Json
$status = $campos.fields | Where-Object { $_.name -eq 'Status' }
$opt = @{}
foreach ($o in $status.options) { $opt[$o.name] = $o.id }

# ---------- 3. Issues ----------
$filas = Get-Content 'docs\backlog.md' -Encoding UTF8 | Where-Object { $_ -match '^\| T\d+' }
foreach ($fila in $filas) {
    $c = $fila.Split('|')
    $id = $c[1].Trim(); $tarea = $c[2].Trim(); $unidad = $c[3].Trim(); $prio = $c[4].Trim(); $resp = $c[5].Trim()
    $tarea = $tarea -replace '"', "'"   # PowerShell 5 rompe argumentos con comillas dobles

    $lbl = "prioridad:$prio"
    if ($unidad -match '^[1-7]$') { $lbl += ",unidad-$unidad" }
    if ($tarea -match '[Cc]ambio') { $lbl += ',cambio' }
    if ($tarea -match '(ZIP|Video|Informe|README|[Cc]aptura)') { $lbl += ',entrega' }

    $cuerpo = "Tarea $id del backlog (docs/backlog.md). Unidad: $unidad. Prioridad: $prio. Responsable: $resp.`nVer definición de terminado en docs/plan_trabajo.md."

    $ghArgs = @('issue', 'create', '--repo', $REPO, '--title', "$id - $tarea", '--body', $cuerpo, '--label', $lbl)
    if ($resp -like '*SC*') { $ghArgs += @('--assignee', $USR_SC) }
    if ($resp -like '*JC*') { $ghArgs += @('--assignee', $USR_JC) }

    $url = (Gh @ghArgs | Select-Object -Last 1).Trim()
    $item = (Gh project item-add $projNum --owner $OWNER --url $url --format json --jq .id | Select-Object -Last 1).Trim()

    switch ($id) {
        'T01'   { $estado = $opt['Done'] }
        'T02'   { $estado = $opt['In Progress'] }
        default { $estado = $opt['Todo'] }
    }
    Gh project item-edit --id $item --project-id $projId --field-id $status.id --single-select-option-id $estado | Out-Null
    if ($id -eq 'T01') { Gh issue close $url --reason completed | Out-Null }

    $linea = "$id -> #$($url.Split('/')[-1]) ($resp)"
    Write-Host $linea
    [IO.File]::AppendAllText($MAPA, "$linea`n", $utf8)
}

Write-Host ''
Write-Host "Listo: https://github.com/users/$OWNER/projects/$projNum"
Write-Host 'Correspondencia guardada en docs\mapa_issues.txt (súbela al repo).'
Write-Host 'En la vista Board activa View > Fields > Assignees y Labels antes de la captura.'
