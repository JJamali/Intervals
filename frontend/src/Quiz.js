import React, { useEffect } from 'react';
import { TokenContext } from './TokenContext.js';

export default function Quiz({token, updateUser}) {
    const [question, setQuestion] = React.useState({});
    const [guess, setGuess] = React.useState("");

    const getQuestion = () => {
        fetch('http://localhost:8000/api/intervals/question/', {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json'
            }
        })
        .then(res => res.json())
        .then(question => {
            console.log('question', question);
            setQuestion(question);
        });
    };

    const answerCheck = (e, data) => {
        e.preventDefault();
        console.log(token);
        fetch('http://localhost:8000/api/intervals/answer_check/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                Authorization: `Bearer ${token.access}`
            },
            // body collects data (in the form of a dictionary) to be sent to backend
            body: JSON.stringify({question: question, guess: guess})
        })
        .then(response => response.json())
        .then(data => {
            console.log(data);
            updateUser();
        });
    };

    const handleGuessChange = (e) => {
        setGuess(e.target.value);
    }

    useEffect(() => {
        getQuestion();
    }, []);

    return (
        <>
            Quiz
            <form onSubmit={answerCheck}>
                Question: {question.question}
                <input type="text" name="guess" onChange={handleGuessChange} />
                <input type="submit" value="Submit" />
            </form>
        </>
    );
}
