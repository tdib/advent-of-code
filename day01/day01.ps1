# Contents of text file
$lines = Get-Content test.txt
# Initialise empty array
$sums = @()

$currSum = 0
ForEach ($line in $lines) {
  # We have reached a blank space - add the rolling total to sums and reset it
  if ($line.Length -eq 0) {
    $sums += ,$currSum
    $currSum = 0
  # We have encountered a number - add it to the current sum
  } else {
    $currSum += $line
  }
}

$n = 3
$topN = ($sums | Sort-Object -Descending)[0..$n--]
$topNSum = ($topN | Measure-Object -Sum).Sum
"The answer is $topNSum"