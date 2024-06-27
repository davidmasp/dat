
.down.done: scripts/download.sh
	./download.sh

index.csv: scripts/build_index.sh .down.done
	./build_index.sh

.pipe.done: main.nf index.csv
	nextflow run $< -profile $(NFPROF) -resume --index index.csv

all: .pipe.done

clean:
	sh clean.sh
