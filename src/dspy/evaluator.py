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
            "meaning_preservation_explanation": meaning_preservation_result.explanation,
            "readability_preservation_explanation": readability_preservation_result.explanation,
            "final_score": final_score,
            "readability_preservation_score": readability_preservation_score,
            "meaning_preservation_score": meaning_preservation_score,
        }


trainset = [
    dspy.Example(
        english="It was a bright cold day in April, and the clocks were striking thirteen. Winston Smith, his chin nuzzled into his breast in an effort to escape the vile wind, slipped quickly through the glass doors of Victory Mansions, though not quickly enough to prevent a swirl of gritty dust from entering along with him.",
    ).with_inputs("english"),
    dspy.Example(
        english="The hallway smelt of boiled cabbage and old rag mats. At one end of it a coloured poster, too large for indoor display, had been tacked to the wall. It depicted simply an enormous face, more than a metre wide: the face of a man of about forty-five, with a heavy black moustache and ruggedly handsome features. Winston made for the stairs. It was no use trying the lift. Even at the best of times it was seldom working, and at present the electric current was cut off during daylight hours. It was part of the economy drive in preparation for Hate Week. The flat was seven flights up, and Winston, who was thirty-nine and had a varicose ulcer above his right ankle, went slowly, resting several times on the way. On each landing, opposite the lift-shaft, the poster with the enormous face gazed from the wall. It was one of those pictures which are so contrived that the eyes follow you about when you move. BIG BROTHER IS WATCHING YOU, the caption beneath it ran.",
    ).with_inputs("english"),
    dspy.Example(
        english="Inside the flat a fruity voice was reading out a list of figures which had something to do with the production of pig-iron. The voice came from an oblong metal plaque like a dulled mirror which formed part of the surface of the right-hand wall. Winston turned a switch and the voice sank somewhat, though the words were still distinguishable. The instrument (the telescreen, it was called) could be dimmed, but there was no way of shutting it off completely. He moved over to the window: a smallish, frail figure, the meagreness of his body merely emphasized by the blue overalls which were the uniform of the party. His hair was very fair, his face naturally sanguine, his skin roughened by coarse soap and blunt razor blades and the cold of the winter that had just ended.",
    ).with_inputs("english"),
    dspy.Example(
        english="Outside, even through the shut window-pane, the world looked cold. Down in the street little eddies of wind were whirling dust and torn paper into spirals, and though the sun was shining and the sky a harsh blue, there seemed to be no colour in anything, except the posters that were plastered everywhere. The blackmoustachio'd face gazed down from every commanding corner. There was one on the house-front immediately opposite. BIG BROTHER IS WATCHING YOU, the caption said, while the dark eyes looked deep into Winston's own. Down at streetlevel another poster, torn at one corner, flapped fitfully in the wind, alternately covering and uncovering the single word INGSOC. In the far distance a helicopter skimmed down between the roofs, hovered for an instant like a bluebottle, and darted away again with a curving flight. It was the police patrol, snooping into people's windows. The patrols did not matter, however. Only the Thought Police mattered.",
    ).with_inputs("english"),
    dspy.Example(
        english="It must have been about a month before she disappeared. It was a moment of reconciliation, when the nagging hunger in his belly was forgotten and his earlier affection for her had temporarily revived. He remembered the day well, a pelting, drenching day when the water streamed down the window-pane and the light indoors was too dull to read by. The boredom of the two children in the dark, cramped bedroom became unbearable. Winston whined and grizzled, made futile demands for food, fretted about the room pulling everything out of place and kicking the wainscoting until the neighbours banged on the wall, while the younger child wailed intermittently. In the end his mother said, 'Now be good, and I'Il buy you a toy. A lovely toy -- you'll love it'; and then she had gone out in the rain, to a little general shop which was still sporadically open nearby, and came back with a cardboard box containing an outfit of Snakes and Ladders. He could still remember the smell of the damp cardboard. It was a miserable outfit. The board was cracked and the tiny wooden dice were so ill-cut that they would hardly lie on their sides. Winston looked at the thing sulkily and without interest. But then his mother lit a piece of candle and they sat down on the floor to play. Soon he was wildly excited and shouting with laughter as the tiddly-winks climbed hopefully up the ladders and then came slithering down the snakes again, almost to the starting-point. They played eight games, winning four each. His tiny sister, too young to understand what the game was about, had sat propped up against a bolster, laughing because the others were laughing. For a whole afternoon they had all been happy together, as in his earlier childhood. ",
    ).with_inputs("english"),
    dspy.Example(
        english="Under the table Winston's feet made convulsive movements. He had not stirred from his seat, but in his mind he was running, swiftly running, he was with the crowds outside, cheering himself deaf. He looked up again at the portrait of Big Brother. The colossus that bestrode the world! The rock against which the hordes of Asia dashed themselves in vain! He thought how ten minutes ago -- yes, only ten minutes -- there had still been equivocation in his heart as he wondered whether the news from the front would be of victory or defeat. Ah, it was more than a Eurasian army that had perished! Much had changed in him since that first day in the Ministry of Love, but the final, indispensable, healing change had never happened, until this moment.",
    ).with_inputs("english"),
    dspy.Example(
        english="For a moment he was violently angry. During the month that he had known her the nature of his desire for her had changed. At the beginning there had been little true sensuality in it. Their first love-making had been simply an act of the will. But after the second time it was different. The smell of her hair, the taste of her mouth, the feeling of her skin seemed to have got inside him, or into the air all round him. She had become a physical necessity, something that he not only wanted but felt that he had a right to. When she said that she could not come, he had the feeling that she was cheating him. But just at this moment the crowd pressed them together and their hands accidentally met. She gave the tips of his fingers a quick squeeze that seemed to invite not desire but affection. It struck him that when one lived with a woman this particular disappointment must be a normal, recurring event; and a deep tenderness, such as he had not felt for her before, suddenly took hold of him. He wished that they were a married couple of ten years' standing. He wished that he were walking through the streets with her just as they were doing now but openly and without fear, talking of trivialities and buying odds and ends for the household. He wished above all that they had some place where they could be alone together without feeling the obligation to make love every time they met. It was not actually at that moment, but at some time on the following day, that the idea of renting Mr Charrington's room had occurred to him. When he suggested it to Julia she had agreed with unexpected readiness. Both of them knew that it was lunacy. It was as though they were intentionally stepping nearer to their graves. As he sat waiting on the edge of the bed he thought again of the cellars of the Ministry of Love. It was curious how that predestined horror moved in and out of one's consciousness. There it lay, fixed in future times, preceding death as surely as 99 precedes 100. One could not avoid it, but one could perhaps postpone it: and yet instead, every now and again, by a conscious, wilful act, one chose to shorten the interval before it happened.",
    ).with_inputs("english"),
    dspy.Example(
        english="But she did not need to tell him why she had wrapped it up. The smell was already filling the room, a rich hot smell which seemed like an emanation from his early childhood, but which one did occasionally meet with even now, blowing down a passage-way before a door slammed, or diffusing itself mysteriously in a crowded street, sniffed for an instant and then lost again.",
    ).with_inputs("english"),
    dspy.Example(
        english="She must have slipped into some shop in the proletarian quarters and bought herself a complete set of make-up materials. Her lips were deeply reddened, her cheeks rouged, her nose powdered; there was even a touch of something under the eyes to make them brighter. It was not very skilfully done, but Winston's standards in such matters were not high. He had never before seen or imagined a woman of the Party with cosmetics on her face. The improvement in her appearance was startling. With just a few dabs of colour in the right places she had become not only very much prettier, but, above all, far more feminine. Her short hair and boyish overalls merely added to the effect. As he took her in his arms a wave of synthetic violets flooded his nostrils. He remembered the half-darkness of a basement kitchen, and a woman's cavernous mouth. It was the very same scent that she had used; but at the moment it did not seem to matter.",
    ).with_inputs("english"),
    dspy.Example(
        english="Already the black instant of panic was half-forgotten. Feeling slightly ashamed of himself, he sat up against the bedhead. Julia got out of bed, pulled on her overalls, and made the coffee. The smell that rose from the saucepan was so powerful and exciting that they shut the window lest anybody outside should notice it and become inquisitive. What was even better than the taste of the coffee was the silky texture given to it by the sugar, a thing Winston had almost forgotten after years of saccharine. With one hand in her pocket and a piece of bread and jam in the other, Julia wandered about the room, glancing indifferently at the bookcase, pointing out the best way of repairing the gateleg table, plumping herself down in the ragged arm-chair to see if it was comfortable, and examining the absurd twelve-hour clock with a sort of tolerant amusement. She brought the glass paperweight over to the bed to have a look at it in a better light. He took it out of her hand, fascinated, as always, by the soft, rainwatery appearance of the glass.",
    ).with_inputs("english"),
]

for example in trainset:
    example.with_inputs("english")


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
