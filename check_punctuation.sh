#!/bin/bash
# Check for banned punctuation (em dashes, double hyphens) in prose text.
# Allows Markdown horizontal rules (---) and BEM CSS classes (md-button--primary).
# Usage: ./check_punctuation.sh [directory ...]

VIOLATIONS=0

for DIR in "$@"; do
    while IFS= read -r file; do
        # Strip HR lines, then search for violations
        # - : — (em dash) anywhere
        # - -- (double hyphen) only when surrounded by spaces (prose), not in CSS (word--word)
        result=$(sed '/^[[:space:]]*---[[:space:]]*$/d' "$file" | perl -ne 'print "$.: $_" if /—|(?<!\w)--(?!\w)/')
        if [ -n "$result" ]; then
            echo "FAIL $file"
            echo "$result" | sed 's/^/  /'
            VIOLATIONS=1
        fi
    done < <(find "$DIR" -name '*.md' -not -name '*_notes.md' -not -path '*/site/*' -not -name 'styleguide_en.md')
done

if [ "$VIOLATIONS" -eq 0 ]; then
    echo "OK"
fi
exit "$VIOLATIONS"
