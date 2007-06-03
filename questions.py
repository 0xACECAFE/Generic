true = 1
false = 0
import string

question_list = [["What colour is the sky?","blue"],\
        ["What is the answer to life, the universe and everything?","42"],\
        ["What is a three letter word for mouse trap?","cat"],\
        ["What noise does a truly advanced machine make?","ping"]]

reply_list = ['t','a','q']

def get_questions(question_list):
    return question_list

def check_question(question_and_answer):
    question = question_and_answer[0]
    answer = question_and_answer[1]
    given_answer = raw_input(question)
    if answer == given_answer:
        print "Correct"
        return true
    else:
        print "Incorrect, correct answer was",answer
        return false

def run_test(questions):
    if len(questions) == 0:
        print "No questions were given"
        return
    index = 0
    right = 0
    while index < len(questions):
        if check_question(questions[index]):
            right = right + 1
        index = index + 1
    print "You got ",right*100/len(questions),"% right, out of",len(questions)

def add_question():
    question = raw_input("Give a question")
    answer = raw_input("What is the answer")
    question_list.append([question,answer])
    return question_list

def proceed():
    test_or_add = ''
    while test_or_add <> 'q':
        try:
            test_or_add = string.lower(raw_input("Test, Add question or Quit (t|a|q) "))
        except KeyboardInterrupt:
            print ("Stopped\n")
            break
        if test_or_add == 't':
            run_test(get_questions(question_list))
        elif test_or_add == 'a':
            add_question()
        elif reply_list.count(test_or_add) == 0: 
            print ("t|a|q\n")
    print ("Quit\n")

proceed()
