import Data.List
import Text.Printf

main = interact solve
solve s = printf "Part 1 answer: %d\nPart 2 answer: %d\n" (solve_part_1 s) (solve_part_2 s)

parse :: String -> [Int]
parse s = 
  let groups = split "" $ lines s
      sum_string_list group = sum (map read group)
  in map sum_string_list groups

solve_part_1 :: String -> Int
solve_part_1 s = foldr max 0 $ parse s

solve_part_2 :: String -> Int
solve_part_2 s = sum $ take 3 $ reverse $ sort $ parse s

split :: Eq a => a -> [a] -> [[a]]
split delim [] = []
split delim s =
  let (curr, next) = span (/=delim) s
  in curr : split delim (drop 1 next)
