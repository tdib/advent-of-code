
function getLines()
    return io.lines("input.txt")
end

function solvePart1()
    ans = 0
    dial = 50
    for line in getLines() do
        num = string.sub(line, 2)
        mult = line:sub(1, 1) == "L" and -1 or 1
        dial = (dial + num * mult) % 100
        if dial == 0 then
            ans = ans + 1
        end
    end
    return ans
end

function solvePart2()
    ans = 0
    dial = 50
    for line in getLines() do
        num = string.sub(line, 2)
        prevDial = dial
        mult = line:sub(1, 1) == "L" and -1 or 1
        dial = dial + num * mult

        ans = ans + num // 100
        num = num % 100
        if prevDial ~= 0 and (dial % 100 == 0 or dial % 100 ~= dial) then
            ans = ans + 1
        end
        dial = dial % 100
    end
    return ans
end

print("Part 1 answer: " .. solvePart1())
print("Part 2 answer: " .. solvePart2())
