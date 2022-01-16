# import Flask itself, from [flask], and import all of the Flask features...
# (i.e., render_template, redirect) that you will be using in this application.
from flask import Flask, request, render_template, redirect, flash, session

# import desired survey(s) from the [survey.py] file.
from survey import satisfaction_survey as survey

# Key names will be used to store some things in the session;
# put here as constants so we're guaranteed to be consistent in
# our spelling of these.
RESPONSES_KEY = "responses"

app = Flask(__name__)
app.config["SECRET_KEY"] = "secret"


@app.route("/")
def show_survey_start():
    """Immediately route users to the survey you've chosen."""

    return render_template("survey_start.html", survey=survey)


@app.route("/begin", methods=["POST"])
def start_survey():
    """
    This is the user's first stop on their journey to survey completion...
    Here we ensure that the list of responses has been reset / cleared...
    Then, we immediately redirect users to the URL for survey question one.
    """

    session[RESPONSES_KEY] = []

    return redirect("/questions/0")


@app.route("/questions/<int:qid>")
def show_question(qid):
    """Display the current question."""
    responses = session.get(RESPONSES_KEY)

    if len(responses) == len(survey.questions):
        # If the user has answered all of the questions...
        # route them to the "survey completed" page.
        return redirect("/complete")

    # The following [if] statement ensures that users are not skipping questions...
    # it is effective because the length of the responses key will always...
    # be equal to the total number of questions that the user has answered.
    if len(responses) != qid:
        # If a user attempts to access the survey questions out of their proper order...
        # "flash" them the following message + redirect them to the apporpriate question.
        flash(
            f"Question #{qid + 1} is not the question that you should be answering right now. Naughty, naughty user."
        )
        return redirect(f"/questions/{len(responses)}")

    question = survey.questions[qid]
    return render_template("question.html", question_num=qid, question=question)


# After answering each survey question, users are directed to the following route.
@app.route("/answer", methods=["POST"])
def handle_question():

    # This line of code captures the [value] -- the string assigned to...
    # the answer choice the user selected (i.e., "yes", "no", etc.) --
    # ... from the ["name": "value"] pair that was "POST(ed)".
    choice = request.form["answer"]

    # Add this response to the [session] object...
    # The [session] object allows you to store info...
    # specific to a user, from one request to the next.
    responses = session[RESPONSES_KEY]
    responses.append(choice)
    session[RESPONSES_KEY] = responses

    if len(responses) == len(survey.questions):
        # The user has answered all the questions...
        # Route them to the "survey completed" page.
        return redirect("/complete")

    else:
        # The user still has questions left to answer...
        # Redirect them to the appropriate question.
        return redirect(f"/questions/{len(responses)}")


@app.route("/complete")
def finished():
    """The survey has been completed. Render the appropriate HTML page."""

    responses = session[RESPONSES_KEY]
    questions = survey.questions
    return render_template("completion.html", responses=responses, questions=questions)
