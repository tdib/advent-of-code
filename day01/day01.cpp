#include <iostream> // std::cout
#include <fstream> // std:ifstream
#include <string> // std::string
#include <vector> // std::vector
#include <algorithm> // std::sort
#include <numeric> // std::accumulate
using namespace std;

int main(void) {
  ifstream infile("input.txt");
  string line;
  int subtotal = 0;
  vector<int> totals = vector<int>();

  while (getline(infile, line)) {
    // There are no numbers on this line, just a newline
    if (line.length() == 1) {
      // We add our current sum to our totals vector and reset
      totals.push_back(subtotal);
      subtotal = 0;
    // There is a number on this line, so we increment the subtotal by this number
    } else {
      subtotal += stoi(line);
    }
  }
  // Add the remaining subtotal to the totals
  totals.push_back(subtotal);

  // Sort and reverse the vector - higher values will be at the start (i.e. descending order)
  sort(totals.begin(), totals.end());
  reverse(totals.begin(), totals.end());

  // Simply take the first element of the vector (which is the highest)
  int part1 = totals[0];
  // Sum the first n elements of the vector
  int n = 3;
  int part2 = accumulate(totals.begin(), totals.begin()+n, 0);

  cout << "Part 1 answer: " << part1 << endl;
  cout << "Part 2 answer: " << part2 << endl;

  infile.close();
  return EXIT_SUCCESS;
}