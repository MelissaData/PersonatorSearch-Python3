# Name:    PersonatorSearchCloudAPI
# Purpose: Execute the PersonatorSearchCloudAPI program


######################### Parameters ##########################
param(
    $fullname = '', 
    $addressline1 = '', 
    $city = '', 
    $state = '', 
    $postal = '', 
    $license = '', 
    [switch]$quiet = $false
    )


########################## Main ############################
Write-Host "`n===================== Melissa Personator Search Cloud API ======================`n"

# Get license (either from parameters or user input)
if ([string]::IsNullOrEmpty($license) ) {
  $license = Read-Host "Please enter your license string"
}

# Check for License from Environment Variables 
if ([string]::IsNullOrEmpty($license) ) {
  $license = $env:MD_LICENSE
}

if ([string]::IsNullOrEmpty($license)) {
  Write-Host "`nLicense String is invalid!"
  Exit
}

# Run project
if ([string]::IsNullOrEmpty($fullname) -and [string]::IsNullOrEmpty($addressline1) -and [string]::IsNullOrEmpty($city) -and [string]::IsNullOrEmpty($state) -and [string]::IsNullOrEmpty($postal)) {
  python3 PersonatorSearchPython3.py --license $license 
}
else {
  python3 PersonatorSearchPython3.py --license $license --fullname $fullname --addressline1 $addressline1 --city $city --state $state --postal $postal
}
