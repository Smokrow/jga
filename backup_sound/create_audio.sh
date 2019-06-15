for i in $(ls ../backend/levels); do
	INPUT=$i
	OUTPUT=$(basename "$INPUT" .txt).wav
	echo Converting:  $INPUT to $OUTPUT
	espeak -f ../backend/levels/$INPUT  --stdout > $OUTPUT
done
echo Creating Introduction
espeak -f Intro.txt --stdout > Intro.wav
