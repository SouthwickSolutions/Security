<#
Basic powershell startup script

https://www.petri.com/run-powershell-scripts-with-administrative-privileges

#>

#########START RUN AS ADMIN##########

param([switch]$Elevated)

function Check-Admin{
    $currentUser = New-Object Security.Principal.WindowsPrincipal $([Security.Principal.WindowsIdentity]::GetCurrent())
    $currentUser.IsInRole([Security.Principal.WindowsBuiltinRole]::Administrator)
}

if((Check-Admin) -eq $false){
    if($elevated){
        # could not elevate, quit
    }
 
    else{
        Start-Process powershell.exe -Verb RunAs -ArgumentList ('-noprofile -noexit -file "{0}" -elevated' -f ($myinvocation.MyCommand.Definition))
    }
    exit
}

##########END RUN AS ADMIN##########

Start-Transcript
Import-Module PSReadLine
Update-Help