import QuizBl from "./quiz/bl.js";

export default function Profile({user}) {
    const { recentResults } = QuizBl();

    console.log('recent', recentResults); 

    return (
        <div>
            <h2>Home</h2>
            <h3>Hello, {user.username}</h3>
            <div>
                <div>Level: {user.profile.level}</div>
                <div>Current level: {user.profile.current_level}</div>
                <div>Total completed: {recentResults.total_completed}</div>
                <div>Total correct: {recentResults.total_correct}</div>
            </div>
        </div>
    )
}
