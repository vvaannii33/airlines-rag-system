import http from "k6/http";

export default function () {
    http.post(
        "http://127.0.0.1:8000/ask",
        JSON.stringify({
            query: "What is the probation period for technical roles?"
        }),
        {
            headers: {
                "Content-Type": "application/json"
            }

            
        }
    );
}

export const options = {
    vus: 10, // Number of virtual users
    iterations: 10 // Number of iterations for the test
};