


cd "/mnt/CRUCIAL_UPGRADE/TV Shows/"
select d in */; do test -n "$d" && break; echo ">>> Invalid Selection"; done
cd "$d" && pwd
files=(./*/*.mkv)

# Run this first to get the track info and figure out your numbers
echo ${files[0]}
mkvmerge -i "${files[0]}"

# Set your track numbers

#Audio Track to KEEP
audio=1
#Subtitle Track to KEEP
subtitle=3

#Run it on first episode as a test

#mkvmerge -o "${files[0]}_out" -a 1 -s 3 "${files[0]}"

for f in "${files[@]}"
do
  mkvmerge -o "${f}_out" -a 1 -s 3 "$f"
done
