class Question:
    """Instances of this [Question] class will be...
    individual questions on a questionnaire."""

    def __init__(self, question, choices=None, allow_text=False):
        """Create a "yes" or "no" question."""

        if not choices:
            choices = ["yes", "no"]

        self.question = question
        self.choices = choices
        self.allow_text = allow_text


class Survey:
    """Instances of this [Survey] class will be...
    questionnaires / surveys for the user to complete."""

    def __init__(self, title, instructions, questions):
        """Create a questionnaire."""

        self.title = title
        self.instructions = instructions
        self.questions = questions


satisfaction_survey = Survey(
    "Onboarding Questionnaire",
    "Answer these questions, or else...",
    [
        Question("Did Archer tell you he was a secret agent?"),
        Question("Did you meet Lana?"),
        Question("Was Mallory drinking?"),
        Question(
            "Do you feel prepared for your first assignment?",
            ["Only if it involves an airboat.", "RAMPAGE!!"],
            allow_text=True,
        ),
    ],
)

personality_quiz = Survey(
    "Pseudo-appropriate Personality Quiz",
    "Answer the following questions honestly, or else...",
    [
        Question(
            "Beyonce, Rihanna, or Cardi?",
            ["Bey", "Riri", "Cardi"],
            allow_text=True,
        ),
        Question("Do you dream about hyperinflation?"),
        Question("Is BTC going up forever?"),
        Question(
            "Austin or Miami?",
            ["ATX", "MIA"],
        ),
    ],
)

surveys = {"satisfaction": satisfaction_survey, "personality": personality_quiz}
