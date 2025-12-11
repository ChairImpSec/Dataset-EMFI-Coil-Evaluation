.PHONY: all clean analysis analysis-clean post-process help full-rebuild

# Default target - uses cached data if available
all: analysis post-process

# Full rebuild from scratch
full-rebuild: clean analysis-clean post-process

# Help target
help:
	@echo "Available targets:"
	@echo "  make              - Run analysis and post-processing (uses cache, ~1 min)"
	@echo "  make full-rebuild - Clean and regenerate everything from scratch (~30 min)"
	@echo "  make analysis     - Generate results using cached preprocessed data"
	@echo "  make analysis-clean - Regenerate results from raw measurement files"
	@echo "  make post-process - Run all post-processing scripts"
	@echo "  make clean        - Remove all generated files"
	@echo "  make help         - Show this help message"

# Run analysis using cached data (default partial mode)
analysis:
	@echo "Running analysis with cached data..."
	python read.py --no-show-plots --all all

# Run the main analysis script from scratch
analysis-clean:
	@echo "Running analysis from scratch (this may take ~30 minutes)..."
	python read.py --clean --no-show-plots --all all

# Run all post-processing scripts
post-process:
	@echo "Running post-processing scripts..."
	cd results && python ../merge-coil-polarity-results.py
	cd results && python ../merge-coil-results.py
	cd results && python ../merge-coil-types-for-polarity.py
	cd results && python ../merge-coil-polarity-first-reaction.py

# Clean all generated files
clean:
	@echo "Removing all generated CSV and Parquet files..."
	@for exp in v3-10rep-1_1mx1_1mm v4-10rep-1_1mx1_1mm v5-10rep-1_1mx1_1mm; do \
		if [ -d "results/$$exp" ]; then \
			echo "Cleaning results/$$exp..."; \
			find "results/$$exp" -name "*.csv" -type f -delete; \
			find "results/$$exp" -name "*.parquet" -type f -delete; \
		fi; \
	done
	@echo "Cleaning merged files in results/..."
	@find results -maxdepth 1 -name "*.csv" -type f -delete
	@find results -maxdepth 1 -name "*.parquet" -type f -delete
	@echo "Clean complete!"
