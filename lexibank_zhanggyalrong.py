from collections import OrderedDict
from pathlib import Path

import attr
from pylexibank import Concept, Language
from pylexibank.dataset import Dataset as MyDataset
from pylexibank.forms import FormSpec
from pylexibank.util import progressbar

@attr.s
class CustomConcept(Concept):
    Chinese_Gloss = attr.ib(default=None)

@attr.s
class CustomLanguage(Language):
    Latitude = attr.ib(default=None)
    Longitude = attr.ib(default=None)
    ChineseName = attr.ib(default=None)
    SubGroup = attr.ib(default=None)
    Family = attr.ib(default="Sino-Tibetan")
    DataSource = attr.ib(default=None)
    Autonym = attr.ib(default=None)
    ISO = attr.ib(default=None)
    Name_in_Source = attr.ib(default=None)
    Location = attr.ib(default=None)

class Dataset(MyDataset):
    dir = Path(__file__).parent
    id = "zhanggyalrong"
    concept_class = CustomConcept
    language_class = CustomLanguage
    # NEED TO FURTHER EDIT
    #
    # form_spec = FormSpec(
    #     missing_data=["*", "---", "-"],
    #     separators=";/,",
    #     strip_inside_brackets=True,
    #     brackets={"(": ")"},
    # )

    def cmd_makecldf(self, args):
        data = self.raw_dir.read_csv("zhang2019-oc-rgyal.tsv", dicts=True)
        languages, concepts = {}, {}
        # NEED TO EDIT
        # for concept in self.conceptlists[0].concepts.values():
        #     args.writer.add_concept(
        #         ID=concept.number,
        #         Name=concept.gloss,
        #         Concepticon_ID=concept.concepticon_id,
        #         Concepticon_Gloss=concept.concepticon_gloss,
        #         Chinese_Gloss=concept.attributes["chinese"],
        #     )
        #     concepts[concept.attributes["chinese"]] = concept.number
        #
        # args.writer.add_languages()
        #
        # languages = OrderedDict([(k["Name"], k["ID"]) for k in self.languages])
        # args.writer.add_sources(*self.raw_dir.read_bib())
        # missing = {}
        # for cgloss, entry in progressbar(enumerate(data), desc="cldfify the data", total=len(data)):
        #     if entry["Chinese gloss"] in concepts.keys():
        #         for language in languages:
        #             if entry[language].strip():
        #                 args.writer.add_lexemes(
        #                     Language_ID=languages[language],
        #                     Parameter_ID=concepts[entry["Chinese gloss"]],
        #                     Value=entry[language],
        #                     Source=["Chen2013"],
        #                 )
        #     else:
        #         missing[entry["Chinese gloss"]] += 1
