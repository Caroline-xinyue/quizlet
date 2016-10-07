from quizXZ.models import Quiz, Question, Choice

def create_db():
	quizzes = []
	for i in range(2):
		quizzes.append( Quiz() )

	quizzes[0].difficulty = 2
	quizzes[0].subject = "jango"
	quizzes[1].difficulty = 8
	quizzes[1].subject = "math"

	for i in range(2):
		quizzes[i].save()

	questions = []
	for i in range(4):
		questions.append( Question() )

	for i in range(2):
		questions[i].quiz = quizzes[0]
	for i in range(2,4):
		questions[i].quiz = quizzes[1]
	questions[0].text = "A?"
	questions[1].text = "B?"
	questions[2].text = "C?"
	questions[3].text = "D?"

	for i in range(4):
		questions[i].save()

	choices = []
	for i in range(8):
		choices.append( Choice() )

	for i in range(2):
		choices[i].question = questions[0]
	for i in range(2,4):
		choices[i].question = questions[1]
	for i in range(4,6):
		choices[i].question = questions[2]
	for i in range(6,8):
		choices[i].question = questions[3]

	choices[0].text = "1"
	choices[0].point = 0
	choices[1].text = "2"
	choices[1].point = 1
	choices[2].text = "3"
	choices[2].point = 2
	choices[3].text = "4"
	choices[3].point = 0
	choices[4].text = "5"
	choices[4].point = 1
	choices[5].text = "6"
	choices[5].point = 2
	choices[6].text = "7"
	choices[6].point = 1
	choices[7].text = "8"
	choices[7].point = 0

	for i in range(8):
		choices[i].save()
