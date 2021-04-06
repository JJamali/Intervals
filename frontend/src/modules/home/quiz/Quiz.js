import React from "react";
import QuizBl from "./bl.js";

export default function Quiz() {
    const { question, handleGuessChange, handleSubmit } = QuizBl();

    return (
        <>
            Quiz
            <form onSubmit={handleSubmit}>
                Question: {question.question}
                <input type="text" name="guess" onChange={handleGuessChange} />
                <input type="submit" value="Submit" />
            </form>
        </>
    );
}
