import sys, re, json, os

filepath = "/Users/wond_erwall/Desktop/2026-1/인포메이션 비주얼라이제이션/wk 05/ai_image_map-홍서진.html"
with open(filepath, "r", encoding="utf-8") as f:
    text = f.read()

# Match the DB object
match = re.search(r'const DB = (\{.*?\});', text)
if not match:
    print("Could not find DB")
    sys.exit(1)

db_json_str = match.group(1)
db = json.loads(db_json_str)

for file in db["files"]:
    path = file.get("path")
    size = 0
    if path and os.path.exists(path):
        size = os.path.getsize(path)
    # Ensure it's populated
    file["size"] = size

new_db_json_str = json.dumps(db, ensure_ascii=False, separators=(',', ':'))
text = text.replace(db_json_str, new_db_json_str)

# Replace getNodeSize function
old_node_size_pattern = r'function getNodeSize\(f\) \{.*?\n\}'
# We will use re.sub for this
new_node_size = """function getNodeSize(f) {
  const min = 8, max = 32;
  const maxSize = Math.max(...DB.files.map(x => x.size || 0), 1);
  const size = f.size || 0;
  // Create a slight curve so small files are still visible
  return min + ((max - min) * Math.sqrt(size / maxSize));
}"""
text = re.sub(old_node_size_pattern, new_node_size, text, flags=re.DOTALL)

# Replace legend
text = text.replace("● 크기 = 파일 순서/인덱스", "● 크기 = 파일 용량 (크기가 클수록 원이 큼)")

# Add tooltip info
text = text.replace("`ext: ${f.ext}<br>` +", "`ext: ${f.ext}<br>` +\n    (f.size ? `size: ${(f.size / 1024).toFixed(0)} KB<br>` : '') +")

with open(filepath, "w", encoding="utf-8") as f:
    f.write(text)
print("Done")
