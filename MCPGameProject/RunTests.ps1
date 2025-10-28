#!/usr/bin/env pwsh
<#
.SYNOPSIS
    Enhanced test runner for MCPGameProject with formatted output and failure analysis

.DESCRIPTION
    Runs automation tests for MCPGameProject with improved formatting, clear failure reporting,
    and stack trace analysis. Replaces the basic RunTests.bat with comprehensive test reporting.

.PARAMETER TestFilter
    Test filter to specify which tests to run (default: "UnrealMCP")

.PARAMETER OutputPath
    Path where test results will be saved (default: ".\TestResults")

.PARAMETER LogLevel
    Logging level: Verbose, Normal, Minimal (default: "Normal")

.PARAMETER ShowStackTrace
    Show detailed stack traces for failed tests (default: $true)

.EXAMPLE
    .\RunTests.ps1
    Runs all UnrealMCP tests with normal output

.EXAMPLE
    .\RunTests.ps1 -TestFilter "UnrealMCP.Actor" -LogLevel Verbose
    Runs only Actor tests with verbose logging

.EXAMPLE
    .\RunTests.ps1 -OutputPath "C:\Temp\MyResults" -ShowStackTrace $false
    Runs tests and saves results to custom path without stack traces
#>

param(
    [Parameter(Position = 0)]
    [string]$TestFilter = "UnrealMCP",

    [string]$OutputPath = ".\TestResults",

    [ValidateSet("Verbose", "Normal", "Minimal")]
    [string]$LogLevel = "Normal",

    [bool]$ShowStackTrace = $true,

    [switch]$Help
)

# Show help
if ($Help) {
    Get-Help $MyInvocation.MyCommand.Path -Full
    exit 0
}

# Utility functions
function Write-SectionHeader {
    param([string]$Title, [string]$Color = "Cyan")

    Write-Host "`n" -NoNewline
    Write-Host ("═" * 80) -ForegroundColor $Color
    Write-Host ("  " + $Title) -ForegroundColor $Color
    Write-Host ("═" * 80) -ForegroundColor $Color
    Write-Host ""
}

function Write-TestResult {
    param(
        [string]$TestName,
        [string]$Status,
        [string]$Message = "",
        [string]$Duration = ""
    )

    $statusColor = switch ($Status) {
        "PASSED" { "Green" }
        "FAILED" { "Red" }
        "SKIPPED" { "Yellow" }
        "WARNING" { "Yellow" }
        default { "White" }
    }

    $statusSymbol = switch ($Status) {
        "PASSED" { "✓" }
        "FAILED" { "✗" }
        "SKIPPED" { "→" }
        "WARNING" { "⚠" }
        default { "•" }
    }

    $output = "[{0}] {1}" -f $statusSymbol, $TestName
    if ($Duration -and $LogLevel -ne "Minimal") {
        $output += " ($Duration)"
    }

    Write-Host $output -ForegroundColor $statusColor

    if ($Message -and $LogLevel -eq "Verbose") {
        Write-Host "    $Message" -ForegroundColor Gray
    }
}

function Write-FailureDetails {
    param(
        [string]$TestName,
        [string]$ErrorMessage,
        [string]$StackTrace = "",
        [string]$LogFile = ""
    )

    Write-Host ""
    Write-Host "  ❌ FAILURE DETAILS:" -ForegroundColor Red
    Write-Host "  Test: $TestName" -ForegroundColor White
    Write-Host "  Error: $ErrorMessage" -ForegroundColor Red

    if ($ShowStackTrace -and $StackTrace) {
        Write-Host "`n  📋 STACK TRACE:" -ForegroundColor Yellow
        $StackTrace -split "`n" | ForEach-Object {
            Write-Host "    $_" -ForegroundColor Gray
        }
    }

    if ($LogFile) {
        Write-Host "`n  📄 Log File: $LogFile" -ForegroundColor Cyan
    } elseif ($unrealLogFile) {
        Write-Host "`n  📄 Log File: $($unrealLogFile.FullName)" -ForegroundColor Cyan
    }

    Write-Host ""
}

function Find-UnrealEngineInstallation {
    $possiblePaths = @(
        "C:\Program Files\Epic Games\UE_5.6",
        "C:\Program Files\Epic Games\UE_5.5",
        "C:\Program Files\Epic Games\UE_5.4",
        "C:\Program Files\Epic Games\UE_5.3"
    )

    foreach ($path in $possiblePaths) {
        if (Test-Path $path) {
            return $path
        }
    }

    return $null
}

function Parse-TestResults {
    param([string]$LogContent)

    $testResults = @()
    $lines = $LogContent -split "`n"
    $lastTestName = ""
    $lastTestPath = ""

    foreach ($line in $lines) {
        # Test completion patterns - Unreal's actual format
        if ($line -match "LogAutomationController.*Test Completed\. Result=\{(.+)\} Name=\{(.+)\} Path=\{(.+)\}") {
            $status = $matches[1]
            $testName = $matches[2]
            $fullPath = $matches[3]

            # Convert Unreal's result format to our format
            $normalizedStatus = switch ($status) {
                "Success" { "Passed" }
                "Failed" { "Failed" }
                "Error" { "Failed" }
                "Fail" { "Failed" }
                default {
                    if ($status -match "Fail|Error") { "Failed" } else { "Passed" }
                }
            }

            $testResults += [PSCustomObject]@{
                Name = $fullPath
                Duration = ""  # Unreal doesn't log duration in this format
                Status = $normalizedStatus
                ErrorMessage = ""
                StackTrace = ""
            }

            $lastTestName = $testName
            $lastTestPath = $fullPath
        }

        # Test started patterns - track when tests begin
        elseif ($line -match "LogAutomationController.*Test Started\. Name=\{(.+)\} Path=\{(.+)\}") {
            $testName = $matches[1]
            $fullPath = $matches[2]
            $lastTestName = $testName
            $lastTestPath = $fullPath
        }

        # Look for explicit error messages in automation tests
        elseif ($line -match "Error.*LogAutomationController.*Expected.*to be") {
            # This is a test assertion failure - extract the test name and error
            $errorMessage = $line.Trim()
            # Clean up the error message to make it more readable
            $errorMessage = $errorMessage -replace "Error\s+LogAutomationController:\s+", ""

            if ($testResults.Count -gt 0) {
                # Try to find the most recent test result or create one for lastTestPath
                $targetTest = if ($lastTestPath) {
                    $testResults | Where-Object { $_.Name -eq $lastTestPath } | Select-Object -First 1
                } else {
                    $testResults[-1]
                }

                if ($targetTest) {
                    $targetTest.Status = "Failed"
                    if (-not [string]::IsNullOrEmpty($targetTest.ErrorMessage)) {
                        $targetTest.ErrorMessage += "`n" + $errorMessage
                    } else {
                        $targetTest.ErrorMessage = $errorMessage
                    }
                }
            }
        }

        # Look for other error patterns
        elseif ($line -match "Error.*LogAutomationController") {
            $errorMessage = $line.Trim()
            if ($testResults.Count -gt 0) {
                $testResults[-1].ErrorMessage = $errorMessage
                $testResults[-1].Status = "Failed"
            }
        }

        # Stack trace patterns
        elseif ($line -match "\s+at\s+.+\s+\(.+:\d+\)" -or $line -match "\[0x[0-9a-fA-F]+\]") {
            if ($testResults.Count -gt 0 -and $ShowStackTrace) {
                $testResults[-1].StackTrace += $line.Trim() + "`n"
            }
        }
    }

    # Remove duplicates and sort by name
    $uniqueResults = @()
    $seenNames = @{}

    foreach ($result in $testResults) {
        if (-not $seenNames.ContainsKey($result.Name)) {
            $seenNames[$result.Name] = $true
            $uniqueResults += $result
        } else {
            # If duplicate, merge information (prefer failed status)
            $existing = $uniqueResults | Where-Object { $_.Name -eq $result.Name } | Select-Object -First 1
            if ($existing -and $result.Status -eq "Failed") {
                $existing.Status = "Failed"
                if ($result.ErrorMessage) {
                    $existing.ErrorMessage = $result.ErrorMessage
                }
            }
        }
    }

    return $uniqueResults | Sort-Object Name
}

function Get-TestSummary {
    param($TestResults)

    $passed = ($TestResults | Where-Object { $_.Status -eq "Passed" }).Count
    $failed = ($TestResults | Where-Object { $_.Status -eq "Failed" }).Count
    $skipped = ($TestResults | Where-Object { $_.Status -eq "Skipped" }).Count
    $total = $TestResults.Count

    $duration = [math]::Round(($TestResults | Measure-Object -Property Duration -Sum).Sum, 2)

    return @{
        Total = $total
        Passed = $passed
        Failed = $failed
        Skipped = $skipped
        Duration = $duration
        SuccessRate = if ($total -gt 0) { [math]::Round(($passed / $total) * 100, 1) } else { 0 }
    }
}

# Main execution
$ErrorActionPreference = "Stop"

try {
    Write-SectionHeader "MCPGAMEPROJECT TEST RUNNER" "Magenta"

    # Set project paths
    $ProjectRoot = $PSScriptRoot
    $ProjectFile = Join-Path $ProjectRoot "MCPGameProject.uproject"

    if (-not (Test-Path $ProjectFile)) {
        Write-Host "❌ ERROR: Project file not found: $ProjectFile" -ForegroundColor Red
        exit 1
    }

    # Find Unreal Engine
    $UEPath = Find-UnrealEngineInstallation
    if (-not $UEPath) {
        Write-Host "❌ ERROR: Could not find Unreal Engine installation" -ForegroundColor Red
        Write-Host "Please install UE 5.3, 5.4, 5.5, or 5.6 to C:\Program Files\Epic Games\" -ForegroundColor Yellow
        exit 1
    }

    $EditorCmd = Join-Path $UEPath "Engine\Binaries\Win64\UnrealEditor-Cmd.exe"
    if (-not (Test-Path $EditorCmd)) {
        Write-Host "❌ ERROR: UnrealEditor-Cmd.exe not found at: $EditorCmd" -ForegroundColor Red
        exit 1
    }

    # Create output directory
    if (-not (Test-Path $OutputPath)) {
        New-Item -ItemType Directory -Path $OutputPath -Force | Out-Null
    }

    # Generate timestamp for unique log files
    $timestamp = Get-Date -Format "yyyyMMdd_HHmmss"
    $logFile = Join-Path $OutputPath "TestRun_$timestamp.log"
    $resultsFile = Join-Path $OutputPath "TestResults_$timestamp.json"

    Write-Host "🎮 Configuration:" -ForegroundColor Cyan
    Write-Host "   Project: $ProjectFile" -ForegroundColor White
    Write-Host "   Unreal Engine: $UEPath" -ForegroundColor White
    Write-Host "   Test Filter: $TestFilter" -ForegroundColor White
    Write-Host "   Log Level: $LogLevel" -ForegroundColor White
    Write-Host "   Output Path: $OutputPath" -ForegroundColor White
    Write-Host "   Log File: $logFile" -ForegroundColor White

    Write-SectionHeader "RUNNING TESTS" "Green"

    # Run the tests
    $stopwatch = [System.Diagnostics.Stopwatch]::StartNew()

    $testArgs = @(
        "`"$ProjectFile`"",
        "-ExecCmds=`"Automation RunTests $TestFilter;Quit`"",
        "-unattended",
        "-nopause",
        "-nosplash",
        "-log"
    )

    if ($LogLevel -eq "Verbose") {
        $testArgs += "-VerboseLogging"
    }

    Write-Host "🚀 Starting test execution..." -ForegroundColor Green
    Write-Host "Command: $EditorCmd $($testArgs -join ' ')" -ForegroundColor Gray

    # Run tests and capture output
    # Use Start-Process without redirection to let Unreal write its own log files
    $process = Start-Process -FilePath $EditorCmd -ArgumentList $testArgs -Wait -PassThru
    $exitCode = $process.ExitCode

    $stopwatch.Stop()
    $actualDuration = [math]::Round($stopwatch.Elapsed.TotalSeconds, 2)

    Write-Host "`n⏱️  Test execution completed in $actualDuration seconds" -ForegroundColor Cyan

    # Parse results from Unreal's log files
    Write-SectionHeader "ANALYZING RESULTS" "Yellow"

    # Unreal Engine writes to Saved/Logs/ directory, look for the most recent log
    $savedLogsPath = Join-Path $ProjectRoot "Saved\Logs"
    $unrealLogFile = $null

    if (Test-Path $savedLogsPath) {
        # Find the most recent .log file
        $unrealLogFile = Get-ChildItem -Path $savedLogsPath -Filter "*.log" | Sort-Object LastWriteTime -Descending | Select-Object -First 1
    }

    $logContent = ""
    if ($unrealLogFile) {
        try {
            $logContent = Get-Content $unrealLogFile.FullName -Raw -ErrorAction SilentlyContinue
            Write-Host "📋 Using Unreal log file: $($unrealLogFile.Name)" -ForegroundColor Cyan
        } catch {
            Write-Host "⚠️  Warning: Could not read Unreal log file. Results may be incomplete." -ForegroundColor Yellow
        }
    } else {
        Write-Host "⚠️  Warning: No Unreal log files found in Saved/Logs/. Results may be incomplete." -ForegroundColor Yellow
    }

    $testResults = Parse-TestResults -LogContent $logContent
    $summary = Get-TestSummary -TestResults $testResults

    # Display summary
    Write-Host "📊 TEST SUMMARY:" -ForegroundColor Cyan
    Write-Host "   Total Tests: $($summary.Total)" -ForegroundColor White
    Write-Host "   Passed: $($summary.Passed)" -ForegroundColor Green
    Write-Host "   Failed: $($summary.Failed)" -ForegroundColor Red
    Write-Host "   Skipped: $($summary.Skipped)" -ForegroundColor Yellow
    Write-Host "   Success Rate: $($summary.SuccessRate)%" -ForegroundColor $(if ($summary.SuccessRate -ge 90) { "Green" } elseif ($summary.SuccessRate -ge 70) { "Yellow" } else { "Red" })
    Write-Host "   Duration: $($summary.Duration)s" -ForegroundColor White

    # Save results to JSON
    $resultsData = @{
        Timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
        TestFilter = $TestFilter
        Summary = $summary
        Results = $testResults
        ExitCode = $exitCode
        ActualDuration = $actualDuration
    }

    $resultsData | ConvertTo-Json -Depth 3 | Out-File -FilePath $resultsFile -Encoding UTF8

    # Display individual test results
    if ($testResults.Count -gt 0 -and $LogLevel -ne "Minimal") {
        Write-SectionHeader "INDIVIDUAL TEST RESULTS" "Cyan"

        foreach ($result in $testResults) {
            Write-TestResult -TestName $result.Name -Status $result.Status -Duration $result.Duration

            if ($result.Status -eq "Failed" -and $result.ErrorMessage) {
                Write-FailureDetails -TestName $result.Name -ErrorMessage $result.ErrorMessage -StackTrace $result.StackTrace -LogFile $logFile
            }
        }
    }

    # Show failures section if any
    $failedTests = $testResults | Where-Object { $_.Status -eq "Failed" }
    if ($failedTests.Count -gt 0) {
        Write-SectionHeader "FAILED TESTS ANALYSIS" "Red"

        foreach ($failure in $failedTests) {
            Write-FailureDetails -TestName $failure.Name -ErrorMessage $failure.ErrorMessage -StackTrace $failure.StackTrace -LogFile $logFile
        }

        Write-Host "💡 TROUBLESHOOTING TIPS:" -ForegroundColor Yellow
        Write-Host "   1. Check the full log file for detailed error messages" -ForegroundColor White
        Write-Host "   2. Look for asset loading issues or missing dependencies" -ForegroundColor White
        Write-Host "   3. Verify test prerequisites and setup" -ForegroundColor White
        Write-Host "   4. Run individual tests to isolate the problem" -ForegroundColor White
    }

    # Final status
    Write-SectionHeader "COMPLETION" $(if ($exitCode -eq 0) { "Green" } else { "Red" })

    if ($exitCode -eq 0) {
        Write-Host "🎉 ALL TESTS COMPLETED SUCCESSFULLY!" -ForegroundColor Green
        Write-Host "📄 Results saved to: $resultsFile" -ForegroundColor Cyan
        if ($unrealLogFile) {
            Write-Host "📋 Log file: $($unrealLogFile.FullName)" -ForegroundColor Cyan
        } else {
            Write-Host "📋 Log file: $logFile" -ForegroundColor Cyan
        }
        exit 0
    } else {
        Write-Host "❌ TESTS FAILED with exit code $exitCode" -ForegroundColor Red
        Write-Host "📄 Results saved to: $resultsFile" -ForegroundColor Cyan
        if ($unrealLogFile) {
            Write-Host "📋 Log file: $($unrealLogFile.FullName)" -ForegroundColor Cyan
        } else {
            Write-Host "📋 Log file: $logFile" -ForegroundColor Cyan
        }
        Write-Host "💡 Review the failures section above for details" -ForegroundColor Yellow
        exit $exitCode
    }
}
catch {
    Write-Host "`n❌ CRITICAL ERROR: $_" -ForegroundColor Red
    Write-Host "Stack Trace: $($_.ScriptStackTrace)" -ForegroundColor Gray
    exit 1
}