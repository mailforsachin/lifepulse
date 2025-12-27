import fs from "fs"
import path from "path"

const inputFile = path.resolve("./tools/french_raw.txt")
const outputFile = path.resolve("./frontend/lifepulse-ui/src/data/french.json")

const raw = fs.readFileSync(inputFile, "utf-8")
  .split("\n")
  .map(l => l.trim())
  .filter(Boolean)

if (raw.length % 3 !== 0) {
  console.error("❌ Input file line count is not divisible by 3")
  process.exit(1)
}

const result = []

for (let i = 0; i < raw.length; i += 3) {
  const titleLine = raw[i]
  const fr = raw[i + 1]
  const en = raw[i + 2]

  const cleanTitle = titleLine.replace(/^\d+\s*-\s*/, "")

  result.push({
    id: result.length + 1,
    title: cleanTitle,
    fr,
    en,
  })
}

fs.mkdirSync(path.dirname(outputFile), { recursive: true })
fs.writeFileSync(outputFile, JSON.stringify(result, null, 2), "utf-8")

console.log(`✅ Converted ${result.length} entries`)
console.log(`📄 Output: ${outputFile}`)
