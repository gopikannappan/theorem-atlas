import unittest
from scripts.measure_palomar_overlap import document_key, measure, title_key

class PalomarOverlapTest(unittest.TestCase):
    def row(self):
        return {"id": "a", "title": "Catalan constant", "source": "OpenAI mathematics",
                "kind": "result_family", "manuscripts": [{"title": "Catalan constant", "url": "https://github.com/openai/math/blob/" + "a"*40 + "/preprints/Catalan/paper.pdf"}], "references": [], "proofs": []}
    def entry(self, relationship="formalizes"):
        return {"id": "PALOMAR-test", "version": 1, "title": "Partial formalization", "provenance": {"mathematical_sources": [{"title": "Catalan constant", "identifier": "https://github.com/openai/math/tree/" + "b"*40 + "/preprints/Catalan", "relationship": relationship}]}}

    def test_pdf_directory_and_tex_share_document_identity_only(self):
        prefix = "https://github.com/openai/math/"
        key = document_key(prefix + "blob/" + "a"*40 + "/preprints/Catalan/paper.pdf")
        self.assertEqual(key, document_key(prefix + "tree/main/preprints/Catalan"))
        self.assertEqual(key, document_key(prefix + "blob/" + "b"*40 + "/preprints/Catalan/build/paper.tex"))
        self.assertNotEqual(key, document_key(prefix + "blob/main/preprints/Catalans-conjecture/paper.pdf"))

    def test_source_document_match_does_not_become_exact_proof(self):
        result = measure([self.row()], [self.entry()])
        metric = result["openai_result_families"]
        self.assertEqual(metric["direct_source_document_identifiers_ignoring_github_commit"]["matched"], 1)
        self.assertEqual(metric["exact_selected_declaration_and_commit"]["matched"], 0)

    def test_background_references_are_not_direct_coverage(self):
        metric = measure([self.row()], [self.entry("background")])["openai_result_families"]
        self.assertEqual(metric["source_identifier_or_exact_title_candidates"]["matched"], 0)
        self.assertEqual(metric["background_source_references"]["matched"], 1)

    def test_location_urls_are_inspected_and_repeat_entries_do_not_inflate_families(self):
        entry = self.entry()
        source = entry["provenance"]["mathematical_sources"][0]
        source["location"] = source.pop("identifier")
        entry2 = {**entry, "id": "PALOMAR-other"}
        metric = measure([self.row()], [entry, entry2])["openai_result_families"]
        self.assertEqual(metric["direct_source_document_identifiers_ignoring_github_commit"]["matched"], 1)

    def test_titles_are_candidates_and_not_fuzzy_semantic_matches(self):
        entry = self.entry()
        source = entry["provenance"]["mathematical_sources"][0]
        source.pop("identifier")
        metric = measure([self.row()], [entry])["openai_result_families"]
        self.assertEqual(metric["source_identifier_or_exact_title_candidates"]["matched"], 1)
        self.assertEqual(metric["direct_source_document_identifiers_ignoring_github_commit"]["matched"], 0)
        source["title"] = "Catalan conjecture"
        self.assertEqual(measure([self.row()], [entry])["openai_result_families"]["source_identifier_or_exact_title_candidates"]["matched"], 0)

    def test_citation_identity_does_not_erase_arxiv_versions(self):
        self.assertNotEqual(document_key("arXiv:2601.12345v1"), document_key("https://arxiv.org/abs/2601.12345v2"))
        self.assertEqual(title_key("Normal rings — a theorem"), title_key("Normal rings: a theorem"))

if __name__ == "__main__":
    unittest.main()
