# Automated Screenshot Capture for ScholarNexus AI using Headless Microsoft Edge

$edgePath = "C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
if (-not (Test-Path $edgePath)) {
    $edgePath = "C:\Program Files\Microsoft\Edge\Application\msedge.exe"
}

Write-Host "Using Browser: $edgePath"

# 1. Start Streamlit
$proc = Start-Process python -ArgumentList "-m", "streamlit", "run", "app.py", "--browser.gatherUsageStats=false", "--server.port=8501" -PassThru
Write-Host "Started Streamlit PID: $($proc.Id)"

# Wait for server
Start-Sleep -Seconds 6

$urls = @(
    @{ Name = "screenshot_3_1_home_dashboard.png"; Url = "http://localhost:8501/?nav=home" },
    @{ Name = "screenshot_3_2_student_profile.png"; Url = "http://localhost:8501/?nav=profile" },
    @{ Name = "screenshot_3_3_scheme_directory.png"; Url = "http://localhost:8501/?nav=explorer" },
    @{ Name = "screenshot_3_4_document_checklist.png"; Url = "http://localhost:8501/?nav=checklist" },
    @{ Name = "screenshot_3_5_scholarbot_chat.png"; Url = "http://localhost:8501/?nav=chat" },
    @{ Name = "screenshot_3_6_official_portals.png"; Url = "http://localhost:8501/?nav=portals" }
)

try {
    foreach ($item in $urls) {
        $outFile = $item.Name
        $targetUrl = $item.Url
        Write-Host "Capturing $outFile from $targetUrl..."
        
        # Call headless Edge
        & $edgePath --headless --disable-gpu --hide-scrollbars --window-size=1600,1050 --virtual-time-budget=4000 --screenshot="$outFile" "$targetUrl"
        Start-Sleep -Seconds 1
        
        if (Test-Path $outFile) {
            Write-Host "Successfully captured: $outFile ($((Get-Item $outFile).Length) bytes)"
        } else {
            Write-Host "Failed to capture $outFile"
        }
    }
} finally {
    Write-Host "Stopping Streamlit PID: $($proc.Id)"
    Stop-Process -Id $proc.Id -Force
}
