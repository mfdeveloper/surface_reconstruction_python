[CmdletBinding()]
param (
    [string]
    $VirtualEnvFolder = 'venv',
    [bool]
    $Force = $true,
    [bool]
    $Execute = $true
)

function Test-Command-Exists {
<#
.SYNOPSIS
    Check if a command exists: whether is installed or in your $PATH environment variable

.PARAMETER Command
    The to verify if exists in your environment.

.EXAMPLE
     Test-Command-Exists 'python'

.INPUTS
    String

.OUTPUTS
    Boolean

.NOTES
    Author:  Felipe Ferreira
    Website: http://github.com/mfdeveloper
    Twitter: @mfdeveloper
#>
    param (
        [string]
        $Command
    )

    try {
        if(Get-Command -Name $Command){
            return $true
        }
    } catch {
        return $false
    }
    
}

function Install-Pyenv {
<#
.SYNOPSIS
    Try install the pyenv CLI, if not exists in your system

.EXAMPLE
     if(Install-Pyenv) {
         # Continue your script automation process
     }

.OUTPUTS
    Boolean

.NOTES
    Author:  Felipe Ferreira
    Website: http://github.com/mfdeveloper
    Twitter: @mfdeveloper
#>
    if (-not(Test-Command-Exists 'pyenv')) {

        if (-not(Test-Command-Exists 'choco')) {
            Write-Error 'The chocolatey package manager is not installed. Please, install it from: https://chocolatey.org/install'
            return $false
        }
        
        Invoke-Expression 'choco install pyenv-win'
        $result = Invoke-Expression 'pyenv rehash'
        
        Write-Host $result
    }
    
    $pyenvVersion = Invoke-Expression 'pyenv --version'
    Write-Host "$pyenvVersion installed!"
    return $true
}

function Install-Python {
<#
.SYNOPSIS
    Try install the python command, and verify if the version located in .python-versions is equal of in your system

.EXAMPLE
     if(Install-Python) {
         # Continue your script automation process
     }

.OUTPUTS
    Boolean

.NOTES
    Author:  Felipe Ferreira
    Website: http://github.com/mfdeveloper
    Twitter: @mfdeveloper
#>
    if (-not(Test-Command-Exists 'python')) {
        
        $lines = Get-Content -Path .\.python-version
        
        foreach ($version in $lines) {
        
            Invoke-Expression -Command "pyenv install $version"
        }
    }
    
    $currentVersion = Invoke-Expression 'python --version'
    $currentVersion = $currentVersion.Replace("Python ", "")
    $projectVersion = Invoke-Expression 'pyenv local'

    if ($currentVersion -ne $projectVersion) {
        Write-Warning "The version '$currentVersion' in your system is not equals to version '$projectVersion' in '.python-version' file.
        Is recommended to install '$projectVersion' version, and activate it with virtualenv"

        return $false
    }
    
    Write-Host "Python $currentVersion installed!"

    return $true
}

function Mount-Virtual-Env {
<#
.SYNOPSIS
    Create and activate the python virtualenv folder

.PARAMETER FolderName
    The name of the folder to create a virtualenv. By default, the name is "venv"

.EXAMPLE
     # Optionally, pass a custom folder name. In this case is "myenv"
     Mount-Virtual-Env -FolderName myenv

.INPUTS
    String

.OUTPUTS
    Boolean

.NOTES
    Author:  Felipe Ferreira
    Website: http://github.com/mfdeveloper
    Twitter: @mfdeveloper
#>
    [CmdletBinding()]
    param (
        [string]
        $FolderName = 'venv'
    )

    if ($FolderName.Length -le 0) {
        Write-Error "The virtualenv folder '$FolderName' is invalid"
        return $false
    }

    if ($Force) {
        Write-Host "Removing folder '$FolderName' ..."
        Remove-Item ".\$FolderName" -Force
    }
    
    if ( -not(Test-Path ".\$FolderName") ) {
        Write-Host 'Creating Python VIRTUAL ENVIRONMENT:'
    
        $resultCreation = Invoke-Expression "python -m venv $FolderName"
        Write-Host $resultCreation
    } else {
        Write-Host "VIRTUAL ENVIRONMENT '$FolderName' was found!"
    }
    
    Invoke-Expression -Command ".\$FolderName\Scripts\Activate.ps1"
    return $true
}

function Install-Packages-Dependencies {
<#
.SYNOPSIS
    Try install the package dependencies from requirements-dev.txt or requirements.txt file

.EXAMPLE
     Install-Packages-Dependencies

.OUTPUTS
    String

.NOTES
    Author:  Felipe Ferreira
    Website: http://github.com/mfdeveloper
    Twitter: @mfdeveloper
#>
    
    Write-Host 'Installing dependencies'
    $files = @('requirements-dev.txt', 'requirements.txt')

    $invokedInstall = $false

    foreach ($fileName in $files) {
        if (Test-Path $fileName -PathType leaf) {
            Invoke-Expression -Command "pip install -r .\$fileName"
            $invokedInstall = $true
            break
        }
    }

    if (!$invokedInstall) {
        Write-Host 'requirements.txt file was not found'
    }
    
}

function Run {
    
    if(Install-Pyenv) {
    
        if(Install-Python) {
    
            $virtualEnvCreated = Mount-Virtual-Env -FolderName $VirtualEnvFolder
    
            if($virtualEnvCreated) {
                Install-Packages-Dependencies
            }
        }
    }
}

if ($Execute) {
    Run
}
