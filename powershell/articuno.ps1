<#
Basic powershell startup script

RUN SCRIPT AS ADMIN CODE - https://www.petri.com/run-powershell-scripts-with-administrative-privileges

Script Tasks
------------
1.) start itself with admin privileges
2.) start a transcript for the session (stored in default location)
3.) imports the third party PSReadLine module
4.) updates the help system
5.) sets the starting location to C drive
6.) displays the current powershell version

#>

#1.)
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

#2.)
Start-Transcript

#3.)
Import-Module PSReadLine

#4.)
Update-Help

#5.)
Set-Location -Path C:\

#6.)
$PSVersionTable.PSVersion