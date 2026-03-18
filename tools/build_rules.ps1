[CmdletBinding()]
param(
    [Parameter(ValueFromRemainingArguments = $true)]
    [string[]]$ScriptArgs
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$repoRoot = Split-Path -Parent $PSScriptRoot
$pythonScript = Join-Path $PSScriptRoot "build_rules.py"

function Resolve-PythonCommand {
    $candidates = @()

    if ($env:RULEMESH_PYTHON) {
        $candidates += [pscustomobject]@{
            Kind = "Path"
            Value = $env:RULEMESH_PYTHON
            Label = "RULEMESH_PYTHON"
        }
    }

    if ($env:SURGE_CONFIG_PYTHON) {
        $candidates += [pscustomobject]@{
            Kind = "Path"
            Value = $env:SURGE_CONFIG_PYTHON
            Label = "SURGE_CONFIG_PYTHON (legacy)"
        }
    }

    $candidates += [pscustomobject]@{
        Kind = "Path"
        Value = (Join-Path $repoRoot ".venv\Scripts\python.exe")
        Label = ".venv"
    }

    $candidates += [pscustomobject]@{
        Kind = "Path"
        Value = "C:\Users\zaife\AppData\Local\Programs\Python\Python314\python.exe"
        Label = "Python314"
    }

    $pythonCommand = Get-Command python -ErrorAction SilentlyContinue
    if ($pythonCommand) {
        $candidates += [pscustomobject]@{
            Kind = "Command"
            Value = $pythonCommand.Source
            Label = "python"
        }
    }

    foreach ($candidate in $candidates) {
        if ($candidate.Kind -eq "Path" -and -not (Test-Path $candidate.Value)) {
            continue
        }

        return $candidate
    }

    $pyLauncher = Get-Command py -ErrorAction SilentlyContinue
    if ($pyLauncher) {
        return [pscustomobject]@{
            Kind = "Launcher"
            Value = $pyLauncher.Source
            Label = "py -3"
        }
    }

    throw @"
No usable Python interpreter was found.
Try one of these:
1. Set RULEMESH_PYTHON (or legacy SURGE_CONFIG_PYTHON) to a valid python.exe path
2. Install Python and ensure python or py -3 works
3. Use the known local path: C:\Users\zaife\AppData\Local\Programs\Python\Python314\python.exe
"@
}

$python = Resolve-PythonCommand
$env:PYTHONUTF8 = "1"

Write-Host ("[build_rules.ps1] using {0}: {1}" -f $python.Label, $python.Value)

if ($python.Kind -eq "Launcher") {
    & $python.Value -3 -X utf8 $pythonScript @ScriptArgs
}
else {
    & $python.Value -X utf8 $pythonScript @ScriptArgs
}

exit $LASTEXITCODE
