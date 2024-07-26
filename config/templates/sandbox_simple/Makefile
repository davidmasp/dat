
.fig.done: scripts/plot.R ../data/dataSimple/results/output.csv
	./scripts/plot.R
	@ echo "✅  Figures done"
	@touch .fig.done

all: .fig.done

clean:
	sh scripts/clean.sh
