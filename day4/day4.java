import java.io.File;
import java.util.Scanner;
import java.util.Arrays;
import java.util.HashSet;
import java.util.Set;

public class day4 {
  public static void main(String[] args) {
    try {
      File file = new File("input.txt");
      Scanner scanner = new Scanner(file);
      int numRedundant = 0;
      int numOverlap = 0;
      
      while (scanner.hasNextLine()) {
        // Split the assignments into two ranges
        String[] assignments = scanner.nextLine().split(",");
        // Split the ranges into lower and upper for each assignment
        int lower1 = Integer.parseInt(assignments[0].split("-")[0]);
        int upper1 = Integer.parseInt(assignments[0].split("-")[1]);
        int lower2 = Integer.parseInt(assignments[1].split("-")[0]);
        int upper2 = Integer.parseInt(assignments[1].split("-")[1]);
        
        // Increment redundant counter if one range fully encapsulates the other
        if ((lower1 <= lower2 && upper1 >= upper2) || (lower2 <= lower1 && upper2 >= upper1)) {
          numRedundant++;
        }

        // Part 2 //
        // Create arrays filled with each of the numbers from the provided ranges
        Integer[] range1 = range(lower1, upper1+1);
        Integer[] range2 = range(lower2, upper2+1);
        // Adapted from https://stackoverflow.com/a/17863345
        // Create sets for each of the aforementioned ranges
        Set<Integer> s1 = new HashSet<Integer>(Arrays.asList(range1));
        Set<Integer> s2 = new HashSet<Integer>(Arrays.asList(range2));
        // Find intersection - this affects s1 as it is in-place
        s1.retainAll(s2);
        Integer[] intersectingElements = s1.toArray(new Integer[s1.size()]);

        // If there is no intersection, there is some overlap
        if (intersectingElements.length != 0) {
          numOverlap++;
        }

      }
      scanner.close();

      System.out.println("Part 1 answer: " + numRedundant);
      System.out.println("Part 2 answer: " + numOverlap);

    } catch (Exception e) {
      System.err.println(e);
    }
  }

  // Adapted from https://stackoverflow.com/a/62225265
  static Integer[] range(int low, int high) {
    // Create empty array of length corresponding to range
    Integer[] rangeArr = new Integer[high-low];

    // Iterate through the range, adding integers to each empty cell
    int j = low;
    for (int i = 0; i < high-low; i++) {
      rangeArr[i] = j;
      j++;
    }

    return rangeArr;
  }
}