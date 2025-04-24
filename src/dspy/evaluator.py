import dspy
import textstat
from src.dspy.translator import translator


class MeaningPreservationEvaluator(dspy.Signature):
    """Evaluate how well the simplified Swedish preserves the original meaning."""

    english = dspy.InputField()
    easy_swedish = dspy.InputField()

    score = dspy.OutputField(
        desc="Score from 1-100 where 100 means perfect preservation of meaning"
    )

    explanation = dspy.OutputField(
        desc="Explanation of what meaning was preserved or lost"
    )


class ReadabilityPreservationEvaluator(dspy.Signature):
    """Evaluate how well the simplified Swedish is easy to read"""

    english = dspy.InputField()
    easy_swedish = dspy.InputField()

    score = dspy.OutputField(
        desc="Score from 1-100 where 100 means easy to read at A1/A2 level"
    )

    explanation = dspy.OutputField(
        desc="Explanation of what makes the text easy to read or not"
    )


# Guidelines for Easy Swedish that can help the evaluator
EASY_SWEDISH_GUIDELINES = """
Features that make text suitable for Easy Swedish translation:
1. Short sentences (max 15-20 words)
2. Simple vocabulary (A1/A2 level words)
3. Direct subject-verb-object structure
4. Minimal use of subordinate clauses
5. Limited use of idioms and metaphors
6. Concrete rather than abstract concepts
7. Clear pronouns with obvious referents
8. Active voice rather than passive voice
9. Limited use of complex tenses
10. Avoidance of cultural references that don't translate well
"""


class TranslationEvaluator(dspy.Module):
    def __init__(self):
        super().__init__()
        self.meaning_preservation_evaluator = dspy.ChainOfThought(
            MeaningPreservationEvaluator
        )
        self.readability_preservation_evaluator = dspy.ChainOfThought(
            ReadabilityPreservationEvaluator
        )

    def forward(self, english, easy_swedish):
        # Calculate objective readability metrics
        # readability_score = textstat.flesch_reading_ease(simplified)

        meaning_preservation_result = self.meaning_preservation_evaluator(
            english=english, easy_swedish=easy_swedish
        )
        meaning_preservation_score = float(meaning_preservation_result.score)

        readability_preservation_result = self.readability_preservation_evaluator(
            english=english, easy_swedish=easy_swedish
        )
        readability_preservation_score = float(readability_preservation_result.score)

        final_score = (0.6 * readability_preservation_score) + (
            0.4 * meaning_preservation_score
        )

        return {
            "final_score": final_score,
            "readability_preservation_score": readability_preservation_score,
            "readability_preservation_explanation": readability_preservation_result.explanation,
            "meaning_preservation_score": meaning_preservation_score,
            "meaning_preservation_explanation": meaning_preservation_result.explanation,
        }


trainset = [
    dspy.Example(
        english="It was a bright cold day in April, and the clocks were striking thirteen. Winston Smith, his chin nuzzled into his breast in an effort to escape the vile wind, slipped quickly through the glass doors of Victory Mansions, though not quickly enough to prevent a swirl of gritty dust from entering along with him.",
    ),
    dspy.Example(
        english="The hallway smelt of boiled cabbage and old rag mats. At one end of it a coloured poster, too large for indoor display, had been tacked to the wall. It depicted simply an enormous face, more than a metre wide: the face of a man of about forty-five, with a heavy black moustache and ruggedly handsome features. Winston made for the stairs. It was no use trying the lift. Even at the best of times it was seldom working, and at present the electric current was cut off during daylight hours. It was part of the economy drive in preparation for Hate Week. The flat was seven flights up, and Winston, who was thirty-nine and had a varicose ulcer above his right ankle, went slowly, resting several times on the way. On each landing, opposite the lift-shaft, the poster with the enormous face gazed from the wall. It was one of those pictures which are so contrived that the eyes follow you about when you move. BIG BROTHER IS WATCHING YOU, the caption beneath it ran.",
    ),
    dspy.Example(
        english="Inside the flat a fruity voice was reading out a list of figures which had something to do with the production of pig-iron. The voice came from an oblong metal plaque like a dulled mirror which formed part of the surface of the right-hand wall. Winston turned a switch and the voice sank somewhat, though the words were still distinguishable. The instrument (the telescreen, it was called) could be dimmed, but there was no way of shutting it off completely. He moved over to the window: a smallish, frail figure, the meagreness of his body merely emphasized by the blue overalls which were the uniform of the party. His hair was very fair, his face naturally sanguine, his skin roughened by coarse soap and blunt razor blades and the cold of the winter that had just ended.",
    ),
    dspy.Example(
        english="Outside, even through the shut window-pane, the world looked cold. Down in the street little eddies of wind were whirling dust and torn paper into spirals, and though the sun was shining and the sky a harsh blue, there seemed to be no colour in anything, except the posters that were plastered everywhere. The blackmoustachio'd face gazed down from every commanding corner. There was one on the house-front immediately opposite. BIG BROTHER IS WATCHING YOU, the caption said, while the dark eyes looked deep into Winston's own. Down at streetlevel another poster, torn at one corner, flapped fitfully in the wind, alternately covering and uncovering the single word INGSOC. In the far distance a helicopter skimmed down between the roofs, hovered for an instant like a bluebottle, and darted away again with a curving flight. It was the police patrol, snooping into people's windows. The patrols did not matter, however. Only the Thought Police mattered.",
    ),
    dspy.Example(
        english="It must have been about a month before she disappeared. It was a moment of reconciliation, when the nagging hunger in his belly was forgotten and his earlier affection for her had temporarily revived. He remembered the day well, a pelting, drenching day when the water streamed down the window-pane and the light indoors was too dull to read by. The boredom of the two children in the dark, cramped bedroom became unbearable. Winston whined and grizzled, made futile demands for food, fretted about the room pulling everything out of place and kicking the wainscoting until the neighbours banged on the wall, while the younger child wailed intermittently. In the end his mother said, 'Now be good, and I'Il buy you a toy. A lovely toy -- you'll love it'; and then she had gone out in the rain, to a little general shop which was still sporadically open nearby, and came back with a cardboard box containing an outfit of Snakes and Ladders. He could still remember the smell of the damp cardboard. It was a miserable outfit. The board was cracked and the tiny wooden dice were so ill-cut that they would hardly lie on their sides. Winston looked at the thing sulkily and without interest. But then his mother lit a piece of candle and they sat down on the floor to play. Soon he was wildly excited and shouting with laughter as the tiddly-winks climbed hopefully up the ladders and then came slithering down the snakes again, almost to the starting-point. They played eight games, winning four each. His tiny sister, too young to understand what the game was about, had sat propped up against a bolster, laughing because the others were laughing. For a whole afternoon they had all been happy together, as in his earlier childhood. ",
    ),
    dspy.Example(
        english="Under the table Winston's feet made convulsive movements. He had not stirred from his seat, but in his mind he was running, swiftly running, he was with the crowds outside, cheering himself deaf. He looked up again at the portrait of Big Brother. The colossus that bestrode the world! The rock against which the hordes of Asia dashed themselves in vain! He thought how ten minutes ago -- yes, only ten minutes -- there had still been equivocation in his heart as he wondered whether the news from the front would be of victory or defeat. Ah, it was more than a Eurasian army that had perished! Much had changed in him since that first day in the Ministry of Love, but the final, indispensable, healing change had never happened, until this moment.",
    ),
]


def test_evaluator():
    evaluator = TranslationEvaluator()

    # Example original text and a simplified version
    english = trainset[0].english
    easy_swedish = translator(english)["swedish"]

    score = evaluator(
        english=english,
        easy_swedish=easy_swedish,
    )
    print("Score:")
    print(score)


if __name__ == "__main__":
    test_evaluator()
