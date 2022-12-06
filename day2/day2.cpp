#include <iostream>
#include <map>
#include <fstream>
#include <string>
#include <algorithm>

using namespace std;

// Offset X from A
// Used to map X, Y, and Z to A, B, and C respectively
#define CHAR_MAP_OFFSET 23

// Offset from A to 1
// Used to map A, B, and C to 1, 2, and 3 respectively
#define CHAR_SCORE_OFFSET 'A' + 1

#define SCORE_DRAW 3
#define SCORE_WIN 6

int main(void) {
  // A wins against C...
  map<char, char> wins = {
    { 'A', 'C' },
    { 'B', 'A' },
    { 'C', 'B' },
  };

  ifstream infile("input.txt");
  string line;
  int total = 0;
  int totalPart2 = 0;

  while (getline(infile, line)) {
    char theirChoice = line[0];
    char myChoice = line[line.find(' ') + 1] - CHAR_MAP_OFFSET;

    // Part 1 //
    total += myChoice - CHAR_SCORE_OFFSET;
    // Draw
    if (myChoice == theirChoice) {
      total += SCORE_DRAW;
    // Win
    } else if (wins[myChoice] == theirChoice) {
      total += SCORE_WIN;
    }

    // Part 2 //
    char myStrat = line[line.find(' ') + 1];
    // Lose
    if (myStrat == 'X') {
      totalPart2 += wins[theirChoice] - CHAR_SCORE_OFFSET;
    // Draw
    } else if (myStrat == 'Y') {
      totalPart2 += theirChoice - CHAR_SCORE_OFFSET + SCORE_DRAW;
    // Win
    } else if (myStrat == 'Z') {
      // Find the value in the map which corresponds to a loss for the opponent
      for (auto const& [winningOption, losingOption] : wins) {
        if (theirChoice == losingOption) {
          totalPart2 += winningOption - CHAR_SCORE_OFFSET + SCORE_WIN;
          break;
        }
      }
    }
  }

  cout << "Part 1 answer: " << total << endl;
  cout << "Part 2 answer: " << totalPart2 << endl;
  return EXIT_SUCCESS;
}