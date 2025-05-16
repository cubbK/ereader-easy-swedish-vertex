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

evaluator_dataset = [
    dspy.Example(
        english="""Mary did not know what “Wuthering” meant until she listened, and then she understood. It must mean that the wind was blowing through the trees and the bushes and the heather. It was a wild, dreary-sounding wind. It was making a singular, low, rushing sound.
“It’s a wild place,” she said. “They live in such a big, grand house, and there seems no one in it but that queer man and the cook and the housemaid. It’s like a dream.”"""
    ),
    dspy.Example(
        english="""All children, except one, grow up. They soon know that they will grow up, and the way Wendy knew was this. One day when she was two years old she was playing in a garden, and she plucked another flower and ran with it to her mother. I suppose she must have looked rather delightful, for Mrs. Darling put her hand to her heart and cried, “Oh, why can’t you remain like this forever!”"""
    ),
    dspy.Example(
        english="""I resisted all the way: a new thing for me; and a circumstance which greatly strengthened the bad opinion Bessie and Miss Abbot were disposed to entertain of me. The fact is, I was a trifle beside myself; or rather out of myself, as the French would say: I was conscious that a moment’s mutiny had already rendered me liable to strange penalties, and like any other rebel slave, I felt resolved, in my desperation, to go all lengths."""
    ),
    dspy.Example(
        english="""Learn from me, if not by my precepts, at least by my example, how dangerous is the acquirement of knowledge, and how much happier that man is who believes his native town to be the world, than he who aspires to become greater than his nature will allow."""
    ),
    dspy.Example(
        english="""The telescreen received and transmitted simultaneously. Any sound that Winston made, above the level of a very low whisper, would be picked up by it; moreover, so long as he remained within the field of vision which the metal plaque commanded, he could be seen as well as heard."""
    ),
    dspy.Example(
        english="""FAHRENHEIT 451 by RAY BRADBURY.

 

{{This digitised version was scanned and proof-read by Eva Looshan. The
source was the 1976 Panther paperback.

 

I have endeavoured to reproduce the book as exactly as possible. What I
haven’t done is consistently indicate italics, because they weren’t
picked up by my OCR program. In a few cases, where I referred back to
the printed page and noticed italics, I made the correspondeing text all
upper case. I hope soon to be able to refer again to the text and to
create a html version, which will include the emphasis the author chose.
For any other errors, I apologise most profusely.

 

If you read this book perhaps you will be inspired to duplicate this
text file and spread it as widely as you can throughout the digital
world. It is a fitting fate for such a wonderful work, a book which
deserves to be as famous as its thematic cousins ‘1984’ and ‘Brave New
World’

 

Eva Looshan

March 1999}}

 

––––––––––––––––—

RAY BRADBURY

FAHRENHEIT 451

 

This one, with gratitude, is for DON CONGDON.

 

FAHRENHEIT 451:

The temperature at which book-paper catches fire and burns

PART I

IT WAS A PLEASURE TO BURN

IT was a special pleasure to see things eaten, to see things blackened
and changed. With the brass nozzle in his fists, with this great python
spitting its venomous kerosene upon the world, the blood pounded in his
head, and his hands were the hands of some amazing conductor playing all
the symphonies of blazing and burning to bring down the tatters and
charcoal ruins of history. With his symbolic helmet numbered 451 on his
stolid head, and his eyes all orange flame with the thought of what came
next, he flicked the igniter and the house jumped up in a gorging fire
that burned the evening sky red and yellow and black. He strode in a
swarm of fireflies. He wanted above all, like the old joke, to shove a
marshmallow on a stick in the furnace, while the flapping pigeon-winged
books died on the porch and lawn of the house."""
    ),
    dspy.Example(
        english="""They walked in the warm-cool blowing night on the silvered pavement and
there was the faintest breath of fresh apricots and strawberries in the
air, and he looked around and realized this was quite impossible, so
late in the year.

There was only the girl walking with him now, her face bright as snow in
the moonlight, and he knew she was working his questions around, seeking
the best answers she could possibly give.

“Well,” she said, “I’m seventeen and I’m crazy. My uncle says the two
always go together. When people ask your age, he said, always say
seventeen and insane. Isn’t this a nice time of night to walk? I like to
smell things and look at things, and sometimes stay up all night,
walking, and watch the sun rise.”

They walked on again in silence and finally she said, thoughtfully, “You
know, I’m not afraid of you at all.”

He was surprised. “Why should you be?”

“So many people are. Afraid of firemen, I mean. But you’re just a man,
after all…”

He saw himself in her eyes, suspended in two shining drops of bright
water, himself dark and tiny, in fine detail, the lines about his mouth,
everything there, as if her eyes were two miraculous bits of violet
amber that might capture and hold him intact."""
    ),
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
