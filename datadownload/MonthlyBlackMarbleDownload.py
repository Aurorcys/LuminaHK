"""
You can paste this code into the terminal without #!/bin/bash, or use a zsh file as well and run it.
This is a bit more personalized to me as the OUTPUT_DIR is to my specific directory structure. But you
can just edit it to your own environment and situation. This is a very clean and easy code to save you
a tremendous amount of time clicking through the web interface. And downloading each month for 5 years
manually.

The method used here is provided via the EARTHDATA website, and the API can be found after logging in
and being in the profile, which a button for Generate Tokens will be present. Just copy the token there
and replace it with yours.
"""


'''
#!/bin/bash
TOKEN="YOUR TOKEN FROM EARTH DATA"

TILE="h29v06"
OUTPUT_DIR="data/raw/BlackMarbleMonthly22-26feb"

mkdir -p $OUTPUT_DIR

# 2022 (non-leap)
echo "=== 2022 ==="
for month in 001 032 060 091 121 152 182 213 244 274 305 335; do
  case $month in
    001) mon="01" ;;
    032) mon="02" ;;
    060) mon="03" ;;
    091) mon="04" ;;
    121) mon="05" ;;
    152) mon="06" ;;
    182) mon="07" ;;
    213) mon="08" ;;
    244) mon="09" ;;
    274) mon="10" ;;
    305) mon="11" ;;
    335) mon="12" ;;
  esac
  
  file=$(curl -s -H "Authorization: Bearer $TOKEN" "https://ladsweb.modaps.eosdis.nasa.gov/archive/allData/5200/VJ146A3/2022/$month/" | grep -o "VJ146A3\.A2022$month\.$TILE\.[0-9]*\.[0-9]*\.h5" | head -1)
  
  if [ -n "$file" ]; then
    echo "Downloading hk_lights_2022_${mon}_${TILE}.h5"
    curl -H "Authorization: Bearer $TOKEN" -o "$OUTPUT_DIR/hk_lights_2022_${mon}_${TILE}.h5" "https://ladsweb.modaps.eosdis.nasa.gov/archive/allData/5200/VJ146A3/2022/$month/$file"
  else
    echo "No file for 2022-$mon"
  fi
  sleep 1
done

# 2023 (non-leap)
echo "=== 2023 ==="
for month in 001 032 060 091 121 152 182 213 244 274 305 335; do
  case $month in
    001) mon="01" ;;
    032) mon="02" ;;
    060) mon="03" ;;
    091) mon="04" ;;
    121) mon="05" ;;
    152) mon="06" ;;
    182) mon="07" ;;
    213) mon="08" ;;
    244) mon="09" ;;
    274) mon="10" ;;
    305) mon="11" ;;
    335) mon="12" ;;
  esac
  
  file=$(curl -s -H "Authorization: Bearer $TOKEN" "https://ladsweb.modaps.eosdis.nasa.gov/archive/allData/5200/VJ146A3/2023/$month/" | grep -o "VJ146A3\.A2023$month\.$TILE\.[0-9]*\.[0-9]*\.h5" | head -1)
  
  if [ -n "$file" ]; then
    echo "Downloading hk_lights_2023_${mon}_${TILE}.h5"
    curl -H "Authorization: Bearer $TOKEN" -o "$OUTPUT_DIR/hk_lights_2023_${mon}_${TILE}.h5" "https://ladsweb.modaps.eosdis.nasa.gov/archive/allData/5200/VJ146A3/2023/$month/$file"
  else
    echo "No file for 2023-$mon"
  fi
  sleep 1
done

# 2024 (leap year)
echo "=== 2024 (Leap Year) ==="
for month in 001 032 061 092 122 153 183 214 245 275 306 336; do
  case $month in
    001) mon="01" ;;
    032) mon="02" ;;
    061) mon="03" ;;
    092) mon="04" ;;
    122) mon="05" ;;
    153) mon="06" ;;
    183) mon="07" ;;
    214) mon="08" ;;
    245) mon="09" ;;
    275) mon="10" ;;
    306) mon="11" ;;
    336) mon="12" ;;
  esac
  
  file=$(curl -s -H "Authorization: Bearer $TOKEN" "https://ladsweb.modaps.eosdis.nasa.gov/archive/allData/5200/VJ146A3/2024/$month/" | grep -o "VJ146A3\.A2024$month\.$TILE\.[0-9]*\.[0-9]*\.h5" | head -1)
  
  if [ -n "$file" ]; then
    echo "Downloading hk_lights_2024_${mon}_${TILE}.h5"
    curl -H "Authorization: Bearer $TOKEN" -o "$OUTPUT_DIR/hk_lights_2024_${mon}_${TILE}.h5" "https://ladsweb.modaps.eosdis.nasa.gov/archive/allData/5200/VJ146A3/2024/$month/$file"
  else
    echo "No file for 2024-$mon"
  fi
  sleep 1
done

# 2025 (non-leap)
echo "=== 2025 ==="
for month in 001 032 060 091 121 152 182 213 244 274 305 335; do
  case $month in
    001) mon="01" ;;
    032) mon="02" ;;
    060) mon="03" ;;
    091) mon="04" ;;
    121) mon="05" ;;
    152) mon="06" ;;
    182) mon="07" ;;
    213) mon="08" ;;
    244) mon="09" ;;
    274) mon="10" ;;
    305) mon="11" ;;
    335) mon="12" ;;
  esac
  
  file=$(curl -s -H "Authorization: Bearer $TOKEN" "https://ladsweb.modaps.eosdis.nasa.gov/archive/allData/5200/VJ146A3/2025/$month/" | grep -o "VJ146A3\.A2025$month\.$TILE\.[0-9]*\.[0-9]*\.h5" | head -1)
  
  if [ -n "$file" ]; then
    echo "Downloading hk_lights_2025_${mon}_${TILE}.h5"
    curl -H "Authorization: Bearer $TOKEN" -o "$OUTPUT_DIR/hk_lights_2025_${mon}_${TILE}.h5" "https://ladsweb.modaps.eosdis.nasa.gov/archive/allData/5200/VJ146A3/2025/$month/$file"
  else
    echo "No file for 2025-$mon"
  fi
  sleep 1
done

# 2026 Jan (001) and Feb (032) - 2026 is non-leap
echo "=== 2026 Jan & Feb ==="
for month in 001 032; do
  case $month in
    001) mon="01" ;;
    032) mon="02" ;;
  esac
  
  file=$(curl -s -H "Authorization: Bearer $TOKEN" "https://ladsweb.modaps.eosdis.nasa.gov/archive/allData/5200/VJ146A3/2026/$month/" | grep -o "VJ146A3\.A2026$month\.$TILE\.[0-9]*\.[0-9]*\.h5" | head -1)
  
  if [ -n "$file" ]; then
    echo "Downloading hk_lights_2026_${mon}_${TILE}.h5"
    curl -H "Authorization: Bearer $TOKEN" -o "$OUTPUT_DIR/hk_lights_2026_${mon}_${TILE}.h5" "https://ladsweb.modaps.eosdis.nasa.gov/archive/allData/5200/VJ146A3/2026/$month/$file"
  else
    echo "No file for 2026-$mon"
  fi
  sleep 1
done

echo "Done. Files saved in: $OUTPUT_DIR"
ls -lh $OUTPUT_DIR/
'''