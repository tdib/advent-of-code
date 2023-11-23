# Part 1
# A/X: rock
# B/Y: paper
# C/Z: scissors

# Part 2
# X: lose
# Y: draw
# Z: win

$scores = @{
  A = 1
  B = 2
  C = 3
}

# Rock wins against scissors...
$wins = @{
  A = "C"
  B = "A"
  C = "B"
}

# Rock loses against paper...
$loses = @{
  A = "B"
  B = "C"
  C = "A"
}

$charMap = @{
  X = "A"
  Y = "B"
  Z = "C"
}


$lines = Get-Content input.txt
$totalPart1 = 0
$totalPart2 = 0
$SCORE_WIN = 6
$SCORE_DRAW = 3

ForEach ($line in $lines) {
  $theirChoice, $myChoice = $line.Split(" ")

  ### Part 2 ###
  switch ($myChoice) {
    # Lose
    "X" {
      $totalPart2 += $scores[$wins[$theirChoice]]
    }
    # Draw
    "Y" {
      $totalPart2 += $scores[$theirChoice] + $SCORE_DRAW
    }
    # Win
    "Z" {
      $totalPart2 += $scores[$loses[$theirChoice]] + $SCORE_WIN
    }
  }
  ##############

  $myChoice = $charMap[$myChoice]
  $totalPart1 += $scores[$myChoice]
  if ($wins[$myChoice] -eq $theirChoice) {
    $totalPart1 += $SCORE_WIN
  } elseif ($myChoice -eq $theirChoice) {
    $totalPart1 += $SCORE_DRAW
  }

}

"Answer to part 1 is $totalPart1"
"Answer to part 2 is $totalPart2"

# x lose, y draw, z win