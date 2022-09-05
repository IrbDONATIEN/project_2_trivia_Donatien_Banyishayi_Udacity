# API Development and Documentation Final Project

## Trivia App

Udacity is invested in creating bonding experiences for its employees and students. A bunch of team members got the idea to hold trivia on a regular basis and created a webpage to manage the trivia app and play the game, but their API experience is limited and still needs to be built out.

That's where you come in! Help them finish the trivia app so they can start holding trivia and seeing who's the most knowledgeable of the bunch. The application must:

1. Display questions - both all questions and by category. Questions should show the question, category and difficulty rating by default and can show/hide the answer.
2. Delete questions.
3. Add questions and require that they include question and answer text.
4. Search for questions based on a text query string.
5. Play the quiz game, randomizing either all questions or within a specific category.

## Getting Started

### Pre-requisites and Local Development

Developers using this project should already have:

- Python3.7
- Pip
- node.js

#### Backend

Inside the backend folder initialize and activate a virtualenv
```
  python -m virtualenv env
  source env/bin/activate
```

>**Note**Or use only your local machines by installing the necessary packages via the bottom link of this document.
>**Note** - In Windows, the `env` does not have a `bin` directory. Therefore, you'd use the analogous command shown below:
```
  source env/Scripts/activate
```
then run [pip install requirements.txt] All required packages are included in the requirements file.

To run the application run the following commands:

- Linux System:
```
export FLASK_APP=flaskr
export FLASK_ENV=development
flask run
```
- Windows System:
```
$set FLASK_APP=flaskr
$set FLASK_ENV=development
$flask run
```

The application is run on  [http://127.0.0.1:5000/] by default and is a proxy in the frontend configuration.

#### Frontend

This project uses NPM to manage software dependencies. NPM Relies on the package.json file located in the frontend directory of this repository. After cloning, open your terminal and run:
```
$ npm install
```
The frontend app was built using create-react-app. In order to run the app in development mode use npm start. You can change the script in the package.json file.
```
$ npm start
```
Open [http://localhost:3000] to view it in the browser. The page will reload if you make edits.

#### Tests

To run the tests, run
```
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```

## API Reference

### Error Handling

Errors are returned as JSON objects in the following format:
```
{
    "error": 404,
    "message": "resource not found",
    "success": false
}
```
The API will return three error types when requests fail:

- 400: Bad Request
- 404: Resource Not Found
- 422: Not Processable
- 500: Internal Server Error
- 405: Method Not Allowed

### Endpoints

**GET /categories**

General:
- Returns a list of categories, success value
- Results are paginated in groups of 10. Include a request argument to choose page number, starting from 1.

Sample:[`curl http://127.0.0.1:5000/categories`]

```
  {
    "categories": {
      "1": "Science",
      "2": "Art",
      "3": "Geography",
      "4": "History",
      "5": "Entertainment",
      "6": "Sports",
      "7": "Test",
      "8": "Culture"
    },
    "success": true,
    "total_categories": 8
}
```
**POST /categories**


General:
- Creates a new category using the submitted type. Returns the id of the created question id, success value, total questions number, and questions list based on current page number to update the frontend

Sample: ```curl http://127.0.0.1:5000/categories -X POST -H "Content-Type: application/json" -d '{"type":"Culture"}'```
```
{
    "categories": {
      "type": "Culture"
    },
    "success": true,
    "type_id": 8
}
```
**DELETE /questions/{id}**


General:
- Deletes the question of the given ID if it exists. Returns success value.

Sample [`curl -X DELETE http://127.0.0.1:5000/questions/33?page=3`]
```
{
  "deleted": 33,
  "questions": [
    {
      "answer": "Sputnik 1",
      "category": 1,
      "difficulty": 2,
      "id": 31,
      "question": "What was the name of the first man-made satellite launched by the Soviet Union in 1957?"
    }
  ],
  "success": true,
  "total_questions": 21
}
```
**POST /questions/{id}**

General:
- Creates a new question using the submitted title, answer, category and difficulty. Returns the id of the created question id, success value, total questions number, and questions list based on current page number to update the frontend

Sample: ```curl http://127.0.0.1:5000/questions -X POST -H "Content-Type: application/json" -d '{"question":"Who is the current president of the Democratic Republic of Congo?","answer":"Felix Antoine TSHISEKEDI TSHILOMBO","category":"4","difficulty":"4"}'```
```
{
  "question_id": 34,
  "questions": [
    {
      "answer": "Apollo 13",
      "category": 5,
      "difficulty": 4,
      "id": 2,
      "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
    },
    {
      "answer": "Tom Cruise",
      "category": 5,
      "difficulty": 4,
      "id": 4,
      "question": "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?"
    },
    {
      "answer": "Maya Angelou",
      "category": 4,
      "difficulty": 2,
      "id": 5,
      "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
    },
    {
      "answer": "Edward Scissorhands",
      "category": 5,
      "difficulty": 3,
      "id": 6,
      "question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
    },
    {
      "answer": "Muhammad Ali",
      "category": 4,
      "difficulty": 1,
      "id": 9,
      "question": "What boxer's original name is Cassius Clay?"
    },
    {
      "answer": "Brazil",
      "category": 6,
      "difficulty": 3,
      "id": 10,
      "question": "Which is the only team to play in every soccer World Cup tournament?"
    },
    {
      "answer": "George Washington Carver",
      "category": 4,
      "difficulty": 2,
      "id": 12,
      "question": "Who invented Peanut Butter?"
    },
    {
      "answer": "Lake Victoria",
      "category": 3,
      "difficulty": 2,
      "id": 13,
      "question": "What is the largest lake in Africa?"
    },
    {
      "answer": "Agra",
      "category": 3,
      "difficulty": 2,
      "id": 15,
      "question": "The Taj Mahal is located in which Indian city?"
    },
    {
      "answer": "Escher",
      "category": 2,
      "difficulty": 1,
      "id": 16,
      "question": "Which Dutch graphic artist\u2013initials M C was a creator of optical illusions?"
    }
  ],
  "success": true,
  "total_questions": 22
}
```
**POST /questions/searchTerm**


General:
- search for a question using the submitted search by term. Returns the results, success value, total questions.

Sample ``` curl http://127.0.0.1:5000/questions/searchTerm -X POST -H "Content-Type: application/json" -d '{"searchTerm":"who"}' ```
```
{
  "current_category": null,
  "questions": [
    {
      "answer": "Maya Angelou",
      "category": 4,
      "difficulty": 2,
      "id": 5,
      "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
    },
    {
      "answer": "George Washington Carver",
      "category": 4,
      "difficulty": 2,
      "id": 12,
      "question": "Who invented Peanut Butter?"
    },
    {
      "answer": "Alexander Fleming",
      "category": 1,
      "difficulty": 3,
      "id": 21,
      "question": "Who discovered penicillin?"
    },
    {
      "answer": "Donatien BANYISHAYI",
      "category": 4,
      "difficulty": 4,
      "id": 24,
      "question": "Who the author of this trivia project?"
    },
    {
      "answer": "OK",
      "category": 7,
      "difficulty": 1,
      "id": 30,
      "question": "Who the author of this trivia project?"
    },
    {
      "answer": "Felix Antoine TSHISEKEDI TSHILOMBO",
      "category": 4,
      "difficulty": 4,
      "id": 34,
      "question": "Who is the current president of the Democratic Republic of Congo?"
    }
  ],
  "success": true,
  "total_questions": 6
}
```
**GET /categories/{id}/questions**


General:

- Returns a list of questions, in the given category, category total_questions and success value
- Results are paginated in groups of 10. Include a request argument to choose page number, starting from 1.

Sample: ```curl http://127.0.0.1:5000/categories/3/questions```
```
{
  "current_category": "Geography",
  "questions": [
    {
      "answer": "Lake Victoria",
      "category": 3,
      "difficulty": 2,
      "id": 13,
      "question": "What is the largest lake in Africa?"
    },
    {
      "answer": "Agra",
      "category": 3,
      "difficulty": 2,
      "id": 15,
      "question": "The Taj Mahal is located in which Indian city?"
    }
  ],
  "success": true,
  "total_questions": 2
}
```
**POST /quizzes**


General:
- recive the actual question and the category
- return the next question in the same category and success value.

Sample [`'curl http://127.0.0.1:5000/quizzes -X POST -H "Content-Type: application/json" -d '{"quiz_category":{"type":"Geography","id":"3"}, "previous_questions":[13]}'`]
```
{
  "question": {
    "answer": "Agra",
    "category": "3",
    "difficulty": 2,
    "id": 15,
    "question": "The Taj Mahal is located in which Indian city?"
  },
  "success": true
}
```

## Co-Author

- Student: Donatien BANYISHAYI

## Acknowledgements

- Acknowledgement at my instructors : engineers Any Hua and Caryn who have supported us so far.The awesome team Udacity and ALX-T our sponsor and all students, we will soon be search employement or start a business with amazing or extraordinaires full-Stack courses!

> View the [Frontend README](./frontend/README.md) for more details.
