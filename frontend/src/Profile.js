export default function Profile({user}) {
    console.log(user.profile);

    return (
        <div>
            <h2>Home</h2>
            <h3>Hello, {user.username}</h3>
            <div>
                <div>Level: {user.profile.level}</div>
                <div>Total completed: {user.profile.total_completed}</div>
                <div>Total correct: {user.profile.total_correct}</div>
            </div>
        </div>
    )
}
