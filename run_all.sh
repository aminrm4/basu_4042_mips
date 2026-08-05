# Usage: ./run_all.sh   (run from the project root)

set -e
TIMEOUT=2000000
cd "$(dirname "$0")/src"

declare -A PROGRAMS
PROGRAMS[fibo_beq]="../asm/fibo_beq.asm ../asm/fibo_beq_data.txt"
PROGRAMS[fibo_bne]="../asm/fibo_bne.asm ../asm/fibo_bne_data.txt"
PROGRAMS[fact]="../asm/fact.asm ../asm/fact_data.txt"

METHODS="ST SN D1 D2 IQ"

for prog in "${!PROGRAMS[@]}"; do
  read -r inst_file data_file <<< "${PROGRAMS[$prog]}"
  for method in $METHODS; do
    method_lc=$(echo "$method" | tr '[:upper:]' '[:lower:]')
    out="../report/${prog}_${method_lc}.txt"
    echo "Running $prog with $method -> $out"
    python3 main.py "$TIMEOUT" "$method" "$inst_file" "$data_file" "$out" > /dev/null
  done
done

echo "Done. 15 report files written to report/"
