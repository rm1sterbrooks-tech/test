# Settings
$User = "root"
$HostName = "185.167.58.68"
$Dir = "/opt/tictactoe"

# Paths to SSH/SCP (using Git's bundled OpenSSH)
$SSH = "C:\Program Files\Git\usr\bin\ssh.exe"
$SCP = "C:\Program Files\Git\usr\bin\scp.exe"

Write-Host "Starting deployment to $HostName..." -ForegroundColor Green

# 1. Create directory
Write-Host "Creating directory..."
& $SSH $User@$HostName "mkdir -p $Dir"

# 2. Copy files
Write-Host "Copying files (enter password if requested)..."
& $SCP -r docker-compose.yml backend frontend telegram-bot "$User@$HostName`:$Dir"

# 3. Run Docker Compose
Write-Host "Rebuilding and starting containers..."
& $SSH $User@$HostName "cd $Dir && docker-compose down && docker-compose up -d --build"

Write-Host "Deployment complete!" -ForegroundColor Green
Write-Host "Check your site at: http://$HostName:3000" -ForegroundColor Cyan
