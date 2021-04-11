import React from "react";


const RecentResults = ({recentResults, height=16}) => {
    const numSegments = 20;
    const width = 100 / numSegments;
    // const count = recentResults.reduce((acc, curr) => acc + (curr ? 1 : 0), 0);
    // const progress = 100 * count/20;
    // console.log(recentResults);

    return (
        <div style={{ display: "flex", flexDirection: "row", overflow: "hidden", borderRadius: height, border: "solid", borderWidth: 1 }}>
            {recentResults.map((r, i) => {
                const color = r ? "green" : "white";
                const borderLeft = (i === 0) ? "" : "1px solid black";
                return (
                    <div key={i} style={{ width: `${width}%`, background: color, height: height, borderLeft: borderLeft }} />
                )
            })}
        </div>
    );
}

export default RecentResults;
