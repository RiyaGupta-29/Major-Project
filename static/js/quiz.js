const question = document.querySelector ('#question');
const choices = Array.from(document.querySelectorAll ('.choice-text'));
const progressText = document.querySelector ('#progressText');
const progressBarFull = document.querySelector ('#progressBarFull');

let currentQuestion = {}
let acceptingAnswers = true
let depressionScore = 0
let AnxietyScore = 0
let StressScore = 0
let questionCounter = 0
let availableQuestions = []

let questions = [
{
id:1,
question: "I found it hard to wind down",
choice1: "Did not apply to me at all",
choice2: "Applied to me to some degree",
choice3: "Applied to me to a considerable degree or a good part of time",
choice4: "Applied to me very much or most of the time",
},

{
    id:2,
    question: "I was aware of dryness of my mouth",
    choice1: "Did not apply to me at all",
    choice2: "Applied to me to some degree",
    choice3: "Applied to me to a considerable degree or a good part of time",
    choice4: "Applied to me very much or most of the time",
    },

    {
        id:3,
        question: "I couldn’t seem to experience any positive feeling at all",
        choice1: "Did not apply to me at all",
        choice2: "Applied to me to some degree",
        choice3: "Applied to me to a considerable degree or a good part of time",
        choice4: "Applied to me very much or most of the time",
        },

        {
            id:4,
            question: "I experienced breathing difficulty (eg, excessively rapid breathing, breathlessness in the absence of physical exertion)",
            choice1: "Did not apply to me at all",
            choice2: "Applied to me to some degree",
            choice3: "Applied to me to a considerable degree or a good part of time",
            choice4: "Applied to me very much or most of the time",
            },

            {
                id:5,
                question: "I found it difficult to work up the initiative to do things",
                choice1: "Did not apply to me at all",
                choice2: "Applied to me to some degree",
                choice3: "Applied to me to a considerable degree or a good part of time",
                choice4: "Applied to me very much or most of the time",
                },

                {
                    id:6,
                    question: "I tended to over-react to situations",
                    choice1: "Did not apply to me at all",
                    choice2: "Applied to me to some degree",
                    choice3: "Applied to me to a considerable degree or a good part of time",
                    choice4: "Applied to me very much or most of the time",
                    },

                    {
                        id:7,
                        question: "I experienced trembling (e.g. in the hands) ",
                        choice1: "Did not apply to me at all",
                        choice2: "Applied to me to some degree",
                        choice3: "Applied to me to a considerable degree or a good part of time",
                        choice4: "Applied to me very much or most of the time",
                        },

                        {
                            id:8,
                            question: "I felt that I was using a lot of nervous energy ",
                            choice1: "Did not apply to me at all",
                            choice2: "Applied to me to some degree",
                            choice3: "Applied to me to a considerable degree or a good part of time",
                            choice4: "Applied to me very much or most of the time",
                            },

                            {
                                id:9,
                                question: "I was worried about situations in which I might panic and make a fool of myself",
                                choice1: "Did not apply to me at all",
                                choice2: "Applied to me to some degree",
                                choice3: "Applied to me to a considerable degree or a good part of time",
                                choice4: "Applied to me very much or most of the time",
                                },

                                {
                                    id:10,
                                    question: "I felt that I had nothing to look forward to",
                                    choice1: "Did not apply to me at all",
                                    choice2: "Applied to me to some degree",
                                    choice3: "Applied to me to a considerable degree or a good part of time",
                                    choice4: "Applied to me very much or most of the time",
                                    },

                                    {
                                        id:11,
                                        question: "I found myself getting agitated ",
                                        choice1: "Did not apply to me at all",
                                        choice2: "Applied to me to some degree",
                                        choice3: "Applied to me to a considerable degree or a good part of time",
                                        choice4: "Applied to me very much or most of the time",
                                        },

                                        {
                                            id:12,
                                            question: "I found it difficult to relax",
                                            choice1: "Did not apply to me at all",
                                            choice2: "Applied to me to some degree",
                                            choice3: "Applied to me to a considerable degree or a good part of time",
                                            choice4: "Applied to me very much or most of the time",
                                            },

                                            {
                                                id:13,
                                                question: "I felt down-hearted and blue",
                                                choice1: "Did not apply to me at all",
                                                choice2: "Applied to me to some degree",
                                                choice3: "Applied to me to a considerable degree or a good part of time",
                                                choice4: "Applied to me very much or most of the time",
                                                },

                                                {
                                                    id:14,
                                                    question: "I was intolerant of anything that kept me from getting on with what I was doing",
                                                    choice1: "Did not apply to me at all",
                                                    choice2: "Applied to me to some degree",
                                                    choice3: "Applied to me to a considerable degree or a good part of time",
                                                    choice4: "Applied to me very much or most of the time",
                                                    },
                                                    {
                                                        id:15,
                                                        question: "I felt I was close to panic",
                                                        choice1: "Did not apply to me at all",
                                                        choice2: "Applied to me to some degree",
                                                        choice3: "Applied to me to a considerable degree or a good part of time",
                                                        choice4: "Applied to me very much or most of the time",
                                                        },
                                                        {
                                                            id:16,
                                                            question: "I was unable to become enthusiastic about anything ",
                                                            choice1: "Did not apply to me at all",
                                                            choice2: "Applied to me to some degree",
                                                            choice3: "Applied to me to a considerable degree or a good part of time",
                                                            choice4: "Applied to me very much or most of the time",
                                                            },
                                                            {
                                                                id:17,
                                                                question: "I felt I wasn't worth much as a person ",
                                                                choice1: "Did not apply to me at all",
                                                                choice2: "Applied to me to some degree",
                                                                choice3: "Applied to me to a considerable degree or a good part of time",
                                                                choice4: "Applied to me very much or most of the time",
                                                                },
                                                                {
                                                                    id:18,
                                                                    question: "I felt that I was rather touchy",
                                                                    choice1: "Did not apply to me at all",
                                                                    choice2: "Applied to me to some degree",
                                                                    choice3: "Applied to me to a considerable degree or a good part of time",
                                                                    choice4: "Applied to me very much or most of the time",
                                                                    },
                                                                    {
                                                                        id:19,
                                                                        question: "I was aware of the action of my heart in the absence of physical exertion (e.g. sense of heart rate increase, heart missing a beat) ",
                                                                        choice1: "Did not apply to me at all",
                                                                        choice2: "Applied to me to some degree",
                                                                        choice3: "Applied to me to a considerable degree or a good part of time",
                                                                        choice4: "Applied to me very much or most of the time",
                                                                        },
                                                                        {
                                                                            id:20,
                                                                            question: "I felt scared without any good reason",
                                                                            choice1: "Did not apply to me at all",
                                                                            choice2: "Applied to me to some degree",
                                                                            choice3: "Applied to me to a considerable degree or a good part of time",
                                                                            choice4: "Applied to me very much or most of the time",
                                                                            },
                                                                            {
                                                                                id:21,
                                                                                question: "I felt that life was meaningless",
                                                                                choice1: "Did not apply to me at all",
                                                                                choice2: "Applied to me to some degree",
                                                                                choice3: "Applied to me to a considerable degree or a good part of time",
                                                                                choice4: "Applied to me very much or most of the time",
                                                                                }
]

const MAX_QUESTIONS = 21

startQuiz = () => {
questionCounter = 0
score = 0
availableQuestions = [...questions]
getNewQuestion()
}

getNewQuestion = () => {
    if (availableQuestions.length === 0 || questionCounter >= MAX_QUESTIONS) {
        // Post the scores to a Flask route
        const url = `/end?depressionScore=${depressionScore}&AnxietyScore=${AnxietyScore}&StressScore=${StressScore}`;
        window.location.href = url;
        return;
    }

questionCounter++
progressText.innerText = `Question ${questionCounter} of ${MAX_QUESTIONS}`
progressBarFull.style.width = `${(questionCounter/MAX_QUESTIONS) * 100}%`

const questionsIndex = Math.floor (Math.random() * availableQuestions.length)
currentQuestion = availableQuestions[questionsIndex]
question.innerText = currentQuestion.question

choices.forEach(choice =>{
    const number = choice.dataset['number']
    choice.innerText = currentQuestion['choice' + number]
})

availableQuestions.splice (questionsIndex, 1)

acceptingAnswers = true
}

choices.forEach (choice =>{
    choice.addEventListener('click', e =>{
    if (!acceptingAnswers) return

    acceptingAnswers = false
    const selectedChoice = e.target
    const selectedAnswer = selectedChoice.dataset['number']

    let scoreIncrement = 0;
    if (selectedAnswer === '1') {
        scoreIncrement = 0;
    }else if(selectedAnswer === '2'){
        scoreIncrement = 1;
    }else if(selectedAnswer === '3'){
        scoreIncrement = 2;
    }else if(selectedAnswer === '4'){
        scoreIncrement = 3;
    }

    if (currentQuestion.id === 3 || currentQuestion.id === 5 ||currentQuestion.id === 10 || currentQuestion.id === 13|| currentQuestion.id === 16|| currentQuestion.id === 17|| currentQuestion.id === 21) {
            depressionScore += scoreIncrement;
        }else if (currentQuestion.id === 2 || currentQuestion.id === 4 ||currentQuestion.id === 7 || currentQuestion.id === 9|| currentQuestion.id === 15|| currentQuestion.id === 19|| currentQuestion.id === 20) {
            AnxietyScore += scoreIncrement;
        }else if (currentQuestion.id === 1 || currentQuestion.id === 6 ||currentQuestion.id === 8 || currentQuestion.id === 11|| currentQuestion.id === 12|| currentQuestion.id === 14|| currentQuestion.id === 18) {
            StressScore += scoreIncrement;
        }

        getNewQuestion();
    });
});

startQuiz()