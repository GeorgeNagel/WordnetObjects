import nltk

nltk.download("wordnet")
from nltk.corpus import wordnet as wn

output_filename = "raw_objects.txt"

# List of starting points whose hyponyms we want to include
synsets = [
    wn.synset("physical_entity.n.01"),
    wn.synset("instrumentality.n.03"),
    wn.synset("substance.n.07"),
]
# List of synsets whose hyponyms we don't want to include in our output
exclusion_synsets = [wn.synset("inhabitant.n.01")]


def clean_hyponyms(hyponyms):
    """
    Returns a list of hyponyms that are not excluded and whose hypernyms are not excluded
    """
    cleaned = []
    for hyponym in hyponyms:
        hypernyms = hyponym.hypernyms()
        if hyponym in exclusion_synsets:
            continue

        banned_synset = False
        for hypernym in hypernyms:
            if hypernym in exclusion_synsets:
                banned_synset = True
                break
        if banned_synset:
            continue

        cleaned.append(hyponym)
    return cleaned


# Create a list of synsets which have no hyponyms
leaf_synsets = []
for synset in synsets:
    hyponyms = synset.hyponyms()
    cleaned_hyponyms = clean_hyponyms(hyponyms)
    synsets.extend(cleaned_hyponyms)
    if not hyponyms:
        leaf_synsets.append(synset)

# Make sure we're only dealing with unique lemmas
lemmas = set()
for synset in leaf_synsets:
    lemma = synset.lemmas()[0].name()
    cleaned_lemma = lemma.replace("_", " ")
    lemmas.add(cleaned_lemma)


# Write the lemmas to our output file
# Add newlines after every lemma
lines = []
for lemma in sorted(lemmas):
    lines.append(f"{lemma}\n")
with open(output_filename, "w") as fout:
    fout.writelines(lines)
