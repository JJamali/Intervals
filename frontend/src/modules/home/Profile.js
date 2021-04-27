import QuizBl from "./quiz/bl.js";
import {globalStats} from "./quiz/adapter";
import {useState, useEffect} from "react";

export default function Profile({user}) {
    const { recentResults } = QuizBl();
    const [stats, setStats] = useState(null);
    useEffect(() => {
        globalStats().then(data => {
            setStats(data);
        });
    },[]);

    return (
        <div>
            <h2>Home</h2>
            <h3>Hello, {user.username}</h3>
            <div>
                <div>Level: {user.profile.level}</div>
                <div>Current level: {user.profile.current_level}</div>
                <div>Total completed: {recentResults.total_completed}</div>
                <div>Total correct: {recentResults.total_correct}</div>
                <div>Global completed: {stats?.global_answered}</div>
                <div>Global correct: {stats?.global_correct}</div>
            </div>
        </div>
    )
}
