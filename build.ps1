$exclude = @("venv", "Grupo-5.zip")
$files = Get-ChildItem -Path . -Exclude $exclude
Compress-Archive -Path $files -DestinationPath "Grupo-5.zip" -Force